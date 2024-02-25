# Автор - cheuS1 | https://github.com/Telegram-search-anime-bo
import asyncio
import re
from warnings import filterwarnings
import datetime
import telegram.ext
import yaml
from telegram.warnings import PTBUserWarning
# Лоадер конфігу
with open('config.yaml', 'r') as file:
    loadedfile = yaml.safe_load(file)
    archiveID = loadedfile['archive_ID']
    token = loadedfile['TOKEN']
    donatefile = loadedfile['donate-file']
    iam = loadedfile['inline-additional-menu']
    searchtitlevideo = loadedfile['search_title_video_ID']

#import logging
#from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler
from MySQL_Driver import startdbs
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton,
                      InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto, Message,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import *
#from pathlib import Path
from conv_handlers import *
from functions import *
from file_func import *
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
log = logging.getLogger("KiotoBot")
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
##################### Визначення змінних
allanimcategories = ["Антиутопія", "Деменція", "Зомбі",
                     "Махо-шьоджьо", "Постапокаліптика", "Фантастика",
                     "Фантастика", "Джьосей", "Ісекай", "Меха", "Романтика",
                     "Фентезі", "Бойовик", "Драма", "Історія", "Містика", "Сейнен",
                     "Школа", "Буденність", "Для дітей", "Казка", "Музика", "Спорт",
                     "Шьоджьо", "Війна", "Еротика", "Комедія", "Надприродне", "Шьоджьо-aї", "Шьонен",
                     "Готика", "Еччі", "Кіберпанк", "Пародія", "Шьонен-aї", "Детектив", "Жахи", "Кодомо", "Пригоди",
                     "Триллер", "Повсякденність", "Психологія", "Вампіри", "Екшн"]
allanimtypes = ["ТВ", "Короткометражний фільм", "Фільм", "ОВА", "Веб", "Спешл"]

add_title_s, add_title_s1, add_title_s2, add_title_s3, add_title_s4, add_title_s5, add_title_s6, add_title_s7, add_title_s8, add_title_s9, add_title_s10, add_title_s11, add_title_s12, add_title_s13, add_title_s14,add_title_s15, add_title_final = range(17)
del_title_s, del_title_s1, del_title_s2, del_title_s3 = range(4)
add_video = range(1)
del_vl = range(1)
vlid_title_change, vlid_title_change1 = range(2)
vlid_update, vlid_update1 = range(2)
replace_info = range(1)
c_s = range(1)
ccng, ccng1 = range(2)
trntedit, trntedit1 = range(2)
urlget = range(1)
upt, upt2 = range(2)
rmoney = range(1)
# InlineKeyboards
k_start = [["🔍 Знайти"], ["💭 Інформація"]]
k_start_adm = [["🔍 Знайти"], ["❗️ Адмін панель"], ["💭 Інформація"]]
k_admpanel = [["Добавити тайтл", "Видалити тайтл", "Зміна стану тайтлу", "Плеєр"],
              ["Календар","Інструменти редагування", "Адміністратори", "Список тайтлів","Додаткові інструменти", "В головне меню"]]
k_advtools = [["Торрент редагування","Отримати посилання","Змінити рік","Назад"]]
k_replace = [["Редагувати інформацію","Редагувати \"Підтримати нас\"","Назад"]]
k_calendar = [["Зміна інформації календаря","Оновити календар","В головне меню"]]
k_player = [["Добавити список", "Видалити список", "Редагувати VideoList"],
            ["Редагувати VLID тайтлу", "Список по VLID", "Назад"]]
k_addtitile = [["Стандартне додавання", "Назад"]]
k_cancel = [["❌ Скасувати"]]

# Функції
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info(
        f"Прийнятий запит на генерацію InlineQuery, юзер {update.effective_user.full_name} {update.effective_user.id}")
    query = update.inline_query
    ql = QueryList(query.query)
    print(f"QUERY: {query.query}")
    if not ql:
        return
    a = await query.answer(results=ql, is_personal=True)
    if a:
        log.info(f"Запит виконано успішно, юзер {update.effective_user.full_name} {update.effective_user.id}")
    else:
        log.error(f"Запит не виконано!. юзер {update.effective_user.full_name} {update.effective_user.id}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    await update.effective_message.delete()
    args = msg.text.split(" ")
    print(args)
    if len(args) == 1:
        if chat.type == "private":
            if UserIsAdmin(user.id):
                await chat.send_message("Привіт! Я ботик для допомоги кіотикам в пошуку тайтлів!", reply_markup=ReplyKeyboardMarkup(k_start_adm))
            else:
                await chat.send_message("Привіт! Я ботик для допомоги кіотикам в пошуку тайтлів!", reply_markup=ReplyKeyboardMarkup(k_start))
    else:
        p = ParseIDTitle(args[1])
        if len(p) == 0:
            print("Старт не ІД")
        else:
            keyword = args[1]
            print(f"{keyword} KEY")
            a = ParseIDTitle(keyword)[0]
            photo = Path(f"Data/Images/{keyword}")
            await chat.send_photo(photo=open(photo, "rb"))
            if len(a[6]) == 0:
                season = ""
            else:
                season = f"({a[6]})"
            categories = ', '.join(a[3].split(","))
            stR = a[8]
            if stR is None:
                st = "Не вказаний"
            elif len(stR) == 0:
                st = "Не вказаний"
            elif stR == "0":
                st = "⚠️ Озвучується"
            elif stR == "1":
                st = "✅ Закінчений"
            elif stR == "2":
                st = "❔ Онґоїнґ"
            else:
                st = f"Невідомий({a[8]}"
            # f"<b></b> <i></i>"
            msg = (f"<b>{a[1]} / {a[4]} {season}</b>\n\n"
                   f"<b>Стан: {st}</b>\n\n"
                   f"<b>Тип:</b> <i>{a[11]}</i>\n"
                   f"<b>Жанр:</b> <i>{categories}</i>\n"
                   f"<b>Сезон:</b> <i>{a[12]}</i>\n"
                   f"<b>Озвучували аніме:</b> <i>{a[7]}</i>\n"
                   f"<b>Переклад:</b> <i>{a[9]}</i>\n"
                   f"<b>Звукорежисер:</b> <i>{a[10]}</i>\n\n"
                   f"<b>Опис:</b> <i>{a[2]}</i>"
                   )
            msg_adm = (f"<b>{a[1]} / {a[4]} {season}</b>\n\n"
                       f"<b>Стан: {st}</b>\n\n"
                       f"<b>Тип:</b> <i>{a[11]}</i>\n"
                       f"<b>Жанр:</b> <i>{categories}</i>\n"
                       f"<b>Сезон:</b> <i>{a[12]}</i>\n"
                       f"<b>Озвучували аніме:</b> <i>{a[7]}</i>\n"
                       f"<b>Переклад:</b> <i>{a[9]}</i>\n"
                       f"<b>Звукорежисер:</b> <i>{a[10]}</i>\n\n"
                       f"<b>Опис:</b> <i>{a[2]}</i>\n\n"
                       f"Ідентифікатор тайтлу: {a[0]}")
            video = ""
            for x in ParseVLIDVideos(a[5]):
                if x[3] == 1:
                    video = x[4]
                    break
            if a[13] is None or len(a[13]) == 0:
                trnt = 0
            else:
                trnt = 1
            if len(a[5]) == 0:
                if UserIsAdmin(user.id):
                    await chat.send_message(msg_adm, disable_web_page_preview=True,
                                            parse_mode=telegram.constants.ParseMode.HTML)
                else:
                    await chat.send_message(msg, disable_web_page_preview=True,
                                            parse_mode=telegram.constants.ParseMode.HTML)
            else:
                if UserIsAdmin(user.id):
                    if trnt == 0:
                        await chat.send_message(msg_adm, disable_web_page_preview=True,
                                                parse_mode=telegram.constants.ParseMode.HTML,
                                                reply_markup=InlineKeyboardMarkup([
                                                    [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                          callback_data=f"v_{video}")]
                                                ]))
                    else:
                        await chat.send_message(msg_adm, disable_web_page_preview=True,
                                                parse_mode=telegram.constants.ParseMode.HTML,
                                                reply_markup=InlineKeyboardMarkup([
                                                    [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                          callback_data=f"v_{video}")]
                                                    ,
                                                    [InlineKeyboardButton(text="Отримати торрент",
                                                                          callback_data=f"sd_{a[0]}")]
                                                ]))
                else:
                    if len(a[13]) == 0:
                        await chat.send_message(msg, disable_web_page_preview=True,
                                                parse_mode=telegram.constants.ParseMode.HTML,
                                                reply_markup=InlineKeyboardMarkup([
                                                    [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                          callback_data=f"v_{video}")]
                                                ]))
                    else:
                        await chat.send_message(msg, disable_web_page_preview=True,
                                                parse_mode=telegram.constants.ParseMode.HTML,
                                                reply_markup=InlineKeyboardMarkup([
                                                    [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                          callback_data=f"v_{video}")],
                                                    [InlineKeyboardButton(text="Отримати торрент",
                                                                          callback_data=f"sd_{a[0]}")]
                                                ]))


    return ConversationHandler.END


