from sqlalchemy.orm import Session

from ..errors import ApiError
from ..models import (
    Artist,
    Message,
    Order,
    OrderStatus,
    OrderStatusHistory,
    ORDER_STATUS_LABELS,
    User,
    UserRole,
)

ALLOWED_TRANSITIONS = {
    OrderStatus.PENDING_CONFIRM: {OrderStatus.DESIGN_CONFIRM},
    OrderStatus.DESIGN_CONFIRM: {OrderStatus.ASSIGNED},
    OrderStatus.ASSIGNED: {OrderStatus.IN_PRODUCTION},
    OrderStatus.IN_PRODUCTION: {OrderStatus.QUALITY_CHECK},
    OrderStatus.QUALITY_CHECK: {OrderStatus.SHIPPED},
    OrderStatus.SHIPPED: {OrderStatus.COMPLETED},
    OrderStatus.COMPLETED: set(),
}


def transition_order(
    db: Session,
    order: Order,
    to_status: OrderStatus,
    operator: User,
    note: str = "",
    artist_id: int | None = None,
    tracking_no: str | None = None,
) -> OrderStatusHistory:
    if to_status not in ALLOWED_TRANSITIONS[order.status]:
        current = ORDER_STATUS_LABELS[order.status]
        target = ORDER_STATUS_LABELS[to_status]
        raise ApiError(400, 30002, f"订单不能从「{current}」流转为「{target}」")

    if to_status == OrderStatus.ASSIGNED:
        if not order.design_confirmed:
            raise ApiError(400, 30003, "用户尚未确认定稿，不能交付画师")
        selected_artist_id = artist_id or order.artist_id
        if not selected_artist_id:
            raise ApiError(400, 30004, "交付画师前必须选择画师")
        artist = db.get(Artist, selected_artist_id)
        if artist is None or artist.status != "ACTIVE":
            raise ApiError(400, 30005, "所选画师不可用")
        order.artist_id = selected_artist_id
    elif artist_id is not None:
        artist = db.get(Artist, artist_id)
        if artist is None or artist.status != "ACTIVE":
            raise ApiError(400, 30005, "所选画师不可用")
        order.artist_id = artist_id

    if to_status == OrderStatus.IN_PRODUCTION and not order.artist_id:
        raise ApiError(400, 30004, "创作中的订单必须关联画师")
    if to_status == OrderStatus.SHIPPED:
        if not (tracking_no or order.tracking_no):
            raise ApiError(400, 30006, "发货前请填写物流单号")
        order.tracking_no = tracking_no or order.tracking_no

    history = OrderStatusHistory(
        order_id=order.id,
        from_status=order.status,
        to_status=to_status,
        operator_type=operator.role,
        operator_id=operator.id,
        note=note.strip() or f"订单进入「{ORDER_STATUS_LABELS[to_status]}」阶段",
    )
    order.status = to_status
    db.add(history)
    db.add(Message(
        user_id=order.user_id,
        type="ORDER",
        title=f"订单{ORDER_STATUS_LABELS[to_status]}",
        content=f"订单 {order.order_no}：{history.note}",
        ref_order_id=order.id,
    ))
    db.flush()
    return history
