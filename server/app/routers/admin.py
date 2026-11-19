from decimal import Decimal

from fastapi import APIRouter
from sqlalchemy import func, select

from ..errors import ApiError, not_found, ok
from ..models import (
    Artist,
    GenerationTask,
    MediaAsset,
    Order,
    OrderProgressPost,
    OrderStatus,
    Product,
    PromptTemplate,
    TaskStatus,
    User,
    UserRole,
)
from ..schemas import ArtistCreateRequest, ArtistUpdateRequest, OrderStatusUpdateRequest, ProgressCreateRequest
from ..security import AdminUser, DbSession
from ..serializers import artist_data, order_data, product_data, progress_data
from ..services.orders import ALLOWED_TRANSITIONS, transition_order

router = APIRouter(prefix="/api/admin", tags=["运营管理"])


@router.get("/orders")
def admin_list_orders(admin: AdminUser, db: DbSession, status: str | None = None):
    query = select(Order)
    if status:
        try:
            query = query.where(Order.status == OrderStatus(status))
        except ValueError:
            raise ApiError(400, 30009, "未知订单状态") from None
    orders = db.scalars(query.order_by(Order.created_at.desc(), Order.id.desc())).all()
    return ok([order_data(order) for order in orders])


@router.post("/orders/{order_id}/status")
def update_order_status(order_id: int, payload: OrderStatusUpdateRequest, admin: AdminUser, db: DbSession):
    order = db.get(Order, order_id)
    if order is None:
        raise not_found("订单")
    transition_order(
        db,
        order,
        OrderStatus(payload.to_status),
        admin,
        payload.note,
        artist_id=payload.artist_id,
        tracking_no=payload.tracking_no,
    )
    db.commit()
    db.refresh(order)
    return ok(order_data(order), "订单状态已更新")


@router.post("/orders/{order_id}/progress")
def publish_progress(order_id: int, payload: ProgressCreateRequest, admin: AdminUser, db: DbSession):
    order = db.get(Order, order_id)
    if order is None:
        raise not_found("订单")
    if order.status in {OrderStatus.PENDING_CONFIRM, OrderStatus.COMPLETED}:
        raise ApiError(400, 30012, "当前订单阶段不能发布创作动态")
    post = OrderProgressPost(
        order_id=order.id,
        step_name=payload.step_name.strip(),
        content=payload.content.strip(),
        posted_by=admin.id,
        operator_type=UserRole.ADMIN,
    )
    db.add(post)
    db.flush()
    media_ids = []
    for url in payload.media_urls:
        asset = MediaAsset(
            owner_type="ORDER_PROGRESS",
            owner_id=post.id,
            kind="PROGRESS",
            url=url,
            thumbnail_url=url,
            meta_json={"order_id": order.id, "uploaded_by": admin.id},
        )
        db.add(asset)
        db.flush()
        media_ids.append(asset.id)
    post.media_ids = media_ids
    db.commit()
    db.refresh(post)
    return ok(progress_data(db, post), "创作动态已发布")


@router.get("/artists")
def admin_list_artists(admin: AdminUser, db: DbSession):
    artists = db.scalars(select(Artist).order_by(Artist.id)).all()
    return ok([artist_data(artist, include_private=True) for artist in artists])


@router.post("/artists")
def create_artist(payload: ArtistCreateRequest, admin: AdminUser, db: DbSession):
    if db.scalar(select(Artist).where(Artist.pen_name == payload.pen_name)):
        raise ApiError(409, 40001, "画师署名已存在")
    values = payload.model_dump()
    values["rating"] = Decimal(str(values["rating"]))
    values["commission_rate"] = Decimal(str(values["commission_rate"]))
    artist = Artist(**values)
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return ok(artist_data(artist, include_private=True), "画师档案已创建")


@router.put("/artists/{artist_id}")
def update_artist(artist_id: int, payload: ArtistUpdateRequest, admin: AdminUser, db: DbSession):
    artist = db.get(Artist, artist_id)
    if artist is None:
        raise not_found("画师")
    values = payload.model_dump(exclude_unset=True)
    if "pen_name" in values:
        duplicate = db.scalar(select(Artist).where(Artist.pen_name == values["pen_name"], Artist.id != artist_id))
        if duplicate:
            raise ApiError(409, 40001, "画师署名已存在")
    for field in ("rating", "commission_rate"):
        if field in values and values[field] is not None:
            values[field] = Decimal(str(values[field]))
    for key, value in values.items():
        setattr(artist, key, value)
    db.commit()
    db.refresh(artist)
    return ok(artist_data(artist, include_private=True), "画师档案已更新")


@router.get("/stats")
def get_stats(admin: AdminUser, db: DbSession):
    status_rows = db.execute(select(Order.status, func.count(Order.id)).group_by(Order.status)).all()
    orders_by_status = {status.value: 0 for status in OrderStatus}
    orders_by_status.update({status.value: count for status, count in status_rows})
    popular = db.execute(
        select(PromptTemplate.id, PromptTemplate.name, func.count(GenerationTask.id).label("uses"))
        .outerjoin(GenerationTask, GenerationTask.template_id == PromptTemplate.id)
        .group_by(PromptTemplate.id, PromptTemplate.name)
        .order_by(func.count(GenerationTask.id).desc(), PromptTemplate.id)
        .limit(5)
    ).all()
    recent_orders = db.scalars(select(Order).order_by(Order.created_at.desc()).limit(5)).all()
    revenue_cents = db.scalar(select(func.coalesce(func.sum(Order.amount_cents), 0))) or 0
    data = {
        "users": db.scalar(select(func.count(User.id)).where(User.role == UserRole.USER)) or 0,
        "artists": db.scalar(select(func.count(Artist.id)).where(Artist.status == "ACTIVE")) or 0,
        "products": db.scalar(select(func.count(Product.id)).where(Product.status == "ON_SALE")) or 0,
        "orders": db.scalar(select(func.count(Order.id))) or 0,
        "orders_by_status": orders_by_status,
        "generation_tasks": db.scalar(select(func.count(GenerationTask.id))) or 0,
        "successful_generations": db.scalar(
            select(func.count(GenerationTask.id)).where(GenerationTask.status == TaskStatus.SUCCESS)
        ) or 0,
        "generated_assets": db.scalar(select(func.count(MediaAsset.id)).where(MediaAsset.kind == "GENERATED")) or 0,
        "revenue_cents": revenue_cents,
        "revenue": f"{Decimal(revenue_cents) / Decimal(100):.2f}",
        "popular_templates": [{"id": item.id, "name": item.name, "uses": item.uses} for item in popular],
        "recent_orders": [order_data(order) for order in recent_orders],
        "allowed_transitions": {
            status.value: sorted(target.value for target in targets)
            for status, targets in ALLOWED_TRANSITIONS.items()
        },
    }
    return ok(data)
