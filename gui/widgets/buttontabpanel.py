from kivy.uix.stacklayout import StackLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.app import App


class TabButton(Button):
  pass


class TabPanel(StackLayout):
  def addButtons(self, button_names):
    self.children = []
    for name in button_names:
      self.add_widget(TabButton(text=name))


class ButtonTabPanel(ScrollView):
  effect_cls = ScrollEffect

  def __init__(self, **kwargs):
    super(ButtonTabPanel, self).__init__(**kwargs)
    App.get_running_app().registerForEvent("diff_result", self.updateDiffView)

  def updateDiffView(self, **kwargs):
    file_names = [file_name for file_name in kwargs["data"]]

    self.ids.button_container.addButtons(file_names)
