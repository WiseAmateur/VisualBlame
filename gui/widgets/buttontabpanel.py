from kivy.uix.stacklayout import StackLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.app import App


class TabButton(Button):
  background_down = StringProperty('atlas://data/images/defaulttheme/button')
  is_selected = False

  def __init__(self, **kwargs):
    super(TabButton, self).__init__(**kwargs)
    self.background_color = self.deselected_background_color

  def on_press(self):
    if not self.is_selected:
      self.parent.deselectButtons()
      self.select()
      self.parent.parent.updateList(self.text)

    # self.selection_callback(self.index, self.is_selected)

  def select(self):
    self.is_selected = True
    self.background_color = self.selected_background_color

  def deselect(self):
    self.background_color = self.deselected_background_color
    self.is_selected = False


class TabPanel(StackLayout):
  def addButtons(self, button_names):
    self.children = []
    for name in button_names:
      self.add_widget(TabButton(text=name))

  def deselectButtons(self):
    for button in self.children:
      button.deselect()

  def selectButton(self, index):
    print index, len(self.children)
    if index < len(self.children):
      self.children[index].on_press()


class ButtonTabPanel(ScrollView):
  effect_cls = ScrollEffect

  def __init__(self, **kwargs):
    super(ButtonTabPanel, self).__init__(**kwargs)

  def updateTabPanel(self, **kwargs):
    # TODO find another way to do this, this data is most likely also in the cache..
    self.data = kwargs["data"]
    # print self.update_view
    file_names = [file_name for file_name in kwargs["data"]]

    self.ids.button_container.addButtons(file_names)
    try:
      self.ids.button_container.selectButton(file_names[::-1].index(self.active_file))
    except ValueError:
      pass


  def updateList(self, file_name):
    if file_name in self.data:
      self.update_view(self.data[file_name])
