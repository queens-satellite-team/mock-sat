import importlib
from src.satellite import mock_sat
from src.comms.radio import Radio
from colorama import Fore
import os

def print_header():
    print(Fore.RED + '-------------------------------------' + Fore.WHITE, flush=True)
    print(Fore.CYAN + '\tQSAT Mock-Sat Program', flush=True)
    print(Fore.RED + '-------------------------------------' + Fore.WHITE, flush=True)
    print()

def print_footer():
    print()
    print(Fore.RED + '-------------------------------------' + Fore.WHITE, flush=True)
    print(Fore.RED + '-------------------------------------' + Fore.WHITE, flush=True)

def main():
    print_header()

    print('['+Fore.GREEN+'000000'+Fore.WHITE+'] Loading Tasks... ')
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
    

    print('['+Fore.GREEN+'000001'+Fore.WHITE+'] Running Tasks... ')
    print()

    comms = Radio()
    comms.transmit()
    comms.receive()

    print_footer()

if __name__ == '__main__':
    main()