async def start_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if UserIsAdmin(user.id):
        await chat.send_message("Чого бажаєш?", reply_markup=ReplyKeyboardMarkup(k_start_adm))
    else:
        await chat.send_message("Чого бажаєш?", reply_markup=ReplyKeyboardMarkup(k_start))
    print("Stb+")
    return ConversationHandler.END


async def playerinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserIsAdmin(update.effective_user.id):
        await update.effective_chat.send_message("Що хочеш зробити?", reply_markup=ReplyKeyboardMarkup(k_player))

async def replaceinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserIsAdmin(update.effective_user.id):
        await update.effective_chat.send_message("Що хочеш зробити?", reply_markup=ReplyKeyboardMarkup(k_replace))
async def search_title_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ReadOtherFile("search_title_video.txt")
    msg = msg.replace("BOTUSERNAME", context.bot.username)
    if int(searchtitlevideo) == 0:
        await update.effective_chat.send_message(text=msg, parse_mode=telegram.constants.ParseMode.HTML, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Пошук", switch_inline_query_current_chat="")]
            ]))
    else:
        await update.effective_chat.send_video(
            video="BAACAgIAAx0CecxgbAADGGWj3mePh59oE-CBKERduXCs7XMZAAIbQAACOPAhSSvohvo-RHGENAQ", caption=msg,
            parse_mode=telegram.constants.ParseMode.HTML, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Пошук", switch_inline_query_current_chat="")]
            ]))


async def adm_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserIsAdmin(update.effective_user.id):
        chat = update.effective_chat
        msg = update.effective_message
        user = update.effective_user
        await chat.send_message("Вітаю у адмін панелі!")
        await chat.send_message("Що хочеш зробити?", reply_markup=ReplyKeyboardMarkup(k_admpanel))


async def adm_start_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserIsAdmin(update.effective_user.id):
        chat = update.effective_chat
        msg = update.effective_message
        user = update.effective_user
        await chat.send_message("Що хочеш зробити?", reply_markup=ReplyKeyboardMarkup(k_admpanel))
        RemoveTempUser(user.id)
        RemoveValueUser(user.id)
    print("aDM+")
    return ConversationHandler.END

async def addtoolsinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UserIsAdmin(update.effective_user.id):
        await update.effective_chat.send_message("Що обереш?",reply_markup=ReplyKeyboardMarkup(k_advtools))
async def add_title_pre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    if UserIsAdmin(user.id):
        await chat.send_message("Яким саме додаванням ти бажаєш скористатись?",
                                reply_markup=ReplyKeyboardMarkup(k_addtitile))


async def add_title_standart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if not UserIsAdmin(update.effective_user.id):
        return ConversationHandler.END
    a = TotalRandom()
    context.user_data['TT'] = a
    await chat.send_message(
        f"Ти запустив інструмент додавання тайтлу до БД\nДотримуйся того, що я прошу і тайтл буде добавлено\nЗгенерований ідентифікатор тайтлу: {a}",
        reply_markup=ReplyKeyboardMarkup(k_cancel))
    await chat.send_message(
        "Примітка: Старайся писати без помилок, тому що процедуру прийдеться починати спочатку. Також не використовуй [ ] { } __ і тому подібні знаки. \nЦе знаки MarkDown, використовуй тільки якщо впевний у їх правильному написанні")
    await chat.send_message("Надішли мені назву тайтлу українською: (За наявності, знак ` буде видалений з тексту)")
    AddTempUser(user.id, a)
    print(temp_addtitle)
    return add_title_s


async def add_title_standart1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    InitTitle(context.user_data['TT'], msg.text)
    await chat.send_message(
        "Добре! Тепер надішли оригінальну назву мовою автора: (За наявності, знак ` буде видалений з тексту)")
    return add_title_s1


async def add_title_standart2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    categories = ', '.join(allanimcategories)
    UpdateTitles(UserTempTitleID(user.id), "OriginalName", RBS(msg.text))
    await chat.send_message(
        "Чудово! Тепер надішли жанри аніме: (Можна через кому: еччі,деменція,комодо | Без пробілів між комами та словами)")
    await chat.send_message(f"Доступні жанри аніме: \n\n{categories}")
    return add_title_s2


async def add_title_standart3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    mv = 0
    if len(msg.text.split(",")) == 1:
        if msg.text in allanimcategories:
            await chat.send_message(
                "Жанр правильний! Тепер надішли мені опис тайтлу: (За наявності, знак ` буде видалений з тексту) ")
            UpdateTitles(UserTempTitleID(user.id), "Category", RBS(msg.text))
            return add_title_s3
        else:
            await chat.send_message("Жанр неправильний. Попробуй ще раз!")

    elif len(msg.text.split(",")) > 1:

        for x in msg.text.split(","):
            if not x in allanimcategories:
                await chat.send_message(f'Жанр "{x}" неправильний. Попробуй ще раз!')
                mv = 1
                continue
        if mv == 0:
            await chat.send_message(
                "Жанри правильні! Тепер надішли мені опис тайтлу: (Опис не повинен перевищувати приблизно 186 слів або 1024 символів) ")
            UpdateTitles(UserTempTitleID(user.id), "Category", RBS(msg.text))
            return add_title_s3


async def add_title_standart4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if len(msg.text) >= 1024:
        await chat.send_message("Опис перевищує 1024 символів, попробуйте ще раз")
    else:
        UpdateTitles(UserTempTitleID(user.id), "Description", RBS(msg.text))
        await chat.send_message("Прекрасно! Надішли сезон тайтлу: (Якщо тайтл односезонний, надішли нуль - 0)")
        await chat.send_message("Приклад: Сезон 1, частина 1/2")
        return add_title_s4


async def add_title_standart5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if msg.text == "0":
        UpdateTitles(UserTempTitleID(user.id), "Season", "")
    else:
        UpdateTitles(UserTempTitleID(user.id), "Season", RBS(msg.text))
    await chat.send_message("Чудово! Надішли мені акторський склад(актори озвучення, звукорежисери і т.д.)")
    await chat.send_message("Примітка:\n\n"
                            "Знак ` буде видалений за наявності!",
                            disable_web_page_preview=True)
    await chat.send_message(
        "Приклад: Малинка, Ягідка, Пиріжочок, Гангстер")
    return add_title_s5


async def add_title_standart6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    UpdateTitles(UserTempTitleID(user.id), "Actors", RBS(msg.text))
    await chat.send_message("Залишилось ще трохи! Надішли мені VideoListID на список")
    await chat.send_message(
        "Примітка:\nНеправильний VideoListID не дасть переглядати аніме, тому Вам прийдеться перестворювати тайтл.\nЯкщо вибрати вже прив'язаний список, він переприв'яжеться.")
    await chat.send_message("Приклад: Dji2rjaD92dfpagjmnvj5")

    UIDs = []
    msg = "Списки відеоплеєра:\n\n"
    mv = 1
    pv = ParseAllVideos()
    pt = ParseAllTitles()
    for x in pv:
        UIDs.extend([x[0]])
    UIDs = list(set(UIDs))
    conx = 0
    for x in UIDs:
        for x1 in pt:
            if x == x1[5]:
                conx = x1[1]
                break
            else:
                conx = 0
        if conx == 0:
            con = "Відсутня"
        else:
            con = conx
        msg += f"{mv}. VLID: {x} | Прив'язка: {con}\n"
        mv += 1
    await chat.send_message(msg)

    return add_title_s6


async def add_title_standart7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if not CheckListVILD(msg.text):
        await chat.send_message("Такий список відсутній. Попробуйте ще раз")
    else:
        a = CheckListConVILD(msg.text)
        if not a:
            UpdateTitles(UserTempTitleID(user.id), "VideoPost", RBS(msg.text))
            await chat.send_message("Ти просто чудо! Надішли мені зображення обкладинки тайтлу:")
            await chat.send_message("Примітка:\n"
                                    "Кидати як зображення, не як файл!")
            return add_title_s7
        else:
            await chat.send_message("Список вже прив'язаний. Переприв'язую список до нового тайтлу.")
            await chat.send_message(f"Зауважте, список був відв'язаний від старого тайтлу: {ParseIDTitle(a)[0][1]}")
            UpdateTitles(a, "VideoPost", "")
            UpdateTitles(UserTempTitleID(user.id), "VideoPost", RBS(msg.text))
            await chat.send_message("Ти просто чудо! Надішли мені зображення обкладинки тайтлу:")
            await chat.send_message("Примітка:\n"
                                    "Кидати як зображення, не як файл!")
            return add_title_s7


