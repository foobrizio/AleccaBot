import telebot
import Consts
from telegram.ext import ApplicationBuilder

from assicurazione.CheckAssicurazione import CheckAssicurazione

bot = telebot.TeleBot(Consts.bot_token)
print(Consts.bot_token)



@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, "Ciao "+message.from_user.first_name+". Come va?")


@bot.message_handler(commands=['subscribe_assicurazione'])
def subscribe_to_assicurazione(message):
    name = message.from_user.first_name
    chat_id = message.from_user.id
    bot.reply_to(message, "Perfetto. Da ora riceverai aggiornamenti sulla tua assicurazione")
    builder = ApplicationBuilder().job_queue()


@bot.message_handler(commands=['unsubscribe_assicurazione'])
def unsubscribe_from_assicurazione(message):
    bot.reply_to(message, "Come vuoi. Da ora non riceverai più aggiornamenti sulla tua assicurazione")


@bot.message_handler(commands=['send_assicurazione'])
def receive_send_command(message):
    chat_id = message.from_user.id
    if not is_subscribed_to_assicurazione(chat_id):
        return
    print(message)
    if CheckAssicurazione.check_da_scaricare():
        bot.reply_to(message, "Sto scaricando il nuovo file assicurazione. Pazienta qualche secondo...")
        CheckAssicurazione.download()
    send_assicurazione(chat_id)


def is_subscribed_to_assicurazione(chat_id):
    return chat_id == 128314363


def send_assicurazione(chat_id):
    file = open(Consts.document, 'rb')
    bot.send_document(chat_id=chat_id,
                      document=file)


bot.infinity_polling()
