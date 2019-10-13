from glob import glob
from random import choice
import logging
import telegramcalendar

from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler, Filters, CallbackQueryHandler

import sitting

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='mybot.log'
                    )


def greet_user(bot, update, user_data):  #стандартная команда старт
    text = 'Вызван /start'
    logging.info(text)
    update.message.reply_text(text, reply_markup=get_keyboard())

def get_keyboard(): #начальная клавиатура с типами номеров
    contact_button = KeyboardButton('Заказать обратный звонок', request_contact=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Одноместный номер','Двухместный номер','Полулюкс'],
                                        [contact_button],
                                    ], resize_keyboard=True
                                    )   
    return my_keyboard

def get_mykeyboard(bot, update, user_data): #реализации кнопки назад, которая возвращает к начальной клавиатуре
    text = 'Назад'
    logging.info(text)
    update.message.reply_text(text, reply_markup=get_keyboard())


def get_book():  #кнопка забронировать и назад
    my_keyboard_two = ReplyKeyboardMarkup([['Забронировать','Назад']], resize_keyboard=True)
    return my_keyboard_two


def calendar_handler(bot, update, user_data): #реализация календаря 
    update.message.reply_text("Пожалуйста, выберите дату: ",
                        reply_markup=telegramcalendar.create_calendar())

def inline_handler(bot, update, user_data): #реализация календаря 
    selected,date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        bot.send_message(chat_id=update.callback_query.from_user.id,
                        text="Вы выбрали дату %s" % (date.strftime("%d/%m/%Y")),
                        reply_markup=ReplyKeyboardRemove())


def get_contact(bot,update,user_data): 
    print(update.message.contact)
    update.message.reply_text('Спасибо, {}.'.format(update.message.chat.first_name),reply_markup = get_keyboard())



def send_signle_room_picture(bot, update, user_data): #картинки для одноместного номера
    signle_list = glob('room/signle/SO*.jp*g')
    for signle_pic in signle_list:
        bot.send_photo(chat_id=update.message.chat.id, photo=open(signle_pic, 'rb'), reply_markup=get_book())

def send_double_room_picture(bot, update, user_data): #картинки для двухместного номера
    double_list = glob('room/double/SO*.jp*g')
    for double_pic in double_list:
        bot.send_photo(chat_id=update.message.chat.id, photo=open(double_pic, 'rb'), reply_markup=get_book()) 

def send_suite_room_picture(bot, update, user_data): #картинки для номера люкс
    suite_list = glob('room/suite/SO*.jp*g')
    for suite_pic in suite_list:
        bot.send_photo(chat_id=update.message.chat.id, photo=open(suite_pic, 'rb'), reply_markup=get_book())



def main():
    mybot = Updater(setting.API_KEY, request_kwargs=PROXY)
    
    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start',greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('signle',send_signle_room_picture, pass_user_data=True))
    dp.add_handler(CommandHandler('double',send_double_room_picture, pass_user_data=True))
    dp.add_handler(CommandHandler('suite',send_suite_room_picture, pass_user_data=True))
    dp.add_handler(CommandHandler("calendar",calendar_handler, pass_user_data=True ))
    dp.add_handler(CommandHandler('back', get_mykeyboard, pass_user_data=True))


    dp.add_handler(RegexHandler('^(Одноместный номер)$', send_signle_room_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Двухместный номер)$', send_double_room_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Полулюкс)$', send_suite_room_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Забронировать)$', calendar_handler, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Назад)$', get_mykeyboard, pass_user_data=True))



    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))


    dp.add_handler(CallbackQueryHandler(inline_handler, pass_user_data=True)) #выводит ответ, при выборе даты в календаре

    
    
    
    mybot.start_polling()
    mybot.idle()


main()