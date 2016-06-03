from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty

from gui.eventwidget import EventWidget
from gui.widgets.recolorablebg import WidgetRecolorableBorder


class CommitContextView(GridLayout, EventWidget, WidgetRecolorableBorder):
  switch = NumericProperty(0)
  border_color = [0.25, 0.5, 0.75]

  def process_event_result(self, **kwargs):
    if type(kwargs["data"]) is list:
      data = kwargs["data"][0]
    else:
      data = kwargs["data"]

    for widget_id, text in data.iteritems():
      if widget_id in self.ids:
        self.ids[widget_id].text = text

    self.switch = 1 - self.switch

  def get_commit_id(self):
    return self.ids["id"].text

  def empty_commit_context(self):
    for widget_id in self.ids:
      self.ids[widget_id].text = ""
