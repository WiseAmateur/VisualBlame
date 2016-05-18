from kivy.uix.selectableview import SelectableView
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.app import App

from codelistview import CodeLineLabel, CodeListItem, CodeScrollView

class BlameCodeLineLabel(CodeLineLabel):
  def __init__(self, **kwargs):
    super(BlameCodeLineLabel, self).__init__(**kwargs)
    if "selected_bgcolor" in kwargs:
      self.selected_bgcolor = kwargs["selected_bgcolor"]

  def _draw_selected_bg(self):
    self.canvas.before.add(Color(*self.selected_bgcolor))
    self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

  def select(self):
    self.canvas.before.clear()
    self._draw_selected_bg()

  def deselect(self):
    self.canvas.before.clear()


class BlameCodeListItem(SelectableView, ButtonBehavior, CodeListItem):
  def __init__(self, **kwargs):
    kwargs["cls_line_label"] = BlameCodeLineLabel
    super(BlameCodeListItem, self).__init__(**kwargs)

  def select(self, *args):
    self.line_label.select()

  def deselect(self, *args):
    self.line_label.deselect()


# Custom adapter that doesn't fire selection change events when the
# selection is changed through code instead of a user click and that
# visually deselects items
class BlameAdapter(ListAdapter):
  def __init__(self, **kwargs):
    if "cls" not in kwargs:
      kwargs["cls"] = BlameCodeListItem
    super(BlameAdapter, self).__init__(**kwargs)
    self._update_last_selection()

  def select_list(self, view_list, extend=True):
    if not extend:
      # Deselect list with a copy of the current selection
      self.deselect_list(list(self.selection))

    for view in view_list:
      self.select_item_view(view)

    self._update_last_selection()

  def deselect_list(self, view_list):
    for view in view_list:
      self.handle_selection(view, hold_dispatch=True)

  def _update_last_selection(self):
    self.last_selection = {view.index for view in self.selection}

  # Optimalisations/improvements can be made here depending on how the
  # final app will work. Could give whether the item is selected/deselected
  def get_clicked_item_index(self):
    if len(self.last_selection) < len(self.selection):
      # TODO crashes when spam clicking as the selection changes during the clicks
      index = next(view.index for view in self.selection if not view.index in self.last_selection)
    else:
      index = -1

    # Not a great spot to update this, but have to as the results of the last
    # click are not guaranteed to be done (and thus call select list which updates)
    # before the next click.
    self._update_last_selection()
    return index


class BlameCodeListView(CodeScrollView):
  cls_adapter = BlameAdapter
  cls_item = BlameCodeListItem
  selection_mode = "multiple"

  def initCodeView(self, **kwargs):
    self.file_path_rel = kwargs["file_path_rel"]
    super(BlameCodeListView, self).initCodeView(**kwargs)

    self.adapter.bind(on_selection_change=self.handleSelectionChange)
    App.get_running_app().registerForEvent("blame_result", self.updateListSelection)

  def handleSelectionChange(self, adapter):
    line = self.adapter.get_clicked_item_index() + 1
    if line:
      args = {"line": line, "file": self.file_path_rel}
      App.get_running_app().triggerEvent("blame", args)
    else:
      self.adapter.select_list([], False)
      # TODO use kivy event here and bind the corresponding commit to the event to empty itself

  def updateListSelection(self, **kwargs):
    commit_id = kwargs["data"].keys()[0]
    views = []
    for index in kwargs["data"][commit_id]:
      views.append(self.adapter.get_view(index-1))

    self.adapter.select_list(views, False)
    App.get_running_app().triggerEvent("commit_context", {"commit_id": commit_id})
    App.get_running_app().triggerEvent("diff", {"commit_id": commit_id})