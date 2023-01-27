import telebot 
from telebot import types
from parsing import main , today
import json
from os.path import exists

tokken = "5810471871:AAGlkgz2xdwodQvlrUC80XWp-whMIuXbVTA"

bot =telebot.TeleBot(tokken)



def get_keyboard()-> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    with open('news_{today}.json', 'r') as file:
        for number , news in enumerate(json.load(file)):
            keyboard.add(
                types.InlineKeyboardButton(
                    text= news['title'],
                    callback_data = str(number)
                    
                )
            )
        return keyboard


@bot.message_handler(commands=['start', 'stop'])
def start_bot(message:types.Message):
    main()
    bot.send_message(message.chat.id, f"Hello,{message.from_user.full_name}! Here news for you.", reply_markup=get_keyboard())
    if not exists(f'news_{today}.json'):
        main()

@bot.callback_query_handler(func=lambda callback:True)
def send_news_details(callback: types.CallbackQuery):
    with open('news_{today}.json', 'r') as file:
        news = json.load(file)[int(callback.data)]
        text = f"{news['title']}\n{news['description']}\n\n{news['news_link']}"
        bot.send_message(
            callback.message.chat.id,
            text = text
        )

bot.polling()

# TODO: Поправить создание файла
# TODO: При нажатий на кнопку выход должен отпрвить сообщение до свидание 