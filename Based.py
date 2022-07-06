from time import sleep
import pandas as pd
from datetime import datetime
from enum import Enum
import pandas.core.series


class Intro(Enum):
    # Названия магнитов и ссылки на них
    traffic = ['\"Как узнать посещаемость любого сайта конкурента\"', 'https://admin1.ru/director-magnet-intro-traffic']
    context = ["\"Как шпионить за контекстной рекламой конкурента и по каким фразам он продвигается в SEO\"",
               "https://admin1.ru/director-magnet-intro-context-keys-audit"]
    google = ["\"Как заставить Google следить за вашими конкурентами\"", "https://admin1.ru/director-magnet-intro-google-alerts"]
    all_intro = [traffic[0], context[0], google[0]]
    all_links = [traffic[1], context[1], google[1]]


class Based:
    # Класс с функциями для записи в базу данных
    def __init__(self, filename='users.csv'):
        self.filename = filename
        self.sheet = pd.read_csv(filename)
        self.sheet = self.sheet.set_index('chat_id')
        self.link_match = {Intro.traffic.value[0]: 'intro-traffic', Intro.context.value[0]: 'context-keys-audit',
                           Intro.google.value[0]: 'google-alerts'}

    def write_new_row(self, chat_id, link_type):
        self.sheet.drop(chat_id, errors='ignore', inplace=True)
        self.sheet = pd.concat([self.sheet,
                                pd.DataFrame([[chat_id, str(datetime.now().date()), str(datetime.now().time())]],
                                             columns=['chat_id', 'date', 'time']).set_index('chat_id')])
        self.write_link(chat_id, link_type)
        self.save()

    def write_link(self, chat_id, link_type):
        match link_type:
            case "director-magnet-intro-traffic":
                self.write_magnet_intro(chat_id, Intro.traffic.value[0])
                self.write_magnet_intro_url(chat_id, Intro.traffic.value[1])
                self.sheet.loc[chat_id, 'intro'] = Intro.traffic.value[1]

            case "director-magnet-intro-context-keys-audit":
                self.write_magnet_intro(chat_id, Intro.context.value[0])
                self.write_magnet_intro_url(chat_id, Intro.context.value[1])
                self.sheet.loc[chat_id, 'audit'] = Intro.context.value[1]

            case "director-magnet-intro-google-alerts":
                self.write_magnet_intro(chat_id, Intro.google.value[0])
                self.write_magnet_intro_url(chat_id, Intro.google.value[1])
                self.sheet.loc[chat_id, 'alerts'] = Intro.google.value[1]

            case _:
                self.write_magnet_intro(chat_id, Intro.traffic.value[0])
                self.write_magnet_intro_url(chat_id, Intro.traffic.value[1])
                self.sheet.loc[chat_id, 'intro'] = Intro.traffic.value[1]

        self.save()

    def write_magnet_intro(self, chat_id, intro):
        self.sheet.loc[chat_id, 'use_intro'] = intro
        self.save()

    def write_magnet_intro_url(self, chat_id, url):
        self.sheet.loc[chat_id, 'use_url'] = url
        match url:
            case 'https://admin1.ru/director-magnet-intro-traffic':
                self.sheet.loc[chat_id, 'intro'] = url
            case "https://admin1.ru/director-magnet-intro-context-keys-audit":
                self.sheet.loc[chat_id, 'audit'] = url
            case "https://admin1.ru/director-magnet-intro-google-alerts":
                self.sheet.loc[chat_id, 'alerts'] = url

        self.save()

    def write_name(self, chat_id, name):
        self.sheet.loc[chat_id, 'name'] = name
        self.save()

    def write_phone(self, chat_id, phone):
        self.sheet.loc[chat_id, 'phone'] = str(phone)
        self.save()

    def write_magnit(self, chat_id):
        self.sheet.loc[chat_id, 'watched'] = 'Магнит просмотрен'
        self.save()

    def write_payment(self, chat_id):
        self.sheet.loc[chat_id, 'payed'] = 'tripwire оплачен'
        self.save()

    def write_link_sended(self, chat_id):
        self.sheet.loc[chat_id, 'sended'] = 'ссылка на аудит отправлена'
        self.save()

    def set_link_watched(self, chat_id, intro):
        self.write_link(chat_id, self.link_match[intro])
        self.save()

    def nulls_links(self, chat_id):
        self.sheet.loc[chat_id, 'intro'] = None
        self.sheet.loc[chat_id, 'audit'] = None
        self.sheet.loc[chat_id, 'alerts'] = None
        self.write_magnet_intro_url(chat_id, self.sheet.loc[chat_id, 'use_url'])
        self.save()

    def get_name(self, chat_id):
        return self.sheet.loc[chat_id, 'name']

    def get_magnet_intro(self, chat_id):
        return self.sheet.loc[chat_id, 'use_intro']

    def get_magnet_intro_url(self, chat_id):
        return self.sheet.loc[chat_id, 'use_url']

    def get_used(self, chat_id):
        return list(self.sheet.loc[chat_id].iloc[2:5].isna().values)

    def save(self):
        self.sheet.to_csv('users.csv', mode='w')
