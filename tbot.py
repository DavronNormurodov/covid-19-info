import requests
import csv
import telebot
from telebot import types
from datetime import datetime
url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
response_confirmed = requests.get(url_confirmed)
response_recovered = requests.get(url_recovered)
response_deaths = requests.get(url_deaths)
with open("confirmed.csv", "w+") as fail:
    writer = csv.writer(fail)
    for line in response_confirmed.iter_lines():
        writer.writerow(line.decode('utf-8').split(','))

with open("recovered.csv", 'w', encoding='utf-8') as fail:
    writer = csv.writer(fail)
    for line in response_recovered.iter_lines():
        writer.writerow(line.decode('utf-8').split(','))

with open("deaths.csv", "w+") as fail:
    writer = csv.writer(fail)
    for line in response_deaths.iter_lines():
        writer.writerow(line.decode('utf-8').split(','))
with open("confirmed.csv", "r") as f:
    reader = csv.DictReader(f)
    headers_confirmed = reader.fieldnames

with open("deaths.csv", "r") as f:
    reader = csv.DictReader(f)
    headers_deaths = reader.fieldnames

with open("recovered.csv", "r") as f:
    reader = csv.DictReader(f)
    headers_recovered = reader.fieldnames



COUNTRY = ""
COUNTRY_UZ = ""
dict_country_name = {}
list_c_n_uzbek = []
list_c_n_english = []
with open("cn_uzb.csv", "r") as f:
    file = csv.DictReader(f, delimiter=",")
    for row in file:
       list_c_n_uzbek.append(row["davlat"])

with open("cn_eng.csv", "r") as f:
    file = csv.DictReader(f, delimiter=",")
    for row in file:
        list_c_n_english.append(row["country"])

for i, x in enumerate(list_c_n_uzbek):
    dict_country_name[x] = list_c_n_english[i]



TOKEN = "1133639550:AAEGH_EyikzdP8bTldOuA48by5tz7u58bY8"
bot = telebot.TeleBot(token=TOKEN)
WHERE_IS_USER = ""
COUNTRY_IN_KEY = False
COUNTRY_IN_VALUES = False
l_user = {}
DATA_CONFIRMED = headers_confirmed[len(headers_confirmed)-1]
DATA_DEATHS = headers_deaths[len(headers_deaths)-1]
DATA_RECOVERED = headers_recovered[len(headers_recovered)-1]

DATA_INFO_CONFIRMED = "{}/{}/{}".format(DATA_CONFIRMED.split('/')[1], DATA_CONFIRMED.split('/')[0], DATA_CONFIRMED.split('/')[2])
DATA_INFO_DEATHS = "{}/{}/{}".format(DATA_DEATHS.split('/')[1], DATA_DEATHS.split('/')[0], DATA_DEATHS.split('/')[2])
DATA_INFO_RECOVERED = "{}/{}/{}".format(DATA_RECOVERED.split('/')[1], DATA_RECOVERED.split('/')[0], DATA_RECOVERED.split('/')[2])

""" to send news users"""
# with open("user.csv", "r") as f:
#     file = csv.DictReader(f)
#     for row in file:
#         bot.send_message(chat_id=row["chat_id"], text="Habar jo'natildi")


