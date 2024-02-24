import logging
from pathlib import Path

from MySQL_Driver import executeSQL, logger, DBCommit
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton
import datetime as date
import random
import string
from file_func import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
log = logging.getLogger("KiotoBot")

temp_addtitle = []
temp_user_values = []
weekdays = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]
daysemoji = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]


def RBS(Value: str):
    BS = ["`", "'"]
    n = Value
    for x in BS:
        print(f"{x}")
        if x in n:
            print("YES")
            n = n.replace(f"{x}", "")
    return str(n)


def RBS_MarkDown(Value: str):
    BS = ["[", "]", "{", "}"]
    n = Value
    for x in BS:
        print(f"{x}")
        if x in n:
            print("YES")
            n = n.replace(f"{x}", "")
    return str(n)


def ParseAllTitles():  #
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Titles")
    except Exception as e:
        logger.error(f"Exeption ParseAllTitles {e}")
        return False
    return cursor.fetchall()


def ParseIDTitle(ID):
    print(ID)
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Titles WHERE ID=%s", (ID,))
    except Exception as e:
        logger.error(f"Exeption ParseIDTitle {e}")
        return False
    return cursor.fetchall()


def DeleteTitleID(ID):
    p = Path(f"Data/Images/{ID}")
    a = ParseIDTitle(ID)[0]
    tp = Path(f"Data/Torrents/{a[13]}.torrent")
    try:
        cursor = executeSQL()
        cursor.execute(f"DELETE FROM Titles WHERE ID=%s", (ID,))
    except Exception as e:
        logger.error(f"Exeption DeleteTitleID {e}")
        return False
    DBCommit()
    try:
        if os.path.exists(p):
            os.remove(p)
    finally:
        pass
    try:
        if trntexists(tp):
            os.remove(tp)
        else:
            print("TORRENTNUKL")
    finally:
        pass
    return True


def QueryList(query_data):
    log.info(f"Генерація QueryList. Query data:{query_data}")
    results = []
    a = ParseAllTitles()
    mv = 0
    if len(a) == 0:
        log.error("QueryList пустий!")
        return False
    if len(query_data) == 0:
        for x in a:
            mv = mv + 1
            if mv >= 50:
                break
            if len(x[6]) == 0:
                season = ""
            else:
                season = x[6] + "\n"
            results.extend([InlineQueryResultArticle(
                id=str(mv),
                title=x[1],
                description=f"{season}{x[4]}",
                input_message_content=InputTextMessageContent(f"/search_{x[0]}"),
                # thumbnail_url="?",
                # thumbnail_width=128,
                # thumbnail_height=128
            )])
    else:
        print("++")
        for x in a:
            print("cucle")
            category = x[3].split(",")
            catl = []
            for x1 in category:
                catl.extend([x1.lower()])
            qd = str(query_data).lower()
            if (qd in x[1].lower()) or (qd in x[4].lower()) or (qd in catl) or (qd in x[6].lower()) or (qd in [x[1]]):
                print("+")
                mv = mv + 1
                if mv >= 50:
                    continue
                if len(x[6]) == 0:
                    season = ""
                else:
                    season = x[6] + "\n"
                results.extend([InlineQueryResultArticle(
                    id=str(mv),
                    title=x[1],
                    description=f"{season}{x[4]}",
                    input_message_content=InputTextMessageContent(f"/search_{x[0]}"),
                    # thumbnail_url="?",
                    # thumbnail_width=128,
                    # thumbnail_height=128
                )])
    print(mv)
    alt = [InlineQueryResultArticle(
        id="1",
        title="Результати за пошуком відсутні",
        description=f"Мені справді шкода що так вийшло, можливо попробуєте ще раз?",
        input_message_content=InputTextMessageContent(f"В тебе все вийде! Не здавайся!"),
        # thumbnail_url="?",
        # thumbnail_width=128,
        # thumbnail_height=128
    )]
    if len(results) > 0:
        return results
    else:
        log.error(
            "Помилка генерації QueryList - Не знайдено тайтлів по заданим користувачем параметрам\nВідправляю альтернативний results")
        return alt


def UserIsAdmin(UserID):
    try:
        query = "SELECT * FROM Admins WHERE `ID`=%s"
        cursor = executeSQL()
        cursor.execute(query, (UserID,))
        info = cursor.fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції UserIsAdmin. DEBUG:\nException: {e}, UserID={UserID}")
    if len(info) == 0:
        return False
    else:
        return True


