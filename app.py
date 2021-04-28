import getopt
import os
import sys
import docopt
from gamification import Skill, prepreation, flush

if __name__ == "__main__":
    prepreation()
    argument_list = sys.argv[1:]
    options = 'ha:u:r:'
    long_options = [
        'rename',
        'anote=',
        'notes=',
        'rnote=',
        'aurl=',
        'surl=',
    ]
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        for current_argument, current_value in arguments:
            if current_argument in ('-h'):
                print('-a for adding skills\n-u for updating a skill\n-s for showing progress\n-r for removing skill')
            elif current_argument == '-a':
                Skill(current_value)
            elif current_argument == '-u':
                Skill(current_value).add_stat()
            elif current_argument == '-r':
                Skill.remove_skill(current_value)
            elif current_argument == '--rename':
                Skill.rename(values)
            elif current_argument == '--aurl':
                Skill(current_value).set_url(values[0])
            elif current_argument == '--surl':
                Skill(current_value).show_url()
            elif current_argument == '--anote':
                note = ''
                while True:
                    new_line = input()
                    if new_line == 'q':
                        break
                    note = "\n".join((note, new_line))
                Skill(current_value).add_note(note)
            elif current_argument == '--notes':
                Skill(current_value).show_notes()
            elif current_argument == '--rnote':
                Skill.delete_note(current_value)
    except getopt.error as err:
        print('opt faliure', str(err))
    finally:
        try:
            flush()
            skills = Skill.get_all_skills()
            Skill.show_skills()
        except Exception as e:
            print('app failed.', e)
