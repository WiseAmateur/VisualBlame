import logging
import kivy
kivy.require('1.9.1')

from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.app import App

from widgets.blamecodescrollview import BlameCodeScrollView
from widgets.diffcodescrollview import DiffCodeScrollView
from widgets.commitcontextview import CommitContextView
from widgets.buttontabpanel import ButtonTabPanel
from widgets.codescrollview import CodeScrollView


class VisualBlame(App):
  def __init__(self, event_manager = None, **kwargs):
    self.init_args = kwargs
    self.event_manager = event_manager
    super(VisualBlame, self).__init__()

  def build(self):
    self.root = Builder.load_file('gui/gui.kv')

    file_path_rel = self.init_args["file_path_rel"]

    self.root.ids.blame_codelines_list.initCodeView(**self.init_args)
    self.root.ids.diff_codelines_list.initCodeView(data=[])
    self.init_args = None
    # TODO use file similar to modules in which the top widget event listeners are?
    self.registerForEvent("diff_result", self.root.ids.diff_files.updateTabPanel)
    self.registerForEvent("commit_context_result", self.root.ids.blame_commit_context.updateCommitContext)
    self.registerForEvent("commit_context_result", self.root.ids.diff_commit_context.updateCommitContext)

    self.root.ids.blame_commit_context.head = True
    # TODO use a different method to let different widgets call each other
    self.root.ids.diff_files.update_view = self.root.ids.diff_codelines_list.initCodeView
    self.root.ids.diff_files.active_file = file_path_rel
    self.root.ids.blame_history.active_file = file_path_rel
    self.root.ids.blame_history.updateTabPanel(data=[file_path_rel])
    self.triggerEvent("commit_context", {"commit_id": "HEAD"})


  def registerForEvent(self, event, function):
    try:
      self.event_manager.registerForEvent(event, function)
    except AttributeError:
      logging.warn("VisualBlame: incorrect event manager set")

  def triggerEvent(self, event, data=None):
    try:
      self.event_manager.triggerEvent(event, data)
    except AttributeError:
      logging.warn("VisualBlame: incorrect event manager set")
