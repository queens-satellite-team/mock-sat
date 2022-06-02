import imp
from src.comms.radio import Radio
from src.payload.img_compr_raspi import PiCam

def print_header():
    print('--------------------------------')
    print('\tQSAT Mock-Sat Program')
    print('--------------------------------')
    print()

def print_footer():
    print('--------------------------------')
    print('--------------------------------')

def main():
    print_header()

    comms = Radio()
    comms.transmit()
    comms.receive()

    payload = PiCam()

    print_footer()

if __name__ == '__main__':
    main()