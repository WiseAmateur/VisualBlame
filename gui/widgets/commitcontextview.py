from kivy.uix.gridlayout import GridLayout
from kivy.app import App


class CommitContextView(GridLayout):
  head = False
  def __init__(self, **kwargs):
    super(CommitContextView, self).__init__(**kwargs)

  def updateCommitContext(self, **kwargs):
    if (kwargs["data"]["id"] == "HEAD") == self.head:
      for widget_id, text in kwargs["data"].iteritems():
        print widget_id
        if widget_id in self.ids:
          self.ids[widget_id].text = text