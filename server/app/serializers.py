from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import (
    Artist,
    GenerationTask,
    MediaAsset,
    Message,
    Order,
    OrderProgressPost,
    OrderStatusHistory,
    ORDER_STATUS_LABELS,
    Product,
    PromptTemplate,
    User,
)


def iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def money(cents: int) -> str:
    return f"{Decimal(cents) / Decimal(100):.2f}"


def user_data(user: User) -> dict[str, Any]:
    return {
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "role": user.role.value,
        "status": user.status,
        "remaining_count": user.quota.remaining_count if user.quota else 0,
        "quota": {
            "remaining_count": user.quota.remaining_count,
            "total_purchased": user.quota.total_purchased,
            "total_used": user.quota.total_used,
        } if user.quota else None,
        "created_at": iso(user.created_at),
    }


def asset_data(asset: MediaAsset) -> dict[str, Any]:
    return {
        "id": asset.id,
        "task_id": asset.task_id,
        "kind": asset.kind,
        "url": asset.url,
        "thumbnail_url": asset.thumbnail_url or asset.url,
        "width": asset.width,
        "height": asset.height,
        "duration": asset.duration,
        "meta": asset.meta_json,
        "created_at": iso(asset.created_at),
    }


def template_data(template: PromptTemplate) -> dict[str, Any]:
    return {
        "id": template.id,
        "category": template.category,
        "name": template.name,
        "description": template.description,
        "positive_prompt": template.positive_prompt,
        "negative_prompt": template.negative_prompt,
        "params": template.params_json,
        "cover_url": template.cover_url,
        "is_published": template.is_published,
    }


def task_data(task: GenerationTask) -> dict[str, Any]:
    return {
        "id": task.id,
        "template_id": task.template_id,
        "type": task.type,
        "prompt": task.prompt,
        "params": task.params_json,
        "provider_code": task.provider_code,
        "provider_task_id": task.provider_task_id,
        "status": task.status.value,
        "error_msg": task.error_msg,
        "cost_count": task.cost_count,
        "demo_mode": task.demo_mode,
        "assets": [asset_data(asset) for asset in sorted(task.assets, key=lambda item: item.id)],
        "created_at": iso(task.created_at),
        "completed_at": iso(task.completed_at),
    }


def product_data(product: Product) -> dict[str, Any]:
    price = money(product.base_price_cents)
    return {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "base_price_cents": product.base_price_cents,
        "base_price": price,
        "price": price,
        "craft_desc": product.craft_desc,
        "lead_time_days": product.lead_time_days,
        "spec": product.spec_json,
        "cover_url": product.cover_url,
        "status": product.status,
    }


def artist_data(artist: Artist, include_private: bool = False) -> dict[str, Any]:
    data = {
        "id": artist.id,
        "pen_name": artist.pen_name,
        "specialties": artist.specialties,
        "intro": artist.intro,
        "avatar": artist.avatar,
        "representative_media_ids": artist.representative_media_ids,
        "representative_urls": artist.representative_urls,
        "rating": float(artist.rating),
        "years_experience": artist.years_experience,
        "status": artist.status,
        "created_at": iso(artist.created_at),
    }
    if include_private:
        data.update({
            "real_name": artist.real_name,
            "contact": artist.contact,
            "commission_rate": str(artist.commission_rate),
            "updated_at": iso(artist.updated_at),
        })
    return data


def order_data(order: Order) -> dict[str, Any]:
    amount = money(order.amount_cents)
    return {
        "id": order.id,
        "order_no": order.order_no,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "media_asset_id": order.media_asset_id,
        "artist_id": order.artist_id,
        "spec": order.spec_json,
        "amount_cents": order.amount_cents,
        "amount": amount,
        "status": order.status.value,
        "status_label": ORDER_STATUS_LABELS[order.status],
        "shipping_info": order.shipping_info_json,
        "design_confirmed": order.design_confirmed,
        "confirmed_at": iso(order.confirmed_at),
        "tracking_no": order.tracking_no,
        "created_at": iso(order.created_at),
        "updated_at": iso(order.updated_at),
        "product": product_data(order.product) if order.product else None,
        "artist": artist_data(order.artist) if order.artist else None,
        "media_asset": asset_data(order.media_asset) if order.media_asset else None,
    }


def history_data(history: OrderStatusHistory) -> dict[str, Any]:
    return {
        "id": history.id,
        "from_status": history.from_status.value if history.from_status else None,
        "to_status": history.to_status.value,
        "to_status_label": ORDER_STATUS_LABELS[history.to_status],
        "operator_type": history.operator_type.value,
        "operator_id": history.operator_id,
        "note": history.note,
        "created_at": iso(history.created_at),
    }


def progress_data(db: Session, post: OrderProgressPost) -> dict[str, Any]:
    assets = []
    if post.media_ids:
        assets = list(db.scalars(select(MediaAsset).where(MediaAsset.id.in_(post.media_ids))).all())
        by_id = {asset.id: asset for asset in assets}
        assets = [by_id[asset_id] for asset_id in post.media_ids if asset_id in by_id]
    return {
        "id": post.id,
        "order_id": post.order_id,
        "step_name": post.step_name,
        "content": post.content,
        "media_ids": post.media_ids,
        "media_urls": [asset.url for asset in assets],
        "media_assets": [asset_data(asset) for asset in assets],
        "posted_by": post.posted_by,
        "operator_type": post.operator_type.value,
        "created_at": iso(post.created_at),
    }


def message_data(message: Message) -> dict[str, Any]:
    return {
        "id": message.id,
        "type": message.type,
        "title": message.title,
        "content": message.content,
        "is_read": message.is_read,
        "ref_order_id": message.ref_order_id,
        "created_at": iso(message.created_at),
    }
