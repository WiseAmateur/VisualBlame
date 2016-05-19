from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.app import App

from codescrollview import CodeListItem, CodeScrollView


class BlameCodeListItem(ButtonBehavior, CodeListItem):
  is_selected = False

  def __init__(self, **kwargs):
    self.selection_callback = kwargs["on_press_callback"]
    self.index = kwargs["index"]
    super(BlameCodeListItem, self).__init__(**kwargs)

  def on_press(self):
    if not self.is_selected:
      self.select()
    else:
      self.deselect()

    self.selection_callback(self.index, self.is_selected)

  def select(self):
    self.deselect()
    line_label = self.ids.line_label
    line_label.canvas.before.add(Color(*self.selected_bg_color))
    line_label.canvas.before.add(Rectangle(pos=line_label.pos, size=line_label.size))
    self.is_selected = True

  def deselect(self):
    self.ids.line_label.canvas.before.clear()
    self.is_selected = False


class BlameCodeScrollView(CodeScrollView):
  def initCodeView(self, **kwargs):
    self.file_path_rel = kwargs["file_path_rel"]
    App.get_running_app().registerForEvent("blame_result", self.updateListSelection)

    super(BlameCodeScrollView, self).initCodeView(**kwargs)

    # Get the list items and reverse them so that they are in ascending order again
    self.items = self.children[0].children[::-1]

  def _insertData(self, data):
    codeline_container = self.ids.codeline_container

    index = 0
    for codeline in data:
      codeline_container.add_widget(BlameCodeListItem(on_press_callback=self.handleSelectionChange,
                                                      index=index, **codeline))
      index += 1

  def handleSelectionChange(self, pressed_index, selected):
    if (selected):
      args = {"line": pressed_index + 1, "file": self.file_path_rel}
      App.get_running_app().triggerEvent("blame", args)
    else:
      self._deselectItems()
      # TODO use kivy event here and bind the corresponding commit to the event to empty itself

  def _deselectItems(self):
    for item in self.items:
      item.deselect()

  def updateListSelection(self, **kwargs):
    commit_id = kwargs["data"].keys()[0]

    indices = []
    for index in kwargs["data"][commit_id]:
      indices.append(index-1)

    self._selectItems(indices)

    App.get_running_app().triggerEvent("commit_context", {"commit_id": commit_id})
    App.get_running_app().triggerEvent("diff", {"commit_id": commit_id})

  def _selectItems(self, indices):
    self._deselectItems()

    # TODO check if this is actually error in the blame results.
    # Make sure that all the to be selected lines are within the file bounds, in the case of deleted lines in the work dir
    items_len = len(self.items)
    for i in range(len(indices) - 1, -1, -1):
      if indices[i] < items_len:
        indices = indices[:i+1]
        break

    for index in indices:
      self.items[index].select()
