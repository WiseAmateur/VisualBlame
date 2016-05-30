import logging
import pygit2
import sys

from modules.modulebase import GitModuleBase


# Class that gets the blame info from the cache, first filling the cache
# with the info if it is not there.
class Blame(GitModuleBase):
  def __init__(self, file_path="", newest_commit="", line=-1, **kwargs):
    super(Blame, self).__init__(**kwargs)
    self.file_path = file_path
    self.newest_commit = newest_commit
    self.line = line

  def execute(self):
    if self._intermediate_data:
      blame_lines = self._intermediate_data
    else:
      blame_lines = self._get_blame_lines()
      super(Blame, self).return_intermediate_result(blame_lines)

    if self.line > -1:
      # TODO find out how the lines work when there are not committed lines in the file. Pref behavior when selecting uncommitted line is select all uncommitted lines
      for commit_id in blame_lines:
        if self.line >= blame_lines[commit_id][0] and self.line <= blame_lines[commit_id][-1] and self.line in blame_lines[commit_id]:
          line_commit_id = commit_id

      super(Blame, self).return_final_result({"commit_id": str(line_commit_id), "lines": blame_lines[line_commit_id]})

  def _get_blame_lines(self):
    blame_lines = {}
    try:
      blame_obj = self._repo.blame(self.file_path, newest_commit=str(self.newest_commit))
    except KeyError:
      logging.error("Blame: blame failed, no such path '" + self.file_path + "' in HEAD")
      sys.exit()

    for hunk in blame_obj:
      start_linenum = hunk.final_start_line_number
      end_linenum = hunk.final_start_line_number + hunk.lines_in_hunk
      commit_id = hunk.final_commit_id

      hunk_lines = range(start_linenum, end_linenum)
      try:
        blame_lines[commit_id] += hunk_lines
      except KeyError:
        blame_lines[commit_id] = hunk_lines

    return blame_lines
