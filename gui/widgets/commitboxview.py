from kivy.uix.boxlayout import BoxLayout

from gui.eventwidget import EventWidget
from gui.widgets.recolorablebg import WidgetRecolorableBorder


class CommitBox(BoxLayout, WidgetRecolorableBorder):
  def __init__(self, commit_hex="", commit_date="", commit_message="",
               **kwargs):
    super(CommitBox, self).__init__(**kwargs)
    self.ids["commit_hex"].text = commit_hex[:5]
    self.ids["commit_date"].text = commit_date[:8]
    self.ids["commit_message"].text = commit_message


class CommitBoxView(BoxLayout, EventWidget):
  def init_event_call(self, event_config, function):
    super(CommitBoxView, self).init_event_call(event_config, function)
    self.event_call("HEAD", 20)

  def event_call(self, commit_id, amount):
    args = {"start_commit_id": commit_id, "amount": amount}
    #"5217c2001a066041f6a595dc3e062cbb126da9da"
    super(CommitBoxView, self).event_call(args)

  def receive_event_result(self, **kwargs):
    if type(kwargs["data"]) is list:
      self.clear_widgets()
      for commit_data in kwargs["data"]:
        self.add_widget(CommitBox(commit_hex=commit_data["id"], commit_date=commit_data["date"],
                                  commit_message=commit_data["message"]))
