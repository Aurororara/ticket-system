from models import db
from models.show import Show
from models.host import Host
from models.location import Location
from datetime import date
from app import app  # 要有這行！

with app.app_context():
    # 檢查並建立 host
    host = Host.query.filter_by(host_name="Live Nation").first()
    if not host:
        host = Host(
            host_name="Live Nation",
            host_email="fakelivenation@gmail.com",
            createdAt=date.today(),
            updatedAt=date.today()
        )
        db.session.add(host)

    # 檢查並建立 location
    location = Location.query.filter_by(loc_name="林口體育館").first()
    if not location:
        location = Location(
            loc_name="林口體育館",
            createdAt=date.today(),
            updatedAt=date.today()
        )
        db.session.add(location)

    db.session.commit()

    # 建立節目
    show = Show(
        show_name="keshi: REQUIEM TOUR in Taipei 2025",
        show_desc="""全球狂飆百億串流
超人氣亞裔創作才子 keshi
療癒系陪伴 征服全世界

2025 全新進化巡迴
𝐤𝐞𝐬𝐡𝐢: 𝐑𝐄𝐐𝐔𝐈𝐄𝐌 𝐓𝐎𝐔𝐑
2025年3月28日 重返台北
♦ SPECIAL GUESTS：BOYLIFE

※ 全座位，請務必對號入座。
※ 實際時間請以現場公告為準
※ 本場演出於演出前5日始開放取票。
※ VIP 福利活動報到時間 ≠ 演出時間，請至 LIVE NATION TAIWAN 官網確認。
※ 各階段預購僅提供特定服務，座位順序不一定比較前面。

📍禁止攜帶飲料食物、攝影設備、直播器材、行李箱等大型物品。
📍請配合安檢並提早入場。
📍會場無置物櫃，建議輕便前往。
📍主辦單位保留變更及終止活動之權利。

① 所有音樂已依法申請著作權授權。
② 本場演出向 MÜST 取得授權。

* SPONSORED BY：北商四人辣妹組""",
        show_pic="/static/Showdetail/keshi_tour.jpg",  # 圖片記得放對
        host_id=host.host_id,
        location_id=location.loc_id,
        createdAt=date(2025, 3, 20),
        updatedAt=date.today()
    )

    db.session.add(show)
    db.session.commit()

