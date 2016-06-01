import logging

from kivy.uix.button import Button
from gui.eventwidget import EventWidget


class SwitchButton(Button, EventWidget):
  # Get Diff file without removed lines. Get commit so you know when to start looking.
  def on_press(self):
    try:
      scrollview_args = self.from_scrollview.get_data()
      self.to_scrollview.init_code_view(**scrollview_args._asdict())
      args={"amount": 20, "start_commit_id": scrollview_args.newest_commit}
      self.event_call(args)
    except AttributeError:
      logging.warn("SwitchButton: codescrollviews not set")
