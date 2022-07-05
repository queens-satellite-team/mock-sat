import importlib
from src.obc.taskmanager import TaskManager
from src.comms.radio import RF24
from colorama import Fore
from datetime import datetime
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

def print_boot_message(msg:str):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    print('[' + Fore.GREEN + f'{ts:.0f}' + Fore.WHITE +'] ' + msg)

def print_fatal_error(msg:str):
    print(Fore.RED+msg+Fore.WHITE)


def main():
    print_header()
    print_boot_message('booting up mock-sat')
    try:
        from src.common.satellite import mock_sat
    except Exception as e:
        print_fatal_error('! FAILED TO BOOT !')
        raise e

    print_boot_message('booting up OBC')
    mock_sat.obc = TaskManager(debug=False)

    print_boot_message('setting up satellite system resources')
    print('\t     └── comms')
    radio = RF24()
    mock_sat.comms = radio

    print_boot_message('loading tasks...')
    mock_sat.scheduled_tasks = {}
    # schedule all tasks in directory
    for file in os.listdir('tasks'):
        # remove the '.py' from file name
        file=file[:-3]

        # ignore these files
        if file in ('template_task') or file.startswith('_'):
            continue

        # auto-magically import the task file
        exec('import tasks.{}'.format(file))
        print('{}{}'.format('\t     └── ',file))

        # create a helper object for scheduling the task
        task_obj=eval('tasks.'+file).task(mock_sat)

        # schedule each task object and add it to our dict
        mock_sat.scheduled_tasks[task_obj.name] = mock_sat.obc.schedule(task_obj.frequency, task_obj.main_task, task_obj.priority)
    
    print_boot_message( str(len(mock_sat.scheduled_tasks)) + ' tasks loaded...')
    print('[' + Fore.YELLOW + ' --- RUNNING TASKS --- ' + Fore.WHITE + ']')
    mock_sat.obc.run()
    print_footer()

if __name__ == '__main__':
    main()