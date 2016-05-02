from time import sleep
from scheduler import Scheduler
from queue import Queue
from gui import VisualBlame

if __name__ == '__main__':
  scheduler = Scheduler(Queue(), None)
  gui = VisualBlame('main.py')
  gui.run()
  # while (True):
    # print ("in main loop")
    # sleep(1)