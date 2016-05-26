import logging

class EventWidget():
  def init_event_call(self, function, caller, event):
    self._call_function = function
    self._caller = caller
    self._event = event

  def receive_event_result(self, **kwargs):
    pass

  # Event call(s), gets initialized in gui, so in init here should get like some functions to call,
  # should be saved in the event widget and called through this method
  # This will probably make it less flexible in the sense that you can't do multiple different events
  # in one widget, but with the original functionality this is fine.
  def event_call(self, args):
    try:
      self._call_function(self._event, args, self._caller)
    except AttributeError:
      logging.warn("EventWidget: event trigger was called before initialization")
