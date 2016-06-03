import pygit2

from modules.modulebase import GitModuleBase


class Log(GitModuleBase):
  def __init__(self, amount=10, commit_id="HEAD", **kwargs):
    super(Log, self).__init__(**kwargs)
    self.amount = amount
    self.commit_id = commit_id

  def execute(self):
    walker = self._repo.walk(self._repo.head.target, pygit2.GIT_SORT_TIME)

    log_data = [walker.next().hex]

    if self.commit_id == "HEAD":
      self.commit_id = log_data[0]

    while True:
      try:
        commit_id = walker.next().hex
      except StopIteration:
        walker = None
        break
      log_data.append(commit_id)

      if commit_id == self.commit_id:
        break

    if walker:
      for i in range(0, self.amount):
        try:
          log_data.append(walker.next().hex)
        except StopIteration:
          break

    commit_index = log_data.index(self.commit_id)
    if commit_index <= self.amount / 2:
      result_data = log_data[0:self.amount]
    else:
      result_data = log_data[commit_index - self.amount / 2:commit_index + self.amount / 2]

    super(Log, self).return_final_result({"commit_id": result_data})
