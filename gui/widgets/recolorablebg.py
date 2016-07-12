from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label


class WidgetRecolorable(Widget):
    pass


class WidgetRecolorableBorder(Widget):
    pass


class BoxLayoutRecolorable(BoxLayout, WidgetRecolorable):
    pass


class LabelRecolorable(Label, WidgetRecolorable):
    pass


class LabelRecolorableBorder(Label, WidgetRecolorableBorder):
    pass
