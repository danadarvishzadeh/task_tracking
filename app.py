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
import sys

from gamification import prepreation, TaskApp

if __name__ == "__main__":
    try:
        prepreation()
    except Exception as e:
        print(str(e))
        sys.exit()
    task = TaskApp()
    print(task.prepare_response())