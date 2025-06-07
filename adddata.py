from app import app, db
from models import Member, Show, Host, Location, Game, Area, Section, Order, Payment, Ticket, GameArea
from models.refund import Refund
from datetime import datetime, date, time, timedelta
from werkzeug.security import generate_password_hash
import random

with app.app_context():
    db.drop_all()
    db.create_all()

    # === Members ===
    member = Member(
        mem_name="roro",
        mem_email="roro@ggg.com",
        mem_pwd=generate_password_hash("Roro0606"),
        mem_phone="0912345678",
        birthday=date(2025, 10, 11),
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )
    db.session.add(member)


    # === Hosts ===
    hosts_data = [
        ("Live Nation", "livenation@example.com"),
        ("APPLEWOOD", "applewood@example.com"),
        ("ULC Presents", "ulcpresents@example.com"),
        ("相信音樂", "binmusic@example.com"),
        ("遠雄遠藝", "farglorycreative@example.com"),
        ("希林國際", "Chillin@example.com"),
    ]

    hosts = [
        Host(
            host_name=name,
            host_email=email,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        for name, email in hosts_data
    ]
    db.session.add_all(hosts)

    # === Locations ===
    locations_data = [
        "Zepp New Taipei",
        "國立體育大學綜合體育館 (林口體育館)",
        "台北Legacy TERA",
        "Legacy Taipei",
        "高雄國家體育場 (世運主場館)",
        "高雄流行音樂中心（KAOHSIUNG MUSIC CENTER）",
        "台北流行音樂中心表演廳",
        "台北國際會議中心TICC",
    ]

    locations = [
        Location(
            loc_name=name,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        for name in locations_data
    ]
    db.session.add_all(locations)

    db.session.commit()  # 先 commit hosts + locations

    # === Shows Data ===
    shows_data = [
        {
            "show_name": "2025 Jay Park World Tour [Serenades ＆ Body Rolls]",
            "show_desc": """睽違6年！全面回歸！
Jay Park 朴載範 全新世界巡迴 台北站
2025 Jay Park World Tour [Serenades & Body Rolls]
6月19日 Zepp New Taipei 性感開唱
 
2025 Jay Park World Tour [Serenades & Body Rolls]
時間：2025/ 6 / 19（四）20:00
地點：Zepp New Taipei（新莊宏匯廣場8F）

※ 關於福利抽選：親簽拍立得於2025/6/2（一）中午12點截止，完成付款且無退票之所有持票者，將可參與購買票價之相對應福利抽獎活動。各票價中需抽選之福利將不重複抽取。抽獎結果預計將於2025/6/6（五）公布於LIVE NATION TAIWAN官方網站、官方社群網頁及拓元售票系統節目頁面。福利與演出票券僅限同一人使用。
※演出時間不等於福利抽獎活動報到時間，請務必於演出日前至LIVE NATION TAIWAN官方網站及社群頁面詳讀福利抽獎活動入場時間及相關流程，以免損害自身權益。福利抽獎活動將以演出前公布的報到時間為準，逾時者視同放棄權利，主辦單位將有權拒絕未於報到時間內完成報到手續者入場，且不予退票。
※ 實際時間請依現場公告為準。
※ 為了人身安全考量，孕婦及身高未滿110公分或未滿7歲孩童，請勿購買站區票券，主辦方將有權謝絕入場。
※ 請務必於演出日前關注主辦單位官方網站及臉書頁面，詳讀確認入場時間流程及相關規範，以免損害自身權益。""",
            "show_pic": "25_jaypark.jpg",
            "start_date": date(2025, 6, 19),
            "end_date": date(2025, 6, 19),
            "host_name": "Live Nation",
            "location_name": "Zepp New Taipei",
            "sections": [
                "VIP Serenades",
                "VIP Body Rolls",
                "1F站區 GA",
                "2F座位 SEATED",
                "2F站區 GA",
            ],
            "areas": [
                ("一樓站席", 10, 2, 7800, 5000, "VIP Serenades"),
                ("一樓站席", 15, 2, 4800, 2800, "VIP Body Rolls"),
                ("一樓站席", 10, 2, 3300, 1300, "1F站區 GA"),
                ("二樓座位區", 10, 2, 3300, 1300, "2F座位 SEATED"),
                ("二樓站席", 10, 0, 2800, 800, "2F站區 GA"),
            ],
            "games": [
                {
                    "game_date": date(2025, 6, 19),
                    "game_time": time(20, 0),
                    "sale_start_time": datetime(2025, 4, 1, 12, 30, 0),
                    "sale_end_time": datetime(2025, 6, 19, 12, 30, 0),
                },
            ],
        },
        {
            "show_name": "2025 LE SSERAFIM TOUR ’EASY CRAZY HOT’ IN TAIPEI",
            "show_desc": """期待與LE SSERAFIM一同開心共度2025 Summer Party!

𝟐𝟎𝟐𝟓 𝐋𝐄 𝐒𝐒𝐄𝐑𝐀𝐅𝐈𝐌 𝐓𝐎𝐔𝐑 '𝐄𝐀𝐒𝐘 𝐂𝐑𝐀𝐙𝐘 𝐇𝐎𝐓' 𝐈𝐍 𝐓𝐀𝐈𝐏𝐄𝐈

📆 演出日期：

2025.07.19 (六) 6PM (Local Time) | (實際演出時間以現場公告為準)
2025.07.20 (日) 5PM (Local Time) | (實際演出時間以現場公告為準)

📍 演出地點：
國立體育大學綜合體育館 (林口體育館)

FEARNOT～準備好要和LE SSERAFIM一起尋找𝔾𝕆𝕆𝔻 ℙ𝔸ℝ𝕋𝕊了嗎？！🥰
記得查看詳情，一起迎接我們的𝓟𝓮𝓻𝓯𝓮𝓬𝓽 𝓝𝓲𝓰𝓱𝓽！˚₊‧꒰ა 𓂋 ໒꒱ ‧₊˚

⬣ 粉絲福利：粉絲福利詳情請參考粉絲福利說明圖。

※一人一票，憑票入場，孩童亦需購票。因考量人身安全及整體音量恐對孩童造成影響及其身高受限而影響視線，故孕婦及身高未滿110公分或7歲以下之孩童不建議購買搖滾站區，主辦方將有權謝絕入場，購票前請自行斟酌。
※活動現場禁止使用任何器材拍照、攝影、直播、錄音，違者須依照工作人員指示離場。
※場館內禁止攜帶任何種類之金屬、玻璃、雷射筆、煙火或任何危險物品、且不得吸菸、嚼食檳榔及飲酒。
※觀眾席內禁止攜帶外食、飲料。
※禁止攜帶寵物(導盲犬除外)進入館內。
※因應場館規定，不遵守規定者，工作人員得禁止其入場或強制驅離出場。
※請務必於演出日前至主辦單位官方網站及社群頁面確認入場規範、粉絲福利入場流程等相關資訊，以免損害自身權益。如未能於公佈的進場/福利整隊時間內報到，將視為放棄排隊序號或福利權利。
※活動當天入場時需配合嚴格安檢，活動相關內容及詳細辦法請關注活動主辦單位APPLEWOOD及APPLEWOOD TAIWAN官方臉書及拓元售票網頁。

以上活動內容，主辦單位保留異之權力。""",
            "show_pic": "25_lsf.jpg",
            "start_date": date(2025, 7, 19),
            "end_date": date(2025, 7, 20),
            "host_name": "APPLEWOOD",
            "location_name": "國立體育大學綜合體育館 (林口體育館)",
            "sections": [
                "7300區",
                "6300區",
                "5300區",
                "4800區",
                "4300區",
                "3500區",
            ],
            "areas": [
                ("SVIP STANDING A區7300", 100, 2, 7300, 5300, "7300區"),
                ("SVIP STANDING B區7300", 10, 5, 7300, 5300, "7300區"),
                ("SVIP STANDING C區7300", 10, 2, 7300, 5300, "7300區"),
                ("SVIP STANDING D區7300", 10, 2, 7300, 5300, "7300區"),
                ("VIP座位 O1B-2區6300", 15, 2, 6300, 4300, "6300區"),
                ("VIP座位 O2B-1區6300", 15, 1, 6300, 4300, "6300區"),
                ("VIP座位 O2B-2區6300", 15, 2, 6300, 4300, "6300區"),
                ("VIP座位 O4B-1區6300", 15, 1, 6300, 4300, "6300區"),
                ("VIP座位 B2B-1區6300", 15, 1, 6300, 4300, "6300區"),
                ("VIP座位 B2B-2區6300", 15, 2, 6300, 4300, "6300區"),
                ("VIP座位 B3B-1區6300", 15, 1, 6300, 4300, "6300區"),
                ("VIP座位 B3B-2區6300", 15, 2, 6300, 4300, "6300區"),
                ("VIP座位 B4B-1區6300", 15, 1, 6300, 4300, "6300區"),
                ("VIP座位 B4B-2區6300", 15, 2, 6300, 4300, "6300區"),
                ("VIP座位 Y4B-2區6300", 15, 2, 6300, 4300, "6300區"),
                ("VIP座位 Y2B-1區6300", 15, 1, 6300, 4300, "6300區"),
                ("VIP座位 Y2B-2區6300", 15, 2, 6300, 4300, "6300區"),
                ("VIP座位 Y1B-1區6300", 15, 1, 6300, 4300, "6300區"),
                # 5300區
                ("O1B-1區5300", 15, 1, 5300, 3300, "5300區"),
                ("O4B-2區5300", 15, 2, 5300, 3300, "5300區"),
                ("B1B-1區5300", 15, 1, 5300, 3300, "5300區"),
                ("B1B-2區5300", 15, 2, 5300, 3300, "5300區"),
                ("B5B-1區5300", 15, 1, 5300, 3300, "5300區"),
                ("B5B-2區5300", 15, 2, 5300, 3300, "5300區"),
                ("Y4B-1區5300", 15, 1, 5300, 3300, "5300區"),
                ("Y1B-2區5300", 15, 2, 5300, 3300, "5300區"),
                # 4800區
                ("B1A-1區4800", 15, 1, 4800, 2800, "4800區"),
                ("B1A-2區4800", 15, 2, 4800, 2800, "4800區"),
                ("B2A-1區4800", 15, 1, 4800, 2800, "4800區"),
                ("B2A-2區4800", 15, 2, 4800, 2800, "4800區"),
                ("B4A-2區4800", 15, 2, 4800, 2800, "4800區"),
                ("B5A-1區4800", 15, 1, 4800, 2800, "4800區"),
                ("B5A-2區4800", 15, 2, 4800, 2800, "4800區"),
                ("B5A-3區4800", 15, 3, 4800, 2800, "4800區"),
                # 4300區
                ("O1A-2區4300", 15, 2, 4300, 2300, "4300區"),
                ("O2A-1區4300", 15, 1, 4300, 2300, "4300區"),
                ("O2A-2區4300", 15, 2, 4300, 2300, "4300區"),
                ("O4A-1區4300", 15, 1, 4300, 2300, "4300區"),
                ("Y4A-1區4300", 15, 1, 4300, 2300, "4300區"),
                ("Y4A-2區4300", 15, 2, 4300, 2300, "4300區"),
                ("Y2A-1區4300", 15, 1, 4300, 2300, "4300區"),
                ("Y2A-2區4300", 15, 2, 4300, 2300, "4300區"),
                ("Y1A-1區4300", 15, 1, 4300, 2300, "4300區"),
                # 3500區
                ("O1A-2區3500", 15, 2, 3500, 1500, "3500區"),
                ("O2A-1區3500", 15, 1, 3500, 1500, "3500區"),
                ("O2A-2區3500", 15, 2, 3500, 1500, "3500區"),
                ("O4A-1區3500", 15, 1, 3500, 1500, "3500區"),
                ("Y4A-1區3500", 15, 1, 3500, 1500, "3500區"),
                ("Y4A-2區3500", 15, 2, 3500, 1500, "3500區"),
                ("Y2A-1區3500", 15, 1, 3500, 1500, "3500區"),
                ("Y2A-2區3500", 15, 2, 3500, 1500, "3500區"),
                ("Y1A-1區3500", 15, 1, 3500, 1500, "3500區"),
            ],
            "games": [
                {
                    "game_date": date(2025, 7, 19),
                    "game_time": time(18, 0),
                    "sale_start_time": datetime(2025, 4, 1, 12, 30, 0),
                    "sale_end_time": datetime(2025, 7, 19, 12, 30, 0),
                },
                {
                    "game_date": date(2025, 7, 20),
                    "game_time": time(17, 0),
                    "sale_start_time": datetime(2025, 4, 1, 12, 30, 0),
                    "sale_end_time": datetime(2025, 7, 20, 12, 30, 0),
                },
            ],
        },
        {
            "show_name": "MEW 30 THE FAREWELL SHOW TAIPEI",
            "show_desc": """不算朋友，也不算陌生人的大家

丹麥另類搖滾天團成軍 30 週年告別巡迴台北站，一起互道永別吧！

1997 年開始，哥本哈根四個大男孩嘗試成為一個真正的樂團，在家中用四軌機獨立製作錄音，既有美式另類的吉他聲響、也有英式搖滾的纖細文藝，在丹麥音樂圈造成極大迴響。2003 年加入主流廠牌後發行專輯《Frengers》，名稱源自他們結合朋友 (friends) 與陌生人 (strangers) 的自創單字，專輯中多首歌曲〈Am I Wry? No〉、〈156〉、〈She Came Home for Christmas〉都是獨立製作時期的再進化之作，樂團最具代表性的歌曲〈Comforting Sounds〉，細膩地堆疊情緒、爆發，感動全球無數樂迷。當年或許他們被 BBC 等音樂媒體給刻意忽略，但這張專輯發行遍佈全球，從日本、台灣到印尼，從俄羅斯到阿根廷，靠音樂征服樂迷。

樂團獲得成功後，MEW 步調緩慢但總交出動聽傑作，2005 年回歸吉他搖滾的專輯《and the Glass handed Kites》、2015 年氣度恢宏的《+ -》，甚至 2018 年與哥本哈根交響樂團合作的現場專輯，MEW 就像 Mercury Rev、Spiritualized 等經典樂團一樣，不斷昇華另類音樂的可能性。

非常感動曾多次訪台演出的 MEW，選擇台北作為告別巡迴的一站。Johan、Silas、Jonas 在公布巡迴消息時，留下了一段感人的話：「今天我們已經走遍了世界各地，表演了比我們記憶中更多的場次，但感覺就像昨天一樣，坐在那個嘈雜的臥室裡努力成為一支樂團。」

「我們誠摯邀請全球所有 Frengers 成員共同慶祝 MEW 成立30週年。我們非常興奮能參與這些演出，因為這對我們、對您以及 MEW 來說都是一個意義非凡的時刻。」

MEW 30 THE FAREWELL SHOW TAIPEI

日期：2025 年 11 月 21 日（五）

場地：Zepp New Taipei (宏匯廣場 8F)

時間：19:00 入場 / 20:00 開演

主辦：ULC Presents
""",
            "show_pic": "25_mewfarewe.jpg",
            "start_date": date(2025, 11, 21),
            "end_date": date(2025, 11, 21),
            "host_name": "ULC Presents",
            "location_name": "Zepp New Taipei",
            "sections": [
                "2280區",
                "3280區",
            ],
            "areas": [
                ("1F 站位區", 50, 2, 2280, 1200, "2280區"),
                ("2F 座位區", 15, 10, 3280, 1200, "3280區"),
            ],
            "games": [
                {
                    "game_date": date(2025, 11, 21),
                    "game_time": time(19, 0),
                    "sale_start_time": datetime(2025, 6, 30, 12, 30, 0),
                    "sale_end_time": datetime(2025, 11, 21, 12, 30, 0),
                },
            ],
        },
        {
            "show_name": "蘇慧倫Tarcy Su《就說給我聽Just Tell Me》新專輯演唱會",
            "show_desc": """蘇慧倫——就說給我聽，就唱給你聽

也許這不只是一場演唱會

而是一場交換禮物的夜晚

彼此聊聊最近過得好嗎



我們捧在掌心的輕與重

都等著在這夜晚，慢慢攤開，逐一聽見



她唱的每一句，是拆開的序幕

你聽的每一段，是回應的心事



這一夜，我們把故事打開

蘇慧倫和你面對面

把她不一定記得的風景

和我們不一定忘得了的心事

一首一首唱給你聽



就說給我聽——

說給這些年來的自己聽

說給你仍在想念的人聽

隨旋律流過的回憶

都化為一片片溫柔的光影



這一夜，我們就一起——

說給彼此聽


蘇慧倫Tarcy Su《就說給我聽Just Tell Me》新專輯演唱會New Album Live Tour 2025

6/22（日）19：00 台北Legacy TERA

主辦：相信音樂

※ 相關規定以活動官網及現場公告為主，主辦單位保留加場、修改、終止及本活動相關演出內容之權利。

※ 主辦單位於本演唱會進行過程中，將進行錄音/影、拍攝，部分觀眾之影像可能被拍攝或使用於演唱會影片中，敬請諒解！
""",
            "show_pic": "25_tarcysu.jpg",
            "start_date": date(2025, 6, 22),
            "end_date": date(2025, 6, 22),
            "host_name": "相信音樂",
            "location_name": "台北Legacy TERA",
            "sections": [
                "2600區",
            ],
            "areas": [
                ("A區", 50, 2, 2600, 1200, "2600區"),
                ("B區", 50, 2, 2600, 1200, "2600區"),
                ("C區", 50, 5, 2600, 1200, "2600區"),
                ("D區", 40, 2, 2600, 1200, "2600區"),
            ],
            "games": [
                {
                    "game_date": date(2025, 6, 22),
                    "game_time": time(19, 0),
                    "sale_start_time": datetime(2025, 3, 30, 12, 30, 0),
                    "sale_end_time": datetime(2025, 6, 22, 12, 30, 0),
                },
            ],
        },
        {
            "show_name": "VALLEY：WATER THE FLOWERS，PRAY FOR A GARDEN ASIA TOUR 2025",
            "show_desc": """VALLEY : WATER THE FLOWERS, PRAY FOR A GARDEN ASIA TOUR 2025
 
邁向成軍10週年 重返台北
多倫多獨立搖滾樂團 Valley

朱諾音樂大獎提名 流行樂壇新指標

 

2025 全新世界巡迴 💧🌻🙏🏻🪴

VALLEY : WATER THE FLOWERS, PRAY FOR A GARDEN ASIA TOUR

6月11日 Legacy Taipei 活力開唱

 

 

VALLEY : WATER THE FLOWERS, PRAY FOR A GARDEN ASIA TOUR 2025
時間：2025/06/11 (三) 20:00
地點：Legacy Taipei
 
📍入場須配合安檢及入場須知，
為安全考量，禁止攜帶後背包、超過 37 x 25 x 11.5公分之包包和行李箱；會場內全面禁止攜帶外食和飲料(水除外)、除手機之外任何形式之拍攝及錄音電子設備、自拍棒與危險物品（依主辦單位定義）等入場，主辦單位有權請違反規定者立即離開現場，會場內僅有少量置物櫃，如額滿請自行另覓處所寄物，建議輕便前往，並請提早到場進行安檢以避免耽誤觀賞演出。相關規定請關注LIVE NATION TAIWAN官方網站、官方臉書粉絲專頁、Instagram、Ｘ 獲得最新資訊。


📍以上活動內容，主辦單位保留異動之權力。 

①本公司為尊重他人音樂著作財產權，秉持事先授權原則，承諾於所舉辦之演唱會演出前向權利人申請合法授權。
②本場演出所使用音樂將向MÜST取得授權。""",
            "show_pic": "25_valley.jpg",
            "start_date": date(2025, 6, 11),
            "end_date": date(2025, 6, 11),
            "host_name": "Live Nation",
            "location_name": "Legacy Taipei",
            "sections": [
                "VALLEY",
            ],
            "areas": [
                ("全區", 50, 8, 1900, 1000, "VALLEY"),
            ],
            "games": [
                {
                    "game_date": date(2025, 6, 11),
                    "game_time": time(12, 0),
                    "sale_start_time": datetime(2025, 3, 12, 12, 30, 0),
                    "sale_end_time": datetime(2025, 6, 11, 9, 0, 0),
                },
            ],
        },
        {
            "show_name": "2025 STAYC TOUR [STAY TUNED] in TAIPEI　",
            "show_desc": """2025 STAYC TOUR [STAY TUNED] in TAIPEI　

今年暑假 關注鎖定
完顏全能女團 STAYC

全新世界巡迴
2025 STAYC TOUR [STAY TUNED] in TAIPEI
8月23日 (六) TICC 實力開唱
 

2025 STAYC TOUR [STAY TUNED] in TAIPEI

時間：2025/8/23 (六) 18:00
地點：台北國際會議中心TICC

M&G WITH SOUNDCHECK VIP PACKAGE套票，NT$ 7,800
包含：前排座席x1、演前隨機與其中一位團員單獨自拍、演前soundcheck、VIP紀念掛繩及吊牌、周邊商品優先購買權
SOUNDCHECK VIP PACKAGE套票，NT$ 5,800
包含：前區座席x1、演前soundcheck、VIP紀念掛繩及吊牌、周邊商品優先購買權


📍入場須配合安檢及入場須知，
為安全考量，禁止攜帶超過 37 x 25 x 11.5公分之包包和行李箱；會場內全面禁止攜帶外食和飲料(水除外)、除手機之外任何形式之拍攝及錄音電子設備、自拍棒與危險物品（依主辦單位定義）等入場，主辦單位有權請違反規定者立即離開現場，會場內無置物櫃，請自行另覓處所寄物，建議輕便前往，並請提早到場進行安檢以避免耽誤觀賞演出。相關規定請於演出日前造訪LIVE NATION TAIWAN官方網站、官方臉書粉絲專頁、Instagram、Ｘ 獲得最新資訊。

📍以上活動內容，主辦單位保留異動之權力。

 

①本公司為尊重他人音樂著作財產權，秉持事先授權原則，承諾於所舉辦之演唱會演出前向權利人申請合法授權。
②本場演出所使用音樂將向MÜST取得授權。

""",
            "show_pic": "25_stayc.jpg",
            "start_date": date(2025, 8, 23),
            "end_date": date(2025, 8, 23),
            "host_name": "Live Nation",
            "location_name": "台北國際會議中心TICC",
            "sections": [
                "M&G WITH SOUNDCHECK VIP PACKAGE 7800",
                "SOUNDCHECK VIP PACKAGE 5800",
                "4300區",
                "3800區",
                "2800區",
            ],
            "areas": [
                ("2M樓7800", 50, 2, 7800, 5800, "M&G WITH SOUNDCHECK VIP PACKAGE 7800"),
                ("2M樓5800", 50, 2, 5800, 3800, "SOUNDCHECK VIP PACKAGE 5800"),
                ("3樓7800", 50, 2, 5800, 3800, "SOUNDCHECK VIP PACKAGE 5800"),
                ("4樓4300", 50, 2, 4300, 2300, "4300區"),
                ("5樓3800", 50, 2, 3800, 1800, "3800區"),
                ("5樓包廂單號3800", 50, 2, 2800, 800, "3800區"),
                ("5樓包廂雙號3800", 50, 2, 2800, 800, "3800區"),
                ("6樓2800", 10, 2, 2800, 800, "2800區"),
                ("5樓包廂單號2800", 15, 5, 2800, 800, "2800區"),
                ("5樓包廂雙號2800", 15, 5, 2800, 800, "2800區"),
            ],
            "games": [
                {
                    "game_date": date(2025, 8, 23),
                    "game_time": time(18, 0),
                    "sale_start_time": datetime(2025, 4, 2, 12, 30, 0),
                    "sale_end_time": datetime(2025, 8, 23, 12, 30, 0),
                },
            ],
        },
        {
            "show_name": "iLiFE! Zepp6venue tour -TRAVE LiFE!-",
            "show_desc": """iLiFE! 首次海外公演 確定！
iLiFE! Zepp6venue tour -TRAVE LiFE!-

iLiFE! Zepp6venue tour -TRAVE LiFE!-
時間：2025/06/08 (日) 18:30
地點：Zepp New Taipei（新莊宏匯廣場8F）

※ 實際時間請依現場公告為準。
※ 為了人身安全考量，孕婦及身高未滿110公分或未滿7歲孩童，請勿購買站區票券，主辦方將有權謝絕入場。
※ 請務必於演出日前關注主辦單位官方網站及臉書頁面，詳讀確認入場時間流程及相關規範，以免損害自身權益。


主辦單位：Live Nation Taiwan、 HIP

📍入場須配合安檢及入場須知
為安全考量，禁止攜帶後背包、超過 37 x 25 x 11.5公分之包包和行李箱；會場內全面禁止攜帶外食和飲料(水除外)。未經主辦單位同意，禁止使用手機、行動裝置、各類相機、攝錄影機、DV、錄音機等，進行錄音、錄影、拍照、直播，並請勿攜帶各類照相與攝影設備等入場（含自拍棒），購票前請務必三思確認自己可以配合再買票。會場外設有限量置物櫃，建議輕便前往，並請提早到場進行安檢以避免耽誤觀賞演出。相關規定請於演出日前造訪LIVE NATION TAIWAN官方網站、官方臉書粉絲專頁、Instagram、Ｘ 獲得最新資訊。

📍以上活動內容，主辦單位保留異動之權力。

①本公司為尊重他人音樂著作財產權，秉持事先授權原則，承諾於所舉辦之演唱會演出前向權利人申請合法授權。
②本場演出所使用音樂將向MÜST取得授權。
""",
            "show_pic": "25_ilifetour.jpg",
            "start_date": date(2025, 6, 8),
            "end_date": date(2025, 6, 8),
            "host_name": "Live Nation",
            "location_name": "Zepp New Taipei",
            "sections": [
                "1F坐區(SEATED)",
                "1F站區",
            ],
            "areas": [
                ("SS-1F坐區4300", 50, 3, 4300, 2300, "1F坐區(SEATED)"),
                ("S-1F站區2800", 15, 3, 2800, 800, "1F站區"),
                ("GA-1F站區1500", 15, 3, 1500, 800, "1F站區"),
                ("GA-1F站區1000", 15, 3, 1000, 600, "1F站區"),
            ],
            "games": [
                {
                    "game_date": date(2025, 6, 8),
                    "game_time": time(18, 30),
                    "sale_start_time": datetime(2025, 5, 16, 12, 30, 0),
                    "sale_end_time": datetime(2025, 6, 8, 12, 30, 0),
                },
            ],
        },
        {
            "show_name": "2025 HYERI FANMEETING TOUR ＜Welcome to HYERI’s STUDIO＞ IN TAIPEI",
            "show_desc": """憑藉韓劇《善意的競爭》再創演藝事業高峰的韓國女演員 Girl’s Day 成員惠利，出道後的首次個人見面會巡迴《2025 HYERI FANMEETING TOUR <Welcome to HYERI’s STUDIO> IN TAIPEI》臺灣場門票甫開賣即銷售一空，經主辦單位積極與韓方爭取後，確認將加開 C 區及 D 區座位，並配合加開區域新增部分粉絲福利。加開座位門票將於 5 月 24 日上午 11 點在拓元票系統網站開賣，採實名制售票，票價為 C 區 TWD 3,600 / D 區 TWD 3,200，所有購票者皆可參與 HI-BYE 、獲得一張官方海報，C 區會獲得一張限定小卡，並擁有 1:20 團體合照及親簽海報的抽獎資格。

日前主辦單位才公布惠利與臺灣粉絲問候的影片，惠利除了分享對於睽違十年再度訪臺的期待心情，也提到她所主演的《善意的競爭》在臺灣非常受到歡迎，因此十分感謝粉絲的支持。惠利不只預告了自己正在認真準備見面會內容，還在影片的最後用中文說了劇中的經典台詞「雖然我可能會稍微遲到，但你一定要等我哦」，讓粉絲又驚又喜，也更加期待 7 月 5 日見面會的來臨。

 
《2025 HYERI FANMEETING TOUR <Welcome to HYERI’s STUDIO> IN TAIPEI》

𑁍 活動時間 ⎪ 2025 年 7 月 5 日（六）6PM（實際以現場為準）

𑁍 活動地點 ⎪ 台北國際會議中心TICC （臺北市信義區信義路五段1號）

𑁍 主辦單位 ⎪ O.N worldwide 오엔기획, HakunaMatata, 希林國際 Chillin International

""",
            "show_pic": "25_hyeri.png",
            "start_date": date(2025, 7, 5),
            "end_date": date(2025, 7, 5),
            "host_name": "希林國際",
            "location_name": "台北國際會議中心TICC",
            "sections": [
                "2M樓5600",
                "3樓5600",
                "4樓4600",
                "5樓3600",
                "5樓包廂3200",
                "6樓3200",
            ],
            "areas": [
                ("2M樓A1區5600", 70, 3, 5600, 3600, "2M樓5600"),
                ("2M樓A2區5600", 70, 3, 5600, 3600, "2M樓5600"),
                ("2M樓A3區5600", 70, 3, 5600, 3600, "2M樓5600"),
                ("2M樓A4區5600", 70, 3, 5600, 3600, "2M樓5600"),
                ("2M樓A5區5600", 70, 3, 5600, 3600, "2M樓5600"),
                ("3樓A6區5600", 50, 2, 5600, 3600, "3樓5600"),
                ("3樓A7區5600", 50, 2, 5600, 3600, "3樓5600"),
                ("3樓A8區5600", 50, 2, 5600, 3600, "3樓5600"),
                ("3樓A9區5600", 50, 2, 5600, 3600, "3樓5600"),
                ("3樓A10區5600", 50, 2, 5600, 3600, "3樓5600"),
                ("4樓B1區4600", 40, 2, 4600, 2600, "4樓4600"),
                ("4樓B2區4600", 40, 2, 4600, 2600, "4樓4600"),
                ("4樓B3區4600", 40, 2, 4600, 2600, "4樓4600"),
                ("4樓B4區4600", 40, 2, 4600, 2600, "4樓4600"),
                ("4樓B5區4600", 40, 2, 4600, 2600, "4樓4600"),
                ("5樓C1區3600", 50, 2, 3600, 2600, "5樓3600"),
                ("5樓C2區3600", 50, 2, 3600, 2600, "5樓3600"),
                ("5樓C3區3600", 50, 2, 3600, 2600, "5樓3600"),
                ("5樓C4區3600", 50, 2, 3600, 2600, "5樓3600"),
                ("5樓C5區3600", 50, 2, 3600, 2600, "5樓3600"),
                ("5樓單號包廂D6區3200", 10, 2, 3200, 1200, "5樓包廂3200"),
                ("5樓雙號包廂D6區3200", 10, 2, 3200, 1200, "5樓包廂3200"),
                ("6樓D1區3200", 50, 2, 3200, 1200, "6樓3200"),
                ("6樓D2區3200", 50, 2, 3200, 1200, "6樓3200"),
                ("6樓D3區3200", 50, 2, 3200, 1200, "6樓3200"),
                ("6樓D4區3200", 50, 2, 3200, 1200, "6樓3200"),
                ("6樓D5區3200", 50, 2, 3200, 1200, "6樓3200"), 
            ],
            "games": [
                {
                    "game_date": date(2025, 7, 5),
                    "game_time": time(18, 0),
                    "sale_start_time": datetime(2025, 5, 24, 11, 0, 0),
                    "sale_end_time": datetime(2025, 7, 5, 12, 30, 0),
                },
            ],
        },
        {
            "show_name": "2025 KAI SOLO CONCERT TOUR ＜KAION＞ IN TAIPEI",
            "show_desc": """🐻‍❄️ 2025 KAI SOLO CONCERT TOUR <KAION> IN TAIPEI 🐻‍❄️

2025 KAI SOLO CONCERT TOUR <KAION> IN TAIPEI

🐻演出時間：2025.07.12 (六) 18:00（實際演出時間以現場公告為準）

🐻演出地點：台北流行音樂中心表演廳

🐻粉絲福利：VIP通行證 / 彩排福利 / 團體合照 / 印刷簽名海報 （福利分配以福利圖為準）

福利注意事項:

抽選資格為所有於2025年6月30日 (一) 23:59 前完成購票付款且無退票之持票者。
抽選結果將於2025年7月3日 (四) 18:00公告於「遠雄創藝」官方社群。
抽選機制 : 福利抽選過程皆委任售票系統隨機抽選。
主辦單位保有活動變更或終止的權利。
""",
            "show_pic": "25_kai.jpg",
            "start_date": date(2025, 7, 12),
            "end_date": date(2025, 7, 12),
            "host_name": "遠雄遠藝",
            "location_name": "台北流行音樂中心表演廳",
            "sections": [
                "6300區",
                "5800區",
                "4800區",
                "3800區",
            ],
            "areas": [
                ("1樓VIP A區6300", 100, 2, 6300, 4300, "6300區"),
                ("1樓VIP B區6300", 100, 2, 6300, 4300, "6300區"),
                ("1樓VIP C區6300", 100, 2, 6300, 4300, "6300區"),
                ("2樓2A區5800", 48, 2, 5800, 3800, "5800區"),
                ("2樓2B區5800", 48, 2, 5800, 3800, "5800區"),
                ("2樓2C區5800", 48, 2, 5800, 3800, "5800區"),
                ("2樓2D區5800", 48, 2, 5800, 3800, "5800區"),
                ("2樓2E區5800", 48, 2, 5800, 3800, "5800區"),
                ("2樓2F區5800", 48, 2, 5800, 3800, "5800區"),
                ("2樓2G區5800", 48, 2, 5800, 3800, "5800區"),
                ("3樓3A區4800", 50, 2, 4800, 2800, "4800區"),
                ("3樓3B區4800", 50, 2, 4800, 2800, "4800區"),
                ("3樓3C區4800", 50, 2, 4800, 2800, "4800區"),
                ("3樓3D區4800", 50, 2, 4800, 2800, "4800區"),
                ("3樓3E區4800", 50, 2, 4800, 2800, "4800區"),
                ("3樓3F區4800", 50, 2, 4800, 2800, "4800區"),
                ("3樓3G區4800", 50, 2, 4800, 2800, "4800區"),
                ("3樓3B區3800", 50, 2, 3800, 1800, "3800區"),
                ("3樓3C區3800", 50, 2, 3800, 1800, "3800區"),
                ("3樓3D區3800", 50, 2, 3800, 1800, "3800區"),
                ("3樓3E區3800", 50, 2, 3800, 1800, "3800區"),
                ("3樓3F區3800", 50, 2, 3800, 1800, "3800區"),
            ],
            "games": [
                {
                    "game_date": date(2025, 7, 12),
                    "game_time": time(18, 00),
                    "sale_start_time": datetime(2025, 5, 3, 12, 30, 0),
                    "sale_end_time": datetime(2025, 7, 12, 12, 30, 0),
                },
            ],
        },
        {
            "show_name": "2025 BABYMONSTER 1ST WORLD TOUR ＜HELLO MONSTERS＞ IN TAIPEI",
            "show_desc": """
2025 BABYMONSTER 1ST WORLD TOUR <HELLO MONSTERS> IN TAIPEI

台北MONSTIEZ! got drip, drip, drip!

怪物新人女團 BABYMONSTER 首次世界巡迴 台北站

2025 BABYMONSTER 1st WORLD TOUR <HELLO MONSTERS> IN TAIPEI

2025.6.28 (六) 林口體育館 震撼開唱

 

2025 BABYMONSTER 1ST WORLD TOUR <HELLO MONSTERS> IN TAIPEI

時間：2025/06/28 (六) 18:00
           2025/06/29 (日) 18:00
地點：國立體育大學綜合體育館（林口體育館）


VIP Gold套票 - NT$ 6,800
包含 SEND-OFF PARTY 、SOUNDCHECK PARTY、專屬VIP掛牌及掛繩、專屬明信片
VIP Silver套票 - NT$ 5,800
包含 SOUNDCHECK PARTY 、專屬VIP掛牌及掛繩 、專屬明信片

 

SPONSORED BY：台灣三星電子、星展萬事達卡DBS Mastercard、台灣大哥大、MyVideo ⁠⁠
 

""",
            "show_pic": "25_bm.jpg",
            "start_date": date(2025, 6, 28),
            "end_date": date(2025, 6, 29),
            "host_name": "Live Nation",
            "location_name": "國立體育大學綜合體育館 (林口體育館)",
            "sections": [
                "6800區 VIP",
                "5800區 VIP",
                "4800區",
                "4300區",
                "3800區",
                "2800區",
            ],
            "areas": [
                ("特一區VIP1", 250, 1, 6800, 4800, "6800區 VIP"),
                ("特二區VIP1", 250, 1, 6800, 4800, "6800區 VIP"),     
                ("特一區VIP2", 250, 1, 5800, 3800, "5800區 VIP"),     
                ("特二區VIP2", 250, 1, 5800, 3800, "5800區 VIP"),     
                ("特三區VIP2", 250, 1, 5800, 3800, "5800區 VIP"),     
                ("特四區VIP2", 250, 1, 5800, 3800, "5800區 VIP"),     
                ("特五區VIP2", 250, 1, 5800, 3800, "5800區 VIP"),     
                ("橙1B-2區5800", 150, 2, 5800, 3800, "5800區 VIP"),     
                ("橙2B-1區5800", 150, 2, 5800, 3800, "5800區 VIP"),     
                ("橙2B-2區5800", 150, 2, 5800, 3800, "5800區 VIP"),     
                ("黃2B-1區5800", 150, 2, 5800, 3800, "5800區 VIP"),     
                ("黃2B-2區5800", 150, 2, 5800, 3800, "5800區 VIP"),     
                ("黃1B-1區5800", 150, 2, 5800, 3800, "5800區 VIP"),     
                ("橙1B-1區4800", 50, 2, 4800, 2800, "4800區"),     
                ("橙1B-2區4800", 50, 2, 4800, 2800, "4800區"),     
                ("橙2B-1區4800", 50, 2, 4800, 2800, "4800區"),     
                ("橙2B-2區4800", 50, 2, 4800, 2800, "4800區"),     
                ("藍2B-1區4800", 50, 2, 4800, 2800, "4800區"),         
                ("藍2B-2區4800", 50, 2, 4800, 2800, "4800區"),         
                ("藍3B-1區4800", 50, 2, 4800, 2800, "4800區"),         
                ("藍3B-2區4800", 50, 2, 4800, 2800, "4800區"),         
                ("藍4B-1區4800", 50, 2, 4800, 2800, "4800區"),         
                ("藍4B-2區4800", 50, 2, 4800, 2800, "4800區"),         
                ("黃2B-1區4800", 50, 2, 4800, 2800, "4800區"),         
                ("黃2B-2區4800", 50, 2, 4800, 2800, "4800區"),         
                ("黃1B-1區4800", 50, 2, 4800, 2800, "4800區"),         
                ("黃1B-2區4800", 50, 2, 4800, 2800, "4800區"),         
                ("橙4B-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("橙4B-2區4300", 50, 2, 4300, 2300, "4300區"),         
                ("藍1B-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("藍1B-2區4300", 50, 2, 4300, 2300, "4300區"),         
                ("藍5B-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("藍5B-2區4300", 50, 2, 4300, 2300, "4300區"),         
                ("黃4B-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("黃4B-2區4300", 50, 2, 4300, 2300, "4300區"),         
                ("橙1A-2區4300", 50, 2, 4300, 2300, "4300區"),         
                ("橙2A-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("橙4A-2區4300", 50, 2, 4300, 2300, "4300區"),         
                ("橙4A-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("藍2A-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("藍2A-2區4300", 50, 2, 4300, 2300, "4300區"),         
                ("藍3A-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("藍4A-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("藍4A-2區4300", 50, 2, 4300, 2300, "4300區"),         
                ("藍5A-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("黃4A-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("黃4A-2區4300", 50, 2, 4300, 2300, "4300區"),         
                ("黃2A-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("黃2A-2區4300", 50, 2, 4300, 2300, "4300區"),         
                ("黃1A-1區4300", 50, 2, 4300, 2300, "4300區"),         
                ("橙1A-2區4300", 50, 2, 4300, 2300, "4300區"),        
                ("橙1A-2區3800", 50, 2, 3800, 1800, "3800區"),         
                ("橙2A-1區3800", 50, 2, 3800, 1800, "3800區"),         
                ("橙2A-2區3800", 50, 2, 3800, 1800, "3800區"),         
                ("橙4A-2區3800", 50, 2, 3800, 1800, "3800區"),         
                ("橙4A-1區3800", 50, 2, 3800, 1800, "3800區"),         
                ("藍1A-1區3800", 50, 2, 3800, 1800, "3800區"),         
                ("藍1A-2區3800", 50, 2, 3800, 1800, "3800區"),         
                ("藍5A-2區3800", 50, 2, 3800, 1800, "3800區"),         
                ("藍5A-3區3800", 50, 2, 3800, 1800, "3800區"),         
                ("黃4A-1區3800", 50, 2, 3800, 1800, "3800區"),         
                ("黃4A-2區3800", 50, 2, 3800, 1800, "3800區"),         
                ("黃2A-1區3800", 50, 2, 3800, 1800, "3800區"),         
                ("黃2A-2區3800", 50, 2, 3800, 1800, "3800區"),         
                ("黃1A-1區3800", 50, 2, 3800, 1800, "3800區"),
                ("橙1A-2區2800", 50, 2, 2800, 800, "2800區"),         
                ("橙2A-1區2800", 50, 2, 2800, 800, "2800區"),         
                ("橙2A-2區2800", 50, 2, 2800, 800, "2800區"),         
                ("橙4A-2區2800", 50, 2, 2800, 800, "2800區"),         
                ("橙4A-1區2800", 50, 2, 2800, 800, "2800區"),         
                ("藍1A-1區2800", 50, 2, 2800, 800, "2800區"),         
                ("藍5A-3區2800", 50, 2, 2800, 800, "2800區"),         
                ("黃4A-1區2800", 50, 2, 2800, 800, "2800區"),         
                ("黃4A-2區2800", 50, 2, 2800, 800, "2800區"),         
                ("黃2A-1區2800", 50, 2, 2800, 800, "2800區"),         
                ("黃2A-2區2800", 50, 2, 2800, 800, "2800區"),         
                ("黃1A-1區2800", 50, 2, 2800, 800, "2800區"),
            ],
            "games": [
                {
                    "game_date": date(2025, 6, 28),
                    "game_time": time(18, 0),
                    "sale_start_time": datetime(2025, 3, 28, 12, 30, 0),
                    "sale_end_time": datetime(2025, 6, 28, 12, 30, 0),
                },
                {
                    "game_date": date(2025, 6, 29),
                    "game_time": time(18, 0),
                    "sale_start_time": datetime(2025, 3, 28, 12, 30, 0),
                    "sale_end_time": datetime(2025, 6, 29, 12, 30, 0),
                },
            ],
        },

    ]

    for show_info in shows_data:
        # === Section 建立 ===
        section_objs = []
        for sect_name in show_info["sections"]:
            section = Section(
                sect_name=sect_name,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )
            db.session.add(section)
            section_objs.append(section)
        db.session.commit()  # commit 才能拿 sect_id

        # === Area 建立 ===
        loc_id = next(l.loc_id for l in locations if l.loc_name == show_info["location_name"])

        area_objs = []
        for area_name, seat_count, disabled_seats, price, disabled_price, sect_name in show_info["areas"]:
            sect_id = next(s.sect_id for s in section_objs if s.sect_name == sect_name)
            area = Area(
                area_name=area_name,
                seat_count=seat_count,
                disabled_seats=disabled_seats,
                price=price,
                disabled_price=disabled_price,
                loc_id=loc_id,
                sect_id=sect_id,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )
            db.session.add(area)
            area_objs.append(area)
        db.session.commit()

        # === Show 建立 ===
        host_id = next(h.host_id for h in hosts if h.host_name == show_info["host_name"])
        show = Show(
            show_name=show_info["show_name"],
            show_desc=show_info["show_desc"],
            show_pic=f"/static/images/{show_info["show_pic"]}",
            start_date=show_info["start_date"],
            end_date=show_info["end_date"],
            host_id=host_id,
            location_id=loc_id,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        db.session.add(show)
        db.session.commit()

        # === Game + GameArea 建立 ===
        for game_info in show_info["games"]:
            game = Game(
                game_date=game_info["game_date"],
                game_time=game_info["game_time"],
                sale_start_time=game_info["sale_start_time"],
                sale_end_time=game_info["sale_end_time"],
                game_status="A",
                total_seats=0,
                available_seats=0,
                show_id=show.show_id,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )
            db.session.add(game)
            db.session.flush()  # 拿 game_id

            total_seats = 0
            for area in area_objs:
                area_total = area.seat_count + area.disabled_seats
                total_seats += area_total
                game_area = GameArea(
                    available_seats=area.seat_count,
                    disabled_available_seats=area.disabled_seats,
                    game_id=game.game_id,
                    area_id=area.area_id,
                    createdAt=datetime.now(),
                    updatedAt=datetime.now()
                )
                db.session.add(game_area)

            game.total_seats = total_seats
            game.available_seats = total_seats

        db.session.commit()

    print("✅ 全部 Show / Section / Area / Game / GameArea 建立完成")
