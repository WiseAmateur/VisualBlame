class GitModuleBase(object):
  def __init__(self, **kwargs):
    self._callback = kwargs["callback"]
    self._config = kwargs["config"]
    self._event_id = kwargs["event_id"]
    self._repo = kwargs["repo"]
    self._intermediate_data = kwargs["intermediate_data"]
    self._cache_only = kwargs["cache_only"]

  def execute(self):
    pass

  # Return the intermediate result without triggering an event (serves for caching purposes)
  def return_intermediate_result(self, data):
    self._callback(self._event_id, data, cache_only=True)

  def return_final_result(self, data):
    self._callback(self._event_id, data, config=self._config,
                   cache_only=self._cache_only)