async def add_title_standart8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    sp = Path(f"Data/Images/{UserTempTitleID(user.id)}")
    file = await context.bot.get_file(update.message.photo[-1])
    await file.download_to_drive(sp)
    """await chat.send_message("Тайтл добавлено в БД:")
    a = ParseIDTitle(UserTempTitleID(user.id))[0]
    msg = (f"{a[1]} {a[6]}\n"
           f"{a[4]}\n\n"
           f"Опис: {a[2]}\n\n"
           f"Жанр: {a[3]}\n\n"
           f"Склад команди озвучення: {a[7]}\n\n"
           f"Детальніше: {a[5]}")
    await chat.send_photo(caption=msg, photo=open(sp, "rb"), reply_markup=ReplyKeyboardMarkup(k_admpanel))
    RemoveTempUser(user.id)
    return ConversationHandler.END"""
    await chat.send_message("Тепер надішли мені пупсиків, які перекладали тайтл:")
    return add_title_s8
async def add_title_standart9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    UpdateTitles(UserTempTitleID(user.id), "Translator", msg.text)
    await chat.send_message("Молодець! Тепер я очікую від тебе кличку звукорежисера(-ів):")
    return add_title_s9
async def add_title_standart10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    UpdateTitles(UserTempTitleID(user.id), "Soundman", msg.text)
    await chat.send_message("Тип тайтлу?:")
    await chat.send_message("Типи: ТВ, Короткометражний фільм, Фільм, ОВА, Веб, Спешл")
    return add_title_s10
async def add_title_standart11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if msg.text in allanimtypes:
        UpdateTitles(UserTempTitleID(user.id), "Type", msg.text)
        await chat.send_message("Ти просто зайчик! Надішли мені Сезон тайтлу")
        await chat.send_message("Сезони: Зима, Весна, Літо, Осінь")
        return add_title_s11
    else:
        await chat.send_message(f"Я не знаю такого типу тайтлу: {msg.text}")
        await chat.send_message("Попробуй ще раз")
        await chat.send_message("Тип тайтлу:")
async def add_title_standart12(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if msg.text in ["Зима","Весна","Літо","Осінь"]:
        UpdateTitles(UserTempTitleID(user.id), "Age", msg.text)
        await chat.send_message("Надішли Torrent-файл")
        await chat.send_message("Якщо такого немає, надішли 0")
        return add_title_s13
    else:
        await chat.send_message(f"Я не знаю сезону: {msg.text}")
        await chat.send_message("Попробуй ще раз")
        await chat.send_message("Сезон тайтлу:")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_message.text)
async def add_title_standart13(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    tr = trntTotalRandom()
    context.user_data['tr'] = tr
    p = Path(f"Data/Torrents/{tr}.torrent")
    print(f"MSG: {msg}")
    if msg.text is None:
        msf = await context.bot.get_file(msg.document)
        await msf.download_to_drive(p)
        UpdateTitles(UserTempTitleID(user.id), "Torrent", tr)
        await chat.send_message("Надішліть мені рік виходу тайтлу:")
        await chat.send_message("Приклад: 2014")
        return add_title_s14
    elif msg.text == "0":
        UpdateTitles(UserTempTitleID(user.id), "Torrent", "")
        await chat.send_message("Надішліть мені рік виходу тайтлу:")
        await chat.send_message("Приклад: 2014")
        return add_title_s14
    else:
        await chat.send_message("Попробуйте ще раз.")
async def add_title_standart14(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if msg.text.isdigit():
        aaa = msg.text.replace(" ", "")
        UpdateTitles(UserTempTitleID(user.id), "Year", aaa)
        p = Path(f"Data/Torrents/{context.user_data['tr']}.torrent")
        a = ParseIDTitle(UserTempTitleID(user.id))[0]
        await chat.send_message("Тайтл додано!", reply_markup=ReplyKeyboardMarkup(k_admpanel))
        if trntexists(p) == 0:
            trnt = "Відсутній"
        else:
            trnt = f"{a[13]}"
        msg = (f"{a[1]} {a[6]}\n"
               f"{a[4]}\n\n"
               f"Опис: {a[2]}\n\n"
               f"Тип: {a[11]}\n\n"
               f"Жанр: {a[3]}\n\n"
               f"Склад команди озвучення: {a[7]}\n\n"
               f"VLID: {a[5]}\n\n"
               f"Torrent: {trnt}\n\n"
               f"Рік {a[14]}\n\n"
               )
        if len(msg) > 1000:
            msg = ("Успішно добавлено!\n"
                   "Додаткова інформація прихована, через перевищення ліміту символів.")
        sp = Path(f"Data/Images/{a[0]}")
        try:
            await chat.send_photo(caption=msg, photo=open(sp, "rb"))
            RemoveTempUser(user.id)
        except Exception as e:
            print(e)
        finally:
            return ConversationHandler.END
    else:
        await chat.send_message("Щось не так, попробуйте ще раз")

"""async def trntTOmagnet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if UserIsAdmin(user.id):
        await chat.send_message("Це інструмент перетворення торент файлу на магнет посилання",
                                reply_markup=ReplyKeyboardMarkup(k_cancel))
        await chat.send_message("Це інструмент перетворення торент файлу на магнет посилання")
        await chat.send_message("Надішли мені Torrent-файл і я надішлю тобі Magnet посилання:")
        return trntmag
    else:
        return ConversationHandler.END

async def trntTOmagnet1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    file = await context.bot.get_file(update.effective_message.document)
    p = Path(f"Data/tmp/{tmpTotalRandom()}")
    print(p)
    await file.download_to_drive(p)
    ctf = check_torrent_file(p)
    if not ctf:
        await chat.send_message("Дивний торент, я не можу його прочитати! Попробуй інший торент-файл:")
    elif not None:
        await chat.send_message(f"Твоє Magnet посилання:\n\n<code>{ctf}</code>",parse_mode=telegram.constants.ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(k_advtools) )
        os.remove(p)
        return ConversationHandler.END
    else:
        print("Якась хуйня з парсингом торенту")"""

async def trnteditf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if not UserIsAdmin(user.id):
        return ConversationHandler.END
    else:
        await chat.send_message("Це інструмент зміни торенту у тайтла. Надішли мені тайтл через @pankioto_bot:", reply_markup=ReplyKeyboardMarkup(k_cancel))
        return trntedit
async def trnteditf1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    pattern = r'^/search_(\w+)$'
    match = re.match(pattern, msg.text)
    keyword = match.group(1)
    a = ParseIDTitle(keyword)[0]
    print(f"{keyword} KEY")
    if not len(a) == 0:
        await chat.send_message(f"Тайтл {a[1]} {a[6]} прийнято.")
        AddTempUser(user.id, keyword)
        await chat.send_message("Очікую надсилання торент файлу:")
        return trntedit1
async def trnteditf2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    msf = await context.bot.get_file(msg.document)
    a = ParseIDTitle(UserTempTitleID(user.id))[0]
    tr = trntTotalRandom()
    p = Path(f"Data/Torrents/{tr}.torrent")
    if not a[13] is None:
        if trntexists(f"Data/Torrents/{a[13]}.torrent"):
            os.remove(f"Data/Torrents/{a[13]}.torrent")
    try:
        await msf.download_to_drive(p)

        UpdateTitles(UserTempTitleID(user.id), "Torrent", tr)
        await chat.send_message("Торент успішно оновлено!", reply_markup=ReplyKeyboardMarkup(k_advtools))
        RemoveTempUser(user.id)
    except Exception as e:
        print(e)
    finally:
        return ConversationHandler.END

async def getURL(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if not UserIsAdmin(user.id):
        return ConversationHandler.END
    else:
        await chat.send_message("Це інструмент генерування посилання на тайтл. Надішли мені тайтл через @pankioto_bot:",
                                reply_markup=ReplyKeyboardMarkup(k_cancel))
        return urlget

async def getURL1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    pattern = r'^/search_(\w+)$'
    match = re.match(pattern, msg.text)
    keyword = match.group(1)
    a = ParseIDTitle(keyword)[0]
    print(f"{keyword} KEY")
    if not len(a) == 0:
        await chat.send_message(f"Тайтл {a[1]} {a[6]} прийнято.", reply_markup=ReplyKeyboardMarkup(k_advtools))
        await chat.send_message(f"Посилання: https://t.me/pankioto_bot?start={keyword}")
        return ConversationHandler.END
    else:
        await chat.send_message("Щось пішло не так! Попробуй ще раз!")
async def undone_add_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    p = Path(f"Data/Torrents/{UserTempTitleID(user.id)}.torrent")
    if trntexists(p):
        os.remove(p)
    try:
        DeleteTitleID(UserTempTitleID(user.id))
        RemoveTempUser(user.id)
    except Exception as e:
        print(e)
    print(temp_addtitle)
    await adm_start_back(update, context)
    return ConversationHandler.END


async def AdminList(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if UserIsAdmin(user.id):
        mv = 1
        a = ParseAllAdm()
        if len(a) == 0:
            await chat.send_message("Адміністратори відсутні")
        else:
            msg = "Адміністратори\n\n"
            for x in a:
                msg = msg + f"{mv}. UserID: {x[0]}\n"
                mv = mv + 1
        await chat.send_message(msg)


async def search_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    pattern = r'^/search_(\w+)$'
    match = re.match(pattern, msg.text)
    keyword = match.group(1)
    print(f"{keyword} KEY")
    a = ParseIDTitle(keyword)[0]

    await update.effective_message.delete()

    photo = Path(f"Data/Images/{keyword}")
    await chat.send_photo(photo=open(photo, "rb"))
    if len(a[6]) == 0:
        season = ""
    else:
        season = f"({a[6]})"
    categories = ', '.join(a[3].split(","))
    stR = a[8]
    if stR is None:
        st = "Не вказаний"
    elif len(stR) == 0:
        st = "Не вказаний"
    elif stR == "0":
        st = "⚠️ Озвучується"
    elif stR == "1":
        st = "✅ Закінчений"
    elif stR == "2":
        st = "❔ Онґоїнґ"
    else:
        st = f"Невідомий({a[8]}"
    if a[14] is None or a[14] == "":
        year = ""
    else:
        year = f"{a[14]}"
    ### РЕЗЕРВНІ МСГ
    """msg = (f"<b>Назва:</b> <i>{a[1]} {season}</i>\n"
           f"<b>Стан: {st}</b>\n"
           f"<b>Жанр:</b> <i>{categories}</i>\n"
           f"<b>Задіяні в озвученні:</b> <i>{a[7]}</i>\n"
           f"<b>Опис:</b> <i>{a[2]}</i>")
    msg_adm = (f"<b>Назва:</b> <i>{a[1]} {season}</i>\n"
           f"<b>Стан: {st}</b>\n"               
           f"<b>Жанр:</b> <i>{categories}</i>\n"
           f"<b>Задіяні в озвученні:</b> <i>{a[7]}</i>\n"
           f"<b>Опис:</b> <i>{a[2]}</i>\n\n"
               f"Ідентифікатор тайтлу: {a[0]}")"""
    # f"<b></b> <i></i>"
    msg = (f"<b>{a[1]} / {a[4]} {season}</b>\n\n"
           f"<b>Стан: {st}</b>\n\n"
           f"<b>Тип:</b> <i>{a[11]}</i>\n"
            f"<b>Жанр:</b> <i>{categories}</i>\n"
           f"<b>Сезон:</b> <i>{a[12]} {year}</i>\n"
           f"<b>Озвучували аніме:</b> <i>{a[7]}</i>\n"
           f"<b>Переклад:</b> <i>{a[9]}</i>\n"
           f"<b>Звукорежисер:</b> <i>{a[10]}</i>\n\n"
           f"<b>Опис:</b> <i>{a[2]}</i>"
           )
    msg_adm = (f"<b>{a[1]} / {a[4]} {season}</b>\n\n"
           f"<b>Стан: {st}</b>\n\n"
           f"<b>Тип:</b> <i>{a[11]}</i>\n"
            f"<b>Жанр:</b> <i>{categories}</i>\n"
           f"<b>Сезон:</b> <i>{a[12]} {year}</i>\n"
           f"<b>Озвучували аніме:</b> <i>{a[7]}</i>\n"
           f"<b>Переклад:</b> <i>{a[9]}</i>\n"
           f"<b>Звукорежисер:</b> <i>{a[10]}</i>\n\n"
           f"<b>Опис:</b> <i>{a[2]}</i>\n\n"
               f"Ідентифікатор тайтлу: {a[0]}")
    if a[13] is None or len(a[13]) == 0:
        trnt = 0
    else:
        trnt = 1
    video = ""
    for x in ParseVLIDVideos(a[5]):
        if x[3] == 1:
            video = x[4]
            break
    if len(a[5]) == 0:
        if UserIsAdmin(user.id):
            await chat.send_message(msg_adm, disable_web_page_preview=True,
                                    parse_mode=telegram.constants.ParseMode.HTML)
        else:
            await chat.send_message(msg, disable_web_page_preview=True, parse_mode=telegram.constants.ParseMode.HTML)
    else:
        if UserIsAdmin(user.id):
            if trnt == 0:
                await chat.send_message(msg_adm, disable_web_page_preview=True,
                                        parse_mode=telegram.constants.ParseMode.HTML,
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                  callback_data=f"v_{video}")]
                                        ]))
            else:
                await chat.send_message(msg_adm, disable_web_page_preview=True,
                                        parse_mode=telegram.constants.ParseMode.HTML,
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                  callback_data=f"v_{video}")]
                                            ,
                                            [InlineKeyboardButton(text="Отримати торрент",
                                                                  callback_data=f"sd_{a[0]}")]
                                        ]))
        else:
            if len(a[13]) == 0:
                await chat.send_message(msg, disable_web_page_preview=True,
                                        parse_mode=telegram.constants.ParseMode.HTML,
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                  callback_data=f"v_{video}")]
                                        ]))
            else:
                await chat.send_message(msg, disable_web_page_preview=True,
                                        parse_mode=telegram.constants.ParseMode.HTML,
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                  callback_data=f"v_{video}")],
                                            [InlineKeyboardButton(text="Отримати торрент",
                                                                  callback_data=f"sd_{a[0]}")]
                                        ]))


