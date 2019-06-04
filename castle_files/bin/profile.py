"""
В этом модуле содержатся функции замкового бота для работы с профилями, как по запросу, так и в базе данных
(например, приём и обновление /hero)
"""

from castle_files.work_materials.globals import DEFAULT_CASTLE_STATUS, cursor, moscow_tz, construction_jobs
from castle_files.work_materials.equipment_constants import get_equipment_by_code, equipment_names
from castle_files.work_materials.filters.general_filters import filter_is_merc
from castle_files.libs.player import Player
from castle_files.libs.guild import Guild

from castle_files.bin.buttons import send_general_buttons
from castle_files.bin.service_functions import check_access
from castle_files.bin.buttons import get_profile_buttons

from castle_files.work_materials.filters.general_filters import filter_is_pm

import re
import logging
import datetime
import random


trade_divisions_access_list = [439637823, 320365073]  # Игроки, которым дал доступ к хуизу в связи с альянсами

status_messages = [
    "В таверне вы слышали, как этот человек отзывался на имя <b>{}</b>",
    "Кажется, это <b>{}</b>, вы видели его не стенде объявлений. Он занимался крафтом в неположенном месте.",
    "Да это же <b>{}</b>! Вот кто привёл ручного дракона на прошлой неделе и чуть не сжёг все казармы.",
    "Есть люди, которые пропускают битвы. Но <b>{}</b> не из таких. Он вообще на них не ходит.",
    "*Крики о помощи*\nО! Кажется, это <b>{}</b> вновь полез в колодец за “счастливыми” монетками. Может, "
    "стоит подать ему веревку, в обмен на мелочь?",
    "Снова этот <b>{}</b> хвастается своим Грифоновским кинжалом. Может кто-то ему расскажет, что выгоднее точить "
    "Хантер?"
]


