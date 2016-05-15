import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label

from codelistview import CodeListView
from commitcontextview import CommitContextView


class LabelRecolorable(Label):
  pass


class VisualBlame(App):
  def __init__(self, file_path_abs, file_path_rel, event_manager):
    self.file_path_rel = file_path_rel
    self.file_path_abs = file_path_abs
    self.event_manager = event_manager
    super(VisualBlame, self).__init__()

  def build(self):
    self.root = Builder.load_file('gui/gui.kv')

    self.root.ids.codelines_list.initCodeView(self.file_path_abs, self.file_path_rel)

  def registerForEvent(self, event, function):
    self.event_manager.registerForEvent(event, function)

  def triggerEvent(self, event, data=None):
    self.event_manager.triggerEvent(event, data)