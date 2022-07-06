import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from re import fullmatch
from yoomoney import Client, Quickpay
from datetime import datetime
from Based import Based, Intro

base = Based()
# В скобочки выше можно в кавычках написать название файла с расширением csv для bd
with open('token.txt', 'r') as f:
    token = f.readline()

client = Client(token)

bot = telebot.TeleBot('5338622440:AAG0KsPDPHg5qjF9sDOpb3TGJRcu0XnN6pE')


# Токен бота

def choose_yes_or_no(chatid: int, msgtext: str, yesbtntext: str, nobtntext: str, yesdata, nodata):
    # Макет отправки двух кнопок
    markup = InlineKeyboardMarkup()
    yesbtn = InlineKeyboardButton(yesbtntext, callback_data=yesdata)
    nobtn = InlineKeyboardButton(nobtntext, callback_data=nodata)
    markup.add(yesbtn, nobtn)
    bot.send_message(chatid, msgtext, reply_markup=markup)


def extract_magnet_type(text):
    return text.split()[1] if len(text.split()) > 1 else None


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    # Коллбэки для всех кнопок
    chatid = call.message.chat.id
    name = base.get_name(chatid)
    markup = InlineKeyboardMarkup()
    if call.data[-3:] == 'yes':
        but = InlineKeyboardButton('Да', callback_data='None')
    elif call.data[-2:] == 'no':
        but = InlineKeyboardButton('Нет', callback_data='None')
    elif call.data != 'None':
        but = call.message.reply_markup.keyboard[0][0]
    else:
        bot.answer_callback_query(call.id, 'Кнопка уже была нажата')
        return 0
    if call.data != 'cb_chk' and call.data != 'cb_35':
        bot.answer_callback_query(call.id)
        markup.add(but)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)
    match call.data:
        case 'cb_3_yes':
            claim_info(chatid)
        case 'cb_3_no':
            choose_yes_or_no(chatid, 'Возможно вы передумаете?', 'Хорошо, поделюсь', 'Нет, не передумаю',
                             'cb_4_yes', 'cb_4_no')
        case 'cb_4_yes':
            claim_info(chatid)
        case 'cb_4_no':
            interest_find(chatid)
        case 'cb_8_yes':
            claim_instr(chatid)
        case 'cb_8_no':
            interest_find(chatid)
        case 'cb_9_yes':
            bot.send_message(chatid,
                             'Записаться на консультацию можно вот тут '
                             'https://admin1.ru/director-main-intro-product-consulting15/',
                             disable_web_page_preview=True)
            time.sleep(30)
            # Таймер между 10 и 3
            claim_instr(chatid)
        case 'cb_9_no':
            time.sleep(30)
            # Таймер между 9 и 3
            claim_instr(chatid)
        case 'cb_14_yes':
            please_write_phone(chatid)
        case 'cb_14_no':
            msg = bot.send_message(chatid, 'Введите, пожалуйста, своё имя:')
            bot.register_next_step_handler(msg, name_entr)
        case 'cb_15_yes':
            msg = bot.send_message(chatid, 'Введите имя ещё раз')
            bot.register_next_step_handler(msg, name_entr)
        case 'cb_15_no':
            bot.send_message(chatid, 'Ваше имя вам решать)')
            your_name(chatid)
        case 'cb_21_yes':
            client_watched_instruction(call.message.chat.id)
        case 'cb_21_no':
            any_question(call.message.chat.id)
        case 'cb_22_yes':
            consult(chatid)
        case 'cb_22_no':
            base.nulls_links(chatid)
            bot.send_message(call.message.chat.id, f'{name}, очень жаль, имейте в виду на всякий случай!')
            circle_interest(call.message.chat.id)
        case 'cb_26_yes':
            watch_instruction(call.message.chat.id)
        case 'cb_26_no':
            circle_interest(call.message.chat.id)
        case 'cb_28_yes':
            send_instruction(chatid)
        case 'cb_28_no':
            any_question(call.message.chat.id)
        case 'cb_chk':
            try:
                operation = client.operation_history(label=str(call.message.chat.id)).operations[0]
                if operation.status == 'success' and datetime.timestamp(operation.datetime) > datetime.timestamp(
                        datetime.now()) - 172800:
                    give_item(call.message.chat.id)
                else:
                    bot.send_message(chatid, 'Операция ещё не завершилась, подождите немного и проверьте ещё раз')
            except IndexError:
                bot.send_message(chatid, 'Операция ещё не завершилась, подождите немного и проверьте ещё раз')
        case 'cb_35_yes':
            bot.send_message(chatid,
                             f'{name}, записаться на консультацию можно вот тут: https://admin1.ru/director-main-intro-product-consulting15/',
                             disable_web_page_preview=True)
            audit_offer(chatid)
        case 'cb_35_no':
            audit_offer(chatid)
        case 'cb_36_yes':
            bot.send_message(chatid, 'Благодарю за доверие! И вот ссылка на условия аудита:\n'
                                     'https://admin1.ru/director-main-intro-product-website-audit/',
                             disable_web_page_preview=True)
        case 'cb_36_no':
            time.sleep(30)
            # Таймер между 37 и 36
            audit_offer(chatid)


