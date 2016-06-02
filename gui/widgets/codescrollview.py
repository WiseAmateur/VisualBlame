from collections import namedtuple

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from gui.widgets.recolorablebg import LabelRecolorable


class CodeListItem(BoxLayout):
  line_bg_color = [0, 0, 0]

  def __init__(self, str_index="", line="", **kwargs):
    self.linenum_text = str_index
    self.line_text = line
    super(CodeListItem, self).__init__(**kwargs)


class CodeContainer(GridLayout):
  pass


class CodeScrollView(ScrollView):
  item_container_cls = CodeContainer
  line_item_cls = CodeListItem

  def init_code_view(self, data=None, **kwargs):
    self._remove_all_lines()

    self.item_container = self.item_container_cls()

    for line in self._format_line_data(data):
      self._insert_line(**line._asdict())

    self.add_widget(self.item_container)

  def _insert_line(self, **kwargs):
    self.item_container.add_widget(self.line_item_cls(**kwargs))

  def _remove_all_lines(self):
    # The first time there is no item_container yet, catch that error
    try:
      self.remove_widget(self.item_container)
    except AttributeError:
      pass

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
