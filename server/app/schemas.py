from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    nickname: str = Field(min_length=1, max_length=80)

    @field_validator("nickname")
    @classmethod
    def clean_nickname(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("昵称不能为空")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=2, max_length=2000)
    template_id: int | None = None
    ratio: Literal["1:1", "3:4", "9:16"] = "1:1"
    count: int = Field(default=1, ge=1, le=4)
    style_strength: float = Field(default=0.75, ge=0, le=1)

    @field_validator("prompt")
    @classmethod
    def clean_prompt(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("提示词至少 2 个字符")
        return value


class ShippingInfo(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    phone: str = Field(min_length=5, max_length=32)
    address: str = Field(min_length=5, max_length=500)


class OrderSpec(BaseModel):
    size: str = Field(default="标准尺寸", max_length=100)
    framing: str = Field(default="按产品默认工艺", max_length=100)
    inscription: str = Field(default="", max_length=200)
    note: str = Field(default="", max_length=1000)


class OrderCreateRequest(BaseModel):
    product_id: int
    media_asset_id: int
    artist_id: int | None = None
    spec: OrderSpec = Field(default_factory=OrderSpec)
    shipping_info: ShippingInfo


class OrderStatusUpdateRequest(BaseModel):
    to_status: Literal[
        "PENDING_CONFIRM",
        "DESIGN_CONFIRM",
        "ASSIGNED",
        "IN_PRODUCTION",
        "QUALITY_CHECK",
        "SHIPPED",
        "COMPLETED",
    ]
    note: str = Field(default="", max_length=500)
    artist_id: int | None = None
    tracking_no: str | None = Field(default=None, max_length=100)


class ProgressCreateRequest(BaseModel):
    step_name: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=3000)
    media_urls: list[str] = Field(default_factory=list, max_length=9)

    @field_validator("media_urls")
    @classmethod
    def validate_media_urls(cls, urls: list[str]) -> list[str]:
        for url in urls:
            if not (url.startswith("/static/") or url.startswith("https://") or url.startswith("http://")):
                raise ValueError("素材仅支持 /static/ 路径或 HTTP(S) URL")
            if len(url) > 500:
                raise ValueError("素材 URL 过长")
        return urls


class ArtistCreateRequest(BaseModel):
    pen_name: str = Field(min_length=1, max_length=100)
    real_name: str | None = Field(default=None, max_length=100)
    contact: str | None = Field(default=None, max_length=255)
    specialties: list[str] = Field(default_factory=list, max_length=10)
    intro: str = Field(min_length=1, max_length=5000)
    avatar: str | None = Field(default=None, max_length=500)
    representative_urls: list[str] = Field(default_factory=list, max_length=12)
    years_experience: int = Field(default=0, ge=0, le=100)
    rating: float = Field(default=5.0, ge=0, le=5)
    commission_rate: float = Field(default=0.6, ge=0, le=1)
    status: Literal["ACTIVE", "INACTIVE"] = "ACTIVE"


class ArtistUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pen_name: str | None = Field(default=None, min_length=1, max_length=100)
    real_name: str | None = Field(default=None, max_length=100)
    contact: str | None = Field(default=None, max_length=255)
    specialties: list[str] | None = Field(default=None, max_length=10)
    intro: str | None = Field(default=None, min_length=1, max_length=5000)
    avatar: str | None = Field(default=None, max_length=500)
    representative_urls: list[str] | None = Field(default=None, max_length=12)
    years_experience: int | None = Field(default=None, ge=0, le=100)
    rating: float | None = Field(default=None, ge=0, le=5)
    commission_rate: float | None = Field(default=None, ge=0, le=1)
    status: Literal["ACTIVE", "INACTIVE"] | None = None

    @field_validator(
        "pen_name",
        "specialties",
        "intro",
        "representative_urls",
        "years_experience",
        "rating",
        "commission_rate",
        "status",
    )
    @classmethod
    def reject_null_for_required_columns(cls, value):
        if value is None:
            raise ValueError("该字段不能为 null")
        return value