@bot.message_handler(commands=['start'])
def say_hello(message: telebot.types.Message):
    # 1, 2
    magnet_type = extract_magnet_type(message.text)
    chatid = message.chat.id
    base.write_new_row(chatid, magnet_type)
    bot.send_message(message.chat.id, 'Здравствуйте!')
    claim_instr(message.chat.id)


def claim_info(chatid):
    # 11
    bot.send_message(chatid,
                     'Отлично!\n Я благодарен, что вы согласились поделиться своими контактами')
    msg = bot.send_message(chatid, 'Введите пожалуйста своё имя:')
    bot.register_next_step_handler(msg, name_entr)


def claim_instr(chatid):
    # 3
    magnet_intro = base.get_magnet_intro(chatid)
    bot.send_message(chatid,
                     f'Для того, чтобы забрать видео-инструкцию {magnet_intro},'
                     f' нужно ввести свои контактные данные: Имя и телефон.')
    bot.send_message(chatid, 'Это может пригодиться если вы захотите заказать у меня бесплатную консультацию')
    choose_yes_or_no(chatid, 'Вы согласны?', 'Да', 'Нет', 'cb_3_yes', 'cb_3_no')


def peredumal_func(chk: bool, chatid):
    # 4
    if chk:
        claim_info(chatid)
    else:
        choose_yes_or_no(chatid, 'Возможно вы передумаете?', 'Хорошо, поделюсь', 'Нет, не передумаю',
                         'cb_3_yes', 'cb_4_no')


def interest_find(chatid):
    # 5, 6, 7, 8, 9
    bot.send_message(chatid, 'Очень и очень жаль =(')
    time.sleep(30)
    # Таймер между 5 и 6
    used = base.get_used(chatid)
    magnet_intro = base.get_magnet_intro(chatid)
    base.set_link_watched(chatid, magnet_intro)
    bot.send_message(chatid,
                     f'Здравствуйте!\n Пару дней назад вы хотели получить инструкцию: {magnet_intro}, '
                     f'но так и не скачали её')
    if used.count(True) == 0:
        choose_yes_or_no(chatid, f'Две другие инструкции Вас тоже не заинтересовали.'
                                 'Хотите, я Вас проконсультирую. Это БЕСПЛАТНО.'
                                 'Интересует?',
                         'Да', 'Нет', 'cb_9_yes', 'cb_9_no')
    else:
        for n, i in enumerate(used):
            if i:
                magnet_intro = Intro.all_intro.value[n]
                base.write_magnet_intro(chatid, magnet_intro)
                for j in Intro:
                    if j.value[0] == magnet_intro:
                        base.write_magnet_intro_url(chatid, j.value[1])
                choose_yes_or_no(chatid, f'Возможно вас заинтересует видео-инструкция о том, {magnet_intro}?',
                                 'Да, интересует',
                                 'Нет, не интересует', 'cb_8_yes', 'cb_8_no')
                break


def your_name(chatid):
    # 14
    choose_yes_or_no(chatid, f'Ваше имя {base.get_name(chatid)}?', 'Да', 'Нет', 'cb_14_yes', 'cb_14_no')


def name_entr(message: Message):
    # 13, 15
    base.write_name(message.chat.id, message.text)
    if fullmatch(r'^[а-яА-ЯёЁa-zA-Z]+ ?[а-яА-ЯёЁazA-Z]+ ?[а-яА-ЯёЁa-zA-Z]', message.text):
        your_name(message.chat.id)
    else:
        choose_yes_or_no(message.chat.id,
                         'Имя введено неверно. Используйте только русские или'
                         ' латинские буквы и не более 3 слов(ФИО).\nПовторим ввод имени?',
                         'Да, повторим', 'Нет', 'cb_15_yes', 'cb_15_no')


def please_write_phone(chatid):
    # 17
    msg = bot.send_message(chatid,
                           f'{base.get_name(chatid)}, очень приятно!\nВведите пожалуйста свой'
                           f' контактный номер телефона в формате +79219114848')
    bot.register_next_step_handler(msg, phone_entr)


