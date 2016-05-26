from collections import namedtuple
import pygit2

from modules.modulebase import GitModuleBase


class Log(GitModuleBase):
  def __init__(self, **kwargs):
    super(Log, self).__init__(**kwargs)
    self.amount = kwargs["amount"]
    try:
      self.start_commit_id = kwargs["start_commit_id"]
    except KeyError:
      self.start_commit_id = self._repo.head.target

  # Input, amount of commits and start commit
  # Output, commits for timeline, visualize as rectangles with date in middle?
  # So output is log -> [commit ids]
  # problem is, not guaranteed to be enough commits before/after go get target amount
  # or just do simple and get commits after given one, if then not enough also take some from before
  # but rather always before and after if possible
  def execute(self):
    walker = self._repo.walk(self.start_commit_id, pygit2.GIT_SORT_TIME)
    walker_rev = self._repo.walk(self.start_commit_id, pygit2.GIT_SORT_TIME | pygit2.GIT_SORT_REVERSE)

    log_data = []

    while len(log_data) < self.amount:
      try:
        log_data.append(walker.next())
      except StopIteration:
        pass

      try:
        log_data.insert(0, walker_rev.next())
      except StopIteration:
        pass

    # TODO IN COMMIT FUNCTIONALITY, ALLOW FOR MULTIPLE COMMIT INFO RETRIEVES AT ONCE (LIST INPUT OF IDS) SO THAT LESS THREADS ARE NEEDED IN CASES OF LOG COMMIT DETAILS.
    # TODO instead of amount, do blame commit + 1 before and 1 after, and do diff commit + 1 before and 1 after. ( with something like ... in between if there is a gap which is likely)

    super(Log, self).return_final_result(log_data)
