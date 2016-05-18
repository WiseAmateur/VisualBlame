import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label

from codelistview import CodeScrollView
from blamecodelistview import BlameCodeScrollView
from diffcodelistview import DiffCodeListView
from commitcontextview import CommitContextView


class LabelRecolorable(Label):
  pass


class VisualBlame(App):
  def __init__(self, **kwargs):
    self.init_args = kwargs
    self.event_manager = kwargs["event_manager"]
    super(VisualBlame, self).__init__()

  def build(self):
    self.root = Builder.load_file('gui/gui.kv')

    self.root.ids.blame_codelines_list.initCodeView(**self.init_args)
    self.root.ids.diff_codelines_list.initCodeView(data=[])
    self.init_args = None

  def registerForEvent(self, event, function):
    self.event_manager.registerForEvent(event, function)

  def triggerEvent(self, event, data=None):
    self.event_manager.triggerEvent(event, data)