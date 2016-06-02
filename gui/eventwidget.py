from functools import partial

from kivy.clock import Clock


class EventWidget():
  def init_event_call(self, event_config, function):
    self._config = event_config
    self._call_function = function

  def receive_event_result(self, **kwargs):
    # Use the thread safe Clock schedule once to update the UI, as this
    # function can be called from different threads
    Clock.schedule_once(partial(self._call_event_processing, kwargs))

  def _call_event_processing(self, kwargs, *largs):
    self.process_event_result(**kwargs)

  def process_event_result(self, **kwargs):
    # Function to be implemented by child classes to handle the results
    pass

  def event_call(self, args):
    self._call_function(self._config, args)
