from time import sleep
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
    data = {}
    blame = self.repo.blame(self.file_path)

    for hunk in blame:
      lines = range(hunk.final_start_line_number, hunk.final_start_line_number + hunk.lines_in_hunk)
      commit_id = hunk.final_commit_id
      if commit_id in data:
        data[commit_id] += lines
      else:
        data[commit_id] = lines

    for key, value in data.iteritems():
      if self.line in value:
        self.callback("blame_result", value)
        self.callback("commit_context", {"id": key})