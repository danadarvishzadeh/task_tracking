import sqlite3
from sqlite3 import Error

from consts import *
from queries import CREATING_TABLE_QUERIES, SELECT_ALL_TABLES


def get_input(conn, input_text='' , multi=False, integer=False):
    text = ''
    while True:
        if conn is not None:
            conn.sendall(input_text.encode('utf-8'))
            new_line = conn.recv(1024).decode('utf-8')
        else:
            try:
                new_line = input('\n'+input_text)
            except KeyboardInterrupt:
                pass
            except:
                pass
        if new_line == 'q':
            break
        if not multi:
            text += new_line
            break
        text = "\n".join((text, new_line))
    if integer:
        try:
            text = int(text)
        except:
            return 'This is not a fucking integer. With love.'
    return text

def create_database():
    connection = None
    cursor = None
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        return connection, cursor
    except Error as e:
        err = ''
        err += str(e)
        if connection is None:
            err += '\nconnection did not established.'
        if cursor is None:
            err += '\ncursor did not set.'
        raise Exception(err)

def create_tables(cursor, create_table_sql):
    try:
        cursor.execute(create_table_sql)
    except Error as e:
        return str(e)

def make_bar(key, value):
    bar_part_one = ((5-len(str(value)))//2)*' '
    bar_part_two = '|' + ((value//INTERVAL)-1)*'='
    if value == 100:
        bar_part_two += '='
    elif value > 0:
        bar_part_two += '»'
    bar_part_two += (11 - len(bar_part_two))*' ' + '|'
    bar = bar_part_one + bar_part_two
    bar = ('%').join([str(value), bar])
    if value != 100:
        bar = ' ' + bar
    return f"{key} {(20-len(key))*'-'} {bar}"