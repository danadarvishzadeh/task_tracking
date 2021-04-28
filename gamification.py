import csv
import sqlite3
from sqlite3 import Error

from consts import *
from queries import *


def create_database():
    global cursor, connection
    connection = None
    cursor = None
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
    except Error as e:
        print(e)
    finally:
        if connection is None:
            raise Exception('connection did not established.')
        if cursor is None:
            raise Exception('cursor did not set.')

def create_tables(create_table_sql):
    try:
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)

def prepreation():
    global skills
    create_database()
    for query in CREATING_TABLE_QUERIES:
        create_tables(query)
    skills = Skill.get_all_skills()

def flush():
    connection.commit()

class Skill:

    def __init__(
        self,
        name):
        self.name = name
        self.notes = dict()
        self.load_or_create()
                
    def add_note(self, note):
        cursor.execute(NOTE_INSERT_QUERY, (note, self.id))

    def set_url(self, url):
        cursor.execute(SET_URL, (url, self.name))

    def show_url(self):
        print(self.url, end='\n\n')

    @staticmethod
    def delete_note(_id):
        cursor.execute(NOTE_DELETE_QUERY, (_id,))

    def show_notes(self):
        i = 1
        for k, v in self.notes.items():
            print(f"{i}{v}---id={k}", end="\n\n")
            i += 1

    def add_stat(self):
        if self.stats < 100:
            self.stats += INTERVAL
            cursor.execute(ADD_STATS, (self.stats, self.name))

    def load_or_create(self):
        try:
            if self.name not in skills:
                cursor.execute(SKILL_INSERT_QUERY, (self.name,))
                connection.commit()
            cursor.execute(SKILL_LOAD_QUERY, (self.name,))
            self.id, self.stats, self.url = cursor.fetchall()[0]
            self.load_notes()
        except Error as e:
            print(e)
    
    @staticmethod
    def rename(names):
        old_name, new_name = names
        cursor.execute(SKILL_RENAME_QUERY, (new_name, old_name))

    def load_notes(self):
        cursor.execute(GET_SKILL_NOTES, (self.id,))
        result = cursor.fetchall()
        for k, v in result:
            self.notes[k] = v

    @staticmethod
    def remove_skill(name):
        cursor.execute(SKILL_DELETE_QUERY, (name,))
    
    @staticmethod
    def get_all_skills():
        try:
            cursor.execute(GET_ALL_SKILLS)
            result = cursor.fetchall()
            result_dict = dict()
            for k, v in result:
                result_dict[k] = v
        except Error as e:
            print(e)
        return result_dict
    
    @staticmethod
    def show_skills():
        for key in skills.keys():
            percent = int(skills[key])
            bar = ((5-len(str(percent)))//2)*' ' + '|' + ((percent//INTERVAL)-1)*'='
            if percent == 100:
                bar += '='
            elif percent > 0:
                bar += '»'
            bar += ((100-percent)//INTERVAL)*' ' + '|'
            bar = ('%').join([str(percent), bar])
            if percent != 100:
                bar = ' ' + bar
            print(f"{key} {(15-len(key))*'-'} {bar}")
        

# if __name__ == "__main__":
#     prepreation()
#     argument_list = sys.argv[1:]
#     options = 'ha:u:r:'
#     long_options = [
#         'rename',
#         'anote=',
#         'notes=',
#         'rnote=',
#         'aurl=',
#         'surl=',
#     ]
#     try:
#         arguments, values = getopt.getopt(argument_list, options, long_options)
#         for current_argument, current_value in arguments:
#             if current_argument in ('-h'):
#                 print('-a for adding skills\n-u for updating a skill\n-s for showing progress\n-r for removing skill')
#             elif current_argument == '-a':
#                 Skill(current_value)
#             elif current_argument == '-u':
#                 Skill(current_value).add_stat()
#             elif current_argument == '-r':
#                 Skill.remove_skill(current_value)
#             elif current_argument == '--rename':
#                 Skill.rename(values)
#             elif current_argument == '--aurl':
#                 Skill(current_value).set_url(values[0])
#             elif current_argument == '--surl':
#                 Skill(current_value).show_url()
#             elif current_argument == '--anote':
#                 note = ''
#                 while True:
#                     new_line = input()
#                     if new_line == 'q':
#                         break
#                     note = "\n".join((note, new_line))
#                 Skill(current_value).add_note(note)
#             elif current_argument == '--notes':
#                 Skill(current_value).show_notes()
#             elif current_argument == '--rnote':
#                 Skill.delete_note(current_value)
#     except getopt.error as err:
#         print('opt faliure', str(err))
#     finally:
#         try:
#             connection.commit()
#             skills = Skill.get_all_skills()
#             Skill.show_skills()
#         except:
#             print('app failed.')
