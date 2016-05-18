from kivy.adapters.listadapter import ListAdapter
from kivy.app import App

from codelistview import CodeScrollView

class DiffAdapter(ListAdapter):
  def __init__(self, **kwargs):
    if "cls" not in kwargs:
      kwargs["cls"] = CodeListItem
    super(DiffAdapter, self).__init__(**kwargs)
    self.data = [{"index": "1", "line": "test", "bgcolor": (0.5, 0.5, 0.5)}]

  def updateData(self, data):
    self.data = data


class DiffCodeListView(CodeScrollView):
  color_mapping = {"+": (0, 1, 0), "-": (1, 0, 0), " ": (0, 0, 0)}
  cls_adapter = DiffAdapter

  # The diff view initially starts with no data
  def initCodeView(self, **kwargs):
    super(DiffCodeListView, self).initCodeView(**kwargs)
    App.get_running_app().registerForEvent("diff_result", self.updateListData)

  def updateListData(self, **kwargs):
    list_data = []
    counter = 1
    for key in kwargs["data"]:
      for block in kwargs["data"][key]:
        bgcolor = self.color_mapping[block["type"]]
        for line in block["lines"]:
          list_data.append({"index": str(counter), "line": line, "bgcolor": bgcolor})
          counter += 1
      break

    # print list_data
    self.adapter.updateData(list_data)
