from collections import namedtuple

from kivy.uix.label import Label

from gui.widgets.buttontabpanel import ButtonTabPanel, TabPanel, TabButton
from gui.eventwidget import EventWidget


class BlameTabButtonLabel(Label):
    pass


class BlameTabButton(TabButton):
    def __init__(self, commit_id, **kwargs):
        self.commit_id = commit_id
        super(BlameTabButton, self).__init__(**kwargs)

        self.add_widget(BlameTabButtonLabel(text=commit_id[:5]))

    def on_press(self):
        if not self.is_selected:
            self.callback(self.text, self.commit_id)
            self.select()


class BlameTabPanel(TabPanel):
    def add_buttons(self, button_data):
        for commit_file in button_data:
            self.add_widget(BlameTabButton(text=commit_file[0],
                                           commit_id=commit_file[1],
                                           callback=self.item_select_callback))


class BlameButtonTabPanel(ButtonTabPanel, EventWidget):
    panel_cls = BlameTabPanel
    data = []

    def __init__(self, **kwargs):
        super(BlameButtonTabPanel, self).__init__(**kwargs)
        self.item_select_callback = self.update_list

    def add_commit_file(self, file_path, commit_id):
        CommitFile = namedtuple("CommitFile", ["file_path", "commit_id"])
        self.data = [CommitFile(file_path, commit_id)] + self.data

        super(BlameButtonTabPanel, self).update_active_file(file_path)
        self._init_tab_panel(data=self.data)

    def update_list(self, file_path, commit_id):
        # Commit_file
        args = {"commit_id": commit_id, "file_path": file_path}
        self.event_call(args)

        # Commit context and log
        args2 = {"commit_id": commit_id}
        self.event_call(args2, 1)
        self.event_call(args2, 2)