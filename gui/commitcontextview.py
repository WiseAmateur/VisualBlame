from kivy.uix.gridlayout import GridLayout
from kivy.app import App


class CommitContextView(GridLayout):
  def __init__(self, **kwargs):
    super(CommitContextView, self).__init__(**kwargs)
    App.get_running_app().registerForEvent("commit_context_result", self.updateCommitContext)

  def updateCommitContext(self, **kwargs):
    for widget_id, text in kwargs["data"].iteritems():
      if widget_id in self.ids:
        self.ids[widget_id].text = text