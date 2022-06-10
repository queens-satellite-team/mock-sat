from tasks.template_task import Task
import time

class task(Task):
    priority = 1
    frequency = 1/5 # once every 5s
    name = 'radio'
    color = 'red'

    async def main_task(self):
        self.debug('radio start: {}'.format(time.monotonic()))
        self.debug('Sending beacon')
        time.sleep(1)
        self.debug('radio stop: {}'.format(time.monotonic()))