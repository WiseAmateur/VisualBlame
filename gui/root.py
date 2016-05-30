import kivy
kivy.require('1.9.1')

from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.app import App

from gui.widgets.blamecodescrollview import BlameCodeScrollView
from gui.widgets.diffcodescrollview import DiffCodeScrollView
from gui.widgets.commitcontextview import CommitContextView
from gui.widgets.initcommitcontextview import InitCommitContextView
from gui.widgets.buttontabpanel import ButtonTabPanel
from gui.widgets.codescrollview import CodeScrollView
from gui.widgets.switchbutton import SwitchButton
from gui.widgets.commitboxview import CommitBoxView


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
    self.init_args = None

    self._register_result_events()
    self._register_call_events()

    # TODO use a different method to let different widgets call each other
    self.root.ids.diff_files.view_to_update = self.root.ids.diff_codelines_list
    self.root.ids.diff_files.active_file = file_path_rel
    self.root.ids.blame_history.active_file = file_path_rel
    self.root.ids.blame_history.receive_event_result(data=[file_path_rel])

    self.root.ids.diff_files.commit_view = self.root.ids.diff_commit_context
    self.root.ids.diff_to_blame.set_scroll_views(self.root.ids.diff_files,
                                               self.root.ids.blame_codelines_list)

  # The register functions assume the event manager is set correctly
  # and the widget ids are correct
  def _register_result_events(self):
    for widget_id in self.widget_event_listeners:
      self.event_manager.register_for_result_event(self.widget_event_listeners[widget_id],
                                                   self.root.ids[widget_id].receive_event_result)

  def _register_call_events(self):
    for widget_id in self.widget_event_triggers:
      self.root.ids[widget_id].init_event_call(self.widget_event_triggers[widget_id],
                                             self.event_manager.trigger_call_event)
