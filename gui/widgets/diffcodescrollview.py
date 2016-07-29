from collections import namedtuple

from gui.widgets.codescrollview import CodeScrollView, CodeListItem
from gui.eventwidget import EventWidget


class DiffCodeListItem(CodeListItem):
    def __init__(self, bg_color=[0, 0, 0], **kwargs):
        self.line_bg_color = bg_color
        super(DiffCodeListItem, self).__init__(**kwargs)


class DiffCodeScrollView(CodeScrollView, EventWidget):
    color_mapping = {"+": [0.5, 0.6, 0.25], "-": [0.6, 0.1, 0.1],
                     " ": [0, 0, 0]}
    line_item_cls_colored = DiffCodeListItem

    def process_event_result(self, data=[], **kwargs):
        self.init_code_view(data=data.hunks)

    def _insert_line(self, **kwargs):
        if kwargs["bg_color"] != [0, 0, 0]:
            self.item_container.add_widget(
                self.line_item_cls_colored(**kwargs))
        else:
            super(DiffCodeScrollView, self)._insert_line(**kwargs)

    def _format_line_data(self, data):
        ColoredLine = namedtuple('ColoredLine',
                                 ['str_index', 'line', 'bg_color'])
        list_data = []
        line_num = 1

        for diff_hunk in data:
            bg_color = self.color_mapping[diff_hunk.origin]
            if diff_hunk.origin != "-":
                for line in diff_hunk.lines:
                    list_data.append(ColoredLine(str(line_num), line,
                                                 bg_color))
                    line_num += 1
            # Removed lines don't get a line number
            else:
                for line in diff_hunk.lines:
                    list_data.append(ColoredLine(" ", line, bg_color))

        max_str_len = len(str(line_num))

        # Append and prepend spaces to the line number to make them all equal
        # str length
        for i in range(len(list_data)):
            line = list_data[i]
            final_str_index = " " * (max_str_len - len(line.str_index)) +\
                line.str_index + "    "
            list_data[i] = line._replace(str_index=final_str_index)

        return list_data
