from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import (
    Artist,
    GenerationTask,
    MediaAsset,
    Message,
    Order,
    OrderProgressPost,
    OrderStatus,
    OrderStatusHistory,
    Product,
    PromptTemplate,
    TaskStatus,
    User,
    UserQuota,
    UserRole,
)
from .security import hash_password
from .services.ai_provider import create_demo_art

TEMPLATES = [
    ("工笔", "工笔·仕女图", "细腻线描与典雅设色的东方人物画像", "中国工笔画人物，精致五官，细腻白描线条，淡雅矿物色，宋代仕女造型，宣纸肌理，留白构图"),
    ("水墨", "水墨·云山行旅", "墨色浓淡之间，人物与山水相生", "中国水墨写意，人物行旅，层叠远山，云雾氤氲，飞白笔触，黑白灰辅以朱砂点染，诗意留白"),
    ("敦煌", "敦煌·飞天入梦", "汲取壁画配色与飘带韵律", "敦煌壁画风人物，飞天飘带，石青石绿与赭石朱砂配色，唐代纹样，矿物颜料斑驳质感，庄严柔美"),
    ("剪纸", "剪纸·纸上生花", "以镂空线条重塑国风形象", "中国非遗剪纸艺术，人物侧影，对称窗花，镂空纹样，朱砂红宣纸，边缘清晰，传统吉祥图案"),
    ("青花", "青花·瓷韵肖像", "青花纹样与清雅人物融合", "青花瓷风格人物画像，钴蓝线描，缠枝莲纹，白瓷底色，清雅蓝白渐变，东方器物之美"),
    ("油画", "油画·流光肖像", "厚重笔触下的东方人物情绪", "古典油画人物肖像，柔和伦勃朗光，厚涂笔触，东方服饰细节，深黛蓝背景，鎏金光影，博物馆质感"),
    ("国潮", "Q版·国潮少年", "明快可爱的潮流国风形象", "Q版国潮人物，三头身，灵动表情，现代中式服装，祥云与回纹，朱砂红黛蓝撞色，精致潮流插画"),
    ("山水", "新中式·月下清影", "圆月竹影中的诗意人物剪影", "新中式国风插画，月下人物剪影，竹林与水墨山峦，宣纸底，黛蓝渐变，朱砂钤印，高级留白"),
]

PRODUCTS = [
    ("国画卷轴", "国画", 89900, "宣纸手绘后以传统浆糊装裱，配锦绫天地杆与题款钤印，适合厅堂陈设。", 18, ["45×90cm", "60×120cm"]),
    ("非遗团扇", "扇面", 39900, "桑蚕丝绢面团扇，画师依扇形构图，手工收边，配流苏与礼盒。", 12, ["直径21cm", "直径24cm"]),
    ("青花料彩瓷板画", "瓷板画", 129900, "瓷板人工绘色后低温固彩，釉色莹润，配实木框，兼具收藏与装饰价值。", 25, ["30×40cm", "40×60cm"]),
    ("博物馆级油画布框", "油画", 159900, "亚麻画布与实木内框，手工塑形底、分层罩染，完成后涂保护光油。", 28, ["50×60cm", "60×80cm"]),
    ("苏绣肖像摆件", "刺绣", 189900, "以蚕丝线分层施针，呈现人物肤色与衣纹层次，配胡桃木双面绣台屏。", 35, ["25cm圆绣", "30cm圆绣"]),
    ("国风伴手礼盒", "礼盒", 25900, "含手绘小卡、宣纸折页与朱砂印章收藏卡，适合节日赠礼与纪念。", 8, ["A6小卡", "8寸折页"]),
]

ARTISTS = [
    ("沈砚秋", "沈老师", "13800001001", ["工笔", "国画"], "研习工笔人物十二年，擅长以细密线描捕捉人物神韵，作品多次入选青年工艺美术展。", 12, "4.98"),
    ("林青黛", "林老师", "13800001002", ["水墨", "扇面"], "出身书画世家，主攻水墨写意与绢本扇面，笔墨清润，注重东方留白与人物情态。", 10, "4.96"),
    ("苏锦绣", "苏老师", "13800001003", ["苏绣", "肖像"], "苏绣青年传承人，善用虚实针与散套针表现肖像层次，让针线呈现细腻光影。", 15, "5.00"),
]