def phone_entr(message: Message):
    # 18, 19
    magnet_intro, magnet_intro_url, name = base.get_magnet_intro(message.chat.id), base.get_magnet_intro_url(
        message.chat.id), base.get_name(message.chat.id)
    if fullmatch(r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$', message.text):
        base.write_phone(message.chat.id, message.text)
        watch_instruction(message.chat.id)
    else:
        msg = bot.send_message(message.chat.id, f'{name}, телефон {message.text} не верный, повторите ввод.')
        bot.register_next_step_handler(msg, phone_entr)


def watch_instruction(chatid):
    # 20, 21
    magnet_intro, magnet_intro_url = base.get_magnet_intro(chatid), base.get_magnet_intro_url(chatid)
    bot.send_message(chatid,
                     f'Супер!\nМожете посмотреть видео-инструкцию {magnet_intro} по ссылке {magnet_intro_url}',
                     disable_web_page_preview=True)
    base.write_magnit(chatid)
    time.sleep(10)
    # таймер между 20 и 21
    choose_yes_or_no(chatid, f'{base.get_name(chatid)}, удалось ли вам посмотреть эту инструкцию?', 'Да', 'Нет',
                     'cb_21_yes', 'cb_21_no')


def client_watched_instruction(chatid):
    # 27,
    bot.send_message(chatid, f'Отлично, {base.get_name(chatid)}!\nНадеюсь вам понравилось)!')
    time.sleep(3)
    # Таймер между 27 и 28
    possible_interest(chatid)


def possible_interest(chatid):
    # 28
    choose_yes_or_no(chatid,
                     'Возможно вас заинтересует инструкция о том, как буквально за 10'
                     ' минут можно найти ошибки на своём сайте и проверить своего SEO'
                     ' специалиста или подрядчика. Вам интересно посмотреть эту инструкцию?',
                     'Да, интересно', 'Нет, не интересно', 'cb_28_yes', 'cb_28_no')


def any_question(chatid):
    # 22
    choose_yes_or_no(chatid, 'Если остались вопросы, я могу вас проконсультировать. Это бесплатно. Вам это интересно?',
                     'Да', 'Нет', 'cb_22_yes', 'cb_22_no')


def circle_interest(chatid):
    # 24, 25, 26
    time.sleep(30)
    # Таймер между 23 и 24
    used = base.get_used(chatid)
    magnet_intro = base.get_magnet_intro(chatid)
    base.set_link_watched(chatid, magnet_intro)
    bot.send_message(chatid,
                     f'Здравствуйте!\nПару дней назад вы хотел получить инструкцию:'
                     f'{magnet_intro}, но так и не скачали её')

    if used.count(True) == 0:
        possible_interest(chatid)
    else:
        for n, i in enumerate(used):
            if i:
                magnet_intro = Intro.all_intro.value[n]
                base.write_magnet_intro(chatid, magnet_intro)
                for j in Intro:
                    if j.value[0] == magnet_intro:
                        base.write_magnet_intro_url(chatid, j.value[1])
                choose_yes_or_no(chatid, f'Возможно вас заинтересует видео-инструкция о том, {magnet_intro}?',
                                 'Да, интересует',
                                 'Нет, не интересует', 'cb_26_yes', 'cb_26_no')
                break


def consult(chatid):
    # 29
    bot.send_message(chatid,
                     f'{base.get_name(chatid)}, записаться на консультацию можно вот'
                     f' тут https://admin1.ru/director-main-intro-product-consulting15/', disable_web_page_preview=True)
    possible_interest(chatid)


def send_instruction(chatid):
    # 30, 32, 34
    bot.send_message(chatid, f'{base.get_name(chatid)}, благодарю за проявленный интерес! Вот ссылка на инструкцию\n'
                             f'https://admin1.ru/director-tripwire-intro-check-seo_TG/', disable_web_page_preview=True)
    time.sleep(30)
    # Таймер между 34 и 35
    bot.send_message(chatid, 'Оплатить доступ к инструкции по проверке своего SEO специалиста')
    quickpay = Quickpay(receiver="4100117787586620", quickpay_form='shop', paymentType='SB', sum=2,
                        targets='Инструкция', label=str(chatid))
    markup = InlineKeyboardMarkup(row_width=2)
    chkbtn = InlineKeyboardButton('Проверить оплату', callback_data='cb_chk')
    markup.add(chkbtn)
    bot.send_message(chatid, f'{quickpay.base_url}', reply_markup=markup)


def give_item(chatid):
    # 35
    base.write_payment(chatid)
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chatid,
                     'Благодарю за приобретение инструкции!\nПо этой ссылке вы можете ею вопользоваться:\n'
                     'https://admin1.ru/director-tripwire-product-check-seo', reply_markup=markup,
                     disable_web_page_preview=True)
    time.sleep(30)
    # markup = InlineKeyboardMarkup(row_width=2)
    # chkbtn = InlineKeyboardButton('Да, нужна консультация', callback_data='cb_35')
    # markup.add(chkbtn)
    # bot.send_message(chatid, f'По инструкции остались вопросы или нужна консультация?', reply_markup=markup)
    choose_yes_or_no(chatid, 'По инструкции остались вопросы или нужна консультация?', 'Да, нужна консультация',
                     'Нет, не нужна', 'cb_35_yes', 'cb_35_no')


def audit_offer(chatid):
    # 36
    base.write_link_sended(chatid)
    choose_yes_or_no(chatid,
                     'Хотите я сделаю аудит сайта за вас, а из стоимости вычту деньги, потраченные вами на покупку'
                     ' инструкции?!', 'Да, хочу', 'Нет, не хочу', 'cb_36_yes', 'cb_36_no')


bot.infinity_polling()
