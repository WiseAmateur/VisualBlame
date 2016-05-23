import logging

from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.app import App

from codescrollview import CodeScrollView, CodeContainer, CodeListItem


class BlameCodeListItem(ButtonBehavior, CodeListItem):
  is_selected = False

  def __init__(self, callback=None, index=-1, **kwargs):
    self.select_callback = callback
    self.index = index
    super(BlameCodeListItem, self).__init__(**kwargs)

  def on_press(self):
    if not self.is_selected:
      self.select()
    else:
      self.deselect()

    try:
      self.select_callback(self.index, self.is_selected)
    except TypeError:
      logging.warn("VisualBlame: no line select callback function set")

  def select(self):
    self.ids.line_label.bg_color = self.selected_bg_color
    self.is_selected = True

  def deselect(self):
    self.ids.line_label.bg_color = self.deselected_bg_color
    self.is_selected = False


class BlameCodeContainer(CodeContainer):
  def selectItems(self, indices):
    self.deselectItems()

    items_len = len(self.children)

    # TODO check if this is actually error in the blame results.
    # Make sure that all the to be selected lines are within the file bounds, in the case of deleted lines in the work dir
    for i in range(len(indices) - 1, -1, -1):
      if indices[i] < items_len:
        indices = indices[:i+1]
        break

    items_asc_order = self.children[::-1]
    for index in indices:
      items_asc_order[index].select()

  def deselectItems(self):
    for list_item in self.children:
      list_item.deselect()


class BlameCodeScrollView(CodeScrollView):
  item_container_cls = BlameCodeContainer
  line_item_cls = BlameCodeListItem
  line_index = 0

  def initCodeView(self, file_path_rel="", **kwargs):
    self.file_path_rel = file_path_rel
    # TODO move register to another higher level place, right now the view can't be re initialized properly
    App.get_running_app().registerForEvent("blame_result", self.updateListSelection)

    super(BlameCodeScrollView, self).initCodeView(**kwargs)

  def _insertLine(self, **kwargs):
    super(BlameCodeScrollView, self)._insertLine(callback = self.handleSelectionChange,
                                                 index = self.line_index, **kwargs)
    self.line_index += 1

  def handleSelectionChange(self, pressed_index, selected):
    if (selected):
      args = {"line": pressed_index + 1, "file": self.file_path_rel}
      App.get_running_app().triggerEvent("blame", args)
    else:
      self.item_container.deselectItems()

  def updateListSelection(self, **kwargs):
    commit_id = kwargs["data"].keys()[0]

    indices = []
    for index in kwargs["data"][commit_id]:
      indices.append(index-1)

    self.item_container.selectItems(indices)

    App.get_running_app().triggerEvent("commit_context", {"commit_id": commit_id})
    App.get_running_app().triggerEvent("diff", {"commit_id": commit_id})
