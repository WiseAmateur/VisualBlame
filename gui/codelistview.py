from kivy.uix.listview import ListView, ListItemReprMixin
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.adapters.listadapter import ListAdapter
from kivy.graphics import Color, Rectangle, Callback
from kivy.clock import Clock
from kivy.app import App


class CodeNumLabel(Label):
  pass
  # _height = 60

  # Set the label width to the texture width, reset the pos and schedule a redraw
  # def on_texture(self, instance, value):
    # self.size = [value.size[0], self._height]
    # self.pos = [0,0]
    # Clock.schedule_once(self.update_canvas)

  # def update_canvas(self, *args):
    # self.canvas.before.clear()
    # with self.canvas.before:
      # Color(*self.bgcolor)
      # Rectangle(pos=self.pos, size=self.size)


class CodeLineLabel(Label):
  pass
  # shorten = True
  # def __init__(self, **kwargs):
    # super(CodeLineLabel, self).__init__(**kwargs)
    # self.bgcolor = kwargs["bgcolor"]
    # Clock.schedule_once(self.update_canvas)

  # def on_texture(self, instance, value):
    # print instance, value
    # if value:# and value.size[1] > 25:
      # print self.parent.num_label.text, "IS TOO BIG"
      # print self.parent.num_label.text, value.size, self.text_size, self.texture_size
      # new_y = self.texture_size[1] / 21 * 25
      # if new_y >= 25:
        # self.size[1] = new_y
        # self.parent.size[1] = new_y
      # print self.parent.num_label.text, self.size, self.parent.size
      # self.size = value.size

  # def update_canvas(self, *args):
    # self.canvas.before.clear()
    # with self.canvas.before:
      # Color(*self.bgcolor)
      # Rectangle(pos=self.pos, size=self.size)

  # def _draw_bg(self, *args):
    # self.canvas.before.clear()
    # self.canvas.before.add(Color(*self.bgcolor))
    # self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))


class CodeListItem(BoxLayout):
  cls_line_label = CodeLineLabel
  bgcolor = (1, 0, 0)
  # cols = 2
  # row_default_height = 21
  # CURRENT PLAN: use row default height to control row height, set it from the codelinelabel depending on how many height that one needs
  # height = 60
  # row_force_defeault = True

  def __init__(self, **kwargs):
    # TODO make unneccesary
    # if "cls_line_label" in kwargs:
      # self.cls_line_label = kwargs["cls_line_label"]
    # if "bgcolor" in kwargs["text"]:
      # self.bgcolor = kwargs["text"]["bgcolor"]

    super(CodeListItem, self).__init__(**kwargs)
    self.ids.linenum_label.text = kwargs["text"]["index"]
    self.ids.line_label.text = kwargs["text"]["line"]
    # self.num_label = CodeNumLabel(text=kwargs["text"]["index"], size_hint_x=None)
    # self.line_label = self.cls_line_label(text=kwargs["text"]["line"], bgcolor=self.bgcolor)#, size_hint_y=None)
    # self.add_widget(self.num_label)
    # self.add_widget(self.line_label)
    # print self.size

    # self.size[1] = 21

    # TRYING some resizing of labels that need to have more height to contain the text
    # self.bind(minimum_height=self.setter('height'))
    # self.line_label.bind(width=lambda label, width: label.setter('text_size')(label, (width, None)))
    # self.line_label.bind(texture_size=self.line_label.setter('size'))
    # self.line_label.bind(width=self.test)

  # def on_size(self, instance, value):
    # print self.size
    # if self.children:
      # print self.children[1].text, self.children[1].size


class CodeListView(ListView):
  cls_adapter = ListAdapter
  cls_item = CodeListItem
  selection_mode = "none"

  def initCodeView(self, **kwargs):
    data = self._format_line_data(kwargs["data"])

    self.adapter = self.cls_adapter(data=data, selection_mode=self.selection_mode, cls=self.cls_item)

  def _format_line_data(self, data):
    max_index_len = len(data)
    max_str_len = len(str(max_index_len))

    for index in range(max_index_len):
      index_str = str(index+1)
      # Prepend spaces to every str index that has smaller length than the max index
      for i in range(len(index_str), max_str_len):
        index_str = " " + index_str
      data[index] = {"index": index_str + "  ", "line": data[index]}

    return data