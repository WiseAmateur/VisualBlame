class EventWidget():
  def init_event_call(self, event_config, function):
    self._config = event_config
    self._call_function = function

  def receive_event_result(self, **kwargs):
    pass

  def event_call(self, args):
    self._call_function(self._config, args)
