from kivy.uix.boxlayout import BoxLayout

from gui.eventwidget import EventWidget
from gui.widgets.recolorablebg import LabelRecolorableBorder


class CommitBox(LabelRecolorableBorder):
  pass


class CommitBoxView(BoxLayout, EventWidget):
  def init_event_call(self, event_config, function):
    super(CommitBoxView, self).init_event_call(event_config, function)
    self.event_call({"start_commit_id": "5217c2001a066041f6a595dc3e062cbb126da9da", "amount": 10})

  def receive_event_result(self, **kwargs):
    print kwargs
    for commit_hex in kwargs["data"]:
      self.add_widget(CommitBox(text=commit_hex[:5]))
