from gui.widgets.blamecodescrollview import BlameCodeScrollView
from gui.widgets.diffcodescrollview import DiffCodeScrollView
from gui.widgets.commitcontextview import CommitContextView
from gui.widgets.initcommitcontextview import InitCommitContextView
from gui.widgets.buttontabpanel import ButtonTabPanel
from gui.widgets.diffbuttontabpanel import DiffButtonTabPanel
from gui.widgets.blamebuttontabpanel import BlameButtonTabPanel
from gui.widgets.codescrollview import CodeScrollView
from gui.widgets.switchbutton import SwitchButton
from gui.widgets.commitboxview import CommitBoxView
from kivy.lang import Builder
from kivy.app import App

import kivy
kivy.require('1.9.1')


class VisualBlame(App):
    def __init__(self, event_manager=None, widget_event_listeners=[],
                 widget_event_triggers=[], file_path_rel="", commit_id=""):
        self.init_file_path = file_path_rel
        self.init_commit_id = commit_id
        self.event_manager = event_manager

        # Can't register the events here, as the widgets are not built yet
        self.widget_event_listeners = widget_event_listeners
        self.widget_event_triggers = widget_event_triggers

        super(VisualBlame, self).__init__()

    def build(self):
        self.root = Builder.load_file('gui/root.kv')

        self._register_result_events()
        self._register_call_events()

        self.root.ids.blame_history.add_commit_file(self.init_file_path,
                                                    self.init_commit_id)
        self.init_file_path = None
        self.init_commit_id = None

    def get_view_by_id(self, view_id):
        if view_id in self.root.ids:
            return self.root.ids[view_id]

        return None

    # The register functions assume the event manager is set correctly
    # and the widget ids are correct
    def _register_result_events(self):
        for widget_id in self.widget_event_listeners:
            self.event_manager.register_for_result_event(
                self.widget_event_listeners[widget_id],
                self.root.ids[widget_id].receive_event_result)

        self.widget_event_listeners = None

    def _register_call_events(self):
        for widget_id in self.widget_event_triggers:
            self.root.ids[widget_id].init_event_call(
                self.widget_event_triggers[widget_id],
                self.event_manager.trigger_call_event)

        self.widget_event_triggers = None
