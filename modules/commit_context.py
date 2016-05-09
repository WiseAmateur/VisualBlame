from __future__ import unicode_literals
from datetime import tzinfo, timedelta
from datetime import datetime
from modulebase import ModuleBase
import pygit2

class CommitContext(ModuleBase):
  def __init__(self, repo, callback, **kwargs):
    self.repo = repo
    self.callback = callback
    self.commit_id = kwargs["id"]

  def execute(self):
    commit = self.repo.get(self.commit_id)
    time = FixedOffset(commit.author.offset)
    dt = datetime.fromtimestamp(float(commit.author.time), time)
    timestr = dt.strftime('%x  %T  %z')

    data = {"id": str(self.commit_id), "author_name": commit.author.name,
    "author_email": commit.author.email, "committer_name": commit.committer.name,
    "committer_email": commit.committer.email, "message": commit.message,
    "date": timestr}

    self.callback("commit_context_result", data)

class FixedOffset(tzinfo):
  """Fixed offset in minutes east from UTC. https://media.readthedocs.org/pdf/pygit2/latest/pygit2.pdf page 12"""
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