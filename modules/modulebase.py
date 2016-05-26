class GitModuleBase(object):
  def __init__(self, **kwargs):
    self._callback = kwargs["callback"]
    self._event = kwargs["event"]
    self._event_id = kwargs["event_id"]
    self.repo = kwargs["repo"]
    self.intermediate_data = kwargs["intermediate_data"]
    self._caller = kwargs["caller"]

  def execute(self):
    pass

  # Return the intermediate result without triggering an event (serves for caching purposes)
  def returnIntermediateResult(self, data):
    self._callback(self._caller, self._event_id, self._event, data, False)

  def returnFinalResult(self, data):
    self._callback(self._caller, self._event_id, self._event, data)
