from collections import namedtuple

from kivy.uix.label import Label

from gui.widgets.buttontabpanel import ButtonTabPanel, TabPanel, TabButton


class DiffTabButtonLabel(Label):
  pass


class DiffTabButton(TabButton):
  def __init__(self, stats, **kwargs):
    super(DiffTabButton, self).__init__(**kwargs)
    text = str(stats[1]) + " [color=#809940]+[/color], " +\
           str(stats[2]) + " [color=#991919]-[/color]"
    self.add_widget(DiffTabButtonLabel(text=text))


class DiffTabPanel(TabPanel):
  def add_buttons(self, button_data):
    button_names = [file_name for file_name in button_data]
    for name in button_names:
      self.add_widget(DiffTabButton(text=name, stats=button_data[name].stats,
                                    callback=self.item_select_callback))

class DiffButtonTabPanel(ButtonTabPanel):
  panel_cls = DiffTabPanel

  def get_data(self):
    BlameArgs = namedtuple("BlameArgs", ["file_path_rel", "newest_commit", "data"])
    file_name = self.selected_file
    newest_commit = self.commit_view.get_commit_id()
    lines = self.view_to_update.get_lines()

    self._remove_tab_buttons()
    self.view_to_update._remove_all_lines()
    self.commit_view.empty_commit_context()

    return BlameArgs(file_name, newest_commit, lines)
