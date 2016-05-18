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


class CodeNumLabel(Label):
  pass


class CodeLineLabel(Label):
  pass


class CodeListItem(BoxLayout):
  cls_line_label = CodeLineLabel
  bgcolor = (1, 0, 0)

  def __init__(self, **kwargs):
    super(CodeListItem, self).__init__(**kwargs)
    self.ids.linenum_label.text = kwargs["text"]["index"]
    self.ids.line_label.text = kwargs["text"]["line"]


class CodeScrollView(ScrollView):
  def initCodeView(self, **kwargs):
    data = self._format_line_data(kwargs["data"])

    codeline_container = self.ids.codeline_container

    for codeline in data:
      codeline_container.add_widget(CodeListItem(text=codeline))
    # print data

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

class CodeItemContainer(GridLayout):
  pass


class CodeListView(ListView):
  cls_adapter = ListAdapter
  cls_item = CodeListItem
  selection_mode = "none"

  def initCodeView(self, **kwargs):
    data = self._format_line_data(kwargs["data"])

    self.adapter = self.cls_adapter(data=data, selection_mode=self.selection_mode, cls=self.cls_item)

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