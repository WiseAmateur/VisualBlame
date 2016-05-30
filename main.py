import sys
import os.path
import logging
import pygit2
import argparse

from scheduler import Scheduler
from gui.root import VisualBlame
from events import EventManager
from modules.module_event_config import module_events
from gui.widget_event_config import widget_event_listeners, widget_event_triggers


# Function handling the input of the application. The application expects
# one command line argument containing the file path of the file to open
# the application with
def handle_argv():
  parser = argparse.ArgumentParser()
  parser.add_argument("file_path", type=str, help="Path to the file to start the application with")

  file_path = parser.parse_args().file_path

  if not os.path.isfile(file_path):
    logging.error("Input: invalid file path")
    sys.exit()

  return file_path


def read_file(file_path):
  with open(file_path) as f:
    return f.read().splitlines()


if __name__ == '__main__':
  file_path = handle_argv()
  file_path_abs = os.path.abspath(file_path)
  git_dir = pygit2.discover_repository(file_path)
  file_path_rel = file_path_abs[len(git_dir) - 5:]

  event_manager = EventManager()
  scheduler = Scheduler(git_dir, event_manager, module_events)

  data = read_file(file_path_abs)

  gui = VisualBlame(data=data, file_path_rel=file_path_rel, event_manager=event_manager,
                    widget_event_listeners=widget_event_listeners, widget_event_triggers=widget_event_triggers)
  gui.run()
