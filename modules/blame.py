import logging
import pygit2
import sys
from collections import namedtuple

from modules.modulebase import GitModuleBase


# Class that gets the blame info from the cache, first filling the cache
# with the info if it is not there. Does not support untracked lines.
class Blame(GitModuleBase):
  def __init__(self, file_path="", newest_commit="", line=-1, **kwargs):
    super(Blame, self).__init__(**kwargs)
    self.file_path = file_path
    self.newest_commit = newest_commit
    self.line = line
    self.key = file_path + newest_commit

  def get_result_from_cache(self, data):
    try:
      return data[self.key][self.line-1]
    # TypeError if the data is None, KeyError if the data doesn't
    # contain the key of this module
    except (TypeError, KeyError):
      return None

  def execute(self):
    blame_lines = self._get_blame_lines()

    try:
      super(Blame, self).return_cache_result(self.key, blame_lines)
      super(Blame, self).return_final_result(blame_lines[self.line-1])
    except KeyError:
      logging.error("Blame: blame failed, selected line not found in results")

  def _get_blame_lines(self):
    BlameLines = namedtuple("BlameLines", ["commit_id", "lines", "orig_path"])

    # The by_commit dictionary is only used to add the lines of a hunk
    # to the BlameLines of its corresponding commit in the case it
    # already exists
    blame_lines_by_commit = {}
    blame_lines_by_line = []

    try:
      blame_obj = self._repo.blame(self.file_path, newest_commit=str(self.newest_commit))
    except KeyError:
      logging.error("Blame: blame failed, no such path '" + self.file_path + "' in " + str(self.newest_commit))
      sys.exit()

    for hunk in blame_obj:
      start_linenum = hunk.final_start_line_number
      end_linenum = hunk.final_start_line_number + hunk.lines_in_hunk
      commit_id = str(hunk.final_commit_id)

      # When/if switching to python3, use list() around this
      hunk_lines = range(start_linenum, end_linenum)

      try:
        blame_lines = blame_lines_by_commit[commit_id]
        blame_lines.lines.extend(hunk_lines)
      except KeyError:
        blame_lines = BlameLines(commit_id, hunk_lines, hunk.orig_path)
        blame_lines_by_commit[commit_id] = blame_lines

      # Store the references to the BlameLines Python object for every
      # line it contains.
      for i in xrange(len(hunk_lines)):
        # The hunk lines are already sorted, so we can use append
        blame_lines_by_line.append(blame_lines)

    return blame_lines_by_line