async def delete_titles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if not UserIsAdmin(user.id):
        return ConversationHandler.END
    else:
        await chat.send_message("Вітаю у інструменті видалення тайтлів!", reply_markup=ReplyKeyboardMarkup(k_cancel))
        await chat.send_message(
            " Надішліть тайтл через <b>Пошук</b> і я його видалю.\nБудь обережний, <u>підтвердження видалення не буде</u>",
            parse_mode=telegram.constants.ParseMode.HTML, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Пошук", switch_inline_query_current_chat="")]
            ]))
        return del_title_s


async def delete_titles1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    pattern = r'^/search_(\w+)$'
    match = re.match(pattern, msg.text)
    keyword = match.group(1)
    a = ParseIDTitle(keyword)[0]
    print(f"{keyword} KEY")
    if DeleteTitleID(keyword):
        await chat.send_message(f"Тайтл {a[1]} {a[6]} видалено успішно!")
        await chat.send_message(f"Очікую наступний тайтл на видалення:\nЩоб скасувати: ❌ Скасувати")
    else:
        await chat.send_message("Помилка видалення тайтлу")


async def add_title_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if not UserIsAdmin(user.id):
        return ConversationHandler.END
    await chat.send_message("Це інструмент пакетного додавання тайтлів")
    await chat.send_message("Очікую текстовий файл")