def UserHavePrivileges(UserID: int, Pvlgs: str):
    if UserIsAdmin(UserID):
        try:
            cursor = executeSQL()
            cursor.execute("SELECT Privileges FROM Admins WHERE `ID`=%s", (UserID,))
            print(cursor.fetchone()[0])
            info = cursor.fetchone()
        finally:
            pass
    if str(info[0]) == Pvlgs:
        return True
    else:
        return False


def TotalRandom() -> str:
    import random
    import string
    a = ParseAllTitles()
    x = 0
    while x == 0:
        ab = 0
        characters = string.ascii_letters + string.digits
        random_chars = ''.join(random.choice(characters) for _ in range(16))
        if len(a) == 0:
            print("NULLLEN")
            return random_chars
        for x1 in a:
            if not x1[0] == random_chars:
                ab = ab + 1
        if ab == len(a):
            print("FULL rand")
            x = 1
    return random_chars


def trntTotalRandom() -> str:
    a = get_file_names_in_directory("Data/Torrents")
    x = 0
    while x == 0:
        ab = 0
        characters = string.ascii_letters + string.digits
        random_chars = ''.join(random.choice(characters) for _ in range(16))
        if len(a) == 0:
            print("NULLLEN")
            return random_chars
        for x1 in a:
            if not x1[0] == random_chars:
                ab = ab + 1
        if ab == len(a):
            print("FULL rand")
            x = 1
    return random_chars


def trntexists(Path):
    print(Path)
    if os.path.exists(Path):
        return True
    else:
        return False


"""def get_trackers_from_torrent(torrent_file_path):
    with open(torrent_file_path, 'rb') as torrent_file:
        metadata = bencode.bdecode(torrent_file.read())
        if 'announce-list' in metadata:
            trackers = [tracker for tier in metadata['announce-list'] for tracker in tier]
        elif 'announce' in metadata:
            trackers = [metadata['announce']]
        else:
            trackers = []
    return trackers"""
"""def check_torrent_file(torrent_file_path):
    try:
        with open(torrent_file_path, 'rb') as torrent_file:
            metadata = bencode.bdecode(torrent_file.read())
            hashcontents = bencode.bencode(metadata['info'])
            digest = hashlib.sha1(hashcontents).digest()
            b32hash = base64.b32encode(digest)
            print(b32hash.decode('utf-8'))
            trackers = get_trackers_from_torrent(torrent_file_path)
            magnet_link = f"magnet:?xt=urn:btih:{b32hash.decode('utf-8')}"
            if trackers:
                tracker_string = "&tr=".join(trackers)
                magnet_link += f"&tr={tracker_string}"
            return magnet_link
    except Exception as e:
        print(f"Помилка: {e}")
        return False"""


def VSTotalRandom() -> str:
    import random
    import string
    a = ParseAllVideos()
    x = 0
    while x == 0:
        ab = 0
        characters = string.ascii_letters + string.digits
        random_chars = ''.join(random.choice(characters) for _ in range(16))
        if len(a) == 0:
            print("NULLLEN")
            return random_chars
        for x1 in a:
            if not x1[3] == random_chars:
                ab = ab + 1
        if ab == len(a):
            print("FULL rand")
            x = 1
    return random_chars


def InitTitle(TitleID, TitleName: str):
    print(TitleID)
    print(TitleName)
    try:
        cursor = executeSQL()
        cursor.execute("INSERT INTO Titles (ID, Name, Description, Category, OriginalName, VideoPost, Season) VALUES("
                       "%s, %s, '', '', '', '', '');", (TitleID, TitleName))
        DBCommit()
    except Exception as e:
        logger.error(e)
        return False
    return True


def UpdateTitles(TitleID, column, value):
    print(f"UPDATE - {TitleID}, {column}, {value}")
    try:
        cursor = executeSQL()
        cursor.execute(f"UPDATE Titles SET {column}=%s WHERE ID=%s;", (value, TitleID))
        DBCommit()
    except Exception as e:
        logger.error(f"Exept UT e {e}")
        return False
    return True


def RemoveTempUser(UserID: int):
    if len(temp_addtitle) == 0:
        return True
    for x in temp_addtitle:
        if int(x[0]) == UserID:
            temp_addtitle.remove(x)
            return True
    return False


def AddTempUser(UserID: int, TitleID: str):
    temp_addtitle.extend([[UserID, TitleID]])


