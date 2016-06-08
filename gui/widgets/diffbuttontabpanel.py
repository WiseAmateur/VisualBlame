import time, psutil, os
from collections import namedtuple

from kivy.uix.label import Label

from gui.widgets.buttontabpanel import ButtonTabPanel, TabPanel, TabButton
from gui.eventwidget import EventWidget


# source: http://fa.bianp.net/blog/2013/different-ways-to-get-memory-consumption-or-lessons-learned-from-memory_profiler/
def memory_usage_psutil():
  # return the memory usage in MB
  process = psutil.Process(os.getpid())
  mem = process.memory_info().rss / float(2 ** 20)
  return mem


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

class DiffButtonTabPanel(ButtonTabPanel, EventWidget):
  panel_cls = DiffTabPanel
  commit_id = ""

  def process_event_result(self, data=[], **kwargs):
    self.file_names = [name for name in data]
    self._init_tab_panel(data)
    print "time on diff result,", time.time()
    print "mem on diff result,", memory_usage_psutil()

  def update_commit_id(self, commit_id):
    self.commit_id = commit_id

  def update_list(self, file_name):
    if file_name in self.file_names:
      self.selected_file = file_name
      args = {"commit_id": self.commit_id, "file_path": file_name}
      print "mem on diff lines start,", memory_usage_psutil()
      print "time on diff lines start,", time.time()
      self.event_call(args)

  def get_data(self):
    BlameArgs = namedtuple("BlameArgs", ["file_path_rel", "newest_commit", "data"])
    file_name = self.selected_file
    newest_commit = self.commit_view.get_commit_id()
    lines = self.view_to_update.get_lines()

    self._remove_tab_buttons()
    self.view_to_update._remove_all_lines()
    self.commit_view.empty_commit_context()

    return BlameArgs(file_name, newest_commit, lines)
