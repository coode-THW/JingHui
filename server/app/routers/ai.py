from fastapi import APIRouter, Query
from sqlalchemy import select

from ..errors import ApiError, not_found, ok
from ..models import GenerationTask, MediaAsset, PromptTemplate
from ..schemas import GenerateRequest
from ..security import CurrentUser, DbSession
from ..serializers import asset_data, task_data, template_data
from ..services.generation import generate_images

router = APIRouter(prefix="/api/ai", tags=["AI 创作"])


@router.get("/templates")
def list_templates(db: DbSession, category: str | None = Query(default=None, max_length=50)):
    query = select(PromptTemplate).where(PromptTemplate.is_published.is_(True))
    if category:
        query = query.where(PromptTemplate.category == category)
    templates = db.scalars(query.order_by(PromptTemplate.sort_order, PromptTemplate.id)).all()
    return ok([template_data(template) for template in templates])


@router.post("/generate")
def generate(payload: GenerateRequest, user: CurrentUser, db: DbSession):
    template = None
    if payload.template_id is not None:
        template = db.get(PromptTemplate, payload.template_id)
        if template is None or not template.is_published:
            raise ApiError(400, 20004, "所选提示词模板不存在或已下架")
    prompt = payload.prompt
    negative_prompt = "低质量，模糊，肢体变形，文字乱码，水印"
    if template:
        prompt = f"{template.positive_prompt}\n用户定制要求：{payload.prompt}"
        negative_prompt = template.negative_prompt or negative_prompt
    params = {
        "ratio": payload.ratio,
        "count": payload.count,
        "style_strength": payload.style_strength,
        "negative_prompt": negative_prompt,
    }
    task = generate_images(db, user, prompt, payload.template_id, params)
    db.refresh(user.quota)
    data = task_data(task)
    data["remaining_count"] = user.quota.remaining_count
    return ok(data, "生成成功（本地 Demo 渠道）" if task.demo_mode else "生成成功")


@router.get("/tasks/{task_id}")
def get_task(task_id: int, user: CurrentUser, db: DbSession):
    task = db.get(GenerationTask, task_id)
    if task is None:
        raise not_found("生成任务")
    if task.user_id != user.id:
        raise ApiError(403, 10003, "无权查看其他用户的生成任务")
    return ok(task_data(task))


@router.get("/assets")
def list_assets(
    user: CurrentUser,
    db: DbSession,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    assets = db.scalars(
        select(MediaAsset)
        .where(
            MediaAsset.owner_type == "USER",
            MediaAsset.owner_id == user.id,
            MediaAsset.kind == "GENERATED",
        )
        .order_by(MediaAsset.created_at.desc(), MediaAsset.id.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return ok([asset_data(asset) for asset in assets])
