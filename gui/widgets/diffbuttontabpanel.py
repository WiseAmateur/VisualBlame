from collections import namedtuple

from gui.widgets.buttontabpanel import ButtonTabPanel


class DiffButtonTabPanel(ButtonTabPanel):
  def get_data(self):
    BlameArgs = namedtuple("BlameArgs", ["file_path_rel", "newest_commit", "data"])
    file_name = self.selected_file
    newest_commit = self.commit_view.get_commit_id()
    lines = self.view_to_update.get_lines()

    self._remove_tab_buttons()
    self.view_to_update._remove_all_lines()
    self.commit_view.empty_commit_context()

    return BlameArgs(file_name, newest_commit, lines)
