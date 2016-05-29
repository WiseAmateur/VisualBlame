from collections import namedtuple

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from gui.widgets.recolorablebg import LabelRecolorable


class CodeListItem(BoxLayout):
  def __init__(self, str_index="", line="", **kwargs):
    super(CodeListItem, self).__init__(**kwargs)
    self.ids.linenum_label.text = str_index
    self.ids.line_label.text = line


class CodeContainer(GridLayout):
  pass


class CodeScrollView(ScrollView):
  item_container_cls = CodeContainer
  line_item_cls = CodeListItem

  def __init__(self, **kwargs):
    super(CodeScrollView, self).__init__(**kwargs)
    self.item_container = self.item_container_cls()
    self.add_widget(self.item_container)

  def init_code_view(self, data=None, **kwargs):
    self._insert_lines(self._format_line_data(data))

  def _insert_lines(self, lines):
    self._remove_all_lines()

    for line in lines:
      self._insert_line(**line._asdict())

  def _insert_line(self, **kwargs):
    self.item_container.add_widget(self.line_item_cls(**kwargs))

  def _remove_all_lines(self):
    self.item_container.children = []

  # Change the data from [line] to [namedtuple(index, line)]
  def _format_line_data(self, lines):
    FormattedLine = namedtuple('FormattedLine', ['str_index', 'line'])
    max_index = len(lines)
    max_str_len = len(str(max_index))

    for index in range(max_index):
      index_str = str(index+1)
      # Prepend spaces if necessary so that every index has the same str length
      # Append spaces to every index to create space between the index and line
      index_str = (max_str_len - len(index_str)) * " " + index_str + "  "
      lines[index] = FormattedLine(index_str, lines[index])

    return lines
