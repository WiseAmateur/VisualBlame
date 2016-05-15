from modulebase import ModuleBase
import pygit2

# Class that gets the blame info from the cache, first filling the cache
# with the info if it is not there. TODO: receive potential data from scheduler from cache
class Blame(ModuleBase):
  def __init__(self, repo, callback, **kwargs):
    self.repo = repo
    self.callback = callback
    self.file_path = kwargs["file"]
    self.line = kwargs["line"]

  def execute(self):
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

    # TODO find out how the lines work when there are not committed lines in the file. Pref behavior when selecting uncommitted line is select all uncommitted lines
    for commit_id in blame_lines:
      if self.line >= blame_lines[commit_id][0] and self.line <= blame_lines[commit_id][-1] and self.line in blame_lines[commit_id]:
        line_commit_id = commit_id


    self.callback("blame_result", blame_lines[line_commit_id])
    self.callback("commit_context", {"id": line_commit_id})