import sys
import os.path
import logging
import pygit2

from time import sleep
from scheduler import Scheduler
from gui.gui import VisualBlame
from events import EventManager


# Function handling the input of the application. The application expects
# one command line argument containing the file path of the file to open
# the application with
def handleArgv():
  if len(sys.argv) != 2:
    logging.error("Input: Wrong input, expecting path of file as argument")
    sys.exit()

  file_path = sys.argv[1]

  if not os.path.isfile(file_path):
    logging.error("Input: invalid file path")
    sys.exit()

  return file_path


def readFile(file_path):
    with open(file_path) as f:
      return f.read().splitlines()


if __name__ == '__main__':
  file_path = handleArgv()
  file_path_abs = os.path.abspath(file_path)
  git_dir = pygit2.discover_repository(file_path)
  file_path_rel = file_path_abs[len(git_dir) - 5:]

  event_manager = EventManager()
  scheduler = Scheduler(git_dir, event_manager)

  data = readFile(file_path_abs)

  gui = VisualBlame(data=data, file_path_rel=file_path_rel, event_manager=event_manager)
  gui.run()
