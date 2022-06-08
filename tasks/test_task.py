from .template_task import Task
import time

class task(Task):
    priority = 4
    frequency = 1/30 # once every 30s
    name = 'test'
    color = 'green'

    schedule_later = True

    def main_task(self):
        self.debug('test start: {}'.format(time.monotonic()))
        time.sleep(10)
        self.debug('test stop: {}'.format(time.monotonic()))