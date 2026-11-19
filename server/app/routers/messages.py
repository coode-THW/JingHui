from fastapi import APIRouter, Query
from sqlalchemy import select

from ..errors import ok
from ..models import Message
from ..security import CurrentUser, DbSession
from ..serializers import message_data

router = APIRouter(prefix="/api/messages", tags=["站内消息"])


@router.get("")
def list_messages(
    user: CurrentUser,
    db: DbSession,
    unread_only: bool = False,
    limit: int = Query(default=50, ge=1, le=100),
):
    query = select(Message).where(Message.user_id == user.id)
    if unread_only:
        query = query.where(Message.is_read.is_(False))
    messages = db.scalars(query.order_by(Message.created_at.desc(), Message.id.desc()).limit(limit)).all()
    return ok([message_data(message) for message in messages])
