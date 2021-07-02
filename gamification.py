import sqlite3
from sqlite3 import Error

from docopt import docopt

import utils
from consts import INTERVAL
from queries import *
from utils import (create_database, create_tables, get_input,
                                 make_bar)


def prepreation():
    global connection, cursor
    global skills
    connection_or_error, cursor = create_database()
    if cursor is None:
        return connection_or_error
    else:
        connection = connection_or_error
    for query in CREATING_TABLE_QUERIES:
        err = create_tables(cursor, query)
        if err:
            return err
    skills = Skill.get_all_skills()

def flush():
    global skills
    connection.commit()
    skills = Skill.get_all_skills()

class Skill:

    def __init__(
        self,
        name,
        total=None,
        interval=None,
        binary=False):
        self.name = name
        self.total = total
        self.interval = interval
        self.notes = list()
        self.steps = list()
        self.number_of_steps = None
        self.url = None
        self.binary = binary
        self.buffer = ''
        self.load_or_create()


################ LOADINGS ################

    def load_or_create(self, binary=False):
        if self.name not in skills:
            cursor.execute(INSERT_INTO_SKILLS, (self.name, self.total, self.interval))
            connection.commit()
        cursor.execute(SELECT_FROM_SKILLS, (self.name,))
        (
            self.stats,
            self.number_of_steps,
            self.total,
            self.interval,
        ) = cursor.fetchone()
        self.load_url()
        self.load_notes()
        if self.number_of_steps is not None:
            self.load_steps()

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

    def add_stats(self, progress=None):
        if self.stats < 100:
            if progress is not None:
                self.stats += abs(((int(progress) / self.total)*100))
            else:
                self.stats += abs(((self.interval / self.total)*100))
            cursor.execute(UPDATE_STATS_SKILLS, (self.stats, self.name))

    def add_url(self, url):
        cursor.execute(INSERT_INTO_URLS, (self.name, '', '', url))

    def add_step_url(self, step_order, url):
        self.steps[step_order].add_url(url)


################ SHOWS ################

    def show_url(self):
        if self.url is not None:
            self.buffer += self.url + '\n\n'
        else:
            self.buffer += '\nthis skill does not have a reference url.'

    def show_notes(self):
        for note in self.notes:
            self.buffer += '\n' + note.show() + '\n\n'

    def show_details(self):
        bar = make_bar(self.name, self.stats)
        self.buffer += bar + '\n\n------------\n'
        for note in self.notes:
            self.buffer += note.show()
        self.buffer += '\n------------\n'
        for step in self.steps:
            self.buffer += step.show()
        self.buffer += f"update steps:{self.interval}\n"

    def get_buffer(self):
        buffer = self.buffer
        self.buffer = ''
        return buffer

################ STATIC METHODS ################

    @staticmethod
    def show_skills():
        for key in skills.keys():
            percent = int(skills[key])
            bar = make_bar(key, percent)
            return bar

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
            return str(e)
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
        url,):
        self.skill_name = skill_name
        self.url = url
        self.step_order = step_order
        self.objective = objective
    
################ UPDATES ################

    def add_url(self, url):
        cursor.execute(INSERT_INTO_URLS, (
            self.skill_name,
            self.skill_name,
            self.step_order,
            url,))

################ SHOWS ################

    def show(self):
        response = ''
        response += str(self.step_order) + '\n'
        response += str(self.objective) + '\n\n'
        if self.url != 'NULL' and self.url is not None:
            response += self.url
        return response

################ STATIC METHODS ################

    @staticmethod
    def define_steps(skill_name, number_of_steps, conn=None):
        for i in range(number_of_steps):
            objective = get_input(conn=conn, input_text=f'\nobjective for step number {i}\n')
            cursor.execute(INSERT_INTO_STEPS, (skill_name, i, objective))
            connection.commit()
        cursor.execute(UPDATE_STEPS_SKILLS, (skill_name, number_of_steps))


class Note:

    def __init__(
        self,
        note_id,
        text,):
        self.note_id = note_id
        self.text = text

################ SHOWS ################

    def show(self):
        return f"\nid:{self.note_id}{self.text}"
    
################ STATIC METHODS ################

    @staticmethod
    def define_note(skill_name, text):
        cursor.execute(INSERT_INTO_NOTES, (skill_name, text))
    
    @staticmethod
    def delete_note(note_id):
        cursor.execute(DELETE_FROM_NOTES, (note_id,))



