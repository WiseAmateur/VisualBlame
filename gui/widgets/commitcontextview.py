from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty

from gui.eventwidget import EventWidget
from gui.widgets.recolorablebg import WidgetRecolorableBorder


class CommitContextView(BoxLayout, EventWidget, WidgetRecolorableBorder):
    switch = NumericProperty(0)
    border_color = [0.25, 0.5, 0.75]

    def process_event_result(self, data=None, **kwargs):
        data = data[0]

        for widget_id, text in data.iteritems():
            if widget_id in self.ids:
                self.ids[widget_id].text = text

        # TODO share the commit information in another way, the switch is
        # not doing anything for the widget itself
        self.switch = 1 - self.switch

    def get_commit_id(self):
        return self.ids["id"].text

    def get_data(self):
        result = {}
        for widget_id in self.ids:
            result[widget_id] = self.ids[widget_id].text

        return result

    def empty_commit_context(self):
        for widget_id in self.ids:
            self.ids[widget_id].text = ""