def _create_user(db: Session, email: str, password: str, nickname: str, role: UserRole) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        user = User(email=email, password_hash=hash_password(password), nickname=nickname, role=role)
        user.quota = UserQuota(remaining_count=30, total_purchased=30, total_used=0)
        db.add(user)
        db.flush()
    elif user.quota is None:
        user.quota = UserQuota(remaining_count=30, total_purchased=30, total_used=0)
        db.flush()
    return user


def seed_database(db: Session) -> None:
    """按唯一键逐项补齐种子，重复启动不会重复插入或重置用户配额。"""
    demo = _create_user(db, "demo@jinghui.art", "Demo123456", "镜绘体验官", UserRole.USER)
    admin = _create_user(db, "admin@jinghui.art", "Admin123456", "镜绘运营", UserRole.ADMIN)

    for index, (category, name, description, prompt) in enumerate(TEMPLATES, start=1):
        if db.scalar(select(PromptTemplate).where(PromptTemplate.name == name)) is None:
            art = create_demo_art(prompt, "3:4", f"template_{index:02d}")
            db.add(PromptTemplate(
                category=category,
                name=name,
                description=description,
                positive_prompt=prompt,
                negative_prompt="低质量，模糊，肢体变形，五官错位，现代水印，文字乱码",
                params_json={"ratio": "3:4", "style_strength": 0.75},
                cover_url=art.url,
                sort_order=index,
            ))

    for index, (name, category, price, description, days, sizes) in enumerate(PRODUCTS, start=1):
        if db.scalar(select(Product).where(Product.name == name)) is None:
            art = create_demo_art(f"{name}，{description}", "1:1", f"product_{index:02d}")
            db.add(Product(
                name=name,
                category=category,
                base_price_cents=price,
                craft_desc=description,
                lead_time_days=days,
                spec_json={"sizes": sizes, "framing": "含基础装裱", "custom_inscription": True},
                cover_url=art.url,
                sort_order=index,
            ))

    for index, (pen_name, real_name, contact, specialties, intro, years, rating) in enumerate(ARTISTS, start=1):
        if db.scalar(select(Artist).where(Artist.pen_name == pen_name)) is None:
            avatar = create_demo_art(f"{pen_name}，{intro}", "1:1", f"artist_{index:02d}_avatar")
            work = create_demo_art(f"{specialties[0]}代表作品，{intro}", "3:4", f"artist_{index:02d}_work")
            db.add(Artist(
                pen_name=pen_name,
                real_name=real_name,
                contact=contact,
                specialties=specialties,
                intro=intro,
                avatar=avatar.url,
                representative_urls=[work.url],
                years_experience=years,
                rating=rating,
            ))
    db.commit()

    seed_prompts = [
        "工笔仕女，执团扇立于海棠花下，淡雅矿物色",
        "水墨青年，衣袂临风，远山与圆月相映",
        "敦煌飞天，飘带回旋，石青朱砂配色",
        "青花瓷韵少女，缠枝莲纹，清雅蓝白",
    ]
    demo_assets = []
    for index, prompt in enumerate(seed_prompts, start=1):
        task = db.scalar(select(GenerationTask).where(GenerationTask.provider_task_id == f"seed-demo-{index}"))
        if task is None:
            ratio = "3:4" if index % 2 else "1:1"
            art = create_demo_art(prompt, ratio, f"demo_artwork_{index:02d}")
            created = datetime.now(timezone.utc) - timedelta(days=10 - index)
            template = db.scalar(
                select(PromptTemplate).where(PromptTemplate.name == TEMPLATES[index - 1][1])
            )
            task = GenerationTask(
                user_id=demo.id,
                template_id=template.id if template else None,
                prompt=prompt,
                params_json={"ratio": ratio, "count": 1, "style_strength": 0.75},
                provider_code="demo",
                provider_task_id=f"seed-demo-{index}",
                status=TaskStatus.SUCCESS,
                cost_count=1,
                demo_mode=True,
                created_at=created,
                completed_at=created,
            )
            db.add(task)
            db.flush()
            asset = MediaAsset(
                task_id=task.id,
                owner_type="USER",
                owner_id=demo.id,
                kind="GENERATED",
                url=art.url,
                thumbnail_url=art.url,
                width=art.width,
                height=art.height,
                meta_json=art.meta,
                created_at=created,
            )
            db.add(asset)
            db.flush()
        else:
            asset = db.scalar(select(MediaAsset).where(MediaAsset.task_id == task.id).order_by(MediaAsset.id))
        demo_assets.append(asset)
    db.commit()

    order_no = "JH-DEMO-20261104-001"
    if db.scalar(select(Order).where(Order.order_no == order_no)) is None:
        product = db.scalar(select(Product).order_by(Product.id))
        artist = db.scalar(select(Artist).order_by(Artist.id))
        created = datetime.now(timezone.utc) - timedelta(days=6)
        order = Order(
            order_no=order_no,
            user_id=demo.id,
            product_id=product.id,
            media_asset_id=demo_assets[0].id,
            artist_id=artist.id,
            spec_json={"size": "45×90cm", "framing": "锦绫传统装裱", "inscription": "岁岁常欢愉", "note": "保留定稿中的海棠与团扇"},
            amount_cents=product.base_price_cents,
            status=OrderStatus.IN_PRODUCTION,
            shipping_info_json={"name": "林小镜", "phone": "13800000000", "address": "浙江省杭州市西湖区镜绘路 88 号"},
            design_confirmed=True,
            confirmed_at=created + timedelta(days=2),
            created_at=created,
        )
        db.add(order)
        db.flush()
        histories = [
            (None, OrderStatus.PENDING_CONFIRM, UserRole.USER, demo.id, "定稿与定制需求已提交，等待平台确认", 0),
            (OrderStatus.PENDING_CONFIRM, OrderStatus.DESIGN_CONFIRM, UserRole.ADMIN, admin.id, "平台已整理定稿图与卷轴制作要求", 1),
            (OrderStatus.DESIGN_CONFIRM, OrderStatus.ASSIGNED, UserRole.USER, demo.id, "用户确认定稿，订单交付沈砚秋画师", 2),
            (OrderStatus.ASSIGNED, OrderStatus.IN_PRODUCTION, UserRole.ADMIN, admin.id, "画师已接单并备妥宣纸、矿物颜料", 3),
        ]
        for from_status, to_status, operator_type, operator_id, note, days in histories:
            db.add(OrderStatusHistory(
                order_id=order.id,
                from_status=from_status,
                to_status=to_status,
                operator_type=operator_type,
                operator_id=operator_id,
                note=note,
                created_at=created + timedelta(days=days),
            ))
        progress = [
            ("起稿 · 立意定型", "画师根据 AI 定稿重新经营位置，以淡墨勾勒人物、团扇与海棠的主次关系，保留画面左侧诗意留白。", "seed_progress_01", 3),
            ("勾线 · 墨线骨法", "以中锋细笔完成人物衣纹与花枝勾线，线条轻重随结构起伏，团扇纹样也已逐笔理清。", "seed_progress_02", 4),
            ("分染 · 层层敷色", "采用花青、赭石与淡朱砂多次分染，衣色渐显温润层次；下一步将罩染背景并题款钤印。", "seed_progress_03", 5),
        ]
        for step, content, filename, days in progress:
            post = OrderProgressPost(
                order_id=order.id,
                step_name=step,
                content=content,
                posted_by=admin.id,
                operator_type=UserRole.ADMIN,
                created_at=created + timedelta(days=days),
            )
            db.add(post)
            db.flush()
            art = create_demo_art(f"{step}，{content}", "3:4", filename)
            asset = MediaAsset(
                owner_type="ORDER_PROGRESS",
                owner_id=post.id,
                kind="PROGRESS",
                url=art.url,
                thumbnail_url=art.url,
                width=art.width,
                height=art.height,
                meta_json={"order_id": order.id, "stage": step},
                created_at=post.created_at,
            )
            db.add(asset)
            db.flush()
            post.media_ids = [asset.id]
        db.add(Message(
            user_id=demo.id,
            type="ORDER",
            title="您的卷轴正在创作中",
            content="沈砚秋画师已完成起稿、勾线与首轮分染，点击查看创作实拍。",
            ref_order_id=order.id,
            created_at=created + timedelta(days=5),
        ))
    if not db.scalar(select(Message).where(Message.user_id == demo.id, Message.type == "WELCOME")):
        db.add(Message(
            user_id=demo.id,
            type="WELCOME",
            title="欢迎来到镜绘",
            content="已为您预置 4 幅 AI 国风形象与 1 个创作中的订单，另赠 30 次生成次数，开始体验吧。",
        ))
    db.commit()
