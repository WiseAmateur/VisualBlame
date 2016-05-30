from collections import namedtuple

from kivy.adapters.listadapter import ListAdapter
from kivy.app import App

from gui.widgets.codescrollview import CodeScrollView, CodeListItem


class DiffCodeListItem(CodeListItem):
  def __init__(self, bg_color=(0, 0, 0), **kwargs):
    super(DiffCodeListItem, self).__init__(**kwargs)
    if bg_color != (0, 0, 0):
      self.ids.linenum_label.bg_color = bg_color
    self.ids.line_label.bg_color = bg_color


class DiffCodeScrollView(CodeScrollView):
  color_mapping = {"+": [0.5, 0.6, 0.25], "-": [0.6, 0.1, 0.1], " ": [0, 0, 0]}
  line_item_cls = DiffCodeListItem

  def _format_line_data(self, data):
    ColoredLine = namedtuple('ColoredLine', ['str_index', 'line', 'bg_color'])
    list_data = []
    line_num = 1

    for diff_hunk in data:
      bg_color = self.color_mapping[diff_hunk.origin]
      if diff_hunk.origin != "-":
        for line in diff_hunk.lines:
          list_data.append(ColoredLine(str(line_num), line, bg_color))
          line_num += 1
      # Removed lines don't get a line number
      else:
        for line in diff_hunk.lines:
          list_data.append(ColoredLine(" ", line, bg_color))

    max_str_len = len(str(line_num))

    # Append and prepend spaces to the line number to make them all equal str length
    for i in range(len(list_data)):
      line = list_data[i]
      final_str_index = " " * (max_str_len - len(line.str_index)) + line.str_index + "  "
      list_data[i] = line._replace(str_index=final_str_index)

    return list_data

  def get_lines(self):
    items = self.item_container.children
    result = []
    for item in items[::-1]:
      if item.ids.line_label.bg_color != self.color_mapping["-"]:
        result.append(item.ids.line_label.text)

    return result
