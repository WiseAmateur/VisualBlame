from kivy.adapters.listadapter import ListAdapter
from kivy.app import App

from codescrollview import CodeScrollView

class DiffCodeScrollView(CodeScrollView):
  color_mapping = {"+": (0.5, 0.6, 0.25), "-": (0.6, 0.1, 0.1), " ": (0, 0, 0)}

  # The diff view initially starts with no data
  def initCodeView(self, **kwargs):
    super(DiffCodeScrollView, self).initCodeView(**kwargs)

  def updateListData(self, data):
    # print "in updatelistdata", data
    list_data = []
    counter = 1
    removed_counter = 0
    for diff_hunk in data:
      bgcolor = self.color_mapping[diff_hunk.origin]
      temp_counter = counter
      for line in diff_hunk.lines:
        list_data.append({"index_str": str(temp_counter), "line": line, "bg_color": bgcolor})
        temp_counter += 1
      if diff_hunk.origin != "-":
        counter = temp_counter
      else:
        removed_counter = temp_counter

    if len(list_data):
      max_str_len = max(len(list_data[-1]["index_str"]), len(str(removed_counter)))

    for item in list_data:
      for i in range(len(item["index_str"]), max_str_len):
        item["index_str"] = " " + item["index_str"]
      item["index_str"] += "  "

    # print list_data
    self._removeAllData()
    self._insertData(list_data)
