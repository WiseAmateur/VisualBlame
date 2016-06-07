import time, psutil, os

from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty

from gui.eventwidget import EventWidget
from gui.widgets.recolorablebg import WidgetRecolorableBorder


# source: http://fa.bianp.net/blog/2013/different-ways-to-get-memory-consumption-or-lessons-learned-from-memory_profiler/
def memory_usage_psutil():
  # return the memory usage in MB
  process = psutil.Process(os.getpid())
  mem = process.memory_info().rss / float(2 ** 20)
  return mem


class CommitContextView(GridLayout, EventWidget, WidgetRecolorableBorder):
  switch = NumericProperty(0)
  border_color = [0.25, 0.5, 0.75]

  def process_event_result(self, data=None, **kwargs):
    data = data[0]

    for widget_id, text in data.iteritems():
      if widget_id in self.ids:
        self.ids[widget_id].text = text

    print "time on commit context result,", time.time()
    print "mem on commit context result,", memory_usage_psutil()

    self.switch = 1 - self.switch

  def get_commit_id(self):
    return self.ids["id"].text

  def empty_commit_context(self):
    for widget_id in self.ids:
      self.ids[widget_id].text = ""
