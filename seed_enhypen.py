from models import db
from models.show import Show
from models.host import Host
from models.location import Location
from datetime import date
from app import app  # 要有這行！

with app.app_context():
    # 檢查並建立 host
    host = Host.query.filter_by(host_name="遠雄國際").first()
    if not host:
        host = Host(
            host_name="遠雄國際",
            host_email="farbear@gmail.com",
            createdAt=date.today(),
            updatedAt=date.today()
        )
        db.session.add(host)

    # 檢查並建立 location
    location = Location.query.filter_by(loc_name="台北小巨蛋").first()
    if not location:
        location = Location(
            loc_name="台北小巨蛋",
            createdAt=date.today(),
            updatedAt=date.today()
        )
        db.session.add(location)

    db.session.commit()

    # 建立節目
    show = Show(
        show_name="ENHYPEN WORLD TOUR 'FATE' IN ASIA",
        show_desc="""選秀節目《I-LAND》出道的人氣韓團ENHYPEN透過官方社群平台官方宣布舉辦「ENHYPEN WORLD TOUR ‘FATE’ IN ASIA」，即將於2025年9月開始展開的巡迴演唱會首站為台北，各位ENGENE記得密切鎖定最新搶票消息！
2025年9月2日 引爆台北
♦ SPECIAL GUESTS：北商辣妹四人組

※ 全座位，請務必對號入座。
※ 實際時間請以現場公告為準
※ 本場演出於演出前5日始開放取票。
※ VIP 福利活動報到時間 ≠ 演出時間，請至遠雄國際官網確認。
※ 各階段預購僅提供特定服務，座位順序不一定比較前面。

📍禁止攜帶飲料食物、攝影設備、直播器材、行李箱等大型物品。
📍請配合安檢並提早入場。
📍會場無置物櫃，建議輕便前往。
📍主辦單位保留變更及終止活動之權利。

① 所有音樂已依法申請著作權授權。
② 本場演出向HYPE取得授權。

* SPONSORED BY：北商四人辣妹組""",
        show_pic="/static/Showdetail/E.jpg",  # 圖片記得放對
        host_id=host.host_id,
        location_id=location.loc_id,
        createdAt=date(2025, 3, 20),
        updatedAt=date.today()
    )

    db.session.add(show)
    db.session.commit()

