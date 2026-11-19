import secrets
from datetime import datetime, timezone

from fastapi import APIRouter
from sqlalchemy import select

from ..errors import ApiError, not_found, ok
from ..models import (
    Artist,
    MediaAsset,
    Message,
    Order,
    OrderProgressPost,
    OrderStatus,
    OrderStatusHistory,
    Product,
    User,
    UserRole,
)
from ..schemas import OrderCreateRequest
from ..security import CurrentUser, DbSession
from ..serializers import history_data, order_data, progress_data
from ..services.orders import transition_order

router = APIRouter(prefix="/api/orders", tags=["订单与进度"])


def get_visible_order(db: DbSession, order_id: int, user: User) -> Order:
    order = db.get(Order, order_id)
    if order is None:
        raise not_found("订单")
    if user.role != UserRole.ADMIN and order.user_id != user.id:
        raise ApiError(403, 10003, "无权查看其他用户的订单")
    return order


@router.post("")
def create_order(payload: OrderCreateRequest, user: CurrentUser, db: DbSession):
    product = db.get(Product, payload.product_id)
    if product is None or product.status != "ON_SALE":
        raise ApiError(400, 30007, "所选载体不可购买")
    asset = db.get(MediaAsset, payload.media_asset_id)
    if asset is None or asset.owner_type != "USER" or asset.owner_id != user.id or asset.kind != "GENERATED":
        raise ApiError(403, 30008, "定稿图片不存在或不属于当前用户")
    if payload.artist_id is not None:
        artist = db.get(Artist, payload.artist_id)
        if artist is None or artist.status != "ACTIVE":
            raise ApiError(400, 30005, "所选画师不可用")

    order_no = f"JH{datetime.now(timezone.utc):%Y%m%d%H%M%S}{secrets.token_hex(3).upper()}"
    order = Order(
        order_no=order_no,
        user_id=user.id,
        product_id=product.id,
        media_asset_id=asset.id,
        artist_id=payload.artist_id,
        spec_json=payload.spec.model_dump(),
        amount_cents=product.base_price_cents,
        status=OrderStatus.PENDING_CONFIRM,
        shipping_info_json=payload.shipping_info.model_dump(),
    )
    db.add(order)
    db.flush()
    db.add(OrderStatusHistory(
        order_id=order.id,
        from_status=None,
        to_status=OrderStatus.PENDING_CONFIRM,
        operator_type=UserRole.USER,
        operator_id=user.id,
        note="定稿与定制需求已提交，等待平台确认",
    ))
    db.add(Message(
        user_id=user.id,
        type="ORDER",
        title="定制订单已提交",
        content=f"订单 {order_no} 已提交，平台将尽快与您确认定稿。",
        ref_order_id=order.id,
    ))
    db.commit()
    db.refresh(order)
    return ok(order_data(order), "订单创建成功")


@router.get("")
def list_orders(user: CurrentUser, db: DbSession, status: str | None = None):
    query = select(Order).where(Order.user_id == user.id)
    if status:
        try:
            query = query.where(Order.status == OrderStatus(status))
        except ValueError:
            raise ApiError(400, 30009, "未知订单状态") from None
    orders = db.scalars(query.order_by(Order.created_at.desc(), Order.id.desc())).all()
    return ok([order_data(order) for order in orders])


@router.get("/{order_id}")
def get_order(order_id: int, user: CurrentUser, db: DbSession):
    return ok(order_data(get_visible_order(db, order_id, user)))


@router.get("/{order_id}/timeline")
def get_timeline(order_id: int, user: CurrentUser, db: DbSession):
    order = get_visible_order(db, order_id, user)
    histories = db.scalars(
        select(OrderStatusHistory)
        .where(OrderStatusHistory.order_id == order.id)
        .order_by(OrderStatusHistory.created_at, OrderStatusHistory.id)
    ).all()
    posts = db.scalars(
        select(OrderProgressPost)
        .where(OrderProgressPost.order_id == order.id)
        .order_by(OrderProgressPost.created_at, OrderProgressPost.id)
    ).all()
    history_items = [history_data(item) for item in histories]
    progress_items = [progress_data(db, item) for item in posts]
    timeline = [
        *({"type": "STATUS", **item} for item in history_items),
        *({"type": "PROGRESS", **item} for item in progress_items),
    ]
    timeline.sort(key=lambda item: (item["created_at"] or "", item["id"]))
    return ok({
        "order_id": order.id,
        "order_no": order.order_no,
        "status": order.status.value,
        "history": history_items,
        "progress": progress_items,
        "timeline": timeline,
    })


@router.post("/{order_id}/confirm-design")
def confirm_design(order_id: int, user: CurrentUser, db: DbSession):
    order = get_visible_order(db, order_id, user)
    if order.user_id != user.id:
        raise ApiError(403, 10003, "仅订单所属用户可确认定稿")
    if order.status != OrderStatus.DESIGN_CONFIRM:
        raise ApiError(400, 30010, "当前阶段无需确认定稿")
    if order.design_confirmed:
        raise ApiError(409, 30011, "定稿已确认，请勿重复操作")
    order.design_confirmed = True
    order.confirmed_at = datetime.now(timezone.utc)
    if order.artist_id:
        transition_order(db, order, OrderStatus.ASSIGNED, user, "用户已确认定稿，作品交付预选画师")
    db.add(Message(
        user_id=user.id,
        type="ORDER",
        title="定稿确认成功",
        content=f"订单 {order.order_no} 的 AI 形象已确认，平台将安排后续手绘创作。",
        ref_order_id=order.id,
    ))
    db.commit()
    db.refresh(order)
    return ok(order_data(order), "定稿确认成功")
