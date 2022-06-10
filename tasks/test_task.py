from tasks.template_task import Task
import time

class task(Task):
    priority = 4
    frequency = 1/30 # once every 30s
    name = 'test'
    color = 'green'

    async def main_task(self):
        self.debug('test start: {}'.format(time.monotonic()))
        time.sleep(1)
        self.debug('test stop: {}'.format(time.monotonic()))