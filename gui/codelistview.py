from kivy.uix.listview import ListView, ListItemReprMixin
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.adapters.listadapter import ListAdapter
from kivy.graphics import Color, Rectangle, Callback
from kivy.clock import Clock
from kivy.app import App

from labelrecolorable import LabelRecolorable


class CodeNumLabel(LabelRecolorable):
  pass


class CodeLineLabel(LabelRecolorable):
  pass


class CodeListItem(BoxLayout):
  def __init__(self, **kwargs):
    super(CodeListItem, self).__init__(**kwargs)
    self.ids.linenum_label.text = kwargs["text"]["index"]
    self.ids.line_label.text = kwargs["text"]["line"]


class CodeItemContainer(GridLayout):
  pass


class CodeScrollView(ScrollView):
  def initCodeView(self, **kwargs):
    data = self._format_line_data(kwargs["data"])

    codeline_container = self.ids.codeline_container

    for codeline in data:
      codeline_container.add_widget(CodeListItem(text=codeline))

  def _format_line_data(self, data):
    max_index_len = len(data)
    max_str_len = len(str(max_index_len))

    for index in range(max_index_len):
      index_str = str(index+1)
      # Prepend spaces to every str index that has smaller length than the max index
      for i in range(len(index_str), max_str_len):
        index_str = " " + index_str
      data[index] = {"index": index_str + "  ", "line": data[index]}

    return data