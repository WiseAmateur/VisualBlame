import logging

from gui.eventwidget import EventWidget
from kivy.uix.button import Button
from kivy.app import App


class SwitchButton(Button):
    def switch_commit_context_views(self, from_view, to_view):
        # try:
        visualblame = App.get_running_app()
        commit_context_data = visualblame.get_view_by_id(from_view).get_data()
        visualblame.get_view_by_id(to_view).process_event_result(
            [commit_context_data])
        # except:


class BlameCommitSwitchButton(SwitchButton, EventWidget):
    def on_press(self):
        self.switch_commit_context_views("blame_commit_context",
                                         "diff_commit_context")
        visualblame = App.get_running_app()
        args = {"commit_id": visualblame.get_view_by_id(
            "blame_commit_context").get_commit_id()}
        self.event_call(args)
        self.event_call(args, 1)


class DiffCommitSwitchButton(SwitchButton, EventWidget):
    # Get Diff file without removed lines. Get commit so you know when to start
    # looking.
    def on_press(self):
        try:
            blame_history_args = self.from_tabpanel.get_data()
            if blame_history_args:
                self.switch_commit_context_views("diff_commit_context",
                                                 "blame_commit_context")
                self.to_tabpanel.add_commit_file(**blame_history_args)
                args = {"amount": 10,
                        "commit_id": blame_history_args["commit_id"]}
                self.event_call(args)
            else:
                logging.warn("Switchbutton: diff data not set")
        except AttributeError:
            logging.warn("SwitchButton: codescrollviews not set")