class TaskApp:

    def __init__(self, conn=None):
        self.buffer = ''
        self.conn = conn
        self.doc = """Usage:
            gamified_life
            gamified_life --add <skill_name>
            gamified_life -u <skill_name> [<progress>]
            gamified_life -r <skill_name>
            gamified_life --steps <skill_name> <steps>
            gamified_life --show [<skill_name>]
            gamified_life --rename <old_skill_name> <new_skill_name>
            gamified_life --anote <skill_name>
            gamified_life --notes <skill_name>
            gamified_life --rnote <note_id>
            gamified_life --aurl --steps <skill_name> <step_order> <url>
            gamified_life --aurl <skill_name> <url>
            gamified_life --surl <skill_name>
            
        """
    
################ PRIVATE METHODS ################

    def _proccess(self, request=None):
        if request is not None:
            argv = request.split()[1:]
            opts = TaskApp._parse(self.doc, argv)
        else:
            opts = TaskApp._parse(self.doc)
        try:
            if opts['--add'] and Skill.skill_exists(opts['<skill_name>']):
                self.buffer += '\nthis skill exists.\n'
            elif opts['--add']:
                total = get_input(conn=self.conn, integer=True, input_text='\nEnter total amount of steps:\n')
                interval = get_input(conn=self.conn, integer=True, input_text='\nEnter the interval:\n')
                q_steps = get_input(conn=self.conn, input_text='\nDo you want to define steps?(y or n)\n')
                while q_steps not in ('y', 'n'):
                    q_steps = get_input(conn=self.conn, input_text='\nDo you want to define steps(y or n)?\n')
                Skill(opts['<skill_name>'], total, interval)
                if q_steps == 'y':
                    steps = get_input(conn=self.conn, input_text='\nEnter number of steps:\n')
                    Step.define_steps(opts['<skill_name>'], int(steps))
            elif opts['<skill_name>'] is None or Skill.skill_exists(opts['<skill_name>']):
                if opts['-u']:
                    if opts['<progress>']:
                        Skill(opts['<skill_name>']).add_stats(opts['<progress>'])
                    else:
                        Skill(opts['<skill_name>']).add_stats()
                elif opts['-r']:
                    Skill.delete_skill(opts['<skill_name>'])
                elif opts['--show']:
                    if opts['<skill_name>']:
                        skill = Skill(opts['<skill_name>'])
                        skill.show_details()
                        self.buffer += skill.get_buffer()
                    else:
                        self.buffer += Skill.show_skills()
                elif opts['--rename']:
                    Skill(opts['<old_skill_name>']).rename(opts['<new_skill_name>'])
                elif opts['--aurl'] and opts['--steps']:
                    Skill(opts['<skill_name>']).add_step_url(int(opts['<step_order>']), opts['<url>'])
                elif opts['--steps']:
                    Step.define_steps(opts['<skill_name>'], int(opts['<steps>']))
                elif opts['--aurl']:
                    Skill(opts['<skill_name>']).add_url(opts['<url>'])
                elif opts['--surl']:
                    skill = Skill(opts['<skill_name>'])
                    skill.show_url()
                    self.buffer += skill.get_buffer()
                elif opts['--notes']:
                    skill = Skill(opts['<skill_name>'])
                    skill.show_notes()
                    self.buffer += skill.get_buffer()
                elif opts['--rnote']:
                    Note.delete_note(opts['<note_id>'])
                elif opts['--anote']:
                    note = get_input(conn=self.conn, multi=True)
                    Note.define_note(opts['<skill_name>'], note)
                else:
                    if Skill.show_skills() is not None:
                        self.buffer += Skill.show_skills()
                    else:
                        self.buffer += self.doc
            else:
                self.buffer += '\nyou must first add this skill.\n'
        except Exception as e:
            self.buffer += '\nopt failure or app error\n' + str(e.args) + '\n'
        finally:
            try:
                flush()
            except Exception as e:
                self.buffer += '\napp failed to start.' + str(e) + '\n'

    def _get_buffer(self):
        buffer = self.buffer
        self.buffer = ''
        return buffer

    @staticmethod
    def _parse(doc, argv=None):
        return docopt(doc=doc, argv=argv, help=True, version='v1')

################ PUBLIC METHODS ################
   
    def prepare_response(self, request=None):
        self._proccess(request)
        return self._get_buffer()
