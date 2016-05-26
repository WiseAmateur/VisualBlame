from collections import namedtuple

from kivy.uix.stacklayout import StackLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.app import App


class SwitchButton(Button):
  def setScrollViews(self, from_scrollview, to_scrollview):
    self.from_scrollview = from_scrollview
    self.to_scrollview = to_scrollview

  # Get Diff file without removed lines. Get commit so you know when to start looking.
  def on_press(self):
    scrollview_args = self.from_scrollview.getData()
    self.to_scrollview.initCodeView(**scrollview_args._asdict())
