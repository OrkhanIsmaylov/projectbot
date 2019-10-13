import logging
import os

from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

from glob import glob
from random import choice
import time




def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)


def send_room_picture(bot, update,user_data):
    cat_list = glob('Room1/SO*jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id = update.message.chat.id, photo=open(cat_pic,'rb'), reply_markup = get_keyboard())