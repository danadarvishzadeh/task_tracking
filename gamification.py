import csv
import sqlite3
from sqlite3 import Error

from consts import *
from queries import *


def get_input(input_text=''):
    text = ''
    while True:
        new_line = input(input_text)
        if new_line == 'q':
            break
        text = "\n".join((text, new_line))
    return text

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

def make_bar(key, value):
    bar = ((5-len(str(value)))//2)*' ' + '|' + ((value//INTERVAL)-1)*'='
    if value == 100:
        bar += '='
    elif value > 0:
        bar += '»'
    bar += ((100-value)//INTERVAL)*' ' + '|'
    bar = ('%').join([str(value), bar])
    if value != 100:
        bar = ' ' + bar
    return f"{key} {(15-len(key))*'-'} {bar}"

def prepreation():
    global skills
    create_database()
    for query in CREATING_TABLE_QUERIES:
        create_tables(query)
    skills = Skill.get_all_skills()

def flush():
    global skills
    connection.commit()
    skills = Skill.get_all_skills()


class Skill:

    def __init__(
        self,
        name):
        self.name = name
        self.notes = list()
        self.steps = list()
        self.number_of_steps = None
        self.url = None
        self.load_or_create()


################ LOADINGS ################

    def load_or_create(self):
        try:
            if self.name not in skills:
                cursor.execute(INSERT_INTO_SKILLS, (self.name,))
                connection.commit()
            cursor.execute(SELECT_FROM_SKILLS, (self.name,))
            (
                self.stats,
                self.number_of_steps,
            ) = cursor.fetchone()
            self.load_url()
            self.load_notes()
            if self.number_of_steps is not None:
                self.load_steps()
        except Error as e:
            print(e)

    def load_notes(self):
        cursor.execute(SELECT_FROM_NOTES, (self.name,))
        result = cursor.fetchall()
        for item in result:
            (
                note_id,
                text) = item
            self.notes.append(Note(note_id, text))

    def load_steps(self):
        cursor.execute(SELECT_FROM_STEPS, (self.name,))
        result = cursor.fetchall()
        for item in result:
            (
                skill_name,
                step_order,
                objective,
                url) = item
            self.steps.append(Step(
                    skill_name,
                    step_order,
                    objective,
                    url,))

    def load_url(self):
        cursor.execute(SELECT_SKILL_URLS, (self.name,))
        self.url = cursor.fetchone()

################ UPDATES ################

    def rename(self, new_name):
        cursor.execute(UPDATE_RENAME_SKILLS, (new_name, self.name))

    def add_stats(self):
        if self.stats < 100:
            self.stats += INTERVAL
            cursor.execute(UPDATE_STATS_SKILLS, (self.stats, self.name))

    def add_url(self, url):
        cursor.execute(INSERT_INTO_URLS, (self.name, '', '', url))

    def add_step_url(self, step_order, url):
        self.steps[step_order].add_url(url)


################ SHOWS ################

    def show_url(self):
        if self.url is not None:
            print(self.url, end='\n\n')
        else:
            print('this skill does not have a reference url.')

    def show_notes(self):
        for note in self.notes:
            print(note.show(), end='\n\n')

    def show_details(self):
        bar = make_bar(self.name, self.stats)
        print(bar, end='\n***********\n')
        for note in self.notes:
            note.show()
        print('\n***********\n')
        for step in self.steps:
            step.show()

################ STATIC METHODS ################

    @staticmethod
    def show_skills():
        for key in skills.keys():
            percent = int(skills[key])
            bar = make_bar(key, percent)
            print(bar)

    @staticmethod
    def delete_skill(name):
        cursor.execute(DELETE_FROM_SKILLS, (name,))
    
    @staticmethod
    def get_all_skills():
        try:
            cursor.execute(SELECT_ALL_SKILLS)
            result = cursor.fetchall()
            result_dict = dict()
            for k, v in result:
                result_dict[k] = v
        except Error as e:
            print(e)
        return result_dict
    
    @staticmethod
    def skill_exists(skill_name):
        return skill_name in skills.keys()

class Step:

    def __init__(
        self,
        skill_name,
        step_order,
        objective,
        url):
        self.skill_name = skill_name
        self.url = url
        self.step_order = step_order
        self.objective = objective
    
    def add_url(self, url):
        cursor.execute(INSERT_INTO_URLS, (
            self.skill_name,
            self.skill_name,
            self.step_order,
            url,))

    def show(self):
        print(self.step_order)
        print(self.objective, end='\n\n')
        if self.url != 'NULL':
            print(self.url)

    @staticmethod
    def define_steps(skill_name, number_of_steps):
        for i in range(number_of_steps):
            print(f'objective for step number {i}')
            objective = get_input()
            cursor.execute(INSERT_INTO_STEPS, (skill_name, i, objective))
            connection.commit()
        cursor.execute(UPDATE_STEPS_SKILLS, (skill_name, number_of_steps))

    # def set_url(self, url):
    #     cursor.execute(SET_URL, (url, self.skill_id, self.id))

class Note:

    def __init__(
        self,
        note_id,
        text):
        self.note_id = note_id
        self.text = text
    
    def show(self):
        return f"id:{self.note_id}{self.text}"

    @staticmethod
    def define_note(skill_name, text):
        cursor.execute(INSERT_INTO_NOTES, (skill_name, text))
    
    @staticmethod
    def delete_note(note_id):
        cursor.execute(DELETE_FROM_NOTES, (note_id,))