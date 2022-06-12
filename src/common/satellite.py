import time 

class Satellite:
    def __init__(self):
        self.boot_time = int(time.time())
        self.scheduled_tasks = {}
        self.adcs = None
        self.comms = None
        self.obc = None
        self.payload = None
        self.eps = None

mock_sat = Satellite()