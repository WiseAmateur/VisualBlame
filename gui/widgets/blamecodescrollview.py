import time
import psutil
import os

from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.app import App

from gui.widgets.codescrollview import CodeScrollView, CodeContainer, CodeListItem
from gui.eventwidget import EventWidget


# source: http://fa.bianp.net/blog/2013/different-ways-to-get-memory-consumption-or-lessons-learned-from-memory_profiler/
def memory_usage_psutil():
  # return the memory usage in MB
  process = psutil.Process(os.getpid())
  mem = process.memory_info().rss / float(2 ** 20)
  return mem


class BlameCodeListItem(ButtonBehavior, CodeListItem):
  is_selected = False

  def __init__(self, callback, index=-1, **kwargs):
    self.select_callback = callback
    self.index = index
    super(BlameCodeListItem, self).__init__(**kwargs)

  def on_press(self):
    if not self.is_selected:
      print "mem on blame line click,", memory_usage_psutil()
      print "time on blame line click,", time.time()
      self.select()
    else:
      self.deselect()

    self.select_callback(self.index, self.is_selected)

  def select(self):
    self.ids.line_label.bg_color = self.selected_bg_color
    self.is_selected = True

  def deselect(self):
    self.ids.line_label.bg_color = self.deselected_bg_color
    self.is_selected = False


class BlameCodeContainer(CodeContainer):
  def select_items(self, indices):
    self.deselect_items()

    items_asc_order = self.children[::-1]

    for index in indices:
      try:
        items_asc_order[index-1].select()
      # Can be out of bounds if the file has deleted lines in the
      # working dir, the blame assumes the file is in the state of the
      # corresponding commit. Then break, the indices should be sorted
      except IndexError:
        break

  def deselect_items(self):
    for list_item in self.children:
      list_item.deselect()


class BlameCodeScrollView(CodeScrollView, EventWidget):
  item_container_cls = BlameCodeContainer
  line_item_cls = BlameCodeListItem
  file_path_rel = StringProperty()
  blame_path_rel = StringProperty()
  commit_id = StringProperty()

  def init_code_view(self, file_path_rel="", newest_commit="", **kwargs):
    self.line_index = 0
    self.file_path_rel = file_path_rel
    self.newest_commit = newest_commit

    super(BlameCodeScrollView, self).init_code_view(**kwargs)

  def _insert_line(self, **kwargs):
    super(BlameCodeScrollView, self)._insert_line(callback = self.handle_selection_change,
                                                 index = self.line_index, **kwargs)
    self.line_index += 1

  def handle_selection_change(self, pressed_index, selected):
    if (selected):
      args = {"line": pressed_index + 1, "file_path": self.file_path_rel,
              "newest_commit": self.newest_commit}
      self.event_call(args)
    else:
      self.item_container.deselect_items()

  def process_event_result(self, **kwargs):
    self.commit_id = kwargs["data"].commit_id
    self.blame_path_rel = kwargs["data"].orig_path
    self.item_container.select_items(kwargs["data"].lines)
    print "time on blame result,", time.time()
    print "mem on blame result,", memory_usage_psutil()
