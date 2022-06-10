import importlib
from src.obc.taskmanager import TaskManager
from colorama import Fore
import os

def print_header():
    print(Fore.CYAN + '-------------------------------------' + Fore.WHITE, flush=True)
    print(Fore.GREEN + '\tQSAT Mock-Sat Program' + Fore.WHITE, flush=True)
    print(Fore.CYAN + '-------------------------------------' + Fore.WHITE, flush=True)
    print()

def print_footer():
    print()
    print(Fore.CYAN + '-------------------------------------' + Fore.WHITE, flush=True)
    print(Fore.CYAN + '-------------------------------------' + Fore.WHITE, flush=True)

def main():
    print_header()
    print('['+Fore.GREEN+'000000'+Fore.WHITE+'] booting up mock-sat')
    try:
        from src.common.satellite import mock_sat
        mock_sat.scheduled_tasks={}
    except Exception as e:
        print(Fore.RED+'! FAILED TO BOOT !'+Fore.WHITE)

    print('['+Fore.GREEN+'000001'+Fore.WHITE+'] booting up OBC')
    obc = TaskManager()

    print('['+Fore.GREEN+'000002'+Fore.WHITE+'] loading tasks...')
    # schedule all tasks in directory
    for file in os.listdir('tasks'):
        # remove the '.py' from file name
        file=file[:-3]

        # ignore these files
        if file in ('template_task') or file.startswith('_'):
            continue

        # auto-magically import the task file
        exec('import tasks.{}'.format(file))
        print('{}{}'.format('\t└── ',file))

        # create a helper object for scheduling the task
        task_obj=eval('tasks.'+file).task(mock_sat)

        # schedule each task object and add it to our dict
        mock_sat.scheduled_tasks[task_obj.name] = obc.schedule(task_obj.frequency, task_obj.main_task, task_obj.priority)
    
    print(len(mock_sat.scheduled_tasks),'tasks loaded...')
    print('['+Fore.YELLOW+'--- RUNNING TASKS ---'+Fore.WHITE+']')
    obc.run()
    print_footer()

if __name__ == '__main__':
    main()