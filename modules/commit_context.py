from datetime import tzinfo, timedelta, datetime

from modules.modulebase import GitModuleBase


class CommitContext(GitModuleBase):
  def __init__(self, commit_id="HEAD", **kwargs):
    super(CommitContext, self).__init__(**kwargs)
    if type(commit_id) is not list:
      self.commit_ids = [commit_id]
    else:
      self.commit_ids = commit_id
    self.cache_commit_ids = {}

  def get_result_from_cache(self, data):
    try:
      for commit_id in self.commit_ids:
        if commit_id in data:
          self.cache_commit_ids[commit_id] = data[commit_id]

      # TODO test this, but this should be added else the data from the cache is never returned without using a thread
      if len(self.cache_commit_ids) == len(self.commit_ids):
        data = []
        for commit_id in self.commit_ids:
          try:
            data.append(self.cache_commit_ids[commit_id])
          except KeyError:
            return None

        return data
    # TypeError if data is None
    except TypeError:
      return None

  def execute(self):
    data = []
    for commit_id in self.commit_ids:
      try:
        data.append(self.cache_commit_ids[commit_id])
      except KeyError:
        commit = self._get_commit_data(commit_id)
        data.append(commit)
        super(CommitContext, self).return_cache_result(commit["id"], commit)

    super(CommitContext, self).return_final_result(data)

  def _get_commit_data(self, commit_id):
    try:
      commit = self._repo.get(commit_id)
    except ValueError:
      # If the commit id value is not an id, but something like HEAD
      commit = self._repo.revparse_single(commit_id)

    time = FixedOffset(commit.author.offset)
    dt = datetime.fromtimestamp(float(commit.author.time), time)
    timestr = dt.strftime('%x  %T  %z')

    # TODO figure out what to do with the committer name/mail/date
    return {"id": commit.id.hex, "author_name": commit.author.name,
    "author_email": commit.author.email, "message": commit.message,
    "date": timestr}


class FixedOffset(tzinfo):
  """Fixed offset in minutes east from UTC.
     source: https://media.readthedocs.org/pdf/pygit2/latest/pygit2.pdf
     page 12"""
  def __init__(self, offset):
    self.__offset = timedelta(minutes = offset)

  def utcoffset(self, dt):
    return self.__offset

  def tzname(self, dt):
    # The time zone's name is unknown
    return None

  def dst(self, dt):
     # DST is unknown
    return timedelta(0)
