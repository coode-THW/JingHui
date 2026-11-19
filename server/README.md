# 镜绘 FastAPI 后端

「镜绘」一期后端：AI 形象生成、定稿下单、运营代录手绘进度。默认使用 SQLite 与本地 SVG DemoProvider，无需外网或第三方 Key 即可演示。

## 快速启动

要求 Python 3.13。

```bash
cd server
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- OpenAPI 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/health
- 本地图片：http://localhost:8000/static/generated/...

启动时自动建表并幂等写入模板、载体、画师、演示作品和创作中订单。重复启动不会重复插入，也不会重置已消耗的配额。

## 默认账号

| 角色 | 邮箱 | 密码 | 说明 |
| --- | --- | --- | --- |
| 普通用户 | `demo@jinghui.art` | `Demo123456` | 30 次生成配额、4 幅作品、1 个创作中订单 |
| 管理员 | `admin@jinghui.art` | `Admin123456` | 后台画师、状态、进度和统计接口 |

## 配置

复制 `.env.example` 为 `.env`。所有配置均有本地默认值，Demo 模式可不创建 `.env`。

```dotenv
DATABASE_URL=sqlite:///./jinghui.db
SECRET_KEY=replace-with-a-long-random-string
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
AI_PROVIDER=demo
```

生产 MySQL 示例（驱动已包含 PyMySQL）：

```dotenv
APP_ENV=production
DEBUG=false
DATABASE_URL=mysql+pymysql://jinghui:password@127.0.0.1:3306/jinghui?charset=utf8mb4
SECRET_KEY=use-a-cryptographically-random-secret
AI_PROVIDER=tongyi
TONGYI_API_KEY=sk-...
```

生产环境务必更换默认密钥。演示使用 `create_all` 自动建表；正式迭代建议再引入 Alembic 管理结构变更。

### AI 渠道

- `demo`：默认。根据提示词、画幅与随机构图离线生成独特 SVG，含宣纸肌理、朱砂/黛蓝、水墨山峦、圆月、草木、题字和钤印。
- `tongyi`：通义万相官方异步 HTTP API，适配提交、轮询、下载转存。配置 `TONGYI_API_KEY`，可调整模型和 API 地址。
- `jiemeng`：即梦兼容 HTTP 网关适配，接受 Bearer Key 和 `/v1/images/generations` 请求，支持 URL/Base64 图片。配置 `JIEMENG_API_KEY`、`JIEMENG_BASE_URL` 与模型；火山官方签名网关可由部署侧适配。

真实渠道未配置 Key 时会明确报错，不会静默伪装为成功；生成失败会保留 FAILED 任务并自动返还次数。只有 `AI_PROVIDER=demo` 的响应标记 `demo_mode=true`。

## 接口约定

所有业务响应统一为：

```json
{"code": 0, "message": "success", "data": {}}
```

失败时 `code` 非零，HTTP 状态同时表达错误类型；参数错误统一为 `42200`。认证请求使用：

```text
Authorization: Bearer <access_token>
```

主要接口：

| 模块 | 接口 |
| --- | --- |
| 认证 | `POST /api/auth/register`、`POST /api/auth/login`、`GET /api/auth/me` |
| AI | `GET /api/ai/templates`、`POST /api/ai/generate`、`GET /api/ai/tasks/{id}`、`GET /api/ai/assets` |
| 展示 | `GET /api/products`、`GET /api/artists`、`GET /api/artists/{id}` |
| 订单 | `POST /api/orders`、`GET /api/orders`、`GET /api/orders/{id}`、`GET /api/orders/{id}/timeline`、`POST /api/orders/{id}/confirm-design` |
| 消息 | `GET /api/messages` |
| 后台 | `GET /api/admin/orders`、`POST /api/admin/orders/{id}/status`、`POST /api/admin/orders/{id}/progress`、`GET/POST /api/admin/artists`、`PUT /api/admin/artists/{id}`、`GET /api/admin/stats` |

生成请求示例：

```json
{
  "template_id": 1,
  "prompt": "一位执团扇的少女，海棠花下，温柔回眸",
  "ratio": "3:4",
  "count": 1,
  "style_strength": 0.75
}
```

下单金额由服务端按载体价格计算，客户端不能传入金额。数据库全部使用整数分（`base_price_cents` / `amount_cents`），响应同时提供两位小数字符串，避免浮点误差。

## 订单状态机

```text
PENDING_CONFIRM → DESIGN_CONFIRM → ASSIGNED → IN_PRODUCTION
→ QUALITY_CHECK → SHIPPED → COMPLETED
```

只允许顺序流转。交付画师前必须由用户确认定稿并选择有效画师；发货必须有物流单号。每次流转写入状态流水并生成站内信。普通用户仅能访问自己的任务、作品和订单；后台接口要求 `ADMIN` 角色。

## 目录

```text
app/
  main.py                 # 应用、中间件、统一异常处理
  config.py / database.py
  models.py / schemas.py / serializers.py
  security.py             # PBKDF2 密码哈希、JWT、RBAC
  seed.py                 # 幂等演示数据
  routers/                # 按领域划分接口
  services/
    ai_provider.py        # Demo / 通义 / 即梦适配器与 SVG 生成
    generation.py         # 配额原子扣减、失败返还、任务落库
    orders.py             # 状态机、流水、通知
static/generated/         # 本地生成及种子图片
```
