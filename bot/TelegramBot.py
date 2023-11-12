import telebot
from telebot.types import *
import Consts

from BotFunctions import BotFunctions as bf
from bot.SubscriptionManager import SubscriptionManager

bot = telebot.TeleBot(Consts.bot_token, threaded=False)
bf.set_default_commands(bot)
sub_mgr = SubscriptionManager()


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    print(message)
    hello_message = "Ciao "+message.from_user.first_name+". Come va?"
    bf.send_message(bot=bot,
                    chat_id=message.from_user.id,
                    message=hello_message)
    #bot.reply_to(message, "Ciao "+message.from_user.first_name+". Come va?")


# region THREAD SUBSCRIPTION

@bot.message_handler(commands=['subscribe_test'])
def subscribe_to_test(message):
    subscription_name = "Test"
    name = message.from_user.first_name
    chat_id = message.from_user.id
    if not sub_mgr.is_subscribed(chat_id, subscription_name):
        sub_mgr.start_thread(chat_id=chat_id,
                                    name=subscription_name,
                                    target=bf.send_message,
                                    args=(bot, chat_id, "Questo è un test"))
        bot.reply_to(message, "Perfetto, "+name+". Da ora riceverai aggiornamenti sulla tua assicurazione")
    else:
        bot.reply_to(message, "Sei già iscritto")


@bot.message_handler(commands=['subscribe_assicurazione'])
def subscribe_to_assicurazione(message):
    subscription_name = "Assicurazione"
    name = message.from_user.first_name
    chat_id = message.from_user.id
    if not sub_mgr.is_subscribed(chat_id, subscription_name):
        #threading.Thread(target=send_message, args=(chat_id, "Prova"), daemon=True).start()
        sub_mgr.start_thread(chat_id=chat_id,
                                    name=subscription_name,
                                    target=bf.check_assicurazione,
                                    args=(bot, chat_id))
        bot.reply_to(message, "Perfetto, "+name+". Da ora riceverai aggiornamenti sulla tua assicurazione")
    else:
        bot.reply_to(message, "Sei già iscritto")


# endregion


# TODO: Set the two buttons for the user and capture the answer
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    chat_id = message.from_user.id
    if sub_mgr.has_running_elements(chat_id):
        elements = sub_mgr.get_running_elements(chat_id)
        print(elements)
        if len(elements) > 1:
            # We have to let the user choose which subscription to cancel
            buttons = ReplyKeyboardMarkup(one_time_keyboard=True, selective=True)
            #for elem in elements:
            #    buttons.add(InlineKeyboardButton(text=elem[0]))

            buttons.row_width = 2
            button1 = InlineKeyboardButton(text="/New_settings", callback_data="test")
            button2 = InlineKeyboardButton(text="/Old_settings", callback_data="test")
            buttons.add(button1, button2)
            bot.send_message(chat_id=chat_id,
                             text="Quale sottoscrizione vuoi annullare?",
                             reply_markup=buttons)

        sub_mgr.stop_thread(chat_id=chat_id, thread_name="test")
        bot.reply_to(message, "Come vuoi. Da ora non riceverai più aggiornamenti sul test")
    else:
        bot.reply_to(message, "Non sei iscritto")


# Start the bot polling in a separate thread
bot.infinity_polling()
