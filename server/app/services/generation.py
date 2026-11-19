from datetime import datetime, timezone
from typing import Any

from sqlalchemy import update
from sqlalchemy.orm import Session

from ..config import settings
from ..errors import ApiError
from ..models import GenerationTask, MediaAsset, TaskStatus, User, UserQuota
from .ai_provider import ProviderError, get_ai_provider


def generate_images(
    db: Session,
    user: User,
    prompt: str,
    template_id: int | None,
    params: dict[str, Any],
) -> GenerationTask:
    cost = int(params.get("count", 1))
    result = db.execute(
        update(UserQuota)
        .where(UserQuota.user_id == user.id, UserQuota.remaining_count >= cost)
        .values(
            remaining_count=UserQuota.remaining_count - cost,
            total_used=UserQuota.total_used + cost,
        )
    )
    if result.rowcount != 1:
        db.rollback()
        raise ApiError(400, 20001, "剩余生成次数不足")

    task = GenerationTask(
        user_id=user.id,
        template_id=template_id,
        prompt=prompt,
        params_json=params,
        provider_code=settings.ai_provider.lower(),
        status=TaskStatus.PENDING,
        cost_count=cost,
        demo_mode=settings.ai_provider.lower() == "demo",
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    try:
        task.status = TaskStatus.RUNNING
        db.commit()
        provider_result = get_ai_provider().generate(prompt, params)
        for image in provider_result.images:
            db.add(MediaAsset(
                task_id=task.id,
                owner_type="USER",
                owner_id=user.id,
                kind="GENERATED",
                url=image.url,
                thumbnail_url=image.url,
                width=image.width,
                height=image.height,
                meta_json=image.meta,
            ))
        task.provider_task_id = provider_result.provider_task_id
        task.demo_mode = provider_result.demo_mode
        task.status = TaskStatus.SUCCESS
        task.completed_at = datetime.now(timezone.utc)
        db.commit()
    except Exception as exc:
        db.rollback()
        task = db.get(GenerationTask, task.id)
        if task is not None:
            task.status = TaskStatus.FAILED
            task.error_msg = str(exc)[:2000]
            task.completed_at = datetime.now(timezone.utc)
            quota = db.query(UserQuota).filter(UserQuota.user_id == user.id).one()
            quota.remaining_count += cost
            quota.total_used = max(0, quota.total_used - cost)
            db.commit()
        if isinstance(exc, ProviderError):
            raise ApiError(502, 20002, str(exc)) from exc
        raise ApiError(500, 20003, "生成服务暂时不可用，扣除次数已返还") from exc

    db.refresh(task)
    return task
