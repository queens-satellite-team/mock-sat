from ..common.arduino import Arduino

class RF24(Arduino):
    def __init__(self):
        super().__init__()
        print('called radio init!')

    def transmit(self):
        print('radio is transmitting!')

    def receive(self):
        print('radio is receiving!')