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


class LabelRecolorable(Label):
  pass


class VisualBlame(App):
  def __init__(self, file_path):
    super(VisualBlame, self).__init__()
    self.file_path = file_path
    self.codelines_list = ObjectProperty()
    self.commit_info = ObjectProperty()
    self.select_done = 1
    self.counter = 0

  def build(self):
    self.root = Builder.load_file('gui.kv')

    adapter = ListAdapter(data=self.getListData(),selection_mode='multiple',
                          cls=ListItemButtonCode)
    self.codelines_list = self.root.ids.codelines_list
    self.codelines_list.adapter = adapter
    self.codelines_list.adapter.bind(on_selection_change=self.listCallback)
    self.commit_info = self.root.ids.blame_info

  def getListData(self):
    with open(self.file_path) as f:
      result = f.readlines()
      if len(result) > 1:
        for i in range(0, len(result) - 1):
          # can be done because if it is not the last line, it has a \n
          result[i] = result[i][:-1]
      print(result)
      return result

  def listCallback(self, adapter):
    self.counter += 1;
    print("Selection changed, counter: {}".format(self.counter))
    if len(adapter.selection) > 0:
      self.commit_info.text = adapter.selection[0].text
      # print (self.select_done)
      # if self.select_done is 1:
      if not adapter.get_view(0) in adapter.selection:
        # print("selecting first item")
        adapter.select_list([adapter.get_view(0)], False)
    # self.select_done = 1 - self.select_done
    # print(adapter.data)
    # print(adapter.selection)
    # adapter.selection.is_selected = False
    # doesn't work: adapter.select_list(adapter.data[0])
