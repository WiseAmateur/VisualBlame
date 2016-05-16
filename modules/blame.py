from modulebase import GitModuleBase
import pygit2

# Class that gets the blame info from the cache, first filling the cache
# with the info if it is not there.
class Blame(GitModuleBase):
  def __init__(self, **kwargs):
    super(Blame, self).__init__(**kwargs)
    self.file_path = kwargs["file"]

    # The blame module can be used without a line arg, to get the blame in the cache
    try:
      self.line = kwargs["line"]
    except KeyError:
      self.line = -1

  def execute(self):
    if self.intermediate_data:
      blame_lines = self.intermediate_data
    else:
      blame_lines = self._get_blame_lines()
      super(Blame, self).returnIntermediateResult(blame_lines)

    if self.line > -1:
      # TODO find out how the lines work when there are not committed lines in the file. Pref behavior when selecting uncommitted line is select all uncommitted lines
      for commit_id in blame_lines:
        if self.line >= blame_lines[commit_id][0] and self.line <= blame_lines[commit_id][-1] and self.line in blame_lines[commit_id]:
          line_commit_id = commit_id

      super(Blame, self).returnFinalResult({line_commit_id: blame_lines[line_commit_id]})

  def _get_blame_lines(self):
    blame_lines = {}
    blame_obj = self.repo.blame(self.file_path)

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