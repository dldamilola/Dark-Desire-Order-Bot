

statuses = {
    1: {"name": "🌽 Корнхолио", "price": 500},
    2: {"name": "🦠Бацила", "price": 1000},
    3: {"name": "🌱Первый росток", "price": 2000},
    4: {"name": "🕊Голубь Мира", "price": 4000},
    5: {"name": "🍁9КА", "price": 9000},


    1000: {"name": "🐿Матерь Кусек", "price": None, "unique": True},
    1001: {"name": "🐱Смущённая Киса", "price": None, "unique": True},
}


statuses_to_messages = {
    "🌽 Корнхолио": """ТЫ МНЕ УГРАЖАЕШЬ? Я ВЕЛИКИЙ КУКУРУЗО! ПОДАЙ МНЕ БУМАГИ ДЛЯ МОЕЙ КУКУРУЗИНЫ!
🌽 Корнхолиоооооооооооооооооооо
кхе хе хе хе хе кхе кхе хе хе кхе кхе""",
    "🦠Бацила": """Это страшная 🦠Бацила. Но Гренландия закрыла порты.
ПОРАЖЕНИЕ.
🦠Бацила была полностью ликвидированна.""",
    "🌱Первый росток": """🌱Первый росток на скалистой местности. Ничего необычного. Жетонов было не очень много.""",
    "🕊Голубь Мира": """🕊Голубь Мира -  почетный ветеран Диалога""",
    "🍁9КА": """В память Величайшей Королеве -🍁9КА.
Попробуй со шпротами!""",
    "☘:🔱⚔⚡": """ЛОЙСО ☘️:🔱⚔️⚡️ ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО  ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️ЛОЙСО ☘️:🔱⚔️⚡️...""",
    "☠️Демиург": """Это ☠️Демиург - с воображением не друг.""",
    "УмВачеСэй🌅🦜🏝😔": """Ты заметил грустного папугая, напевающего: "УмВачеСэй🌅🦜🏝😔"...
Передоз ГП, не иначе...""",
    "💫ТалисманKYS": """А вот и 💫ТалисманKYS - шутить над ним боюсь.""",
    "🍥Зефирка": """Это 🍥Зефирка. Если однажды она предложит вам зефирное обертывание... Не соглашайтесь. По крайней мере публично. Лучше тихонечко, в лс. Сохрани конфеденциальность и ни кто не осудит!""",
    "РыцарьЛеся": """Перед вами ветеран - РыцарьЛеся. Рыцарь Леся знаменит тем, что он рыцарь. И он Леся. И он мальчик. Мальчик Рыцарь Леся. Ветеран. Холост. Детей нет.""",
    "🐱Смущённая Киса 🎗": """Это не просто 🐱Смущённая Киса! 🐱Смущённая Киса - красавица и умница. Люби 🐱Смущённую кису!
(или умри)""",
    "🍺Крепкое": """🍺Крепкое. Мощное. Четкое. Звонкое. Может и Могет.""",
    "🎶Мими": """Любовь к музыке у 🎶Мими проявилась еще с детства.
Жаль, что умерла эта любовь в Скале...""",
    "Playstation🎮": """"ГЛЯ! ДА ЭТО ЖЕ Playstation🎮!" - С презрением перешептываются бояре с ЭВМ.""",
    "🌚Даня🌝": """Ты попросил документы у Дани. Ну Даня и протянул.
Что ты ожидал там увидеть? Это Даня - тут так и написанно:
"🌚Даня🌝"
Даня - человек бесхитростный и простой.""",
    "⚔️/ПледгеВамВленту🎗": """Ты смотришь на странную надпись - ⚔️/ПледгеВамВленту🎗
Твое лицо необъяснимо перекашивает, а пересохший рот произносит /pledge""",
    "Мира": """Если однажды вы сделаете стикеры, лучше держитесь подальше от Миры. Поговаривают, что этот парень не только жопит синие свитки, но и страдает особой формой стекерной клептомании.
Прижми стикерпак к груди и проходи мимо!""",
    "👨‍❤️‍👨ЖУЛИК": """👨‍❤️‍👨ЖУЛИК /ne_vorui""",
    "🐿Матерь Кусек 🎗": """Это 🐿Матерь Кусек.
Красавица, умница, любит выдр и Скалу.
Скала любит ее в ответ. А выдры нет.""",
    "🤦‍♂️Серега Феникс": """Это же 🤦‍♂️Серега Феникс! Он еще в академке Феникс +3 с дефа поймал, продал и стальным шмотом затарился! Знатный торговец реликвиями!""",
    "🧞‍♀️ДжинGuru": """Говорят, если долго тереть лампу, рано или поздно ладони станут волосатыми.
А вот 🧞‍♀️ДжинGuru может так и не появиться...""",
    "🐱Кошачий алхимик": """Щепотку валерьяны... Так-так-так... Две пригоршни кошачьей мяты...
🐱Кошачий алхимик знает толк в забористой дури!""",


}


default_status_messages = [
    "В таверне вы слышали, как этот человек отзывался на имя <b>{}</b>",
    "Кажется, это <b>{}</b>, вы видели его не стенде объявлений. Он занимался крафтом в неположенном месте.",
    "Да это же <b>{}</b>! Вот кто привёл ручного дракона на прошлой неделе и чуть не сжёг все казармы.",
    "Есть люди, которые пропускают битвы. Но <b>{}</b> не из таких. Он вообще на них не ходит.",
    "*Крики о помощи*\nО! Кажется, это <b>{}</b> вновь полез в колодец за “счастливыми” монетками. Может, "
    "стоит подать ему веревку, в обмен на мелочь?",
    "Снова этот <b>{}</b> хвастается своим Грифоновским кинжалом. Может кто-то ему расскажет, что выгоднее точить "
    "Хантер?"
]
