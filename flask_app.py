# - *- coding: utf- 8 - *-
import pandas as pd
import telebot
import sqlite3
import time
import datetime

# from matplotlib import pyplot as plt


import pandas_datareader as pdr

from flask import Flask, request

token = "986418369:AAFCzsp0J8J8u9DoQnK05GIGgQ-QN_7iNDc"
secret = 'gygugvhgvhg67yhcchj87'
url = 'https://Hits.pythonanywhere.com/' + secret

bot = telebot.TeleBot(token, threaded=False)  # тут изменил
bot.set_webhook(url=url)
app = Flask(__name__)


@app.route('/' + secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
user_markup.row("/start", 'SELECT_buy')
user_markup.row("SELECT_div", 'SELECT_sell')
user_markup.row('Ticker', 'UPDATE_Ticker')
user_markup.row('INSERT', 'DELETE')
user_markup.row('Portf', 'Portfusd')
user_markup.row('History_div')

markup = telebot.types.ReplyKeyboardMarkup()
markup.row('buy', 'sell')
markup.row('dividend')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать. Выберите команду", reply_markup=user_markup)
    bot.register_next_step_handler(message, repeat_all_messages);
    # bot.enable_save_next_step_handlers(delay=2)
    # bot.load_next_step_handlers(message, repeat_all_messages)


@bot.message_handler(commands=['Text'])
def repeat_all_messages(message):
    try:

        if message.text == "SELECT_buy":
            conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
            c = conn.cursor()
            c.execute("""SELECT Тикер FROM Ticker""")
            Tiker = c.fetchall()
            Tiker = Tiker[0][0]
            sql = "SELECT * FROM buy Where Тикер= ?"
            df = pd.read_sql_query(sql, conn, index_col='id', params=(Tiker,))

            conn.close()
            bot.send_message(message.from_user.id, str(df), reply_markup=user_markup)
            bot.register_next_step_handler(message, repeat_all_messages)
            # bot.enable_save_next_step_handlers(delay=2)
            # bot.load_next_step_handlers(message, repeat_all_messages)

        elif message.text == "SELECT_sell":
            conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
            c = conn.cursor()
            c.execute("""SELECT Тикер FROM Ticker""")
            Tiker = c.fetchall()
            Tiker = Tiker[0][0]
            sql = "SELECT * FROM sell Where Тикер= ?"
            df = pd.read_sql_query(sql, conn, index_col='id', params=(Tiker,))

            conn.close()
            bot.send_message(message.from_user.id, str(df), reply_markup=user_markup)
            bot.register_next_step_handler(message, repeat_all_messages)

        elif message.text == "SELECT_div":
            conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
            c = conn.cursor()
            c.execute("""SELECT Тикер FROM Ticker""")
            Tiker = c.fetchall()
            Tiker = Tiker[0][0]
            sql = "SELECT * FROM Dividend Where Тикер= ?"
            df = pd.read_sql_query(sql, conn, index_col='id', params=(Tiker,))

            conn.close()
            bot.send_message(message.from_user.id, str(df), reply_markup=user_markup)
            bot.register_next_step_handler(message, repeat_all_messages)





        elif message.text == "Ticker":
            conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
            c = conn.cursor()
            c.execute("SELECT Тикер FROM Ticker")
            abc = str(c.fetchall()[0][0])

            conn.close()
            bot.send_message(message.from_user.id, abc, reply_markup=user_markup)
            bot.register_next_step_handler(message, repeat_all_messages)

        elif message.text == "UPDATE_Ticker":
            bot.send_message(message.from_user.id, 'введите Тикер для вывода сделок')
            bot.register_next_step_handler(message, update)

        elif message.text == "Portf":
            bot.send_message(message.from_user.id, 'Вывести портфель')
            bot.register_next_step_handler(message, portfel)

        elif message.text == "Portfusd":
            bot.send_message(message.from_user.id, 'Вывести портфель')
            bot.register_next_step_handler(message, portfelusd)

        elif message.text == "INSERT":
            # markup = telebot.types.ReplyKeyboardMarkup()
            # markup.row('buy', 'sell')
            # markup.row('Дивиденды-купоны')
            bot.send_message(message.from_user.id, 'Введите показатель:', reply_markup=markup)
            bot.register_next_step_handler(message, pokazatel_1)

        elif message.text == "DELETE":
            # markup = telebot.types.ReplyKeyboardMarkup()
            # markup.row('buy', 'sell')
            # markup.row('Dividend')
            bot.send_message(message.from_user.id, 'Введите показатель для удаления:', reply_markup=markup)
            bot.register_next_step_handler(message, delete_1)

        elif message.text == "History_div":
            bot.send_message(message.from_user.id, 'Нажмите еще History_div для вывода суммы дивидендов с 2000г: ')
            bot.register_next_step_handler(message, stock)



        else:
            bot.register_next_step_handler(message, repeat_all_messages)


    except:
        bot.send_message(message.chat.id, 'Ошибка')
        bot.register_next_step_handler(message, repeat_all_messages)


def update(message):
    try:
        tik = str(message.text).upper();
        conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
        c = conn.cursor()
        c.execute("""UPDATE Ticker SET Тикер =:tik """, {u'tik': tik})
        conn.commit()
        conn.close()
        bot.send_message(message.from_user.id, 'Тикер обновлен')
        bot.register_next_step_handler(message, repeat_all_messages);
    except:
        bot.send_message(message.from_user.id, 'Ошибка')
        bot.register_next_step_handler(message, repeat_all_messages)


def portfel(message):
    today = datetime.date.today() + datetime.timedelta(days=1)
    yesterday = datetime.date.today() - datetime.timedelta(days=10)
    conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
    dfbuy = pd.read_sql('SELECT * FROM buy', conn)
    dfbuy = dfbuy[dfbuy['Валюта'] == 'RUB']
    dfbuy['суммапокупки'] = dfbuy['Колво'] * dfbuy['Цена']
    dfbuy['Ценапокупки'] = dfbuy['Цена']
    dfsell = pd.read_sql('SELECT * FROM sell', conn)
    dfsell = dfsell[dfsell['Валюта'] == 'RUB']
    dfsell['суммапродажи'] = dfsell['Колво'] * dfsell['Цена']
    dfsell['Колво'] = dfsell['Колво'] * -1
    dfsell['Ценапродажи'] = dfsell['Цена']
    dfdivid = pd.read_sql('SELECT * FROM Dividend', conn)
    dfdivid = dfdivid[dfdivid['Валюта'] == 'RUB']
    df = dfbuy.append(dfsell)
    df = df.append(dfdivid)
    dfp = df.groupby(['Тикер']).aggregate(sum)  # ПОРТФЕЛЬ РАБОЧИЙ ГРУППИРОВКА
    dfp = dfp.reset_index()
    a = dfp['Тикер']
    df = pd.DataFrame(columns=['Тикер', 'Ценарыночн', 'Ценавчера'])

    for i in a:
        try:
            dfT = pdr.get_data_yahoo(str(i + ".ME"), start=yesterday, end=today)
            df = df.append({'Тикер': i, 'Ценарыночн': dfT.Close[-1], 'Ценавчера': dfT.Close[-2]}, ignore_index=True)
        except:
            df = df.append({'Тикер': i, 'Ценарыночн': .0, 'Ценавчера': .0}, ignore_index=True)

    df3 = df.merge(dfp, on='Тикер', how='left')
    df3['Прибыль'] = df3['Ценарыночн'] * df3['Колво'] + df3['суммапродажи'] - df3['суммапокупки'] + df3['Суммадивид']
    df3['Прибыльвчера'] = (
            df3['Ценавчера'] * df3['Колво'])  # +df3['суммапродажи']-df3['суммапокупки']+df3['Суммадивид']
    df = df3[df3['Колво'] > 0]
    df['измен,р'] = ((df['Ценарыночн'] * df['Колво']) - df['Ценавчера'] * df['Колво']).round(1)
    df['измен,%'] = ((df['Ценарыночн'] - df['Ценавчера']) / df['Ценавчера'] * 100).round(1)
    df['сумма,рын'] = df['Ценарыночн'] * df['Колво']
    df['сумма,вчера'] = df['Ценавчера'] * df['Колво']
    columnlist = ['Тикер', 'измен,р', 'измен,%']
    df2 = df.reindex(columns=columnlist)
    df2 = df2.sort_values(by=['измен,р'], ascending=False)
    df3 = df2['измен,р'].sum()

    conn.close()

    bot.send_message(message.from_user.id, str(df2) + ' Итого ' + str(df3))
    bot.register_next_step_handler(message, repeat_all_messages)


def portfelusd(message):
    today = datetime.date.today() + datetime.timedelta(days=1)
    yesterday = datetime.date.today() - datetime.timedelta(days=10)
    conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
    dfbuy = pd.read_sql('SELECT * FROM buy', conn)
    dfbuy = dfbuy[dfbuy['Валюта'] == 'USD']
    dfbuy['суммапокупки'] = dfbuy['Колво'] * dfbuy['Цена']
    dfbuy['Ценапокупки'] = dfbuy['Цена']
    dfsell = pd.read_sql('SELECT * FROM sell', conn)
    dfsell = dfsell[dfsell['Валюта'] == 'USD']
    dfsell['суммапродажи'] = dfsell['Колво'] * dfsell['Цена']
    dfsell['Колво'] = dfsell['Колво'] * -1
    dfsell['Ценапродажи'] = dfsell['Цена']
    dfdivid = pd.read_sql('SELECT * FROM Dividend', conn)
    dfdivid = dfdivid[dfdivid['Валюта'] == 'USD']
    df = dfbuy.append(dfsell)
    df = df.append(dfdivid)
    dfp = df.groupby(['Тикер']).aggregate(sum)  # ПОРТФЕЛЬ РАБОЧИЙ ГРУППИРОВКА
    dfp = dfp.reset_index()
    a = dfp['Тикер']
    df = pd.DataFrame(columns=['Тикер', 'Ценарыночн', 'Ценавчера'])

    for i in a:
        try:
            dfT = pdr.get_data_yahoo(str(i), start=yesterday, end=today)
            df = df.append({'Тикер': i, 'Ценарыночн': dfT.Close[-1], 'Ценавчера': dfT.Close[-2]}, ignore_index=True)
        except:
            df = df.append({'Тикер': i, 'Ценарыночн': .0, 'Ценавчера': .0}, ignore_index=True)
    df3 = df.merge(dfp, on='Тикер', how='left')
    df3['Прибыль'] = df3['Ценарыночн'] * df3['Колво'] + df3['суммапродажи'] - df3['суммапокупки'] + df3['Суммадивид']
    df3['Прибыльвчера'] = (
            df3['Ценавчера'] * df3['Колво'])  # +df3['суммапродажи']-df3['суммапокупки']+df3['Суммадивид']
    df = df3[df3['Колво'] > 0]
    df['измен,usd'] = ((df['Ценарыночн'] * df['Колво']) - df['Ценавчера'] * df['Колво']).round(1)
    df['измен,%'] = ((df['Ценарыночн'] - df['Ценавчера']) / df['Ценавчера'] * 100).round(1)
    df['сумма,рын'] = df['Ценарыночн'] * df['Колво']
    df['сумма,вчера'] = df['Ценавчера'] * df['Колво']
    columnlist = ['Тикер', 'измен,usd', 'измен,%']
    df2 = df.reindex(columns=columnlist)
    df2 = df2.sort_values(by=['измен,usd'], ascending=False)
    df3 = df2['измен,usd'].sum()

    conn.close()

    bot.send_message(message.from_user.id, str(df2) + ' Итого ' + str(df3))
    bot.register_next_step_handler(message, repeat_all_messages)


def pokazatel_1(message):
    try:
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row('RUB', 'USD')
        pokaz = str(message.text);

        conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
        c = conn.cursor()
        c.execute("""UPDATE Insertdeal SET pokaz =?""", (pokaz,))
        conn.commit()
        conn.close()
        bot.send_message(message.from_user.id, 'показатель  изменен, введите Валюта:', reply_markup=markup)
        bot.register_next_step_handler(message, pokazatel_2);
    except:
        bot.send_message(message.from_user.id, 'Ошибка выбора показателя')
        bot.register_next_step_handler(message, repeat_all_messages, reply_markup=user_markup)


def pokazatel_2(message):
    try:
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row('Stock', 'Bond')
        markup.row('Futeres', 'Cash')
        pokaz = str(message.text);
        conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
        c = conn.cursor()
        c.execute("""UPDATE Insertdeal SET val =?""", (pokaz,))
        conn.commit()
        conn.close()
        bot.send_message(message.from_user.id, 'Валюта изменен, введите Инструмент:', reply_markup=markup)
        bot.register_next_step_handler(message, pokazatel_3);
    except:
        bot.send_message(message.from_user.id, 'Ошибка выбора показателя')
        bot.register_next_step_handler(message, repeat_all_messages, reply_markup=user_markup)


def pokazatel_3(message):
    try:
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row('Finam', 'Tinkof')
        markup.row('Sberbank')
        pokaz = str(message.text);
        conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
        c = conn.cursor()
        c.execute("""UPDATE Insertdeal SET instrument =?""", (pokaz,))
        conn.commit()
        conn.close()
        bot.send_message(message.from_user.id, 'Инструмент изменен, введите Портфель:', reply_markup=markup)
        bot.register_next_step_handler(message, pokazatel_4);
    except:
        bot.send_message(message.from_user.id, 'Ошибка выбора инструмента')
        bot.register_next_step_handler(message, repeat_all_messages, reply_markup=user_markup)


def pokazatel_4(message):
    try:
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row('today')
        pokaz = str(message.text);
        conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
        c = conn.cursor()
        c.execute("""UPDATE Insertdeal SET portfel =?""", (pokaz,))
        conn.commit()
        conn.close()
        bot.send_message(message.from_user.id, 'Портфель изменен, введите Дата в формате YYYY-MM-DD:',
                         reply_markup=markup)
        bot.register_next_step_handler(message, pokazatel_5);
    except:
        bot.send_message(message.from_user.id, 'Ошибка выбора портфеля')
        bot.register_next_step_handler(message, repeat_all_messages, reply_markup=user_markup)


def pokazatel_5(message):
    try:
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row('today')
        pokaz = str(message.text);
        if pokaz == 'today':
            import datetime
            pokaz = str(datetime.date.today())
        else:
            pass
        conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
        c = conn.cursor()
        c.execute("""UPDATE Insertdeal SET date =?""", (pokaz,))
        conn.commit()
        conn.close()
        bot.send_message(message.from_user.id, 'Дата изменена введите Тикер', reply_markup=markup)
        bot.register_next_step_handler(message, pokazatel_6);
    except:
        bot.send_message(message.from_user.id, 'Ошибка выбора показателя')
        bot.register_next_step_handler(message, repeat_all_messages, reply_markup=user_markup)


def pokazatel_6(message):
    try:
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row('Сancel')
        pokaz = str(message.text).upper();
        conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
        c = conn.cursor()
        c.execute("""UPDATE Insertdeal SET tiker =?""", (pokaz,))
        conn.commit()
        conn.close()
        bot.send_message(message.from_user.id, 'Тикер изменен введите количество,для дивид любое знач',
                         reply_markup=markup)
        bot.register_next_step_handler(message, pokazatel_7);
    except:
        bot.send_message(message.from_user.id, 'Ошибка выбора портфеля')
        bot.register_next_step_handler(message, repeat_all_messages, reply_markup=user_markup)


def pokazatel_7(message):
    try:
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row('Сancel')
        pokaz = int(message.text);
        conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
        c = conn.cursor()
        c.execute("""UPDATE Insertdeal SET kolvo =?""", (pokaz,))
        conn.commit()
        conn.close()
        bot.send_message(message.from_user.id, 'кол-во изменен введите цену,для дивид введите сумму общую',
                         reply_markup=markup)
        bot.register_next_step_handler(message, pokazatel_8);
    except:
        bot.send_message(message.from_user.id, 'Ошибка выбора портфеля')
        bot.register_next_step_handler(message, repeat_all_messages, reply_markup=user_markup)


def pokazatel_8(message):
    try:
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row('ADD', 'Сancel')
        pokaz = float(message.text);
        conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
        c = conn.cursor()
        c.execute("""UPDATE Insertdeal SET price =?""", (pokaz,))
        a = c.execute("""SELECT * FROM Insertdeal """).fetchall()
        conn.commit()
        conn.close()
        bot.send_message(message.from_user.id, 'Добавить сделку?' + str(a), reply_markup=markup)
        bot.register_next_step_handler(message, pokazatel_9);
    except:
        bot.send_message(message.from_user.id, 'Ошибка выбора портфеля')
        bot.register_next_step_handler(message, repeat_all_messages, reply_markup=user_markup)


def pokazatel_9(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row("/start", 'SELECT_buy')
    markup.row("SELECT_div", 'SELECT_sell')
    markup.row('Ticker', 'UPDATE_Ticker')
    markup.row('INSERT', 'DELETE')
    markup.row('Portf', 'Portfusd')
    try:
        if message.text == "ADD":
            conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
            c = conn.cursor()
            a = c.execute("""SELECT * FROM Insertdeal """).fetchall()
            if a[0][0] == 'buy':
                c.execute("""INSERT INTO buy(Валюта,Инструмент,Портфель,Дата,Тикер,Колво,Цена)
                    SELECT val,instrument,portfel,date,tiker,kolvo,price
                    FROM Insertdeal""")
                conn.commit()

            elif a[0][0] == 'sell':
                c.execute("""INSERT INTO sell(Валюта,Инструмент,Портфель,Дата,Тикер,Колво,Цена)
                    SELECT val,instrument,portfel,date,tiker,kolvo,price
                    FROM Insertdeal""")
                conn.commit()

            elif a[0][0] == 'dividend':
                c.execute("""INSERT INTO Dividend(Валюта,Инструмент,Портфель,Дата,Тикер,Суммадивид)
                    SELECT val,instrument,portfel,date,tiker,price
                    FROM Insertdeal""")
                conn.commit()

            else:
                pass
            conn.close()
            bot.send_message(message.from_user.id, 'Добавлена' + str(a), reply_markup=markup)
            bot.register_next_step_handler(message, repeat_all_messages);

        else:
            bot.send_message(message.from_user.id, 'Отмена', reply_markup=markup)
            bot.register_next_step_handler(message, repeat_all_messages)
    except:
        bot.send_message(message.from_user.id, 'Ошибка добавления', reply_markup=markup)
        bot.register_next_step_handler(message, repeat_all_messages)


def delete_1(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Dell', 'Cancel')
    conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
    # c = conn.cursor()
    pokaz = str(message.text)
    if pokaz == 'buy':
        a = pd.read_sql('SELECT * FROM buy ORDER BY id DESC LIMIT 5', conn)
        # a = c.execute("""SELECT * FROM buy ORDER BY id DESC LIMIT 5""").fetchall()
        conn.close()
        bot.send_message(message.from_user.id, str(a) + 'введите id для удаления BUY', reply_markup=markup)
        bot.register_next_step_handler(message, delete_buy);
    elif pokaz == 'sell':
        a = pd.read_sql('SELECT * FROM sell ORDER BY id DESC LIMIT 5', conn)
        # a =c.execute("""SELECT * FROM sell ORDER BY id DESC LIMIT 5""").fetchall()
        conn.close()
        bot.send_message(message.from_user.id, str(a) + 'введите id для удаления SELL', reply_markup=markup)
        bot.register_next_step_handler(message, delete_sell);

    else:
        conn.close()
        bot.send_message(message.from_user.id, 'Ошибка добавления', reply_markup=markup)
        bot.register_next_step_handler(message, repeat_all_messages)


def delete_buy(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row("/start", 'SELECT_buy')
    markup.row("SELECT_div", 'SELECT_sell')
    markup.row('Ticker', 'UPDATE_Ticker')
    markup.row('INSERT', 'DELETE')
    markup.row('Portf', 'Portfusd')
    pokaz = str(message.text)
    try:
        if pokaz == "Cancel":
            bot.send_message(message.from_user.id, 'Отменено пользователем', reply_markup=markup)
            bot.register_next_step_handler(message, repeat_all_messages);
        else:
            try:
                conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
                c = conn.cursor()
                pokaz = str(message.text)
                a = c.execute("""SELECT * from buy WHERE id =?""", (pokaz,)).fetchall()
                c.execute("""DELETE from buy WHERE id =?""", (pokaz,))
                conn.commit()
                conn.close()
                bot.send_message(message.from_user.id, str(a) + 'Удален BUY', reply_markup=markup)
                bot.register_next_step_handler(message, repeat_all_messages);
            except:
                bot.send_message(message.from_user.id, 'ошибка', reply_markup=markup)
                bot.register_next_step_handler(message, repeat_all_messages);

    except:
        bot.send_message(message.from_user.id, 'ошибка', reply_markup=markup)
        bot.register_next_step_handler(message, repeat_all_messages);


def delete_sell(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row("/start", 'SELECT_buy')
    markup.row("SELECT_div", 'SELECT_sell')
    markup.row('Ticker', 'UPDATE_Ticker')
    markup.row('INSERT', 'DELETE')
    markup.row('Portf', 'Portfusd')
    pokaz = str(message.text)
    try:

        if pokaz == 'Cancel':
            bot.send_message(message.from_user.id, 'Отменено пользователем', reply_markup=markup)
            bot.register_next_step_handler(message, repeat_all_messages);
        else:
            try:

                conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
                c = conn.cursor()
                pokaz = str(message.text)
                a = c.execute("""SELECT * from sell WHERE id =?""", (pokaz,)).fetchall()
                c.execute("""DELETE from sell WHERE id =?""", (pokaz,))
                conn.commit()
                conn.close()
                bot.send_message(message.from_user.id, str(a) + 'Удален SELL', reply_markup=markup)
                bot.register_next_step_handler(pokaz, repeat_all_messages);
            except:
                bot.send_message(message.from_user.id, 'ошибка', reply_markup=markup)
                bot.register_next_step_handler(message, repeat_all_messages);
    except:
        bot.send_message(message.from_user.id, 'ошибка', reply_markup=markup)
        bot.register_next_step_handler(message, repeat_all_messages)


def stock(message):
    try:

        conn = sqlite3.connect('/home/Hits/portfolio/Porfa.db')
        c = conn.cursor()
        c.execute("""SELECT Тикер FROM Ticker""")
        Tiker = c.fetchall()
        conn.close()
        Tiker = Tiker[0][0]
        df = pdr.data.DataReader(Tiker, 'yahoo-dividends', start="2010-01-01", end="2020-12-31")

        df = df.reset_index()
        df.columns = ['Date', 'Операция', 'Dividends']

        df = df.set_index('Date')
        df = df.Dividends

        df = df.reset_index()
        # df.groupby([df["Date"].dt.year]).sum().plot(kind="bar")

        # plt.savefig(r'/home/Hits/mysite/doc/testplot.png')
        # picture = open('/home/Hits/mysite/doc/testplot.png')

        df2 = pdr.get_data_yahoo(Tiker, start="2010-01-01", end="2021-12-31")
        df2 = df2.reset_index()
        # df2.groupby([df2["Date"].dt.year]).Close.mean().plot(kind="line") #ЭТО РАБОЧИЙ нужно последнее значение для года
        # plt.savefig(r'/home/Hits/mysite/doc/testplot2.png')
        # picture2 = open('/home/Hits/mysite/doc/testplot2.png')

        df_div = df.groupby([df["Date"].dt.year]).Dividends.sum()
        df_Price = df2.groupby([df2["Date"].dt.year]).Close.mean()
        df_div = df_div.reset_index()
        df_Price = df_Price.reset_index()
        df = df_div.merge(df_Price, left_on='Date', right_on='Date', suffixes=('_left', '_right'))
        df['Perc'] = ((df['Dividends'] / df['Close']) * 100).round(1)

        df['Close'] = df['Close'].round(2)
        # df.groupby([df["Date"].dt.year]).Perc.sum().plot(kind="bar")
        # plt.close('all')
        # df['Perc'].plot(kind="hist")
        # plt.savefig(r'/home/Hits/mysite/doc/testplot3.png')
        # picture3 = open(r'/home/Hits/mysite/doc/testplot3.png')

        # bot.send_photo(message.from_user.id, picture)
        # bot.send_photo(message.from_user.id, picture2)
        # bot.send_photo(message.from_user.id, picture3)
        bot.send_message(message.from_user.id, str(df))
        bot.register_next_step_handler(message, repeat_all_messages)
    except:
        bot.send_message(message.from_user.id, 'Ошибка')
        bot.register_next_step_handler(message, repeat_all_messages)


if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling(True)
        except Exception as e:
            print(e)
            time.sleep(15)
