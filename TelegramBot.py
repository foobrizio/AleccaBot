import telebot
from telebot.types import *
import Consts

from bot.BotFunctions import BotFunctions as bf
from bot.SubscriptionManager import SubscriptionManager

bot = telebot.TeleBot(Consts.bot_token, threaded=False)
bf.set_default_commands(bot)
bf.load_modules(bot=bot)
sub_mgr = SubscriptionManager()


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    hello_message = "Ciao "+message.from_user.first_name+". Come va?"
    bf.send_message(event=None,
                    bot=bot,
                    chat_id=message.from_user.id,
                    message=hello_message)


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
        bot.reply_to(message, "Perfetto, "+name+". Da ora riceverai aggiornamenti su "+subscription_name)
    else:
        bot.reply_to(message, "Sei già iscritto")


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    chat_id = message.from_user.id
    if sub_mgr.has_running_elements(chat_id):
        elements = sub_mgr.get_running_elements(chat_id)
        buttons = ReplyKeyboardMarkup(one_time_keyboard=True, selective=True)
        if len(elements) > 1:
            # We have to let the user choose which subscription to cancel
            for elem in elements:
                name = elem[0]
                buttons.add(InlineKeyboardButton(text=name, callback_data=name))
            buttons.row_width = 2
            bot.send_message(chat_id=chat_id,
                             text="Quale sottoscrizione vuoi annullare?",
                             reply_markup=buttons)
            bot.register_next_step_handler(message=message, callback=unsubscribe_callback)
        else:
            thread_name = elements[0][0]
            bot.send_message(chat_id=chat_id,
                             text="Stai annullando la sottoscrizione "+thread_name)
            sub_mgr.stop_thread(chat_id=chat_id, thread_name=thread_name)
            bot.reply_to(message, "Operazione completata. Da ora non riceverai più aggiornamenti su "+thread_name)
    else:
        bot.reply_to(message, "Attualmente non hai nessuna sottoscrizione")


@bot.callback_query_handler(func=lambda callback: True)
def unsubscribe_callback(callback):
    chat_id = callback.from_user.id
    thread_to_stop = callback.text
    result = sub_mgr.stop_thread(chat_id=chat_id, thread_name=thread_to_stop)
    if result:
        bot.send_message(chat_id=chat_id,
                         text="Operazione completata. Da ora non riceverai più aggiornamenti su " + thread_to_stop,
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id=chat_id,
                         text="Operazione non riuscita!!",
                         reply_markup=ReplyKeyboardRemove())
# endregion


bot.infinity_polling()
