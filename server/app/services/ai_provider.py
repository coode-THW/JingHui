"""AI 图片生成渠道适配层。

业务服务只依赖 BaseAIProvider；DemoProvider 始终离线可用，真实渠道通过环境变量启用。
"""

import base64
import hashlib
import html
import random
import re
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from ..config import settings

RATIO_DIMENSIONS = {"1:1": (1024, 1024), "3:4": (960, 1280), "9:16": (900, 1600)}


class ProviderError(RuntimeError):
    """可展示给调用方的渠道异常，内部异常不泄漏密钥或响应敏感信息。"""


@dataclass(slots=True)
class GeneratedImage:
    url: str
    width: int
    height: int
    meta: dict[str, Any]


@dataclass(slots=True)
class ProviderResult:
    images: list[GeneratedImage]
    provider_task_id: str | None = None
    demo_mode: bool = False


class BaseAIProvider(ABC):
    code = "base"

    @abstractmethod
    def generate(self, prompt: str, params: dict[str, Any]) -> ProviderResult:
        """提交并获取图片结果；异步渠道在适配器内部完成轮询。"""


def _art_title(prompt: str) -> str:
    titles = (
        ("敦煌", "飞天入梦"), ("青花", "青花映月"), ("剪纸", "纸上生花"),
        ("工笔", "工笔佳人"), (" oil ", "流光肖像"), ("油画", "流光肖像"),
        ("Q版", "国潮少年"), ("山水", "云山行旅"), ("月", "月下清影"),
    )
    for keyword, title in titles:
        if keyword in prompt:
            return title
    return random.Random(prompt).choice(["镜里芳华", "墨韵浮生", "东方意象", "云水之间"])


def _mountain_path(rng: random.Random, width: int, height: int, base: float, amplitude: float) -> str:
    points = [(0, height * base)]
    segments = 7
    for index in range(segments + 1):
        x = width * index / segments
        y = height * base - rng.uniform(0.15, 1.0) * height * amplitude
        if index in (0, segments):
            y = height * base
        points.append((x, y))
    path = f"M 0 {height} L {points[0][0]:.1f} {points[0][1]:.1f} "
    for index in range(1, len(points)):
        previous = points[index - 1]
        current = points[index]
        control_x = (previous[0] + current[0]) / 2
        path += f"Q {control_x:.1f} {previous[1]:.1f} {current[0]:.1f} {current[1]:.1f} "
    path += f"L {width} {height} Z"
    return path


