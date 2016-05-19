# Class that allows for events to be registered and triggered
class EventManager():
  def __init__(self):
    self.events = {}

  def registerForEvent(self, event, function):
    try:
      self.events[event].append(function)
    except KeyError:
      self.events[event] = [function]

  # Call all functions registered to an event with the given data. This
  # data could either be input data or result data
  def triggerEvent(self, event, data=None):
    result = {"event": event, "data": data}

    if event in self.events:
      for function in self.events[event]:
        function(**result)
