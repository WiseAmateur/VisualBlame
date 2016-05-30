from collections import namedtuple

from kivy.uix.stacklayout import StackLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.app import App

from gui.eventwidget import EventWidget


class TabButton(Button):
  is_selected = False

  def __init__(self, **kwargs):
    super(TabButton, self).__init__(**kwargs)
    self.background_color = self.deselected_background_color

  def on_press(self):
    if not self.is_selected:
      self.parent.deselect_buttons()
      self.select()
      self.parent.parent.update_list(self.text)

    # self.selection_callback(self.index, self.is_selected)

  def select(self):
    self.is_selected = True
    self.background_color = self.selected_background_color

  def deselect(self):
    self.background_color = self.deselected_background_color
    self.is_selected = False


class TabPanel(StackLayout):
  def add_buttons(self, button_names):
    for name in button_names:
      self.add_widget(TabButton(text=name))

  def deselect_buttons(self):
    for button in self.children:
      button.deselect()

  def select_button(self, index):
    if index < len(self.children):
      self.children[index].on_press()


class ButtonTabPanel(ScrollView, EventWidget):
  effect_cls = ScrollEffect
  view_to_update = None

  def __init__(self, **kwargs):
    super(ButtonTabPanel, self).__init__(**kwargs)

  def receive_event_result(self, **kwargs):
    # TODO find another way to do this, this data is most likely also in the cache..
    self.data = kwargs["data"]
    # print self.view_to_update
    file_names = [file_name for file_name in kwargs["data"]]

    self._remove_tab_buttons()
    self.button_container = TabPanel()
    self.add_widget(self.button_container)

    self.button_container.add_buttons(file_names)
    try:
      self.button_container.select_button(file_names[::-1].index(self.active_file))
    except ValueError:
      pass

  def _remove_tab_buttons(self):
    # The first time time there is no button container, catch the error
    try:
      self.remove_widget(self.button_container)
    except AttributeError:
      pass

  def update_list(self, file_name):
    if self.view_to_update and file_name in self.data:
      self.view_to_update.init_code_view(data=self.data[file_name])
      self.diff_active_file = file_name

  def get_data(self):
    BlameArgs = namedtuple("BlameArgs", ["file_path_rel", "newest_commit", "data"])
    file_name = self.diff_active_file
    newest_commit = self.commit_view.get_commit_id()
    lines = self.view_to_update.get_lines()

    self._remove_tab_buttons()
    self.view_to_update._remove_all_lines()
    self.commit_view.empty_commit_context()

    return BlameArgs(file_name, newest_commit, lines)
