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
  def __init__(self, git_dir, file_path, event_manager):
    self.file_path = file_path
    self.git_dir = git_dir
    self.event_manager = event_manager
    super(VisualBlame, self).__init__()

  def build(self):
    self.root = Builder.load_file('gui/gui.kv')

    self.root.ids.codelines_list.initCodeView(self.git_dir, self.file_path)

  def registerForEvent(self, event, function):
    self.event_manager.registerForEvent(event, function)

  def triggerEvent(self, event, data=None):
    self.event_manager.triggerEvent(event, data)