async def Information(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    pth = Path("Data/Other/info.txt")
    a = ParseAllTitles()
    p = ParseAllVideos()
    with open(pth, "r") as file:
        msg = file.read()
    if len(msg) == 0:
        await chat.send_message("Інформація незаповнена. Зверніться до адміністраторів.")
    else:
        text = msg.replace("ALLSERIES_PH", f"{str(len(p))}")
        text = text.replace("ALLTITLES_PH", f"{str(len(a))}")
        await chat.send_message(text, disable_web_page_preview=True)


async def ReplaceInfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if UserIsAdmin(user.id):
        await chat.send_message("Це інструмент заміни тексту в вкладці \"Інформація\"",
                                reply_markup=ReplyKeyboardMarkup(k_cancel))
        await chat.send_message("Щоб записати новий текст, надішли мені нову інформацію один повідомленням:")
        await chat.send_message(
            "Плейсхолдери: ALLTITLES_PH - Кількість всіх тайтлів | ALLSERIES_PH - Кількість всіх серій\n"
            "Приховане посилання: [Купити каву](https://google.com) ПОКИ НЕ ПРАЦЮЄ\n"
            "Заборонені знаки будуть <b>видалені</b> - _ * ` ~", parse_mode=telegram.constants.ParseMode.HTML)
        await chat.send_message("Стара інформація:")
        oldinf = ReadOtherFile("info.txt")
        if len(oldinf) == 0:
            oldinf = "Інформаційна вкладка пуста"
        await chat.send_message(oldinf)
        return replace_info
    else:
        return ConversationHandler.END


async def ReplaceInfo1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    text = msg.text
    WriteOtherFile("info.txt", msg.text)
    await chat.send_message("Готово! Інформація змінена!", reply_markup=ReplyKeyboardMarkup(k_admpanel))
    return ConversationHandler.END

async def ReplaceMoney(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if UserIsAdmin(user.id):
        await chat.send_message("Це інструмент заміни тексту в вкладці \"Підтримати нас\"",
                                reply_markup=ReplyKeyboardMarkup(k_cancel))
        await chat.send_message("Щоб записати новий текст, надішли мені нову інформацію одним повідомленням:")
        await chat.send_message("Примітка: форматування тексту відбувається за HTML")
        await chat.send_message("Стара інформація:")
        oldinf = ReadOtherFile(donatefile)
        if len(oldinf) == 0:
            oldinf = "Інформаційна вкладка пуста"
        await chat.send_message(oldinf)
        return rmoney
    else:
        return ConversationHandler.END


async def ReplaceMoney1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    text = msg.text
    WriteOtherFile(donatefile, msg.text)
    await chat.send_message("Готово! Інформація змінена!", reply_markup=ReplyKeyboardMarkup(k_admpanel))
    return ConversationHandler.END
async def TitleList(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if UserIsAdmin(user.id):
        a = ParseAllTitles()
        if len(a) == 0:
            await chat.send_message("В моїй БД відсутні тайтли.")
        else:
            msg = "Всі тайтли в БД:\n\n"
            mv = 0
            for x in a:
                mv = mv + 1
                if len(x[6]) == 0:
                    season = ""
                else:
                    season = f"({x[6]})"
                if len(x[5]) == 0:
                    con = "Відсутня"
                else:
                    con = x[5]

                msg = msg + f"{mv}. {x[1]} {season} | ID: {x[0]} | Прив'язка: {con}\n"
            await chat.send_message(msg)


async def FileID(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("yes")
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if archiveID == chat.id:
        if chat.type == "supergroup":
            await msg.reply_text(f"Name: {msg.video.file_name}")
            await msg.reply_text(msg.video.file_id)


async def AddVideoList(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if UserIsAdmin(user.id):
        await chat.send_message("Це інструмент створення списку відео для плеєра.")
        await chat.send_message("Надішли мені данні в такому форматі:\nFileID Назва епізоду (частина)\n\nПриклад:\n\n"
                                "HIOio1b19plsdaj31 Лікарня\n"
                                "DAoijfa33fqFAf Монолог мерця\n"
                                "gassshFEW@fesd Мертва тишина (1/2)\n"
                                "rfasdASsfffSfd Мертва тишина (2/2)", reply_markup=ReplyKeyboardMarkup(k_cancel))
        await chat.send_message("Примітка: Якщо назва епізоду відсутня, замість неї напиши 0")
        return add_video


async def AddVideoList1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    x1 = 0
    x2 = 0
    if x1 == 0:
        mv = 1
        vrpostID = VTotalRandom()
        for x in msg.text.split("\n"):
            x = x.split(" ")
            if CheckFLIDUse(x[0]):
                await chat.send_message(
                    f"FileID: {x[0]}\nВже використовується! Ви не можете створити списки з однаковими FileID.")
                await chat.send_message("Виберіть інакший FileID і надішліть мені")
                x2 = 1
                break
            InitVideo(vrpostID, x[0])
            UpdateVideo(x[0], vrpostID, "Episode", mv)
            Capt = " ".join(x).split(" ")
            Capt[0] = ""
            Capt = " ".join(Capt)
            print(f"CAPT {Capt}")
            if str(Capt) == " 0":
                Capt = ""
            UpdateVideo(x[0], vrpostID, "CaptionText", Capt)
            UpdateVideo(x[0], vrpostID, "SFileID", VSTotalRandom())
            mv = mv + 1
        if x2 == 0:
            await chat.send_message(f"Чудова робота! Список створено! VideoListID: {vrpostID}",
                                    reply_markup=ReplyKeyboardMarkup(k_admpanel))
            return ConversationHandler.END


async def VideoList(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if UserIsAdmin(user.id):
        UIDs = []
        msg = "Списки відеоплеєра:\n\n"
        mv = 1
        pv = ParseAllVideos()
        pt = ParseAllTitles()
        conx = 0
        for x in pv:
            UIDs.extend([x[0]])
        UIDs = list(set(UIDs))
        for x in UIDs:
            for x1 in pt:
                print(x1[5])
                if x1[5] == x:
                    conx = x1[1]
                    break
                else:
                    conx = 0
            if conx == 0:
                con = "Відсутня"
            else:
                con = conx
            msg += f"{mv}. VLID: {x} | Прив'язка: {con}\n/series_{x}\n"
            mv += 1
        await chat.send_message(msg)


async def SeriesList(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    pattern = r'^/series_(\w+)$'
    match = re.match(pattern, msg.text)
    VLID = match.group(1)
    print(f"{VLID} VLID KEY")
    if not CheckListVILD(VLID):
        print("FALSE VLID")
        await chat.send_message("Я тебе не розумію. Що ти маєш на увазі?")
        return
    pat = ParseAllTitles()
    con = ""
    for x in pat:
        if x[5] == VLID:
            con = "📺 " + x[1]
            break
        else:
            con = "Відсутня прив'язка до тайтлу, назва не буде відображена."
    series = sortS(ParseVLIDVideos(VLID))
    msg1 = f"{con}\n\n"
    for x in series:
        if len(x[2]) == 0:
            capt = ""
        else:
            capt = " - " + x[2]
        msg1 += f"▶️Епізод {x[3]}{capt}\nДетальніше: /video_{x[4]}\n\n"
    await chat.send_message(msg1)


async def DeleteVideoList(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if UserIsAdmin(user.id):
        await chat.send_message("Це інструмент видалення списку відтворення плеєра.")
        await chat.send_message("Будь ласка, надішліть VLID: ")
        UIDs = []
        msg = "Списки відеоплеєра:\n\n"
        mv = 1
        pv = ParseAllVideos()
        pt = ParseAllTitles()
        for x in pv:
            UIDs.extend([x[0]])
        UIDs = list(set(UIDs))
        conx = 0
        for x in UIDs:
            for x1 in pt:
                if x == x1[5]:
                    conx = x1[1]
                    break
                else:
                    conx = 0
            if conx == 0:
                con = "Відсутня"
            else:
                con = conx
            msg += f"{mv}. VLID: {x} | Прив'язка: {con}\n"
            mv += 1
        await chat.send_message(
            "Примітка: Якщо ви видаляєте список, який прив'язаний до тайтлу, тоді прив'язка буде анульована.",
            reply_markup=ReplyKeyboardMarkup(k_cancel))
        await chat.send_message(msg)
        return del_vl
    else:
        return ConversationHandler.END


async def DeleteVideoList1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if len(ParseVLIDVideos(msg.text)) == 0:
        await chat.send_message("Неправильний VLID, попробуйте ще раз")
    else:
        if DeleteVLID(msg.text):
            await chat.send_message("Список видалено успішно!", reply_markup=ReplyKeyboardMarkup(k_player))
        else:
            await chat.send_message("ПОМИЛКА: Список не видалено!", reply_markup=ReplyKeyboardMarkup(k_player))
        return ConversationHandler.END


async def CallbackQuery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    query = update.callback_query
    await query.answer()
    qd = query.data
    print("+")
    print(qd)
    if qd.startswith("s_"):
        print("+")
        VLID = qd.split("_")[1]
        print(f"{VLID} VLID KEY")
        if not CheckListVILD(VLID):
            print("FALSE VLID")
            await chat.send_message("VLID вказаний неправильно! Зверніться до адміністраторів.")
            return
        pat = ParseAllTitles()
        con = ""
        for x in pat:
            if x[5] == VLID:
                con = "📺 " + x[1]
                break
            else:
                con = "Відсутня прив'язка до тайтлу, назва не буде відображена."

        series = sortS(ParseVLIDVideos(VLID))
        msg1 = f"{con}\n\n"

        for x in series:
            if len(x[2]) == 0:
                name = ""
            else:
                name = " - " + x[2]
            msg1 += f"▶️Епізод {x[3]}{name}\nДетальніше: /video_{x[4]}\n\n"
        await chat.send_message(msg1)
    if qd.startswith("cs_"):
        data = qd.split("_")
        pt = ParseIDTitle(data[1])[0]
        if not pt[8] == str(data[2]):
            UpdateTitles(data[1], "State", data[2])
            oldmsgid = query.message.id
            if data[2] == "0":
                st = "⚠️ Озвучується"
            elif data[2] == "1":
                st = "✅ Закінчений"
            elif data[2] == "2":
                st = "❔ Онґоїнґ"
            else:
                st = f"Невідомий({data[2]})"
            msg = ("Тайтл успішно оновлено.\n\n"
                   f"Назва: {pt[1]} {pt[6]}\nСтан: {st}")
            await context.bot.edit_message_text(chat_id=user.id, message_id=oldmsgid, text=msg)
    if qd == "rtm":
        await query.message.delete()
        await chat.send_message("Вітаю в основному меню!")
        if UserIsAdmin(user.id):
            await chat.send_message("Чого бажаєш?", reply_markup=ReplyKeyboardMarkup(k_start_adm))
        else:
            await chat.send_message("Чого бажаєш?", reply_markup=ReplyKeyboardMarkup(k_start))
    if qd == "restartmenu":
        await query.message.delete()
        p = Path("Data/Other/inline_additional_menu.png")
        await chat.send_photo(photo=open(p, "rb"), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Розклад виходу серій", callback_data="calendar")],
            [InlineKeyboardButton("Випадкове аніме", callback_data="ra")],
            [InlineKeyboardButton(text="Підтримати нас", callback_data="na_revo"),
             InlineKeyboardButton(text="Зв'язок з нами", callback_data="calltogod")],
            [InlineKeyboardButton("Вернутись в основне меню", callback_data="rtm")]
        ]))
    if qd == "calendar":
        datan = date.datetime.now().strftime("%d.%m.%y")
        msg = f"🗓 Розклад виходу серій станом на {datan}:\n\n"
        for x in GenCalendar():
            msg += x
        await query.message.delete()
        await chat.send_message(msg, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад", callback_data="restartmenu")]
        ]))
    if qd == "ra":
        chat = update.effective_chat
        msg = update.effective_message
        user = update.effective_user
        allt = ParseAllTitles()

        if len(allt) == 0:
            await chat.send_message("В моїй базі відсутні тайтли.")
            return
        if len(allt) == 1:
            keywordd = allt[0][0]
        else:
            keywordd = allt[random.randrange(1, stop=len(allt))+1][0]

        print(f"{keywordd} KEY")
        a = ParseIDTitle(keywordd)[0]

        photo = Path(f"Data/Images/{keywordd}")
        await chat.send_photo(photo=open(photo, "rb"))
        if len(a[6]) == 0:
            season = ""
        else:
            season = f"({a[6]})"
        categories = ', '.join(a[3].split(","))
        stR = a[8]
        if stR is None:
            st = "Не вказаний"
        elif len(stR) == 0:
            st = "Не вказаний"
        elif stR == "0":
            st = "⚠️ Озвучується"
        elif stR == "1":
            st = "✅ Закінчений"
        elif stR == "2":
            st = "❔ Онґоїнґ"
        else:
            st = f"Невідомий({a[8]}"
        ### РЕЗЕРВНІ МСГ
        """msg = (f"<b>Назва:</b> <i>{a[1]} {season}</i>\n"
               f"<b>Стан: {st}</b>\n"
               f"<b>Жанр:</b> <i>{categories}</i>\n"
               f"<b>Задіяні в озвученні:</b> <i>{a[7]}</i>\n"
               f"<b>Опис:</b> <i>{a[2]}</i>")
        msg_adm = (f"<b>Назва:</b> <i>{a[1]} {season}</i>\n"
               f"<b>Стан: {st}</b>\n"               
               f"<b>Жанр:</b> <i>{categories}</i>\n"
               f"<b>Задіяні в озвученні:</b> <i>{a[7]}</i>\n"
               f"<b>Опис:</b> <i>{a[2]}</i>\n\n"
                   f"Ідентифікатор тайтлу: {a[0]}")"""
        if a[14] is None or a[14] == "":
            year = ""
        else:
            year = f"{a[14]}"
        msg = (f"<b>{a[1]} / {a[4]} {season}</b>\n\n"
               f"<b>Стан: {st}</b>\n\n"
               f"<b>Тип:</b> <i>{a[11]}</i>\n"
               f"<b>Жанр:</b> <i>{categories}</i>\n"
               f"<b>Сезон:</b> <i>{a[12]} {year}</i>\n"
               f"<b>Озвучували аніме:</b> <i>{a[7]}</i>\n"
               f"<b>Переклад:</b> <i>{a[9]}</i>\n"
               f"<b>Звукорежисер:</b> <i>{a[10]}</i>\n\n"
               f"<b>Опис:</b> <i>{a[2]}</i>"
               )
        msg_adm = (f"<b>{a[1]} / {a[4]} {season}</b>\n\n"
                   f"<b>Стан: {st}</b>\n\n"
                   f"<b>Тип:</b> <i>{a[11]}</i>\n"
                   f"<b>Жанр:</b> <i>{categories}</i>\n"
                   f"<b>Сезон:</b> <i>{a[12]} {year}</i>\n"
                   f"<b>Озвучували аніме:</b> <i>{a[7]}</i>\n"
                   f"<b>Переклад:</b> <i>{a[9]}</i>\n"
                   f"<b>Звукорежисер:</b> <i>{a[10]}</i>\n\n"
                   f"<b>Опис:</b> <i>{a[2]}</i>\n\n"
                   f"Ідентифікатор тайтлу: {a[0]}")
        if a[13] is None or len(a[13]) == 0:
            trnt = 0
        else:
            trnt = 1
        video = ""
        for x in ParseVLIDVideos(a[5]):
            if x[3] == 1:
                video = x[4]
                break
        if len(a[5]) == 0:
            if UserIsAdmin(user.id):
                await chat.send_message(msg_adm, disable_web_page_preview=True,
                                        parse_mode=telegram.constants.ParseMode.HTML)
            else:
                await chat.send_message(msg, disable_web_page_preview=True,
                                        parse_mode=telegram.constants.ParseMode.HTML)
        else:
            if UserIsAdmin(user.id):
                if trnt == 0:
                    await chat.send_message(msg_adm, disable_web_page_preview=True,
                                            parse_mode=telegram.constants.ParseMode.HTML,
                                            reply_markup=InlineKeyboardMarkup([
                                                [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                      callback_data=f"v_{video}")]
                                            ]))
                else:
                    await chat.send_message(msg_adm, disable_web_page_preview=True,
                                            parse_mode=telegram.constants.ParseMode.HTML,
                                            reply_markup=InlineKeyboardMarkup([
                                                [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                      callback_data=f"v_{video}")]
                                                ,
                                                [InlineKeyboardButton(text="Отримати торрент",
                                                                      callback_data=f"sd_{a[0]}")]
                                            ]))
            else:
                if len(a[13]) == 0:
                    await chat.send_message(msg, disable_web_page_preview=True,
                                            parse_mode=telegram.constants.ParseMode.HTML,
                                            reply_markup=InlineKeyboardMarkup([
                                                [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                      callback_data=f"v_{video}")]
                                            ]))
                else:
                    await chat.send_message(msg, disable_web_page_preview=True,
                                            parse_mode=telegram.constants.ParseMode.HTML,
                                            reply_markup=InlineKeyboardMarkup([
                                                [InlineKeyboardButton(text="Відобразити доступні серії",
                                                                      callback_data=f"v_{video}")],
                                                [InlineKeyboardButton(text="Отримати торрент",
                                                                      callback_data=f"sd_{a[0]}")]
                                            ]))
    if qd.startswith("sd_"):
        arg = qd.split("_")[1]
        a = ParseIDTitle(arg)[0]
        p = Path(f"Data/Torrents/{a[13]}")
        dp = Path(f"Data/Torrents/{a[13]}.torrent")
        if trntexists(dp):
            await chat.send_document(open(dp, "rb"),caption=f"Торент файл на тайтл: {a[1]}", parse_mode=telegram.constants.ParseMode.HTML)
        else:
            await chat.send_message("Помилка, існування торент файлу не підтверджене. Будь ласка, напишіть @Quality2Length")
    if qd.startswith("cngseries_"):
        arg = qd.split("_")[1]
        a = ParseSFLIDVideos(arg)[0]
        pat = ParseAllTitles()
        con = ""
        season = ""
        for x in pat:
            if x[5] == a[0]:
                if not len(x[6]) == 0:
                    season = f"| {x[6]}"
                con = f"{x[1]} {season}\n{x[4]} "
                break
            else:
                con = "Відсутня прив'язка до тайтлу, назва не буде відображена."
        #print(a)
        if len(a[2]) == 0:
            capt = ""
        else:
            capt = " - " + a[2]
        msg1 = f"🖥 {con}\n\nЕпізод {a[3]}{capt}"
        await query.message.delete()
        btns = GenVideoButtons(arg)
        await chat.send_video(video=a[1], caption=msg1, reply_markup=InlineKeyboardMarkup(btns))
    if qd.startswith("v_"):
        chat = update.effective_chat
        SFileID = qd.split("_")[1]
        vid = ParseSFLIDVideos(SFileID)[0]
        pat = ParseAllTitles()
        con = ""
        season = ""
        FileID = ParseSFLIDVideos(SFileID)[0][1]
        for x in pat:
            if x[5] == vid[0]:
                if not len(x[6]) == 0:
                    season = f"| {x[6]}"
                con = f"{x[1]} {season}\n{x[4]} "
                break
            else:
                con = "Відсутня прив'язка до тайтлу, назва не буде відображена."
        if len(vid[2]) == 0:
            capt = ""
        else:
            capt = " - " + vid[2]
        msg1 = f"🖥 {con}\n\nЕпізод {vid[3]}{capt}"
        btns = GenVideoButtons(SFileID)
        await chat.send_video(video=FileID, caption=msg1, reply_markup=InlineKeyboardMarkup(btns))
    if qd == "na_revo":
        chat = update.effective_chat
        pth = Path(f"Data/Other/{donatefile}")
        with open(pth, "r") as file:
            msg = file.read()
        await query.message.delete()
        if len(msg) == 0:
            await chat.send_message("Інформація не заповнена. Зверніться до адміністраторів.", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад", callback_data="restartmenu")]]))
        else:
            await chat.send_message(msg,parse_mode=telegram.constants.ParseMode.HTML, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад", callback_data="restartmenu")]]))
    if qd == "calltogod":
        await query.message.delete()
        await chat.send_message("Маєш ідеї, пропозиції чи притензії?\n\nПиши @pan_kioto_sup і тобі допоможуть!",reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад", callback_data="restartmenu")]]))



async def SendVideo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("+")
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    SFileID = msg.text.split("_")[1]
    await msg.delete()
    vid = ParseSFLIDVideos(SFileID)[0]
    pat = ParseAllTitles()
    con = ""
    season = ""
    FileID = ParseSFLIDVideos(SFileID)[0][1]
    for x in pat:
        if x[5] == vid[0]:
            if not len(x[6]) == 0:
                season = f"| {x[6]}"
            con = f"{x[1]} {season}\n{x[4]} "
            break
        else:
            con = "Відсутня прив'язка до тайтлу, назва не буде відображена."
    if len(vid[2]) == 0:
        capt = ""
    else:
        capt = " - " + vid[2]
    msg1 = f"🖥 {con}\n\nЕпізод {vid[3]}{capt}"
    btns = GenVideoButtons(SFileID)
    await chat.send_video(video=FileID, caption=msg1, reply_markup=InlineKeyboardMarkup(btns))


async def UpdateTitleVLID(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if UserIsAdmin(user.id):
        await chat.send_message("Це інструмент зміни VLID в тайтлів")
        await chat.send_message("Щоб почати, надішли мені тайтл через @pankioto_bot Назва тайтлу",
                                reply_markup=ReplyKeyboardMarkup(k_cancel))
        return vlid_title_change
    else:
        return ConversationHandler.END


async def UpdateTitleVLID1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if len(msg.text.split("_")) <= 1:
        await chat.send_message("Щось не так! Попробуй ще раз!")
    else:
        ID = msg.text.split("_")[1]
        pt = ParseIDTitle(ID)
        if len(pt) == 0:
            await chat.send_message("Я не можу знайти цей тайтл, попробуй ще раз.")
        else:
            AddToTemp(user.id, ID)
            if not len(pt[0][5]) == 0:
                con = pt[0][5]
            else:
                con = "Відсутня"
            if len(pt[0][6]) == 0:
                season = ""
            else:
                season = pt[0][6]
            await chat.send_message(f"Тайтл: {pt[0][1]} {season}\nПрив'язка: {con}")
            await chat.send_message("Надішли мені новий VLID, до якого треба прив'язати тайтл:")

            UIDs = []
            msg = "Списки відеоплеєра:\n\n"
            mv = 1
            pv = ParseAllVideos()
            pt = ParseAllTitles()
            for x in pv:
                UIDs.extend([x[0]])
            UIDs = list(set(UIDs))
            conx = 0
            for x in UIDs:
                for x1 in pt:
                    if x == x1[5]:
                        conx = x1[1]
                        break
                    else:
                        conx = 0
                if conx == 0:
                    con = "Відсутня"
                else:
                    con = conx
                msg += f"{mv}. VLID: {x} | Прив'язка: {con}\n"
                mv += 1
            await chat.send_message(msg)

            return vlid_title_change1


async def UpdateTitleVLID2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if not CheckListVILD(msg.text):
        await chat.send_message("Списку за таким VLID не існує, попробуй ще раз")
    else:
        IDVLID = CheckListConVILD(msg.text)
        tid = UserTempTitleID(user.id)
        if not IDVLID:

            UpdateTitles(tid, "VideoPost", msg.text)
            t = ParseIDTitle(tid)[0]
            await chat.send_message(f"VLID тайтлу: \"{t[1]}\" успішно оновлено.",
                                    reply_markup=ReplyKeyboardMarkup(k_admpanel))
        else:
            await chat.send_message("Цей список вже прив'язаний, переприв'язую.")
            UpdateTitles(IDVLID, "VideoPost", "")
            UpdateTitles(tid, "VideoPost", msg.text)
            await chat.send_message("Список успішно переприв'язано до нового тайтлу.",
                                    reply_markup=ReplyKeyboardMarkup(k_player))
        RemoveTempUser(user.id)
        return ConversationHandler.END


async def UpdateVideoList(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if UserIsAdmin(user.id):
        await chat.send_message("Це інструмент оновлення списку плеєра.")
        await chat.send_message("Надішліть мені VLID:", reply_markup=ReplyKeyboardMarkup(k_cancel))

        UIDs = []
        msg = "Списки відеоплеєра:\n\n"
        mv = 1
        pv = ParseAllVideos()
        pt = ParseAllTitles()
        for x in pv:
            UIDs.extend([x[0]])
        UIDs = list(set(UIDs))
        conx = 0
        for x in UIDs:
            for x1 in pt:
                if x == x1[5]:
                    conx = x1[1]
                    break
                else:
                    conx = 0
            if conx == 0:
                con = "Відсутня"
            else:
                con = conx
            msg += f"{mv}. VLID: {x} | Прив'язка: {con}\n"
            mv += 1
        await chat.send_message(msg)
        return vlid_update
    else:
        return ConversationHandler.END


async def UpdateVideoList1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    if not CheckListVILD(msg.text):
        await chat.send_message("Такого списку не існує, попробуйте ще раз!")
        await chat.send_message("Надішліть мені VLID:")
    else:
        AddToValue(user.id, msg.text)
        print(f"TEMP: {temp_user_values}")
        await chat.send_message("VLID прийнято.")
        await chat.send_message("Надішли мені данні в такому форматі:\nFileID Назва епізоду (частина)\n\nПриклад:\n\n"
                                "HIOio1b19plsdaj31 Лікарня\n"
                                "DAoijfa33fqFAf Монолог мерця\n"
                                "gassshFEW@fesd Мертва тишина (1/2)\n"
                                "rfasdASsfffSfd Мертва тишина (2/2)", reply_markup=ReplyKeyboardMarkup(k_cancel))
        await chat.send_message("Примітка: Якщо назва епізоду відсутня, замість неї напиши 0")
        await chat.send_message("Старий VideoList:")
        pv = ParseVLIDVideos(msg.text)
        oldvl = []
        for x in pv:
            print(x)
            if len(x[2]) == 0:
                capt = " 0"
            else:
                capt = f" {x[2]}"
            oldvl.extend([f"{x[1]}{capt}"])
        msg = '\n'.join(oldvl)
        await chat.send_message(msg)
        return vlid_update1


async def UpdateVideoList2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    x1 = 0
    x2 = 0
    mv = 1
    vrpostID = UserTempValue(user.id)
    contid = CheckListConVILD(vrpostID)
    for x in msg.text.split("\n"):
        x = x.split(" ")
        """if CheckFLIDUse(x[0]):
            await chat.send_message(
                f"FileID: {x[0]}\nВже використовується! Ви не можете створити списки з однаковими FileID.")
            await chat.send_message("Виберіть інакший FileID і надішліть мені")
            x2 = 1
            break"""
        if mv == 1:
            DeleteVLID(vrpostID)
            print("DELETEVLID UPDATE")
        InitVideo(vrpostID, x[0])
        UpdateVideo(x[0], vrpostID, "Episode", mv)
        Capt = " ".join(x).split(" ")
        Capt[0] = ""
        Capt = " ".join(Capt)
        print(f"CAPT {Capt}")
        if str(Capt) == " 0":
            Capt = ""
        UpdateVideo(x[0], vrpostID, "CaptionText", Capt)
        UpdateVideo(x[0], vrpostID, "SFileID", VSTotalRandom())
        mv = mv + 1
    if x2 == 0:
        await chat.send_message(f"Чудова робота! Список обновлено! VideoListID: {vrpostID}",
                                reply_markup=ReplyKeyboardMarkup(k_player))
        UpdateTitles(contid, "VideoPost", vrpostID)
        RemoveValueUser(user.id)
        return ConversationHandler.END


async def ChangeState(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if not UserIsAdmin(user.id):
        return ConversationHandler.END
    else:
        await chat.send_message("Це інструмент зміни стану аніме.")
        await chat.send_message("Щоб змінити, надішли мені аніме через <code>@pankioto_bot</code>",
                                parse_mode=telegram.constants.ParseMode.HTML,
                                reply_markup=ReplyKeyboardMarkup(k_cancel))
        return c_s


async def ChangeState1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if len(msg.text.split("_")) <= 1:
        await chat.send_message("Щось не так! Попробуй ще раз!")
    else:
        ID = msg.text.split("_")[1]
        pt = ParseIDTitle(ID)
        print(pt)
        if len(pt) == 0:
            await chat.send_message("Я не можу знайти цей тайтл, попробуй ще раз.")
        else:
            if not len(pt[0][5]) == 0:
                con = pt[0][5]
            else:
                con = "Відсутня"
            if len(pt[0][6]) == 0:
                season = ""
            else:
                season = pt[0][6]
            if pt[0][8] is None:
                st = "Не вказаний"
            elif len(pt[0][8]) == 0:
                st = "Відсутній"
            elif pt[0][8] == "0":
                st = "⚠️ Озвучується"
            elif pt[0][8] == "1":
                st = "✅ Закінчений"
            elif pt[0][8] == "2":
                st = "❔ Онґоїнґ"
            else:
                st = f"Невідомий({pt[0][8]}"
            await chat.send_message("Надсилаю меню керування станом:", reply_markup=ReplyKeyboardMarkup(k_admpanel))
            amsg = await chat.send_message(
                f"Тайтл: {pt[0][1]} {season}\nПрив'язка: {con}\nСтан: {st}\nВибери стан, який ти хочеш присвоїти:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Закінчений", callback_data=f"cs_{ID}_1")],
                    [InlineKeyboardButton("⚠️ Озвучується", callback_data=f"cs_{ID}_0")],
                    [InlineKeyboardButton("❔ Онґоїнґ", callback_data=f"cs_{ID}_2")]
                ]))
            print(amsg.message_id)
            return ConversationHandler.END

async def ChangeCalendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if not UserIsAdmin(user.id):
        return ConversationHandler.END
    else:
        await chat.send_message("Це інструмент зміни позицій розкладу",reply_markup=ReplyKeyboardMarkup(k_cancel))
        await chat.send_message("Вибери день тижня, який бажаєш редагувати:",reply_markup=InlineKeyboardMarkup(GenCalendarInlineButtons()))
    return ccng
async def ChangeCalendarHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data.startswith("ah_cc_"):
        ud = query.data.replace("ah_", "")
        ud = ud.split('_')[1]
        print(f'UD {ud}')
        wdd = int(ud) - int(datetime.datetime.now().strftime("%w"))
        print(f"WWD: {wdd}")
        if wdd < 0:
            am = await update.effective_chat.send_message("Ти не можеш редагувати минулий день! Вибери інший день!")
            await asyncio.sleep(2)
            await am.delete()
        else:
            context.user_data['CC'] = query.data.split('_')[2]
            await context.bot.edit_message_text(f"Надішли нове значення для \"{GetWeekDay(int(ud))}\":\nПримітка: Якщо надіслати 0, ти очистиш позицію.", chat_id=update.effective_user.id, message_id=query.message.id)
            return ccng1
async def ChangeCalendar1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    print(context.args)
    print(context.user_data['CC'])
    difd = int(context.user_data.get('CC')) - int(datetime.datetime.now().strftime("%w"))
    print(f"DIFD {difd}")
    difd = datetime.datetime.now() + date.timedelta(days=difd)
    frmt = difd.strftime("%d.%m.%y")
    pc = ParseDateCalendar(frmt)
    if len(pc) == 0:
        InitCalendar(frmt)
        print("INITTIME")
    if msg.text == "0":
        UpdateCalendar(f"{frmt}", "Text", "")
        await chat.send_message("Позиція очищена!")
    else:
        UpdateCalendar(f"{frmt}", "Text", msg.text)
    UpdateCalendar(f"{frmt}", "WeekDay", context.user_data['CC'])
    await chat.send_message("Успішно змінено!",reply_markup=ReplyKeyboardMarkup(k_calendar))
    return ConversationHandler.END

async def Menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.effective_message.delete()
    p = Path("Data/Other/inline_additional_menu.png")
    a = await chat.send_message("ㅤ",reply_markup=ReplyKeyboardRemove())
    await a.delete()
    await chat.send_photo(photo=open(p,"rb"), reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Розклад виходу серій", callback_data="calendar")],
        [InlineKeyboardButton("Випадкове аніме", callback_data="ra")],
        [InlineKeyboardButton(text="Підтримати нас", callback_data="na_revo"), InlineKeyboardButton(text="Зв'язок з нами", callback_data="calltogod")],
        [InlineKeyboardButton("Вернутись в основне меню", callback_data="rtm")]
    ]))
    """[InlineKeyboardButton("Розклад виходу серій", callback_data="calendar")],
        [InlineKeyboardButton("Випадкове аніме", callback_data="ra"), InlineKeyboardButton("❌ Отримати торрент", callback_data="trnt")],
        [InlineKeyboardButton("❌ Підтримати нас", callback_data="money_cb"),InlineKeyboardButton("❌ Зв'язок з нами", callback_data="support_cb")],
        [InlineKeyboardButton("Вернутись в основне меню", callback_data="rtm")]"""
async def CalendarInfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not UserIsAdmin(user.id):
        return ConversationHandler.END
    else:
        await update.effective_chat.send_message("Що бажаєш зробити?",reply_markup=ReplyKeyboardMarkup(k_calendar))

async def ClearOldCalendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    if UserIsAdmin(user.id):
        DeleteOldCalendar()
        await chat.send_message("Календар оновлено, старі дні очищені.")

async def UpdateTitleYear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if UserIsAdmin(user.id):
        await chat.send_message("Це інструмент оновлення року тайтлу", reply_markup=ReplyKeyboardMarkup(k_cancel))
        await chat.send_message("Надішліть мені тайтл через @pankioto_bot:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Пошук", switch_inline_query_current_chat="")]
        ]))
        return upt
    else:
        return ConversationHandler.END


