import sqlite3
from sqlite3 import Error

from consts import *
from queries import CREATING_TABLE_QUERIES


def get_input(input_text=''):
    text = ''
    while True:
        new_line = input(input_text)
        if new_line == 'q':
            break
        text = "\n".join((text, new_line))
    return text.strip()

def create_database():
    connection = None
    cursor = None
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        return connection, cursor
    except Error as e:
        print(e)
        #if connection is None:
        #    raise Exception('connection did not established.')
        #if cursor is None:
        #    raise Exception('cursor did not set.')
        if connection is None:
            print('connection did not established.')
        if cursor is None:
         print('cursor did not set.')
        exit()



def create_tables(cursor, create_table_sql):
    try:
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)

def make_bar(key, value):
    bar_part_one = ((5-len(str(value)))//2)*' '
    bar_part_two = '|' + int((value//INTERVAL)-1)*'='
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

