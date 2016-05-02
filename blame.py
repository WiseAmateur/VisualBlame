import pygit2

# Class that gets the blame info from the cache, first filling the cache
# with the info if it is not there.
class Blame():
  def __init__(self, repo, path):
    self.repo = repo
    self.file_path = path

  def blame(self):
    pass