def UserTempTitleID(UserID: int):
    if len(temp_addtitle) == 0:
        return False
    print(f"TEMP: {temp_addtitle}")
    for x in temp_addtitle:
        if UserID == x[0]:
            return x[1]
    return False


def AddToTemp(userID: int, TitleID: str):
    temp_addtitle.extend([[userID, TitleID]])


def AddToValue(userID: int, Value: str):
    temp_user_values.extend([[userID, Value]])


def RemoveValueUser(UserID: int):
    if len(temp_user_values) == 0:
        return True
    for x in temp_user_values:
        if int(x[0]) == UserID:
            temp_user_values.remove(x)
            return True
    return False


def UserTempValue(UserID: int):
    if len(temp_user_values) == 0:
        return False
    for x in temp_user_values:
        if UserID == x[0]:
            return x[1]
    return False


def ParseAllAdm():
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Admins;")
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseAllAdm. DEBUG:\nException: {e}")
    return cursor.fetchall()


def ParseAllVideos():
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Video")
    except Exception as e:
        logger.error(f"Exeption ParseAllVideos {e}")
        return False
    return cursor.fetchall()


def ParseVLIDVideos(ID):
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Video WHERE VideoListID=%s", (ID,))
    except Exception as e:
        logger.error(f"Exeption ParseVLIDVideos {e}")
        return False
    return cursor.fetchall()


def ParseSFLIDVideos(ID):
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Video WHERE SFileID=%s", (ID,))
    except Exception as e:
        logger.error(f"Exeption ParseSFLID {e}")
        return False
    return cursor.fetchall()


def ParseFLIDVideos(ID):
    try:
        cursor = executeSQL()
        cursor.execute(f"SELECT * FROM Video WHERE FileID=%s", (ID,))
    except Exception as e:
        logger.error(f"Exeption ParseFLID {e}")
        return False
    return cursor.fetchall()


def sortS(list):
    return sorted(list, key=lambda l: l[3])


def DeleteFileID(ID):
    try:
        cursor = executeSQL()
        cursor.execute(f"DELETE FROM Video WHERE FileID=%s", (ID,))
    except Exception as e:
        logger.error(f"Exeption DeleteFileID {e}")
        return False
    DBCommit()
    return True


def InitVideo(PostID, FileID):
    try:
        cursor = executeSQL()
        cursor.execute("INSERT INTO Video (VideoListID, FileID, CaptionText, Episode) VALUES("
                       "%s, %s, '', 0)", (PostID, FileID))
        DBCommit()
    except Exception as e:
        logger.error(e)
        return False
    return True


def UpdateVideo(FileID, VideoListID, column, value):
    print(f"UPDATE - {FileID}, {column}, {value}")
    try:
        cursor = executeSQL()
        cursor.execute(f"UPDATE Video SET {column}=%s WHERE FileID=%s AND VideoListID=%s;",
                       (value, FileID, VideoListID))
        DBCommit()
    except Exception as e:
        logger.error(f"Exept UT e {e}")
        return False
    return True


def VTotalRandom() -> str:
    import random
    import string
    a = ParseAllVideos()
    x = 0
    while x == 0:
        ab = 0
        characters = string.ascii_letters + string.digits
        random_chars = ''.join(random.choice(characters) for _ in range(16))
        if len(a) == 0:
            print("NULLLEN")
            return random_chars
        for x1 in a:
            if not x1[0] == random_chars:
                ab = ab + 1
        if ab == len(a):
            print("FULL rand")
            x = 1
    return random_chars


def DeleteVLID(ID):
    try:
        cursor = executeSQL()
        cursor.execute(f"DELETE FROM Video WHERE VideoListID=%s", (ID,))
    except Exception as e:
        logger.error(f"Exeption ParseAllTitles {e}")
        return False
    allt = ParseAllTitles()
    for x in allt:
        if x[5] == ID:
            try:
                UpdateTitles(x[0], "VideoPost", "")
            finally:
                pass
    DBCommit()
    return True


def CheckListVILD(VLID):
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Video WHERE VideoListID=%s", (VLID,))
        info = cursor.fetchall()
    except Exception as e:
        logger.error(f"Exeption ParseSFLID {e}")
        return False
    if len(info) == 0:
        return False
    else:
        return True


