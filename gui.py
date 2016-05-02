import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.codeinput import CodeInput
from kivy.extras.highlight import KivyLexer
from kivy.uix.listview import ListItemLabel
from kivy.clock import Clock
from kivy.uix.listview import ListItemButton
from kivy.properties import StringProperty, ObjectProperty
from kivy.adapters.listadapter import ListAdapter

class ListItemButtonCode(ListItemButton):
  pass


class VisualBlame(App):
  def __init__(self, file_path):
    super(VisualBlame, self).__init__()
    self.file_path = file_path
    self.codelines_list = ObjectProperty()

  def build(self):
    self.root = Builder.load_file('gui.kv')
    adapter = ListAdapter(data=self.getListData(),cls=ListItemButtonCode)
    self.codelines_list = self.root.ids.codelines_list
    self.codelines_list.adapter = adapter
    self.codelines_list.adapter.bind(on_selection_change=self.listCallback)

  def getListData(self):
    with open(self.file_path) as f:
      result = f.readlines()
      if len(result) > 1:
        for i in range(0, len(result) - 2):
          # can be done because if it is not the last line, it has a \n
          result[i] = result[i][:-1]
      print(result)
      return result

  def listCallback(self, adapter):
    print("Selection changed")
    print(adapter.data)
    print(adapter.selection)
    adapter.selection.is_selected = False
    # adapter.select_list(adapter.data[0])
