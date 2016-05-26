import logging
import kivy
kivy.require('1.9.1')

from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.app import App

from gui.widgets.blamecodescrollview import BlameCodeScrollView
from gui.widgets.diffcodescrollview import DiffCodeScrollView
from gui.widgets.commitcontextview import CommitContextView
from gui.widgets.buttontabpanel import ButtonTabPanel
from gui.widgets.codescrollview import CodeScrollView
from gui.widgets.switchbutton import SwitchButton


class VisualBlame(App):
  def __init__(self, event_manager=None, widget_event_listeners=[],
               widget_event_triggers=[], **kwargs):
    self.init_args = kwargs
    self.event_manager = event_manager
    # Can't register the events here, as the widgets are not built yet
    self.widget_event_listeners = widget_event_listeners
    self.widget_event_triggers = widget_event_triggers
    super(VisualBlame, self).__init__()

  def build(self):
    self.root = Builder.load_file('gui/root.kv')

    file_path_rel = self.init_args["file_path_rel"]

    self.root.ids.blame_codelines_list.init_code_view(**self.init_args)
    self.root.ids.diff_codelines_list.init_code_view(data=[])
    self.init_args = None

    self._register_result_events()
    self._register_call_events()

    self.root.ids.blame_commit_context.head = True
    # TODO use a different method to let different widgets call each other
    self.root.ids.diff_files.view_to_update = self.root.ids.diff_codelines_list
    self.root.ids.diff_files.active_file = file_path_rel
    self.root.ids.blame_history.active_file = file_path_rel
    self.root.ids.blame_history.receive_event_result(data=[file_path_rel])
    self.trigger_event("commit_context", {"commit_id": "HEAD"})

    self.root.ids.diff_files.commit_view = self.root.ids.diff_commit_context
    self.root.ids.diff_to_blame.set_scroll_views(self.root.ids.diff_files,
                                               self.root.ids.blame_codelines_list)


  def _register_result_events(self):
    try:
      for view_id in self.widget_event_listeners:
        self.event_manager.register_for_result_event(self.widget_event_listeners[view_id],
                                                  self.root.ids[view_id].receive_event_result)
    except AttributeError:
      logging.warn("VisualBlame: incorrect event manager set, unable to register result events")

  def _register_call_events(self):
    try:
      for view_id in self.widget_event_triggers:
        self.root.ids[view_id].init_event_call(self.event_manager.trigger_call_event,
                                               view_id, self.widget_event_triggers[view_id])
    except AttributeError:
      logging.warn("VisualBlame: incorrect event manager set, unable to register call events")

  # TODO ADD MECHANISM FOR CHAIN TRIGGERS SO THAT THIS FUNCTION CAN BE REMOVED
  # ALTHOUGH IT IS ALSO USED FOR FIRST TIME COMMIT CONTEXT, ADD MECHANISM FOR INIT TRIGGERS THEN TOO...
  def trigger_event(self, event, data=None, caller_id=""):
    try:
      self.event_manager.triggerCallEvent(event, data, caller_id)
    except AttributeError:
      logging.warn("VisualBlame: incorrect event manager set")
