from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from gui.eventwidget import EventWidget
from gui.widgets.recolorablebg import WidgetRecolorableBorder


class CommitContextView(BoxLayout, EventWidget, WidgetRecolorableBorder):
    border_color = [0.25, 0.5, 0.75]
    commit_id = StringProperty()

    def process_event_result(self, data=None, **kwargs):
        data = data[0]

        for widget_id, text in data.iteritems():
            if widget_id in self.ids:
                self.ids[widget_id].text = text

        self.commit_id = self.ids["id"].text

    def get_commit_id(self):
        return self.commit_id

    def get_data(self):
        result = {}
        for widget_id in self.ids:
            result[widget_id] = self.ids[widget_id].text

        return result

    def empty_commit_context(self):
        for widget_id in self.ids:
            self.ids[widget_id].text = ""

        self.commit_id = ""