def create_demo_art(prompt: str, ratio: str = "1:1", filename: str | None = None) -> GeneratedImage:
    """生成带宣纸肌理、水墨山峦、圆月、草木和中文题字的独立 SVG。"""
    width, height = RATIO_DIMENSIONS.get(ratio, RATIO_DIMENSIONS["1:1"])
    digest = hashlib.sha256(f"{prompt}|{ratio}|{uuid.uuid4()}".encode("utf-8")).hexdigest()
    rng = random.Random(digest)
    title = _art_title(prompt)
    if filename:
        safe_stem = re.sub(r"[^a-zA-Z0-9_-]", "", filename)[:80]
    else:
        safe_stem = ""
    safe_stem = safe_stem or f"jinghui_{uuid.uuid4().hex}"
    output = settings.static_dir / "generated" / f"{safe_stem}.svg"
    output.parent.mkdir(parents=True, exist_ok=True)

    vermilion = rng.choice(["#A33A2B", "#B03A2E", "#963E32"])
    indigo = rng.choice(["#243B55", "#2C3E5D", "#30465F"])
    gold = rng.choice(["#B99052", "#C9A063", "#AE8950"])
    moon_x = width * rng.uniform(0.62, 0.78)
    moon_y = height * rng.uniform(0.18, 0.28)
    moon_r = min(width, height) * rng.uniform(0.10, 0.15)
    horizon = rng.uniform(0.62, 0.72)
    short_side = min(width, height)
    desc = html.escape(prompt[:240], quote=True)
    escaped_title = html.escape(title)
    birds = []
    for _ in range(4):
        x = rng.uniform(width * 0.16, width * 0.50)
        y = rng.uniform(height * 0.19, height * 0.37)
        size = rng.uniform(8, 15) * width / 1024
        birds.append(
            f'<path d="M {x-size:.1f} {y:.1f} Q {x:.1f} {y-size:.1f} {x+size:.1f} {y:.1f} '
            f'Q {x+size*2:.1f} {y-size:.1f} {x+size*3:.1f} {y:.1f}" fill="none" '
            f'stroke="{indigo}" stroke-width="{max(1.4, size/6):.1f}" opacity=".55"/>'
        )
    reeds = []
    for index in range(9):
        x = width * (0.08 + index * 0.018)
        y = height * 0.88
        reed_h = height * rng.uniform(0.12, 0.25)
        bend = rng.uniform(-25, 35)
        reeds.append(
            f'<path d="M {x:.1f} {y:.1f} Q {x+bend:.1f} {y-reed_h*.55:.1f} '
            f'{x+bend*.6:.1f} {y-reed_h:.1f}" fill="none" stroke="{indigo}" '
            f'stroke-width="{rng.uniform(1.2, 3):.1f}" opacity=".48"/>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">镜绘 · {escaped_title}</title><desc id="desc">{desc}</desc>
<defs>
  <linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FBF7ED"/><stop offset=".52" stop-color="#F2E9D8"/><stop offset="1" stop-color="#E9DDC6"/></linearGradient>
  <radialGradient id="moon"><stop stop-color="#FFF9DF"/><stop offset=".72" stop-color="#EBD6A5"/><stop offset="1" stop-color="#C9A063" stop-opacity=".18"/></radialGradient>
  <linearGradient id="wash" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{indigo}" stop-opacity=".12"/><stop offset="1" stop-color="{indigo}" stop-opacity=".8"/></linearGradient>
  <linearGradient id="vermilion" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{vermilion}" stop-opacity=".08"/><stop offset="1" stop-color="{vermilion}" stop-opacity=".55"/></linearGradient>
  <filter id="grain" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".65" numOctaves="3" seed="{int(digest[:6], 16)}"/><feColorMatrix values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 .045 0"/><feBlend in="SourceGraphic" mode="multiply"/></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="{short_side*.009:.1f}"/></filter>
  <clipPath id="frame"><rect x="{width*.035:.1f}" y="{height*.035:.1f}" width="{width*.93:.1f}" height="{height*.93:.1f}" rx="{short_side*.008:.1f}"/></clipPath>
</defs>
<rect width="{width}" height="{height}" fill="url(#paper)"/>
<g clip-path="url(#frame)" filter="url(#grain)">
  <ellipse cx="{moon_x:.1f}" cy="{moon_y:.1f}" rx="{moon_r*1.55:.1f}" ry="{moon_r*1.55:.1f}" fill="{gold}" opacity=".09" filter="url(#soft)"/>
  <circle cx="{moon_x:.1f}" cy="{moon_y:.1f}" r="{moon_r:.1f}" fill="url(#moon)" opacity=".92"/>
  <path d="M {width*.04:.1f} {height*.49:.1f} C {width*.25:.1f} {height*.39:.1f} {width*.36:.1f} {height*.60:.1f} {width*.58:.1f} {height*.46:.1f} S {width*.84:.1f} {height*.41:.1f} {width*.98:.1f} {height*.49:.1f}" fill="none" stroke="{vermilion}" stroke-width="{short_side*.045:.1f}" opacity=".08" filter="url(#soft)"/>
  <path d="{_mountain_path(rng, width, height, horizon - .09, .19)}" fill="{indigo}" opacity=".13"/>
  <path d="{_mountain_path(rng, width, height, horizon + .02, .22)}" fill="url(#wash)" opacity=".48"/>
  <path d="{_mountain_path(rng, width, height, horizon + .15, .17)}" fill="{indigo}" opacity=".69"/>
  <path d="M 0 {height*.79:.1f} Q {width*.26:.1f} {height*.73:.1f} {width*.51:.1f} {height*.82:.1f} T {width} {height*.78:.1f} L {width} {height} L 0 {height} Z" fill="url(#vermilion)"/>
  {''.join(birds)}
  {''.join(reeds)}
  <g transform="translate({width*.81:.1f} {height*.61:.1f})" fill="none" stroke="{indigo}" stroke-linecap="round" opacity=".66">
    <path d="M 0 {height*.22:.1f} Q {-width*.025:.1f} {height*.11:.1f} {width*.012:.1f} {-height*.07:.1f}" stroke-width="{short_side*.006:.1f}"/>
    <path d="M {width*.004:.1f} {height*.07:.1f} Q {-width*.08:.1f} {height*.015:.1f} {-width*.095:.1f} {-height*.055:.1f} M {width*.008:.1f} {height*.025:.1f} Q {width*.055:.1f} {-height*.015:.1f} {width*.075:.1f} {-height*.07:.1f}" stroke-width="{short_side*.003:.1f}"/>
    <path d="M {-width*.07:.1f} {-height*.02:.1f} q {-width*.025:.1f} {-height*.025:.1f} {-width*.04:.1f} 0 q {width*.02:.1f} {height*.03:.1f} {width*.04:.1f} 0 M {width*.055:.1f} {-height*.04:.1f} q {width*.018:.1f} {-height*.028:.1f} {width*.035:.1f} {-height*.015:.1f} q {-width*.005:.1f} {height*.03:.1f} {-width*.035:.1f} {height*.015:.1f}" fill="{indigo}" stroke="none"/>
  </g>
</g>
<rect x="{width*.035:.1f}" y="{height*.035:.1f}" width="{width*.93:.1f}" height="{height*.93:.1f}" fill="none" stroke="{gold}" stroke-width="1.4" opacity=".62"/>
<path d="M {width*.065:.1f} {height*.09:.1f} h {width*.055:.1f} M {width*.065:.1f} {height*.09:.1f} v {height*.04:.1f} M {width*.935:.1f} {height*.91:.1f} h {-width*.055:.1f} M {width*.935:.1f} {height*.91:.1f} v {-height*.04:.1f}" stroke="{gold}" fill="none" opacity=".65"/>
<g font-family="STKaiti, KaiTi, Noto Serif CJK SC, serif">
  <text x="{width*.12:.1f}" y="{height*.16:.1f}" font-size="{short_side*.057:.1f}" letter-spacing="{short_side*.012:.1f}" fill="{indigo}" opacity=".9">{escaped_title}</text>
  <text x="{width*.125:.1f}" y="{height*.205:.1f}" font-size="{short_side*.019:.1f}" letter-spacing="{short_side*.009:.1f}" fill="{indigo}" opacity=".58">以 AI 为镜 · 以手作绘心</text>
  <text x="{width*.86:.1f}" y="{height*.73:.1f}" writing-mode="vertical-rl" font-size="{short_side*.025:.1f}" letter-spacing="{short_side*.014:.1f}" fill="{indigo}" opacity=".68">镜绘东方意象</text>
</g>
<g transform="translate({width*.12:.1f} {height*.82:.1f})">
  <rect width="{short_side*.067:.1f}" height="{short_side*.067:.1f}" rx="{short_side*.005:.1f}" fill="{vermilion}" opacity=".88"/>
  <text x="{short_side*.0335:.1f}" y="{short_side*.046:.1f}" text-anchor="middle" font-family="KaiTi, serif" font-size="{short_side*.035:.1f}" fill="#F7F3EA">镜绘</text>
</g>
</svg>'''
    output.write_text(svg, encoding="utf-8")
    return GeneratedImage(
        url=f"/static/generated/{output.name}",
        width=width,
        height=height,
        meta={"engine": "demo-svg", "title": title, "ratio": ratio, "prompt": prompt},
    )


class DemoProvider(BaseAIProvider):
    code = "demo"

    def generate(self, prompt: str, params: dict[str, Any]) -> ProviderResult:
        ratio = params.get("ratio", "1:1")
        if ratio not in RATIO_DIMENSIONS:
            raise ProviderError("Demo 渠道不支持该画幅比例")
        count = int(params.get("count", 1))
        images = [create_demo_art(prompt, ratio) for _ in range(count)]
        return ProviderResult(images=images, provider_task_id=f"demo-{uuid.uuid4().hex}", demo_mode=True)


class TongyiProvider(BaseAIProvider):
    """通义万相异步文生图适配器，使用阿里云百炼官方 HTTP API。"""

    code = "tongyi"

    def __init__(self) -> None:
        if not settings.tongyi_api_key:
            raise ProviderError("通义万相未配置 TONGYI_API_KEY；如需离线演示请设置 AI_PROVIDER=demo")
        self.headers = {
            "Authorization": f"Bearer {settings.tongyi_api_key}",
            "X-DashScope-Async": "enable",
        }

    def generate(self, prompt: str, params: dict[str, Any]) -> ProviderResult:
        ratio = params.get("ratio", "1:1")
        sizes = {"1:1": "1024*1024", "3:4": "960*1280", "9:16": "720*1280"}
        payload = {
            "model": settings.tongyi_model,
            "input": {
                "prompt": prompt,
                "negative_prompt": params.get("negative_prompt", "低质量，模糊，变形，文字乱码"),
            },
            "parameters": {
                "size": sizes.get(ratio, "1024*1024"),
                "n": int(params.get("count", 1)),
                "prompt_extend": True,
            },
        }
        try:
            with httpx.Client(timeout=settings.ai_request_timeout) as client:
                response = client.post(settings.tongyi_base_url, headers=self.headers, json=payload)
                response.raise_for_status()
                body = response.json()
                task_id = body.get("output", {}).get("task_id")
                if not task_id:
                    raise ProviderError(f"通义万相未返回任务 ID：{body.get('message', '未知响应')}")
                deadline = time.monotonic() + settings.ai_request_timeout
                while time.monotonic() < deadline:
                    task_response = client.get(
                        f"{settings.tongyi_task_base_url.rstrip('/')}/{task_id}",
                        headers={"Authorization": f"Bearer {settings.tongyi_api_key}"},
                    )
                    task_response.raise_for_status()
                    task_body = task_response.json()
                    output = task_body.get("output", {})
                    status = output.get("task_status")
                    if status == "SUCCEEDED":
                        results = output.get("results", [])
                        images = [
                            self._download(client, item["url"], ratio)
                            for item in results
                            if item.get("url")
                        ]
                        if not images:
                            raise ProviderError("通义万相任务成功但未返回图片")
                        return ProviderResult(images=images, provider_task_id=task_id)
                    if status in {"FAILED", "CANCELED", "UNKNOWN"}:
                        raise ProviderError(output.get("message") or task_body.get("message") or "通义万相生成失败")
                    time.sleep(2)
                raise ProviderError("通义万相任务轮询超时")
        except ProviderError:
            raise
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            raise ProviderError(f"通义万相请求失败：{exc}") from exc

    @staticmethod
    def _download(client: httpx.Client, url: str, ratio: str) -> GeneratedImage:
        response = client.get(url, follow_redirects=True)
        response.raise_for_status()
        if len(response.content) > 20 * 1024 * 1024:
            raise ProviderError("AI 图片超过 20MB 限制")
        content_type = response.headers.get("content-type", "").split(";")[0]
        suffix = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "image/svg+xml": ".svg"}.get(content_type, ".png")
        path = settings.static_dir / "generated" / f"tongyi_{uuid.uuid4().hex}{suffix}"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.content)
        width, height = RATIO_DIMENSIONS.get(ratio, RATIO_DIMENSIONS["1:1"])
        return GeneratedImage(f"/static/generated/{path.name}", width, height, {"source": "tongyi"})


class JiemengProvider(BaseAIProvider):
    """即梦 HTTP 适配器。

    默认采用兼容网关协议：POST {JIEMENG_BASE_URL}/v1/images/generations，Bearer 鉴权，
    响应 data[].url 或 data[].b64_json。接入火山官方签名网关时仅需替换网关地址与模型。
    """

    code = "jiemeng"

    def __init__(self) -> None:
        if not settings.jiemeng_api_key:
            raise ProviderError("即梦未配置 JIEMENG_API_KEY；如需离线演示请设置 AI_PROVIDER=demo")

    def generate(self, prompt: str, params: dict[str, Any]) -> ProviderResult:
        ratio = params.get("ratio", "1:1")
        width, height = RATIO_DIMENSIONS.get(ratio, RATIO_DIMENSIONS["1:1"])
        endpoint = settings.jiemeng_base_url.rstrip("/")
        if not endpoint.endswith("/v1/images/generations"):
            endpoint += "/v1/images/generations"
        payload = {
            "model": settings.jiemeng_model,
            "prompt": prompt,
            "n": int(params.get("count", 1)),
            "size": f"{width}x{height}",
            "response_format": "b64_json",
        }
        try:
            with httpx.Client(timeout=settings.ai_request_timeout) as client:
                response = client.post(
                    endpoint,
                    headers={"Authorization": f"Bearer {settings.jiemeng_api_key}"},
                    json=payload,
                )
                response.raise_for_status()
                items = response.json().get("data", [])
                images = []
                for item in items:
                    if item.get("b64_json"):
                        content = base64.b64decode(item["b64_json"], validate=True)
                        if len(content) > 20 * 1024 * 1024:
                            raise ProviderError("即梦图片超过 20MB 限制")
                        path = settings.static_dir / "generated" / f"jiemeng_{uuid.uuid4().hex}.png"
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(content)
                    elif item.get("url"):
                        path, content = self._download(client, item["url"])
                    else:
                        continue
                    images.append(GeneratedImage(f"/static/generated/{path.name}", width, height, {"source": "jiemeng"}))
                if not images:
                    raise ProviderError("即梦未返回可用图片，请检查网关协议与模型配置")
                return ProviderResult(images=images)
        except ProviderError:
            raise
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            raise ProviderError(f"即梦请求失败：{exc}") from exc

    @staticmethod
    def _download(client: httpx.Client, url: str) -> tuple[Path, bytes]:
        response = client.get(url, follow_redirects=True)
        response.raise_for_status()
        content = response.content
        if len(content) > 20 * 1024 * 1024:
            raise ProviderError("即梦图片超过 20MB 限制")
        suffix = ".jpg" if "jpeg" in response.headers.get("content-type", "") else ".png"
        path = settings.static_dir / "generated" / f"jiemeng_{uuid.uuid4().hex}{suffix}"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path, content


def get_ai_provider() -> BaseAIProvider:
    providers: dict[str, type[BaseAIProvider]] = {
        "demo": DemoProvider,
        "tongyi": TongyiProvider,
        "jiemeng": JiemengProvider,
    }
    code = settings.ai_provider.strip().lower()
    provider_class = providers.get(code)
    if provider_class is None:
        raise ProviderError(f"未知 AI_PROVIDER={code}，可选：{', '.join(providers)}")
    return provider_class()
