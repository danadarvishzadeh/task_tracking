import csv
import getopt
import os
import sys

interval = 10

main_file_address = '/home/dana/Documents/daftar/problems/gamificated.txt'
notes_address = '/home/dana/Documents/daftar/problems/gamificated_notes.txt'


def preperation():

    skill_file_exists = os.path.isfile(main_file_address)
    note_file_exists = os.path.isfile(notes_address)
    if not skill_file_exists or not note_file_exists:
        write_down()
    with open(main_file_address, 'r') as csv_file:
        csv_file.seek(0, 0)
        reader = csv.DictReader(csv_file)
        for row in reader:
            skills[row['skill']] = row['percent']
    with open(notes_address, 'r') as csv_file:
        csv_file.seek(0, 0)
        reader = csv.DictReader(csv_file)
        for row in reader:
            notes[row['skill']] = row['note']


def add_skill(skill_name):
    if skill_name not in skills.keys():
        skills[skill_name] = 0
        write_down()


def add_stats(skill_name):
    percent = int(skills[skill_name])
    if percent < 100:
        percent += interval
        skills[skill_name] = percent
        write_down()


def write_down():
    with open(main_file_address, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['skill', 'percent'])
        writer.writeheader()
        for key in skills.keys():
            writer.writerow({'skill': key, 'percent': skills[key]})
    with open(notes_address, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['skill', 'note'])
        writer.writeheader()
        for key in notes.keys():
            writer.writerow({'skill': key, 'note': notes[key]})


def show_skills():
    for key in skills.keys():
        percent = int(skills[key])
        bar = ((5-len(str(percent)))//2)*' '
        bar += '|' + ((percent//interval)-1)*'='
        if percent == 100:
            bar += '='
        elif percent > 0:
            bar += '»'
        bar += ((100-percent)//interval)*' ' + '|'
        bar = ('%').join([str(percent), bar])
        if percent != 100:
            bar = ' ' + bar
        print(f"{key} {(15-len(key))*'-'} {bar}")


def remove_skill(skill_name):
    if skill_name == 'all':
        skills.clear()
    else:
        del skills[skill_name]
    write_down()


def rename(names):
    old, new = names
    skills[new] = skills[old]
    del skills[old]
    write_down()


def add_note(skill_name, note):
    try:
        notes[skill_name] += "*" + note
    except KeyError:
        notes[skill_name] = note
    write_down()
    print('updated.')


def show_notes(skill_name):
    try:
        results = notes[skill_name].split("*")
        for i, note in enumerate(results):
            print(f"{i+1}{note}", end="\n\n")
    except KeyError:
        print('you have no notes.')
    except Exception as e:
        print(e.args)


def remove_note(data):
    skill_name, note_number = data
    try:
        results = notes[skill_name].split("*")
        del results[int(note_number)-1]
        notes[skill_name] = "*".join(results)
        write_down()
    except KeyError:
        print('you have no notes.')
    except Exception as e:
        print(e.args)


if __name__ == "__main__":
    global skills, notes
    notes = dict()
    skills = dict()
    preperation()
    argument_list = sys.argv[1:]
    options = 'ha:u:r:'
    long_options = ['rename', 'anote=', 'notes=', 'rnote']
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        for current_argument, current_value in arguments:
            if current_argument in ('-h'):
                print(
                    "-a for adding skills\n-u for updating a skill\n"
                    "-s for showing progress\n-r for removing skill\n"
                    "   --anote for adding a note\n--rnote for removing a note"
                )

            elif current_argument == '-a':
                add_skill(current_value)
            elif current_argument == '-u':
                add_stats(current_value)
            elif current_argument == '-r':
                remove_skill(current_value)
            elif current_argument == '--rename':
                rename(values)
            elif current_argument == '--anote':
                note = ''
                while True:
                    new_line = input()
                    if new_line == 'q':
                        break
                    note = "\n".join((note, new_line))
                add_note(current_value, note)
            elif current_argument == '--notes':
                show_notes(current_value)
            elif current_argument == '--rnote':
                remove_note(values)
    except getopt.error as err:
        print(str(err))
    finally:
        show_skills()