@bot.message_handler(commands=['start'])
def start_message_handler(message):
    print(message.text)
    chat_id = message.chat.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_username = message.from_user.username
    with open("user.csv", "a") as f:
        file_user = csv.writer(f, delimiter=",")
        file_user.writerow([chat_id, user_first_name, datetime.now(), user_username])

    msg = "Assalomu alaykum {} {}!\n\nUshbu bot orqali koronavirus haqida bilishimiz kerak bo'lgan eng asosiy malumotlar" \
          " va uning davlatlarda va dunyo miqiyosida  tarqalish soni haqida " \
          "malumot olishingiz mumkin.".format(user_first_name, user_last_name)
    bot.send_message(chat_id=chat_id, text=msg)
    # WHERE_IS_USER = "boshida"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Tarqalish soni haqida")
    button2 = types.KeyboardButton(text="Koronavirus infeksiyasi haqida")
    button3 = types.KeyboardButton(text="Koronavirus belgilari")
    button4 = types.KeyboardButton(text="Koronavirusdan saqlanish qoidalar")
    keyboard.add(button2)
    keyboard.add(button1, button3)
    keyboard.add(button4)
    bot.send_message(chat_id=chat_id, text="Tanlang", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def all_message_handler(message):
    global WHERE_IS_USER
    global COUNTRY
    global COUNTRY_UZ
    is_like = False
    chat_id = message.chat.id
    request_text = message.text
    user_first_name = message.from_user.first_name
    l_user[user_first_name] = chat_id
    print(message.text)


    for x in list_c_n_uzbek:
        if request_text.lower() in x.lower():
            is_like = True
            COUNTRY = dict_country_name[x]
            COUNTRY_UZ = x

    for x in list_c_n_english:
        if request_text.lower() in x.lower():
            k = list(dict_country_name.values()).index(x)
            is_like = True
            COUNTRY = x
            COUNTRY_UZ = list(dict_country_name.keys())[k]

    if request_text == "Tarqalish soni haqida":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(text="◀️orqaga")
        button1 = types.KeyboardButton(text="Davlatlar bo'yicha umumiy ma'lumot")
        button2 = types.KeyboardButton(text="Ayni bir davlat bo'yicha to'liq ma'lumot")
        button3 = types.KeyboardButton(text="Eng ko'p tarqalgan o'ntalik")
        keyboard.add(button3)
        keyboard.add(button1, button2)
        keyboard.add(button)
        bot.send_message(chat_id=chat_id, text="Tanlang", reply_markup=keyboard)

    elif request_text == "Koronavirus infeksiyasi haqida":
        photo = "https://static.xabar.uz/crop/8/4/920__95_848793712.jpg"
        text_malumot = """
     🦠CОВИД-19 пандемияси - Илк маротаба 2019-йилнинг декабрида Хитойнинг Ухан шаҳрида қайд этилган касаллик 2020-йилнинг 11-мартида Жаҳон соғлиқни сақлаш ташкилоти томонидан пандемия деб белгиланди.
    
    🔹Вирус гриппга ўхшаш тарзда йўталганда ҳамда акса берганда чиқариладиган томчилар орқали шахсдан-шахсга юқади.
    
    🔹Вирус беморда касаллик аломатлари юзага келганда энг юқумли бўлса-да, касаллик белгилари пайдо бўлишидан олдин ҳам бошқаларга юқиши мумкин.
    
    🔹Касаллик 10 ёшгача бўлган болалар осонгина кечиришади. Ўрта ёшлилар учун ҳам деярли хавфсиз. Фақат ёши улуғ қарияларда кечиши оғирроқ.
    
    🔹Касаллик аломатлари одатда беш кунда пайдо бўлади, аммо бу давр 2 кундан 14 кунгача давом этиши мумкин.
    
    🔹Айни дамда CОВИД-19 га қарши ваксина ёки препарат йўқ. Касалликни бошқариш симптомларни даволаш ҳамда ёрдам терапиясидан иборат.Коронавируснинг олдини олиш учун турли антибиотикларни ичиш тавсия этилмайди. Иммунитетни кўтарадиган дорилар вирусни ўлдирмайди.
    
    🔹Вирусни юқтирганини тахмин қилаётган шахсларга 14 кун давомида ўзларини изоляция қилиш тавсия қилинади.
        """
        bot.send_message(chat_id=chat_id, text=text_malumot)
    elif request_text == "Koronavirus belgilari":
        text_belgilar = """
Kоронавируснинг асосий аломатлари:
👉Бош оғриғи
👉Юқори ҳарорат(тез-тез)
👉Йўтал(қуруқ)
👉Нимжонлик
👉Нафас қисиши
        """
        photo = "https://uznews.uz/upload/20200316053404W.jpg"
        bot.send_photo(chat_id=chat_id, photo=photo, caption=text_belgilar)


    elif request_text == "Koronavirusdan saqlanish qoidalar":
        text_qoida = """
        Kоронавирусдан сақланиш учун ҳар бир фуқаро қуйидаги тавсияларга амал қилиши керак:

✅ аввало, чет элга боришни режалаштиришда дунёдаги эпидемик вазият бўйича тўлиқ маълумотлардан хабардор бўлинг!

✅ зарурат бўлмаган тақдирда оммавий тадбирларда иштирок этишдан имкон қадар чекланинг!

✅ қўлларни тез-тез, яхшилаб совун билан ювинг ва спиртли дезинфекцияловчи воситалардан фойдаланинг!

✅ фаразандларингизнинг қўл ювишини доимий назоратга олинг!

✅ юз-кўзингизни нотоза қўл билан ушламанг!

✅ уй ҳайвонларини боқишда, асрашда гигиена қоидаларига қатъий риоя қилинг!

✅ одамлар олдида йўталганингизда ёки аксирганингизда оғзингиз ва бурнингизни дастрўмол, салфетка ёки букилган тирсагингиз билан тўсинг!

✅ шамоллаш ёки грипп аломатлари бор одамлар билан яқин, юзма-юз мулоқот қилишдан чекланинг!

✅ овқатланишда яхшилаб пиширилган, асосан қайнатилган ва қовурулган таомлардан истеъмол қилинг, истеъмол қилинаётган гўшт ва сут маҳсулотларининг яхшилаб пишганлигига ишонч ҳосил қилинг!

✅ иситма, йўтал ва нафас қисиши ҳолатлари пайдо бўлганда дарҳол шифокорга мурожаат қилинг!

‼️Энг асосийси, шахсий гигиена қоидаларига қатъий риоя қилинг!

Агарда сизда COVID-19 коронавирус инфекцияси ва у билан боғлиқ вазият юзасидан қўшимча савол туғилса, ССВ ҳузуридаги Санитария-эпидемиологик осойишталик агентлигининг 
71 276-49-66 телефон рақамига мурожаат қилишингиз мумкин.
        """
        bot.send_message(chat_id=chat_id, text=text_qoida)


    elif request_text == "Davlatlar bo'yicha umumiy ma'lumot":
        c_n_global = 0
        text = "📅 {} malumotiga ko'ra\n\n".format(DATA_INFO_CONFIRMED)
        with open("confirmed.csv", "r") as f:
            file = csv.DictReader(f, delimiter=",")
            for row in file:
                c_n_global += int(row[DATA_CONFIRMED])

        # vafot etganlar
        d_n_global = 0
        # text = "📅 {} malumotiga ko'ra\n".format(DATA_INFO_DEATHS)
        with open("deaths.csv", "r") as f:
            file = csv.DictReader(f, delimiter=",")
            for row in file:
                d_n_global += int(row[DATA_DEATHS])

        # tuzalganlar
        r_n_global = 0
        # text = "📅 {} malumotiga ko'ra\n".format(DATA_INFO_RECOVERED)
        with open("recovered.csv", "r") as f:
            file = csv.DictReader(f, delimiter=",")
            for row in file:
                r_n_global += int(row[DATA_RECOVERED])
        text += "Butun dunyo boyicha:\nKasallanganlar:\n  {} kishi\n\nVafot etganlar:\n {} kishi" \
                "\n\nSog'ayganlar:\n {} kishi".format(c_n_global, d_n_global, r_n_global)
        bot.send_message(chat_id=chat_id, text=text)


    elif request_text == "Barcha davlatlar ro'yxati":
        y = 0
        bot.send_message(chat_id=chat_id, text="Barcha davlatlar ro'yxati")
        for x in range((len(list_c_n_english)//50)+1):

            name_keyboard = types.InlineKeyboardMarkup(row_width=2)
            button_eng = types.InlineKeyboardButton(text="-----English-----", callback_data="eng")
            button_uzb = types.InlineKeyboardButton(text="-----Uzbek-----", callback_data="uzb")
            name_keyboard.add(button_eng, button_uzb)
            for i in range(50):

                if y < len(list_c_n_english):
                    button1 = types.InlineKeyboardButton(text="{}.{}".format(y+1, list_c_n_english[y]), callback_data=list_c_n_english[y])
                    button2 = types.InlineKeyboardButton(text="{}.{}".format(y+1, list_c_n_uzbek[y]), callback_data=list_c_n_uzbek[y])
                    name_keyboard.add(button1, button2)
                    y += 1

            if y <= len(list_c_n_english):

                bot.send_message(chat_id=chat_id, text="{} - elliktalik".format(x+1), reply_markup=name_keyboard)



    elif request_text == "Ayni bir davlat bo'yicha to'liq ma'lumot":

        WHERE_IS_USER = "bitta_davlat_qidirishda"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="🔍qidiruv")
        button2 = types.KeyboardButton(text="Barcha davlatlar ro'yxati")
        button3 = types.KeyboardButton(text="🔙orqaga")
        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        bot.send_message(chat_id=chat_id, text="qidiring", reply_markup=keyboard)


    elif request_text == "🔍qidiruv":
        bot.send_message(chat_id=chat_id, text="Davlat nomini kiriting")


    elif is_like:

        text = "📅 {} malumotiga ko'ra\n{} davlatida:\n\n".format(DATA_INFO_CONFIRMED, COUNTRY_UZ)
        confirmed_number = 0
        with open("confirmed.csv", "r") as f:
            file = csv.DictReader(f, delimiter=",")
            for row in file:
                if row["Country/Region"] == COUNTRY:
                    confirmed_number += int(row[DATA_CONFIRMED])
        if confirmed_number == 0:
            text += "Kasallanganlar:\n Bunday holat qayd etilmagan\n\n"
        else:
            text += "Kasallanganlar:\n  {} kishi\n\n".format(confirmed_number)

        # vafot etganlar
        deaths_number = 0
        with open("deaths.csv", "r") as f:
            file = csv.DictReader(f, delimiter=",")
            for row in file:
                if row["Country/Region"] == COUNTRY:
                    deaths_number += int(row[DATA_DEATHS])
        if deaths_number == 0:
            text += "Vafot etganlar:\n Bunday holat qayd etilmagan\n\n"
        else:
            text += "Vafot etganlar:\n  {} kishi\n\n".format(deaths_number)

        # sog'ayganlar
        recovered_number = 0
        with open("recovered.csv", "r") as f:
            file = csv.DictReader(f, delimiter=",")
            for row in file:
                if row["Country/Region"] == COUNTRY:
                    recovered_number += int(row[DATA_RECOVERED])
        if recovered_number == 0:
            text += "Sog'ayganlar:\nBunday holat qayd etilmagan\n\n"
        else:
            text += "Sog'ayganlar:\n  {} kishi\n\n".format(recovered_number)

        bot.send_message(chat_id=chat_id, text=text)


    elif request_text == "Eng ko'p tarqalgan o'ntalik":
        d_confirmed = {}
        number = 0
        text_message = "📅 {} malumotiga ko'ra koronavirus eng ko'p tarqalgan davlatlar o'ntaligi \n\n".format(DATA_INFO_CONFIRMED)
        for country in dict_country_name.values():
            with open("confirmed.csv", "r") as f:
                file = csv.DictReader(f, delimiter=",")
                for row in file:
                    if row["Country/Region"].lower() == country.lower():
                        number += int(row[DATA_CONFIRMED])
            d_confirmed[number] = country
            number = 0
        for i, num in enumerate(sorted(d_confirmed.keys(), reverse=True)[:10]):
            country_name = d_confirmed[num]
            number_confirmed = num
            text_message += "{}. {} - {}\n".format(i+1, country_name, number_confirmed)
        bot.send_message(chat_id=chat_id, text=text_message)


    elif request_text == "◀️orqaga":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="Tarqalish soni haqida")
        button2 = types.KeyboardButton(text="Koronavirus infeksiyasi haqida")
        button3 = types.KeyboardButton(text="Koronavirus belgilari")
        button4 = types.KeyboardButton(text="Koronavirusdan saqlanish qoidalar")
        keyboard.add(button2)
        keyboard.add(button1, button3)
        keyboard.add(button4)
        bot.send_message(chat_id=chat_id, text="Orqaga qaytdim", reply_markup=keyboard)

    elif request_text == "🔙orqaga":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(text="◀️orqaga")
        button1 = types.KeyboardButton(text="Davlatlar bo'yicha umumiy ma'lumot")
        button2 = types.KeyboardButton(text="Ayni bir davlat bo'yicha to'liq ma'lumot")
        button3 = types.KeyboardButton(text="Eng ko'p tarqalgan o'ntalik")
        keyboard.add(button3)
        keyboard.add(button1, button2)
        keyboard.add(button)
        bot.send_message(chat_id=chat_id, text="Orqaga qaytdim", reply_markup=keyboard)

    else:
        bot.send_message(chat_id=chat_id, text="Mavjud emas")


@bot.callback_query_handler(func=lambda call: True)
def all_inline_buttons_handler(message):
    global WHERE_IS_USER
    global COUNTRY
    global COUNTRY_UZ
    # print(message)
    chat_id = message.message.chat.id
    data = message.data
    print(data)
    if ((data in list_c_n_english) or (data in list_c_n_uzbek)) and (data != "eng" or data != "uzb"):
        WHERE_IS_USER = "qidiruv turini tanlashda"
        if data in list_c_n_english:
            COUNTRY = data
            k = list(dict_country_name.values()).index(data)
            COUNTRY_UZ = list(dict_country_name.keys())[k]
        if data in list_c_n_uzbek:
            COUNTRY = dict_country_name[data]
            COUNTRY_UZ = data

        text = "📅 {} malumotiga ko'ra\n{} davlatida:\n\n".format(DATA_INFO_CONFIRMED, COUNTRY_UZ)
        confirmed_number = 0
        with open("confirmed.csv", "r") as f:
            file = csv.DictReader(f, delimiter=",")
            for row in file:
                if row["Country/Region"] == COUNTRY:
                    # print(row["Country/Region"])
                    confirmed_number += int(row[DATA_CONFIRMED])
        if confirmed_number == 0:
            text += "Kasallanganlar:\n Bunday holat qayd etilmagan\n\n"
        else:
            text += "Kasallanganlar:\n  {} kishi\n\n".format(confirmed_number)

        # vafot etganlar
        deaths_number = 0
        with open("deaths.csv", "r") as f:
            file = csv.DictReader(f, delimiter=",")
            for row in file:
                if row["Country/Region"] == COUNTRY:
                    deaths_number += int(row[DATA_DEATHS])
        if deaths_number == 0:
            text += "Vafot etganlar:\n Bunday holat qayd etilmagan\n\n"
        else:
            text += "Vafot etganlar:\n  {} kishi\n\n".format(deaths_number)

        # sog'ayganlar
        recovered_number = 0
        with open("recovered.csv", "r") as f:
            file = csv.DictReader(f, delimiter=",")
            for row in file:
                if row["Country/Region"] == COUNTRY:
                    recovered_number += int(row[DATA_RECOVERED])
        if recovered_number == 0:
            text += "Sog'ayganlar:\nBunday holat qayd etilmagan\n\n"
        else:
            text += "Sog'ayganlar:\n  {} kishi\n\n".format(recovered_number)

        bot.send_message(chat_id=chat_id, text=text)

    else:
        pass

if __name__ == '__main__':
    bot.polling()