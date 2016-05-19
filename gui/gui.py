import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label

from widgets.buttontabpanel import ButtonTabPanel
from widgets.codescrollview import CodeScrollView
from widgets.blamecodescrollview import BlameCodeScrollView
from widgets.diffcodescrollview import DiffCodeScrollView
from widgets.commitcontextview import CommitContextView


class LabelRecolorable(Label):
  pass


class VisualBlame(App):
  def __init__(self, **kwargs):
    self.init_args = kwargs
    self.event_manager = kwargs["event_manager"]
    super(VisualBlame, self).__init__()

  def build(self):
    self.root = Builder.load_file('gui/gui.kv')

    file_path_rel = self.init_args["file_path_rel"]

    self.root.ids.blame_codelines_list.initCodeView(**self.init_args)
    self.root.ids.diff_codelines_list.initCodeView(data=[])
    self.init_args = None
    # TODO use file similar to modules in which the top widget event listeners are?
    self.registerForEvent("diff_result", self.root.ids.diff_files.updateTabPanel)
    # TODO use a different method to let different widgets call each other
    self.root.ids.diff_files.update_view = self.root.ids.diff_codelines_list.updateListData
    self.root.ids.diff_files.active_file = file_path_rel

  def registerForEvent(self, event, function):
    self.event_manager.registerForEvent(event, function)

  def triggerEvent(self, event, data=None):
    self.event_manager.triggerEvent(event, data)