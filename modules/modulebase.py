class GitModuleBase(object):
  def __init__(self, **kwargs):
    self._callback = kwargs["callback"]
    self._event = kwargs["event"]
    self._event_id = kwargs["event_id"]
    self.repo = kwargs["repo"]
    self.intermediate_data = kwargs["intermediate_data"]

  # Return the intermediate result without triggering an event (serves for caching purposes)
  def returnIntermediateResult(self, data):
    self._callback(self._event, self._event + "_result", data, False)

  def returnFinalResult(self, data):
    self._callback(self._event_id, self._event + "_result", data)