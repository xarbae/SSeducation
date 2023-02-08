from webbrowser import get
import telebot
import get_data as gd
import tester as ts


bot = telebot.TeleBot('6006366855:AAHqzmS3VLErV5YuSpRVzWjVGW75iEs0bko')
global categories, test_data, test_num, mark, cur_cat, cur_theme
categories = gd.load_data()
test_data = ts.load_data()
cur_cat = cur_theme = test_num = mark = 0


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global categories, test_data, test_num, mark, cur_cat, cur_theme
    help_message = "{ Система обучения по обществознанию }" \
        " \n ! Проект помогает учащимся найти и выучить термины по многим разделам курса" \
        " \n Для того чтобы получить информацию введите слово /info" \
        " \n Для того чтобы проверить свои знания введите слово /test"

    if str(message.text).lower() == "привет":
        bot.send_message(
            message.from_user.id, "Привет! Я - твой проводник в предмет обществознание. Чтобы узнать термины введите команду /info Чтобы проверить свои знания введите /test")
    elif cur_cat == -1:

        if str(message.text).isdigit():
            cur_cat = int(message.text)
            str1 = gd.get_sub_categories(categories, cur_cat)
            cur_theme = -1
            bot.send_message(
                message.from_user.id, str1)
        else:
            bot.send_message(
                message.from_user.id, "не верно введен номер раздела")
    elif cur_theme == -1:
        if str(message.text).isdigit():
            cur_theme = int(message.text)
            data = gd.get_desc(categories, cur_cat, cur_theme)
            cur_cat = 0
            cur_theme = 0
            str1 = f"{data} \n {help_message}"
            bot.send_message(
                message.from_user.id, str1)
        else:
            bot.send_message(
                message.from_user.id, "не верно введен номер темы")
    elif test_num > 0:
        cur_cat = 0
        cur_theme = 0
        if str(message.text).isdigit():
            mark += ts.check_answer(test_data, test_num - 1, int(message.text))
            if test_num < len(test_data):
                str1 = ts.get_question(test_data, test_num)
                bot.send_message(
                    message.from_user.id, str1)
                test_num += 1
            else:
                test_num = 0
                str1 = f"Вы ответили на {mark} вопросов из {len(test_data)} \n {help_message}"
                bot.send_message(
                    message.from_user.id, str1)
        else:
            bot.send_message(
                message.from_user.id, "не верно введен ответ на вопрос (должна быть цифра)")
    elif str(message.text).lower() == "/info":
        cur_cat = -1
        str1 = gd.get_categories(categories)
        bot.send_message(
            message.from_user.id, str1)
    elif str(message.text).lower() == "/test":
        str1 = ts.get_question(test_data, test_num)
        cur_cat = 0
        cur_theme = 0
        test_num = 1
        mark = 0
        bot.send_message(
            message.from_user.id, str1)
    elif str(message.text).lower() == "/help":
        bot.send_message(
            message.from_user.id, help_message)
    else:
        bot.send_message(message.from_user.id, "Для информации введите /help.")


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
