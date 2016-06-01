from kivy.uix.gridlayout import GridLayout
from kivy.app import App

from gui.eventwidget import EventWidget


class CommitContextView(GridLayout, EventWidget):
  def receive_event_result(self, **kwargs):
    if type(kwargs["data"]) is list:
      data = kwargs["data"][0]
    else:
      data = kwargs["data"]

    for widget_id, text in data.iteritems():
      if widget_id in self.ids:
        self.ids[widget_id].text = text

  def get_commit_id(self):
    return self.ids["id"].text

  def empty_commit_context(self):
    for widget_id in self.ids:
      self.ids[widget_id].text = ""
