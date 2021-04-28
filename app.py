"""Usage:
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
    gamified_life --aurl <skill_name> <url>
    gamified_life --aurl --steps <skill_name> <step_order> <url>
    gamified_life --surl <skill_name>
    
"""
from docopt import docopt

from gamification import Note, Skill, Step, flush, get_input, prepreation

opts = docopt(__doc__, help=True, version='v0.1')

if __name__ == "__main__":
    prepreation()
    try:
        if opts['--add'] and Skill.skill_exists(opts['<skill_name>']):
            print('\nthis skill exists.\n')
        elif opts['--add']:
            total = int(input('\nEnter total amount of steps:\n'))
            interval = int(input('\nEnter the interval:\n'))
            s = Skill(opts['<skill_name>'], total, interval)
            q_steps = input('\nDo you want to define steps?(y or n)\n')
            while q_steps not in ('y', 'n'):
                q_steps = input('\nDo you want to define steps?\n')
            if q_steps == 'y':
                steps = input('\nEnter number of steps:\n')
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
                    Skill(opts['<skill_name>']).show_details()
                else:
                    Skill.show_skills()
            elif opts['--steps']:
                Step.define_steps(opts['<skill_name>'], int(opts['<steps>']))
            elif opts['--rename']:
                Skill(opts['<old_skill_name>']).rename(opts['<new_skill_name>'])
            elif opts['--aurl'] and opts['--steps']:
                Skill(opts['<skill_name>']).add_step_url(opts['<step_order>'], opts['url'])
            elif opts['--aurl']:
                Skill(opts['<skill_name>']).add_url(opts['<url>'])
            elif opts['--surl']:
                Skill(opts['<skill_name>']).show_url()
            elif opts['--notes']:
                Skill(opts['<skill_name>']).show_notes()
            elif opts['--rnote']:
                Note.delete_note(opts['<note_id>'])
            elif opts['--anote']:
                note = get_input()
                Note.define_note(opts['<skill_name>'], note)
            else:
                Skill.show_skills()
        else:
            print('\nyou must first add this skill.\n')
    except Exception as e:
        print('\nopt failure or app error', str(e.args), '\n')
    finally:
        try:
            flush()
        except Exception as e:
            print('\napp failed to start.', e.args, '\n')

