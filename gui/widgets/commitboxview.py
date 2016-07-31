from collections import namedtuple

from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from gui.eventwidget import EventWidget
from gui.widgets.recolorablebg import WidgetRecolorableBorder


class CommitBox(ButtonBehavior, BoxLayout, WidgetRecolorableBorder):
    def __init__(self, commit_hex="", commit_date="", commit_message="",
                 callback=None, **kwargs):
        super(CommitBox, self).__init__(**kwargs)
        self.commit_hex = commit_hex
        self.callback = callback
        self.ids["commit_hex"].text = commit_hex[:5]
        self.ids["commit_date"].text = commit_date[:8]
        self.ids["commit_message"].text = commit_message

    def on_press(self):
        if self.callback:
            diff_files = App.get_running_app().get_view_by_id("diff_files")
            self.callback(self.commit_hex, 0)
            self.callback(self.commit_hex, 2)
            self.callback(self.commit_hex, 3)


class CommitBoxView(GridLayout, EventWidget):
    active_commits = {}

    def init_event_call(self, event_config, function):
        super(CommitBoxView, self).init_event_call(event_config, function)
        self.event_call("HEAD")

    def event_call(self, commit_id, config_num=0):
        args = {"commit_id": commit_id}
        super(CommitBoxView, self).event_call(args, config_num)

    def process_event_result(self, data, **kwargs):
        # Commit context result
        if type(data) is list:
            self.clear_widgets()
            for commit_data in data:
                self.add_widget(CommitBox(
                    commit_hex=commit_data["id"],
                    commit_date=commit_data["date"],
                    commit_message=commit_data["message"],
                    callback=self.event_call))
                self._update_active_commits()
        # Log result
        else:
            self.event_call(data.commit_ids, 1)

    def update_viewed_commit(self, active_commit, commit_id, color, prop):
        ActiveCommit = namedtuple('ActiveCommit',
                                  ['commit_id', 'color', 'prop'])
        self.active_commits[active_commit] = ActiveCommit(commit_id, color,
                                                          prop)
        self._update_active_commits()

    def _update_active_commits(self):
        for key, active_commit in self.active_commits.iteritems():
            for commit_box in self.children:
                if commit_box.commit_hex == active_commit.commit_id:
                    setattr(commit_box, active_commit.prop,
                            active_commit.color)
                    break


class CommitBoxViewContainer(ScrollView):
    effect_cls = ScrollEffect
