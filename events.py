# Class that allows for events to be registered and triggered
class EventManager():
  def __init__(self):
    self.events = {}

  def registerForEvent(self, event, function):
    if event in self.events:
      self.events[event].append(function)
    else:
      self.events[event] = [function]

  def triggerEvent(self, event, data=None):
    result = {"event": event, "data": data}
    # TODO try except?
    if event in self.events:
      for function in self.events[event]:
        function(**result)
    else:
      #exception? return False?
      pass