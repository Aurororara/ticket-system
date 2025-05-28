from app import app
from models import db
from models.show import Show
from models.host import Host
from models.location import Location
from datetime import date

with app.app_context():
    # 檢查是否已存在主辦與地點
    host = Host.query.filter_by(host_name="Live Nation").first()
    if not host:
        host = Host(
            host_name="Live Nation",
            host_email="fakelivenation@gmail.com",
            createdAt=date.today(),
            updatedAt=date.today()
        )
        db.session.add(host)
        db.session.commit()

    location = Location.query.filter_by(loc_name="林口體育館").first()
    if not location:
        location = Location(
            loc_name="林口體育館",
            createdAt=date.today(),
            updatedAt=date.today()
        )
        db.session.add(location)
        db.session.commit()

    # 新增 keshi 節目
    existing_show = Show.query.filter_by(show_name="keshi: REQUIEM TOUR in Taipei 2025").first()
    if not existing_show:
        show = Show(
            show_name="keshi: REQUIEM TOUR in Taipei 2025",
            show_desc="""全球狂飆百億串流
超人氣亞裔創作才子 keshi
療癒系陪伴 征服全世界

2025 全新進化巡迴
𝐤𝐞𝐬𝐡𝐢: 𝐑𝐄𝐐𝐔𝐈𝐄𝐌 𝐓𝐎𝐔𝐑
2025年10月28日 重返台北
♦ SPECIAL GUESTS：BOYLIFE

📍禁止攜帶飲料食物、攝影設備、直播器材、行李箱等大型物品。
📍請配合安檢並提早入場。
📍主辦單位保留變更及終止活動之權利。

* SPONSORED BY：北商四人辣妹組""",
            show_pic="/static/Showdetail/keshi_tour.jpg",
            host_id=host.host_id,
            location_id=location.loc_id,
            start_date=date(2025, 10, 28),
            end_date=date(2025, 10, 28),
            createdAt=date(2025, 8, 27),
            updatedAt=date.today()
        )
        db.session.add(show)
        db.session.commit()
        print("✅ 成功新增 keshi 節目！")
    else:
        print("🟡 已有 keshi 節目，不重複新增")