async def UpdateTitleYear2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    arg = msg.text.split("_")[1]
    context.user_data['tid'] = arg
    if not ParseIDTitle(arg):
        await chat.send_message("Такого тайтлу не існує не існує, попробуйте ще раз!")
    else:
        a = ParseIDTitle(arg)[0]
        if a[14] is None or a[14] == "":
            year = ""
        else:
            year = f"{a[14]}"
        await chat.send_message("Тайтл прийнято.")
        await chat.send_message(f"Тайтл: {a[1]} {a[6]} {year}")
        await chat.send_message("Надішли мені новий рік тайтлу:")
        return upt2



async def UpdateTitleYear3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    if msg.text.isdigit():
        UpdateTitles(context.user_data['tid'], "Year", msg.text)
        await chat.send_message("Рік змінено успішно!",reply_markup=ReplyKeyboardMarkup(k_advtools))
        return ConversationHandler.END
    else:
        await chat.send_message("Ти щось не те написав, попробуй ще раз")

def main():
    app = Application.builder().token(token).build()

    app.add_handler(InlineQueryHandler(inline_query))

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Regex("❗️ Адмін панель"), adm_start))
    app.add_handler(MessageHandler(filters.Regex("В головне меню"), start_back))
    app.add_handler(MessageHandler(filters.Regex("Добавити тайтл"), add_title_pre))
    app.add_handler(MessageHandler(filters.Regex("Назад"), adm_start_back))
    app.add_handler(MessageHandler(filters.Regex("🔍 Знайти"), search_title_info))
    app.add_handler(MessageHandler(filters.Regex("Адміністратори"), AdminList))
    app.add_handler(MessageHandler(filters.Regex("💭 Інформація"), Information))
    app.add_handler(MessageHandler(filters.Regex("Список тайтлів"), TitleList))
    app.add_handler(MessageHandler(filters.Regex("Плеєр"), playerinfo))
    app.add_handler(MessageHandler(filters.Regex("Список по VLID"), VideoList))
    app.add_handler(MessageHandler(filters.Regex("Календар"), CalendarInfo))
    app.add_handler(MessageHandler(filters.Regex("Оновити календар"), ClearOldCalendar))
    app.add_handler(MessageHandler(filters.Regex("Додаткові інструменти"), addtoolsinfo))
    app.add_handler(MessageHandler(filters.Regex("Інструменти редагування"), replaceinfo))
    #CMD
    app.add_handler(CommandHandler("menu", Menu))
    #app.add_handler(MessageHandler(filters.ALL, test))

    # CONV
    app.add_handler(add_title_conv)
    app.add_handler(del_title_conv)
    app.add_handler(add_videolist_conv)
    app.add_handler(del_videolist_conv)
    app.add_handler(upd_titlevlid_conv)
    app.add_handler(update_videolist_conv)
    app.add_handler(upd_info_conv)
    app.add_handler(c_s_conv)
    app.add_handler(cc_conv)
    app.add_handler(ct_conv)
    app.add_handler(get_url_conv)
    app.add_handler(cy_conv)
    app.add_handler(replace_money_conv)
    # FileID
    app.add_handler(MessageHandler(filters.VIDEO, FileID))
    # Alternative handlers
    app.add_handler(MessageHandler(filters.Regex("^/search_(\w+)$"), search_title))
    app.add_handler(MessageHandler(filters.Regex("^/video_(\w+)$"), SendVideo))
    app.add_handler(MessageHandler(filters.Regex("^/series_(\w+)$"), SeriesList))
    app.add_handler(CallbackQueryHandler(CallbackQuery))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    if startdbs():
        main()
