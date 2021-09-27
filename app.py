import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CriptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<кол-во переводимой валюты>\
\n-------------------------------------------\
\nЧтобы увидить список всех доступных валют введите команду: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    count = 1
    text = 'Доступные валюты:\n---------------------------------'
    for key in keys.keys():
        text = f'\n{count})'.join((text, key, ))
        count += 1
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException('Слишком много параметров!')

        quote, base, amount = values

        total_base = CriptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} составляет: {total_base*float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()
