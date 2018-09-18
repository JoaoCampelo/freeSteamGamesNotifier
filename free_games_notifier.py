# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import sqlite3 as lite
import sys
import requests
import os.path
import time
import fbchat
import getpass
import _thread
import threading

def create_database(db_name):
    con = None

    try:
        con = lite.connect(db_name)
        print (time.strftime('%d/%m/%Y %H:%M') + ' -> Database created successfully!')
    except e:
        print ("Error: create_database()")
        sys.exit(1)
    finally:
        if con:
            con.close()

def create_table(db_name, table_name):
    con = lite.connect(db_name)

    with con:
        cur = con.cursor()

        if(table_name == 'GAMES'):
            cur.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name VARCHAR(100) NOT NULL, URL VARCHAR(150) NOT NULL, Date_Time datetime(50) NOT NULL)")
        elif(table_name == 'SENDER'):
            cur.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Username VARCHAR(100) NOT NULL, Password VARCHAR(50) NOT NULL)")
        elif(table_name == 'RECEIVERS'):
            cur.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Username VARCHAR(100) NOT NULL)")

    con.close()

def insert_data(db_name, table_name, game_info):
    con = lite.connect(db_name)

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO " + table_name + " VALUES (NULL, ?, ?, ?);", (game_info[0], game_info[1], game_info[2]))

    con.close()

def insert_fbSender(db_name, table_name, username, password):
    con = lite.connect(db_name)

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO " + table_name + " VALUES (NULL, ?, ?);", (username, password))

    con.close()

def add_more_receivers(db_name, table_name, timeout=5.0):
    con = lite.connect(db_name)
    answer = ''

    print('Answer "exit" if you want to end the program.')
    while answer not in ("yes", "no"):
        answer = input('Want to add new users? (yes / no): ')
        if(answer == 'yes'):
            nr_users = input('How many users?: ')
            print('Make sure the user is your friend on Facebook.')
            for x in range(int(nr_users)):
                username = input('Friend\'s name on Facebook: ')
                with con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO " + table_name + " VALUES (NULL, ?);", [username])
        elif(answer == 'no'):
            break
        elif(answer == 'exit'):
            exit()
        else:
            print('Invalid Option!')
        pass

    con.close()

def send_msg_new_game(db_name, table_name, client, msg):
    con = lite.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute("SELECT Username FROM " + table_name)
        names = cur.fetchall()
    con.close()

    for name in names:
        friends = client.searchForUsers(name[0])
        friend = friends[0]
        sent = client.send(fbchat.models.Message(text=msg), thread_id=friend.uid)
        if sent:
            print("Message sent successfully! --> " + name[0])
        else:
            print("Error: send_msg_new_game()")


def check_game_exists_db(db_name, table_name, game_info):
    con = lite.connect(db_name)

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM " + table_name + " WHERE Name=? AND URL=? AND  Date_Time=?", (game_info[0], game_info[1], game_info[2]))
        rows = cur.fetchone()
        if(not rows):
            insert_data(db_name, table_name, game_info)
            return 1

    con.close()

    return 0

def check_sender_exists_db(db_name, table_name):
    con = lite.connect(db_name)

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM " + table_name)
        rows = cur.fetchone()
        if(not rows):
            return 1

    con.close()

    return 0

def info_new_game(db_name, table_name, table_users, game_info, client):
    new_old = 0

    if (check_game_exists_db(db_name, table_name, game_info) != 0):
        new_old = 1
        print(time.strftime('%d/%m/%Y %H:%M') + ' -> New Game! --> ' + game_info[0])
        msg = ('* New Game Free *\n' + game_info[0] + '\n\n' + game_info[1])
        send_msg_new_game(db_name, table_users, client, msg)

    return new_old

def login_facebook_sender(db_name, table_name):
    con = lite.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM " + table_name)
        rows = cur.fetchone()
        client = fbchat.Client(rows[1], rows[2])
    con.close()

    return client


def giveaway_fsk(db_name, table_name, table_users, url, client):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, 'html.parser')

    game_info = []
    new_old = 0

    for article in soup.find_all('article'):
        for nome in article.find_all('h2', class_='entry-title'):
            game_info.append(nome.text)

        for link in article.find_all('a', class_='item-url custom_link_button'):
            game_info.append(link.get('href'))

        for postado in article.find_all('time', class_='entry-date published'):
            game_info.append(postado.get('datetime'))

        if(game_info):
            info_new_game(db_name, table_name, table_users, game_info, client)

        game_info.clear()

    return new_old

def giveaway_gamehag(db_name, table_name, table_users, url, client):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, 'html.parser')

    game_info = []
    new_old = 0

    for article in soup.find_all('div', class_='single-giveaway'):
        game_info.append(article.find('h2').text)

        game_info.append(article.find('a', class_='btn btn-primary ml-auto').get('href'))

        for child in article.find_all('dd'):
            if(not child.string.isdigit()):
                game_info.append(child.string)

        if(game_info):
            info_new_game(db_name, table_name, table_users, game_info, client)

        game_info.clear()

    return new_old

if __name__ == '__main__':
    url_fsk = 'https://www.freesteamkeys.com/'
    url_gamehag ='https://gamehag.com/pt/giveaway'
    db_name = 'ListGames.db'
    table_games = 'GAMES'
    table_fb = 'SENDER'
    table_users = 'RECEIVERS'
    client = ''

    while True:
        if(os.path.exists (db_name)):
            print(time.strftime('%d/%m/%Y %H:%M') + ' -> Database already exists!')
        else:
            create_database(db_name)
            create_table(db_name, table_games)
            create_table(db_name, table_fb)
            create_table(db_name, table_users)

        add_more_receivers(db_name, table_users)

        while (check_sender_exists_db(db_name, table_fb) == 1):
            username = input('Facebook Username: ')
            password = getpass.getpass("Password: ")
            client = fbchat.Client(username, password)
            if (client.isLoggedIn()):
                insert_fbSender(db_name, table_fb, username, password)
                print('Logout of ' + username + ' successful.')
                client.logout()
            pass

        if(not client):
            client = login_facebook_sender(db_name, table_fb)

        while True:
            if((giveaway_gamehag(db_name, table_games, table_users, url_gamehag, client) == 0) and (giveaway_fsk(db_name, table_games, table_users, url_fsk, client) == 0)):
                print(time.strftime('%d/%m/%Y %H:%M') + ' -> There are no new games!')
            try:
                time.sleep(60)
            except KeyboardInterrupt:
                break
            pass

        pass
