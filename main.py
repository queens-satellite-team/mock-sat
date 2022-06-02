import imp
from src.comms.radio import Radio

def print_header():
    print('--------------------------------')
    print('\tQSAT Mock-Sat Program')
    print('--------------------------------')
    print()

def print_footer():
    print()
    print('--------------------------------')
    print('--------------------------------')

def main():
    print_header()

    comms = Radio()
    comms.transmit()
    comms.receive()

    print_footer()

if __name__ == '__main__':
    main()