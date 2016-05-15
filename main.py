import sys
import os.path
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
    print "Expecting the path of the file to start with as a command line argument"
    sys.exit()

  file_path = sys.argv[1]

  if not os.path.isfile(file_path):
    print "Invalid file path"

  return file_path


if __name__ == '__main__':
  file_path = handleArgv()
  file_path_abs = os.path.abspath(file_path)
  git_dir = pygit2.discover_repository(file_path)
  file_path_rel = file_path_abs[len(git_dir) - 5:]

  event = EventManager()
  scheduler = Scheduler(git_dir, event)

  gui = VisualBlame(file_path_abs, file_path_rel, event)
  gui.run()