def CheckListConVILD(VLID):
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Titles WHERE VideoPost=%s", (VLID,))
        info = cursor.fetchall()
    except Exception as e:
        logger.error(f"Exeption ParseSFLID {e}")
        return False
    if len(info) == 0:
        return False
    else:
        return info[0][0]


def CheckFLIDUse(FLID):
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Video WHERE FileID=%s", (FLID,))
        info = cursor.fetchall()
    except Exception as e:
        logger.error(f"Exeption ParseSFLID {e}")
        return False
    if len(info) == 0:
        return False
    else:
        return True


def ParseCalendar():
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Calendar")
    except Exception as e:
        logger.error(f"Exeption ParseCalendar {e}")
        return False
    return cursor.fetchall()


def ParseDateCalendar(Date):
    try:
        cursor = executeSQL()
        cursor.execute("SELECT * FROM Calendar WHERE Date=%s", (Date,))
    except Exception as e:
        logger.error(f"Exeption ParseDC {e}")
        return False
    return cursor.fetchall()


def UpdateCalendar(Date, column, value):
    print(f"UPDATE - {Date}, {column}, {value}")
    try:
        cursor = executeSQL()
        cursor.execute(f"UPDATE Calendar SET {column}=%s WHERE Date=%s;", (value, Date))
        DBCommit()
    except Exception as e:
        logger.error(f"Exept UC e {e}")
        return False
    return True


def DeleteCalendar(Date):
    try:
        cursor = executeSQL()
        cursor.execute(f"DELETE FROM Calendar WHERE Date=%s", (Date,))
    except Exception as e:
        logger.error(f"Exeption DeleteCalendar {e}")
        return False
    DBCommit()
    return True


def GenCalendarInlineButtons():
    buttons = []
    mv = 0
    for x in weekdays:
        mv += 1
        if mv <= int(date.datetime.now().strftime("%w")):
            print(int(date.datetime.now().strftime("%w")))
            st = "✅ "
        else:
            st = ""
        buttons.extend([[InlineKeyboardButton(st + x, callback_data=f"ah_cc_{mv}")]])
    return buttons


def GetWeekDay(Value: int):
    return weekdays[int(Value) - 1]


def DeleteOldCalendar():
    c = ParseCalendar()
    for x in c:
        data = x[0]
        od = date.datetime.strptime(data, "%d.%m.%y")
        if not date.date(od.year, od.month, od.day).isocalendar().week >= date.datetime.now().isocalendar().week:
            DeleteCalendar(data)
            print(data)


def InitCalendar(Date):
    pc = ParseDateCalendar(Date)
    if len(pc) == 0:
        try:
            cursor = executeSQL()
            cursor.execute("INSERT INTO Calendar (Date, Text) VALUES("
                           "%s, '')", (Date,))
            DBCommit()
        except Exception as e:
            logger.error(e)
            return False
        return True
    return False


def FilterThisWeek() -> list:
    c = ParseCalendar()
    newlist = []
    datestartweek = int(date.datetime.now().strftime("%w"))
    for x in c:
        if date.datetime.strptime(x[0], "%d.%m.%y").isocalendar().week >= datestartweek:
            newlist.extend([x])
    return newlist


def GenCalendar():
    DeleteOldCalendar()
    c = FilterThisWeek()
    print(c)
    msg = []

    for mv in range(1, 8):
        text = "Інформація не вказана"
        for x in c:
            if int(x[2]) == mv:
                if not len(x[1]) == 0:
                    text = x[1]
        msg.extend([f"{daysemoji[mv - 1]} {weekdays[mv - 1]}\n"
                    f"{text}\n\n"])
    return msg


def GenVideoButtons(ID):
    a = ParseSFLIDVideos(ID)[0]
    av = ParseVLIDVideos(a[0])
    #print(av)
    buttons = []
    buttons2 = []
    buttons3 = []
    mv = 1
    #print(a)
    for x in av:
        if mv == int(a[3]):
            buttons.extend([InlineKeyboardButton(text=f"[{mv}]", callback_data="None")])
        else:
            buttons.extend([InlineKeyboardButton(text=f"{mv}", callback_data=f'cngseries_{x[4]}')])
        mv += 1
    for x1 in buttons:
        if len(buttons) < 8:
            buttons = [buttons]
            buttons2.extend(buttons)
            break
        elif len(buttons) > 8:
            bt2 = [buttons[:9]]
            buttons2.extend(bt2)
            buttons = buttons[8:]
    return buttons2

