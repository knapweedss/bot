import telebot  # импортируем модуль pyTelegramBotAPI
import conf     # импортируем наш секретный токен

telebot.apihelper.proxy = conf.PROXY
bot = telebot.TeleBot(conf.TOKEN)  # создаем экземпляр бота

import create_markov_model
import model_learn
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет, я бот-ассистент, "
                     "который попробует подсказать вам что-то "
                     "из мира лингвистики. "
                     "Просто напишите мне то, о чем вы хотите "
                     "узнать побольше (напишите слово типа русский). "
                     "Также вы можете попросить у бота совета /advise")
@bot.message_handler(commands=['advise'])
def bop(message):
    bot.send_message(message.chat.id, create_markov_model.m.make_short_sentence(100))

# этот обработчик реагирует на любое сообщение
@bot.message_handler(func=lambda m: True)
def news_len(message):
    try:
        bot.send_message(message.chat.id, model_learn.pipe.predict([message.text.lower()])[0])
    except Exception:
        bot.send_message(message.chat.id, 'попробуйте другое слово, такому меня не научили:(')

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
