import telebot
from telebot import types
from config import TOKEN, keys
from extensions import APIException, CryptoConverter
from decimal import Decimal



bot = telebot.TeleBot(TOKEN)


#приветствие
@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    if message.from_user.last_name != None:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!')
    else:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')



# команда меню
@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду в следующем формате через пробел:\nимя валюты, \
в какую валюту перевести, \
количество переводимой валюты \nНапример: биткоин доллар 1\nУвидеть список всех доступных валют: /values')
    bot.reply_to(message, text)


#вывод доступных валют
@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))

    bot.reply_to(message, text)#вывод доступных валют


# конвертация валюты, подсчет и вывод
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Слишком мало/много параметров.\nпомощь /help')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')

    else:
        num = Decimal(total_base) * Decimal(amount)
        rounded_amount = num.quantize(Decimal('0.0000000'))
        text = f'Цена {amount} {quote} в {base} - {rounded_amount}'
        bot.send_message(message.chat.id, text)






bot.polling(non_stop=True)
