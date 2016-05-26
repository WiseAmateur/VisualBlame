# from collections import namedtuple
import logging

# Class that allows for events to be registered and triggered
class EventManager():
  def __init__(self):
    self.events = {}
    self.result_append = "_result"

  def registerForResultEvent(self, event_config, function):
    # processed_config = self._processConfig(event_config)
    try:
      event = event_config["caller"] + event_config["event"] + self.result_append
    except KeyError:
      logging.warn("Events: register event config is missing a parameter")
      return

    self._registerEvent(event, function)

  def registerForCallEvent(self, event, function):
    self._registerEvent(event, function)

  def _registerEvent(self, event, function):
    try:
      self.events[event].append(function)
    except KeyError:
      self.events[event] = [function]

  # def _processConfig(self, config):
    # EventConfig = namedtuple("EventConfig", ["event"])

  def triggerCallEvent(self, event, args, caller):
    args = {"event": event, "args": args, "caller": caller}
    self._triggerEvent(event, args)

  def triggerResultEvent(self, event, data, caller):
    result = {"data": data}

    event = event + self.result_append
    self._triggerEvent(event, result)

    event = caller + event
    self._triggerEvent(event, result)

  def _triggerEvent(self, event, data):
    try:
      for function in self.events[event]:
        function(**data)
    except KeyError:
      logging.warn("Events: event '" + event + "' has no listeners")