def get_profile_text(player, self_request=True, user_data=None):
    response = "<b>{}</b> - Воин {}\n".format(player.nickname, "🖤Скалы" if player.castle == '🖤' else player.castle)
    response += "{}id: <code>{}</code>, ".format("@{}, ".format(player.username) if player.username is not None else "",
                                                 player.id)
    response += "🔘: <code>{}</code>\n".format(player.reputation)
    if player.status is not None:
        response += "Статус: <b>{}</b>\n".format(player.status)
    response += "🏅: <code>{}</code>, ⚔: <code>{}</code>, 🛡: <code>{}</code>\n".format(player.lvl, player.attack,
                                                                                      player.defense)
    guild = Guild.get_guild(guild_id=player.guild) if player.guild is not None else None
    response += "Гильдия: {}\n".format("<code>{}</code>".format(guild.tag) if guild is not None else "нет")
    if guild is not None and self_request:
        response += "Покинуть гильдию: /leave_guild\n"
    response += "\nЭкипировка:\n"
    eq_list = list(player.equipment.values())
    for equipment in eq_list:
        if equipment is None:
            continue
        response += "<b>{}</b><code>{}</code><code>{}</code>" \
                    "\n".format(equipment.name, " +{}⚔️ ".format(equipment.attack) if equipment.attack != 0 else "",
                                "+{}🛡 ".format(equipment.defense) if equipment.defense != 0 else "")

    r1, r2, r3 = player.get_reports_count()
    response += "\nРепорты(эта неделя / прошлая / всего): <code>{}</code> / <code>{}</code> / <code>{}</code>" \
                "\n".format(r1, r2, r3)
    response += "Регистрация в боте: <code>{}</code>\n".format(player.created.strftime("%d/%m/%y %H:%M:%S") if
                                                                 player.created is not None else "Оппозит")
    response += "Последнее обновление профиля: " \
                "<code>{}</code>\n".format(player.last_updated.strftime("%d/%m/%y %H:%M:%S") if
                                           player.last_updated is not None else "неизвестно")
    if user_data is None:
        return response
    status = user_data.get("status")
    if status is not None and status in ["sawmill", "quarry", "construction"]:
        if player is not None:
            j = construction_jobs.get(player.id)
            if j is not None:
                seconds_left = j.get_time_left()
                response += "\nВы заняты делом. Окончание через <b>{:02.0f}:{:02.0f}</b>" \
                            "".format(seconds_left // 60, (seconds_left % 60) // 1)
    return response


# Функция вывода профиля
def profile(bot, update, user_data=None):
    mes = update.message
    player = Player.get_player(mes.from_user.id)
    response = get_profile_text(player, user_data=user_data)
    bot.send_message(chat_id=mes.chat_id, text=response, parse_mode='HTML', reply_markup=get_profile_buttons(player))


def view_profile(bot, update):
    mes = update.message
    requested_player_id = mes.from_user.id
    requested_player = Player.get_player(requested_player_id)
    if requested_player is None:
        return
    guild = Guild.get_guild(guild_id=requested_player.guild)
    if not check_access(requested_player_id) and not filter_is_merc(mes) and \
            requested_player_id not in trade_divisions_access_list:
        if guild is None or not guild.check_high_access(requested_player_id):
            bot.send_message(chat_id=mes.chat_id, text="Право распоряжаться людьми необходимо заслужить.",
                             reply_to_message_id=mes.message_id)
            return
    # Доступ к хуизу есть
    reply = False
    if mes.text.startswith("/dok") or mes.text.startswith("/doc"):
        if mes.reply_to_message is not None:
            #  Реплай в чате
            reply = True
            player_id = mes.reply_to_message.from_user.id
        elif "@" in update.message.text:
            # Поиск по юзерке
            request = "select id from players where username = %s"
            cursor.execute(request, (mes.text.partition("@")[2],))
            row = cursor.fetchone()
            if row is None:
                bot.send_message(chat_id=mes.chat_id, text="Игрок не найден.")
                return
            player_id = row[0]
        else:
            # Поиск по нику в игре
            request = "select id from players where nickname = %s or nickname like %s"
            # print(request % mes.text.partition(" ")[2] % "%]" + mes.text.partition(" ")[2])
            cursor.execute(request, (mes.text.partition(" ")[2], "%]" + mes.text.partition(" ")[2]))
            row = cursor.fetchone()
            if row is None:
                bot.send_message(chat_id=mes.chat_id, text="Игрок не найден.")
                return
            player_id = row[0]
    else:
        player_id = re.search("_(\\d+)", mes.text)
        player_id = int(player_id.group(1))
    if player_id is None:
        bot.send_message(chat_id=mes.chat_id, text="Неверный синтаксис.")
        return
    player = Player.get_player(player_id)
    if player is None or (mes.text.startswith("/view_profile") and player.guild != guild.id):
        bot.send_message(chat_id=mes.chat_id, text="Игрок не найден.")
        return
    if reply and player.status is not None:
        # Сообщение со статусом
        bot.send_message(chat_id=mes.chat_id, text=random.choice(status_messages).format(player.status),
                         parse_mode='HTML', reply_to_message_id=mes.message_id)
    buttons = get_profile_buttons(player)
    if (player.guild is None or player.guild != requested_player.guild) and not check_access(requested_player_id) and\
            not filter_is_merc(mes) and requested_player_id not in trade_divisions_access_list:
        guild = Guild.get_guild(guild_id=player.guild)
        bot.send_message(chat_id=mes.from_user.id,
                         text="Вы не знаете этого человека, однако его форма позволяет вам сделать вывод, что он "
                              "служит {}".format("в гильдии <b>{}</b>".format(guild.tag) if guild is not None else
                                                 "как вольный наёмник (без гильдии)"),
                         parse_mode='HTML', reply_markup=buttons)
        return
    response = get_profile_text(player, self_request=False)
    bot.send_message(chat_id=mes.from_user.id, text=response, parse_mode='HTML', reply_markup=buttons)


def guild_history(bot, update):
    data = update.callback_query.data
    mes = update.callback_query.message
    requested_player_id = re.search("_(\\d+)", data)
    if requested_player_id is None:
        bot.send_message(chat_id=mes.chat_id, text="Произошла ошибка. Попробуйте вызвать сообщение заного.")
        return
    requested_player_id = int(requested_player_id.group(1))
    player = Player.get_player(player_id=update.callback_query.from_user.id)
    if player is None:
        return
    player_guild = Guild.get_guild(player.guild) if player.guild is not None else None
    if player.id != requested_player_id and (player_guild is None or not player_guild.check_high_access(player.id)):
        bot.send_message(chat_id=mes.chat_id, text="Доступ запрещён.")
        return
    requested_player = Player.get_player(requested_player_id, notify_on_error=False)
    if requested_player is None:
        bot.send_message(chat_id=mes.chat_id, text="Игрок не найден.")
        return
    if requested_player.guild_history is None:
        requested_player.guild_history = []
    response = "Гильдии, в которых состоял <b>{}</b>:\n<em>Выше — позже</em>\n\n".format(requested_player.nickname)
    for i, guild_id in enumerate(requested_player.guild_history):
        guild = Guild.get_guild(guild_id)
        if guild is None:
            continue
        commander = Player.get_player(guild.commander_id)
        if commander is None:
            continue
        response += "<b>{}</b>, <code>{:3<}</code>: Командир: <b>{}</b> - @{}" \
                    "\n".format(i + 1, guild.tag, commander.nickname, commander.username)
    bot.send_message(chat_id=mes.chat_id, text=response, parse_mode='HTML')
    bot.answerCallbackQuery(callback_query_id=update.callback_query.id)


# Функция для добавления или обновления профиля в базе данных, вызывается, когда бот получает хиро в лс
def hero(bot, update, user_data):
    mes = update.message
    text = mes.text
    castle = text[0]
    if castle != '🖤':
        pass
        # Игрок не из Скалы
        # bot.send_message(chat_id=mes.from_user.id, text="Пользователям не из Скалы запрещена регистрация!")
        # return
    player = Player.get_player(mes.from_user.id, notify_on_error=False)
    if player is None and mes.chat_id != mes.from_user.id:
        # Добавление новых пользователей только в личке у бота
        return
    if datetime.datetime.now() - mes.forward_date > datetime.timedelta(seconds=30):
        bot.send_message(chat_id=mes.chat_id, text="Это устаревший профиль.", reply_to_message_id=mes.message_id)
        return
    # Парсинг хиро
    guild_tag = re.search("[🍁☘🖤🐢🦇🌹🍆🎖]\\[(.+)\\]", text)
    if guild_tag:
        guild_tag = guild_tag.group(1)
    nickname = text.splitlines()[0][1:]
    lvl = int(re.search("🏅Уровень: (\\d+)", text).group(1))
    attack = int(re.search("⚔Атака: (\\d+)", text).group(1))
    defense = int(re.search("🛡Защита: (\\d+)", text).group(1))
    stamina = int(re.search("🔋Выносливость: \\d+/(\\d+)", text).group(1))
    pet = re.search("Питомец:\n.(\\s.+\\(\\d+ lvl\\))", text)
    last_updated = datetime.datetime.now(tz=moscow_tz).replace(tzinfo=None)
    if pet:
        pet = pet.group(1)
    # Парсинг экипировки
    print("parsing eq")
    player_equipment = {
        "main_hand": None,
        "second_hand": None,
        "head": None,
        "gloves": None,
        "armor": None,
        "boots": None,
        "cloaks": None
    }
    equip_strings = text.partition("🎽Экипировка")[2].splitlines()[1:]
    for string in equip_strings:
        # clear_name = re.search("\\+?\\d?\\s?(.+?)\\s\\+", string)
        clear_name = re.search("(⚡?\\+?\\d*\\s?(.+?))\\s\\+((\\d*)⚔)?\\s*\\+?(\\d*)🛡?", string)
        if clear_name is None:
            # logging.warning("Error while parsing item_string\n{}".format(string))
            continue
        else:
            pass
            # logging.info("successful parsed {},, Got: {}".format(string, clear_name.group(1)))
        full_name = clear_name.group(1)
        eq_attack = int(clear_name.group(4)) if clear_name.group(4) is not None and clear_name.group(4) != "" else 0
        eq_defense = int(clear_name.group(5)) if clear_name.group(5) != "" else 0
        clear_name = clear_name.group(2)
        names_list = list(equipment_names.items())
        code = None
        for name, item_code in names_list:
            if name in clear_name:
                code = item_code
                break
        if code is None:
            # logging.warning("Item code is None for item {}".format(clear_name))
            continue
        eq = get_equipment_by_code(code)
        if eq is None:
            logging.warning("Equipment with code {} is None".format(code))
            continue
        eq.name = full_name
        eq.attack = eq_attack
        eq.defense = eq_defense
        player_equipment.update({eq.place: eq})
    if player is None:
        if mes.from_user.username is None:
            bot.send_message(chat_id=mes.chat_id, text="Регистрация без имени пользователя невозможна. Пожалуйста, "
                                                       "установите его в настройках аккаунта Telegram")
            return
        player = Player(mes.from_user.id, mes.from_user.username, nickname, guild_tag, None, lvl, attack, defense,
                        stamina, pet, player_equipment, castle=castle, last_updated=last_updated, created=last_updated)
        # Добавляем игрока в бд
        player.insert_into_database()
        player = player.reload_from_database()

        user_data.update({"status": DEFAULT_CASTLE_STATUS, "location_id": 0})
        bot.send_message(chat_id=mes.chat_id,
                         text="Добро пожаловать в 🖤Скалу, <b>{}</b>!\n\nДля добавления информации о классе "
                              "необходимо прислать ответ @ChatWarsBot на кнопку \"🏅Герой\" (рекомендуется сделать для "
                              "получения доступа к некоторых дополнительным фишкам, особенно стражникам).\n\n"
                              "<em>Вы всегда можете отключить рп составляющую бота командой </em>/change_rp.<em> "
                              "Обратите внимание, что это сделает недоступными некоторые функции "
                              "бота.</em>".format(player.nickname),
                         parse_mode='HTML')
        if filter_is_pm(mes):
            send_general_buttons(mes.from_user.id, user_data)

    else:
        # Обновляем существующую информацию
        player.username = mes.from_user.username
        player.nickname = nickname
        player.guild_tag = guild_tag
        player.lvl = lvl
        player.attack = attack
        player.defense = defense
        player.stamina = stamina
        player.pet = pet
        player.equipment = player_equipment
        player.castle = castle
        player.last_updated = last_updated
        player.update()
        bot.send_message(chat_id=mes.chat_id, text="Профиль успешно обновлён, <b>{}</b>!".format(player.nickname),
                         parse_mode='HTML')
        if player.guild is not None:
            guild = Guild.get_guild(player.guild)
            guild.calculate_attack_and_defense()
            guild.sort_players_by_exp()


def add_class_from_player(bot, update):
    mes = update.message
    player = Player.get_player(mes.from_user.id)
    if player is None:
        bot.send_message(chat_id=mes.from_user.id, text="Сначала необходимо зарегистрироваться. Для этого необходимо "
                                                        "прислать ответ @ChatWarsBot на команду /hero")
        return
    if datetime.datetime.now() - mes.forward_date > datetime.timedelta(seconds=30):
        bot.send_message(chat_id=mes.chat_id, text="Это устаревший профиль.", reply_to_message_id=mes.message_id)
        return
    game_class = re.search("🖤{} (\\w+) Скалы".format(re.escape(player.nickname)), mes.text)
    if game_class is None:
        bot.send_message(chat_id=mes.chat_id, text="Произошла ошибка.", reply_to_message_id=mes.message_id)
        return
    game_class = game_class.group(1)
    player.game_class = game_class
    player.update_to_database()
    bot.send_message(chat_id=mes.from_user.id, text="Информация о классе обновлена, <b>{}</b>! Теперь ты "
                                                    "<b>{}</b>!".format(player.nickname, player.game_class),
                     parse_mode='HTML')


def update_ranger_class_skill_lvl(bot, update):
    mes = update.message
    player = Player.get_player(mes.from_user.id)
    if player is None:
        return
    if player.game_class != 'Ranger':
        bot.send_message(chat_id=mes.chat_id,
                         text="Учёт уровня скиллов пока доступен только лучникам. Для добавления информации о классе "
                              "необходимо прислать ответ @ChatWarsBot на кнопку \"🏅Герой\"")
        return
    class_skill = int(mes.text.partition("Aiming")[0][:-2].split()[-1])
    logging.info("class_skill = {0}".format(class_skill))
    player.class_skill_lvl = class_skill
    player.update()
    bot.send_message(chat_id=mes.from_user.id, text="Информация о скиллах обновлена, <b>{}</b>".format(player.nickname),
                     parse_mode='HTML')


def set_status(bot, update):
    mes = update.message
    if not check_access(mes.from_user.id):
        return
    parse = re.search("set_status (\\d+) (.*)", mes.text)
    if parse is None:
        bot.send_message(chat_id=mes.chat_id, text="Неверный синтаксис", reply_to_message_id=mes.message_id)
        return
    player_id = int(parse.group(1))
    new_status = parse.group(2)
    player = Player.get_player(player_id, notify_on_error=False)
    if player is None:
        bot.send_message(chat_id=mes.chat_id, text="Игрок не найден.", reply_to_message_id=mes.message_id)
        return
    if new_status == "":
        player.status = None
    else:
        player.status = new_status
    player.update()
    bot.send_message(chat_id=mes.chat_id, text="Обновление статуса успешно!", reply_to_message_id=mes.message_id)

