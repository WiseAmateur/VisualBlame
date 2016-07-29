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

    def __init__(self, **kwargs):
        super(DiffButtonTabPanel, self).__init__(**kwargs)
        self.item_select_callback = self.update_list

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

    def get_data(self):
        file_name = self.selected_file
        newest_commit = self.commit_view.get_commit_id()

        if file_name and newest_commit:
            return {"file_path": file_name, "commit_id": newest_commit}

        return None
