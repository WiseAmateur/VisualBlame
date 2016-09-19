from pygit2 import discover_repository, Repository
from argparse import ArgumentParser
from os import path
import logging
import sys
import os

from scheduler import Scheduler
from gui.root import VisualBlame
from events import EventManager
from modules.module_event_config import module_events
from gui.widget_event_config import widget_event_listeners
from gui.widget_event_config import widget_event_triggers


# Function handling the input of the application. The application expects
# one command line argument containing the file path of the file to open
# the application with
def handle_argv():
    parser = ArgumentParser()
    parser.add_argument("file_path", type=str,
                        help="Path to the file to start the application with")

    file_path = parser.parse_args().file_path

    if not path.isfile(file_path):
        logging.error("Input: invalid file path")
        sys.exit()

    return file_path


# Handle the input arguments and initialize the scheduler and GUI
if __name__ == '__main__':
    file_path = handle_argv()
    file_path_abs = path.abspath(file_path)
    git_dir = discover_repository(file_path, True)
    file_path_rel = file_path_abs[len(git_dir) - 5:]

    repo = Repository(git_dir)
    head_commit_id = repo.revparse_single("HEAD").id.hex

    event_manager = EventManager()
    scheduler = Scheduler(repo, event_manager, module_events)

    gui = VisualBlame(file_path_rel=file_path_rel,
                      commit_id=head_commit_id,
                      event_manager=event_manager,
                      widget_event_listeners=widget_event_listeners,
                      widget_event_triggers=widget_event_triggers)
    gui.run()
