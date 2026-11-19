from fastapi import APIRouter
from sqlalchemy import select

from ..errors import ApiError, ok
from ..models import User, UserQuota
from ..schemas import LoginRequest, RegisterRequest
from ..security import CurrentUser, DbSession, create_access_token, hash_password, verify_password
from ..serializers import user_data

router = APIRouter(prefix="/api/auth", tags=["认证"])


def auth_payload(user: User) -> dict:
    token, expires_in = create_access_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "user": user_data(user),
    }


@router.post("/register")
def register(payload: RegisterRequest, db: DbSession):
    email = str(payload.email).lower()
    if db.scalar(select(User).where(User.email == email)):
        raise ApiError(409, 10004, "该邮箱已注册")
    user = User(email=email, password_hash=hash_password(payload.password), nickname=payload.nickname)
    user.quota = UserQuota(remaining_count=30, total_purchased=30, total_used=0)
    db.add(user)
    db.commit()
    db.refresh(user)
    return ok(auth_payload(user), "注册成功，已赠送 30 次生成次数")


@router.post("/login")
def login(payload: LoginRequest, db: DbSession):
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise ApiError(401, 10002, "邮箱或密码错误")
    if user.status != "ACTIVE":
        raise ApiError(403, 10005, "账号已被停用")
    return ok(auth_payload(user), "登录成功")


@router.get("/me")
def me(user: CurrentUser):
    return ok(user_data(user))
