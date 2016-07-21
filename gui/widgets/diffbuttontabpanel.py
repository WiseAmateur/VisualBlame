from collections import namedtuple

from kivy.uix.label import Label

from gui.widgets.buttontabpanel import ButtonTabPanel, TabPanel, TabButton
from gui.eventwidget import EventWidget


class DiffTabButtonLabel(Label):
    pass


class DiffTabButton(TabButton):
    def __init__(self, stats, **kwargs):
        super(DiffTabButton, self).__init__(**kwargs)

        text = str(stats[1]) + " [color=#809940]+[/color], " + str(stats[2]) +\
        " [color=#991919]-[/color]"

        self.add_widget(DiffTabButtonLabel(text=text))


class DiffTabPanel(TabPanel):
    def add_buttons(self, button_data):
        button_names = [file_name for file_name in button_data]
        for name in button_names:
            self.add_widget(DiffTabButton(text=name,
                                          stats=button_data[name].stats,
                                          callback=self.item_select_callback))


class DiffButtonTabPanel(ButtonTabPanel, EventWidget):
    panel_cls = DiffTabPanel
    commit_id = ""

    def process_event_result(self, data=[], **kwargs):
        self.file_names = [name for name in data]
        self._init_tab_panel(data)

    def update_commit_id(self, commit_id):
        self.commit_id = commit_id

    def update_list(self, file_name):
        if file_name in self.file_names:
            self.selected_file = file_name
            args = {"commit_id": self.commit_id, "file_path": file_name}
            self.event_call(args)

    # TODO find a better way to implement this functionality, now this view
    # knows too much/is too coupled to the other views
    def get_data(self):
        BlameArgs = namedtuple("BlameArgs",
                               ["file_path_rel", "newest_commit", "data"])
        file_name = self.selected_file
        newest_commit = self.commit_view.get_commit_id()
        lines = self.view_to_update.get_lines()

        if file_name and newest_commit and lines:
            return BlameArgs(file_name, newest_commit, lines)

        return None
