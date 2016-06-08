from collections import namedtuple

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.stacklayout import StackLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class TabButtonLabel(Label):
  pass


class TabButton(ButtonBehavior, BoxLayout):
  is_selected = False

  def __init__(self, callback, text="", **kwargs):
    self.text = text
    self.callback = callback
    super(TabButton, self).__init__(**kwargs)
    self.add_widget(TabButtonLabel(text=self.text))

  def on_press(self):
    if not self.is_selected:
      self.callback(self.text)
      self.select()

  def select(self):
    self.is_selected = True
    self.background_color = self.selected_background_color

  def deselect(self):
    self.is_selected = False
    self.background_color = self.deselected_background_color


class TabPanel(StackLayout):
  def __init__(self, select_callback, **kwargs):
    self.select_callback = select_callback
    super(TabPanel, self).__init__(**kwargs)

  def add_buttons(self, button_data):
    button_names = [file_name for file_name in button_data]
    for name in button_names:
      self.add_widget(TabButton(text=name, callback=self.item_select_callback))

  def item_select_callback(self, text):
    self.deselect_buttons()
    self.select_callback(text)

  def select_button(self, index):
    self.children[index].on_press()

  def select_button_by_name(self, name):
    names = [child.text for child in self.children]
    try:
      self.select_button(names.index(name))
    # This can happen when the log results come in before the blame
    # results in the GUI, meaning that the argument name could
    # not have a corresponding child here (can happen if they both are
    # finished so quickly that they are scheduled for the same frame)
    except ValueError:
      pass

  def deselect_buttons(self):
    for button in self.children:
      button.deselect()


class ButtonTabPanel(ScrollView):
  effect_cls = ScrollEffect
  panel_cls = TabPanel
  active_file = ""

  def _init_tab_panel(self, data=[]):
    self._remove_tab_buttons()
    self.button_container = self.panel_cls(select_callback=self.update_list)
    self.add_widget(self.button_container)

    self.button_container.add_buttons(data)
    self.select_active_file()

  def _remove_tab_buttons(self):
    try:
      self.clear_widgets()
    # The first time time there is no button container, catch the error
    except AttributeError:
      pass

  def select_active_file(self):
    try:
      self.button_container.select_button_by_name(self.active_file)
    # The active file can be updated before the button container is initialized
    except AttributeError:
      pass

  def update_active_file(self, active_file):
    self.active_file = active_file
    self.select_active_file()

  # To be implemented by the child classes
  def update_list(self, file_name):
    pass
