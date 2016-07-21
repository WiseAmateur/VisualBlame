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


# TODO instead of one generic switch button, just make two custom ones for the
# different functionalities..
class DiffCommitSwitchButton(SwitchButton, EventWidget):
    # Get Diff file without removed lines. Get commit so you know when to start
    # looking.
    def on_press(self):
        try:
            scrollview_args = self.from_scrollview.get_data()
            if scrollview_args:
                self.switch_commit_context_views("diff_commit_context",
                                                 "blame_commit_context")
                self.from_scrollview.remove_data()
                self.to_scrollview.init_code_view(**scrollview_args._asdict())
                args = {"amount": 10,
                        "commit_id": scrollview_args.newest_commit}
                self.event_call(args)
            else:
                logging.warn("Switchbutton: diff data not set")
        except AttributeError:
            logging.warn("SwitchButton: codescrollviews not set")
