from app import app
from models import db
from models.show import Show
from models.host import Host
from models.location import Location
from datetime import date

with app.app_context():
    # 檢查是否已有相同節目名稱，避免重複新增
    existing_show = Show.query.filter_by(show_name="2025 BABYMONSTER 1ST WORLD TOUR <HELLO MONSTER> IN TAIPEI").first()

    if existing_show:
        print("🟡 已經有 BABYMONSTER 節目，不重複新增")
    else:
        # 新增主辦單位
        host = Host(
            host_name="Live Nation",
            host_email="fakelivenation@gmail.com",
            createdAt=date.today(),
            updatedAt=date.today()
        )

        # 新增場地
        location = Location(
            loc_name="林口體育館",
            createdAt=date.today(),
            updatedAt=date.today()
        )

        db.session.add_all([host, location])
        db.session.commit()

        # 新增節目
        show = Show(
            show_name="2025 BABYMONSTER 1ST WORLD TOUR <HELLO MONSTER> IN TAIPEI",
            show_desc="""2025 BABYMONSTER 1ST WORLD TOUR <HELLO MONSTERS> IN TAIPEI
台北MONSTIEZ! got drip, drip, drip!
怪物新人女團 BABYMONSTER 首次世界巡迴 台北站
2025.9.28 (日) 林口體育館 震撼開唱

📍入場須配合安檢及入場須知
禁止攜帶超過 37 x 25 x 11.5 公分包包和行李箱
禁止外食、自拍棒、直播等
請詳讀 LIVE NATION TAIWAN 官方公告資訊
主辦單位保留修改活動權利

SPONSORED BY：北商四人辣妹組""",
            show_pic="/static/Showdetail/bm.jpg",
            host_id=host.host_id,
            location_id=location.loc_id,
            start_date=date(2025, 8, 20),  # ✅ 補上這兩個超關鍵的欄位
            end_date=date(2025, 8, 20),
            createdAt=date.today(),
            updatedAt=date.today()
        )

        db.session.add(show)
        db.session.commit()
        print("✅ BABYMONSTER 節目已成功新增！")

    print("📂 使用的資料庫：", app.config['SQLALCHEMY_DATABASE_URI'])
