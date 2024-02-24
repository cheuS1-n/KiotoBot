from telegram.ext import filters, MessageHandler, ConversationHandler, CallbackQueryHandler

from main import AddVideoList, AddVideoList1, add_video, DeleteVideoList, DeleteVideoList1, del_vl
from main import ChangeCalendar, ChangeCalendarHandler, ChangeCalendar1, ccng, ccng1
from main import ChangeState, ChangeState1
from main import ReplaceInfo, ReplaceInfo1, replace_info
from main import UpdateTitleVLID2, vlid_title_change, UpdateTitleVLID, UpdateTitleVLID1, vlid_title_change1
from main import UpdateTitleYear, UpdateTitleYear2, UpdateTitleYear3, upt, upt2
from main import UpdateVideoList, UpdateVideoList1, UpdateVideoList2, vlid_update, vlid_update1
from main import add_title_s, add_title_s1, add_title_s2, add_title_s3, add_title_s4, add_title_s5, add_title_s6, \
    add_title_s7, add_title_s8, add_title_s9, add_title_s10, add_title_s11, add_title_s13, add_title_s14, \
    add_title_standart14, rmoney, ReplaceMoney, ReplaceMoney1
from main import add_title_standart, add_title_standart1, add_title_standart2, add_title_standart3, add_title_standart4, \
    add_title_standart5, add_title_standart6, add_title_standart7, add_title_standart8, add_title_standart9, \
    add_title_standart10, add_title_standart11, add_title_standart12, add_title_standart13
# froma main import
from main import adm_start_back, undone_add_title, delete_titles, delete_titles1, del_title_s
from main import getURL, getURL1
from main import trnteditf, trnteditf1, trnteditf2, trntedit, trntedit1

"""conv_sub_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Підписатись на розсилку'), callback=sub)],
    states={
        SUB: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.ALL), callback=sub2)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=cancel_conv)],
    )"""

add_title_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("Стандартне додавання"), callback=add_title_standart)],
    states = {
    add_title_s: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT, add_title_standart1)],
    add_title_s1: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT, add_title_standart2)],
    add_title_s2: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT, add_title_standart3)],
    add_title_s3: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT, add_title_standart4)],
    add_title_s4: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT , add_title_standart5)],
    add_title_s5: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT, add_title_standart6)],
    add_title_s6: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT, add_title_standart7)],
    add_title_s7: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.PHOTO, add_title_standart8)],
    add_title_s8: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT, add_title_standart9)],
    add_title_s9: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT, add_title_standart10)],
    add_title_s10: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT, add_title_standart11)],
    add_title_s11: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.TEXT, add_title_standart12)],
    add_title_s13: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.ALL, add_title_standart13)],
    add_title_s14: [MessageHandler(~filters.Regex("❌ Скасувати") & filters.ALL, add_title_standart14)],


    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), undone_add_title)]
)

del_title_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Видалити тайтл'), callback=delete_titles)],
    states={
        del_title_s: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=delete_titles1)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    )

add_videolist_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Добавити список'), callback=AddVideoList)],
    states={
        add_video: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=AddVideoList1)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    )
del_videolist_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Видалити список'), callback=DeleteVideoList)],
    states={
        del_vl: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=DeleteVideoList1)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    )

upd_titlevlid_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Редагувати VLID тайтлу'), callback=UpdateTitleVLID)],
    states={
        vlid_title_change: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=UpdateTitleVLID1)],
        vlid_title_change1: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=UpdateTitleVLID2)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    )

update_videolist_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Редагувати VideoList'), callback=UpdateVideoList)],
    states={
        vlid_update: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=UpdateVideoList1)],
        vlid_update1: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=UpdateVideoList2)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    )

upd_info_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Редагувати інформацію'), callback=ReplaceInfo)],
    states={
        replace_info: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=ReplaceInfo1)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    )
c_s_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Зміна стану тайтлу'), callback=ChangeState)],
    states={
        replace_info: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=ChangeState1)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    per_user=True
    )
cc_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Зміна інформації календаря'), callback=ChangeCalendar)],
    states={
        ccng: [CallbackQueryHandler(ChangeCalendarHandler)],
        ccng1: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=ChangeCalendar1)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    per_user=True
    )
ct_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Торрент редагування'), callback=trnteditf)],
    states={
        trntedit: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=trnteditf1)],
        trntedit1: [MessageHandler(filters.ATTACHMENT, callback=trnteditf2)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    per_user=True
    )
get_url_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Отримати посилання'), callback=getURL)],
    states={
        replace_info: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=getURL1)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    per_user=True
    )
cy_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Змінити рік'), callback=UpdateTitleYear)],
    states={
        upt: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=UpdateTitleYear2)],
        upt2: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=UpdateTitleYear3)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    per_user=True
    )
replace_money_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Редагувати "Підтримати нас"'), callback=ReplaceMoney)],
    states={
        rmoney: [MessageHandler(~filters.Regex("❌ Скасувати") & (filters.TEXT), callback=ReplaceMoney1)]
    },
    fallbacks=[MessageHandler(filters.Regex("❌ Скасувати"), callback=adm_start_back)],
    )