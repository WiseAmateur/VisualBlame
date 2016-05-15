from kivy.uix.listview import ListView, ListItemReprMixin
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.selectableview import SelectableView
from kivy.uix.label import Label
from kivy.adapters.listadapter import ListAdapter
from kivy.graphics import Color, Rectangle
from kivy.app import App


class CodeNumLabel(Label):
  pass


class CodeLineLabel(Label):
  selected_bgcolor = (1, 1, 1)

  def select(self):
    self.canvas.before.clear()
    self.canvas.before.add(Color(*self.selected_bgcolor))
    self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

  def deselect(self):
    self.canvas.before.clear()


class ListItemLabelCode(SelectableView, ButtonBehavior, GridLayout):
  rows = 1
  cols = 2

  def __init__(self, **kwargs):
    super(ListItemLabelCode, self).__init__(**kwargs)
    linenum_text = kwargs["text"]["index"]
    line_text = kwargs["text"]["line"]
    self.num_label = CodeNumLabel(text=linenum_text, size_hint_x=None)
    self.line_label = CodeLineLabel(text=line_text)#, size_hint_y=None)
    self.add_widget(self.num_label)
    self.add_widget(self.line_label)
    # self.bind(minimum_height=self.setter('height'))
    # self.line_label.bind(width=lambda label, width: label.setter('text_size')(label, (width, None)))
    # self.line_label.bind(texture_size=self.line_label.setter('size'))
    # self.line_label.bind(width=self.test)

  def select(self, *args):
    self.line_label.select()

  def deselect(self, *args):
    self.line_label.deselect()


# Custom adapter that doesn't fire selection change events when the
# selection is changed through code instead of a user click and that
# visually deselects items
class CustomAdapter(ListAdapter):
  def __init__(self, **kwargs):
    kwargs["cls"] = ListItemLabelCode
    super(CustomAdapter, self).__init__(**kwargs)
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


class CodeListView(ListView):
  def initCodeView(self, file_path_abs, file_path_rel):
    self.file_path_rel = file_path_rel
    data = self.readFile(file_path_abs)

    max_index_len = len(data)
    for index in range(max_index_len):
      index_str = str(index+1)
      # Prepend spaces to every str index that has smaller length than the max index
      for i in range(len(index_str), len(str(max_index_len))):
        index_str = " " + index_str
      data[index] = {"index": index_str + "  ", "line": data[index]}

    self.adapter = CustomAdapter(data=data, selection_mode='multiple')
    self.adapter.bind(on_selection_change=self.handleSelectionChange)
    App.get_running_app().registerForEvent("blame_result", self.updateListSelection)

  def readFile(self, file_path):
    with open(file_path) as f:
      return f.read().splitlines()

  def handleSelectionChange(self, adapter):
    line = self.adapter.get_clicked_item_index() + 1
    if line:
      args = {"line": line, "file": self.file_path_rel}
      App.get_running_app().triggerEvent("blame", args)
    else:
      self.adapter.select_list([], False)

  def updateListSelection(self, **kwargs):
    views = []
    for index in kwargs["data"]:
      views.append(self.adapter.get_view(index-1))

    self.adapter.select_list(views, False)