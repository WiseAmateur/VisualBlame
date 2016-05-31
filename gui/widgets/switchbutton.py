from collections import namedtuple
import logging

from kivy.uix.stacklayout import StackLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.app import App


class SwitchButton(Button):
  # Get Diff file without removed lines. Get commit so you know when to start looking.
  def on_press(self):
    try:
      scrollview_args = self.from_scrollview.get_data()
      self.to_scrollview.init_code_view(**scrollview_args._asdict())
    except AttributeError:
      logging.warn("SwitchButton: codescrollviews not set")
