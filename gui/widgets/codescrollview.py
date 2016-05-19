from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from labelrecolorable import LabelRecolorable


class CodeListItem(BoxLayout):
  def __init__(self, **kwargs):
    super(CodeListItem, self).__init__(**kwargs)
    try:
      self.ids.linenum_label.text = kwargs["index_str"]
      self.ids.line_label.text = kwargs["line"]
      self.ids.line_label.bg_color = kwargs["bg_color"]
    # In case of a KeyError, do nothing as the labels are not required to have text
    except KeyError:
      pass


class CodeScrollView(ScrollView):
  def initCodeView(self, **kwargs):
    self._insertData(self._formatLineData(kwargs["data"]))

  def _insertData(self, data):
    codeline_container = self.ids.codeline_container

    for item_data in data:
      codeline_container.add_widget(CodeListItem(**item_data))

  def _removeAllData(self):
    self.ids.codeline_container.children = []

  # Change the data from [line] to [{index: index, line: line}]
  def _formatLineData(self, data):
    max_index_len = len(data)
    max_str_len = len(str(max_index_len))

    for index in range(max_index_len):
      index_str = str(index+1)
      # Prepend spaces to every str index that has smaller length than the max index
      for i in range(len(index_str), max_str_len):
        index_str = " " + index_str
      data[index] = {"index_str": index_str + "  ", "line": data[index]}

    return data