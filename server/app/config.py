from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "镜绘 API"
    app_env: str = "development"
    debug: bool = True
    database_url: str = f"sqlite:///{(BASE_DIR / 'jinghui.db').as_posix()}"
    secret_key: str = "jinghui-local-demo-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"

    ai_provider: str = "demo"
    ai_request_timeout: int = 60
    tongyi_api_key: str = ""
    tongyi_base_url: str = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    tongyi_task_base_url: str = "https://dashscope.aliyuncs.com/api/v1/tasks"
    tongyi_model: str = "wanx-v1"
    jiemeng_api_key: str = ""
    jiemeng_base_url: str = "https://visual.volcengineapi.com"
    jiemeng_model: str = "jimeng_vgfm_t2i_lcg"

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    @property
    def static_dir(self) -> Path:
        return BASE_DIR / "static"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
