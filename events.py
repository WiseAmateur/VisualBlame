from collections import namedtuple
import logging


# Result namedtuple, making sure the callers are in a list and optional
class ResultConfig(namedtuple('ResultConfig', 'event callers')):
    def __new__(cls, event, callers=[""]):
        if type(callers) is not list:
            callers = [callers]

        return super(ResultConfig, cls).__new__(cls, event, callers)


# Call namedtuple, making sure the events are in a dict
class CallConfig(namedtuple('CallConfig', 'events caller result_args')):
    def __new__(cls, events, caller, result_args=""):
        if isinstance(events, basestring):
            events = {events: []}

        return super(CallConfig, cls).__new__(cls, events, caller, result_args)


# Class that allows for events to be registered and triggered
class EventManager():
    def __init__(self):
        self._events = {}
        self.active_call_config = None
        self.result_append = "_result"

    def register_for_result_event(self, result_configs, function):
        if type(result_configs) is not list:
            result_configs = [result_configs]

        for result_config in result_configs:
            # Assumes the result config is valid
            event = result_config.event + self.result_append

            for caller in result_config.callers:
                self._register_event(caller + event, function)

    def register_for_call_event(self, event, function):
        self._register_event(event, function)

    def _register_event(self, event, function):
        try:
            self._events[event].append(function)
        except KeyError:
            self._events[event] = [function]

    def trigger_call_event(self, call_config, args):
        self.active_call_config = call_config

        # Assumes the call config is valid
        self._trigger_event(call_config.events.keys()[0], call_config, args)

    def trigger_result_event(self, call_config, data):
        result = {"data": data}

        orig_event = call_config.events.keys()[0]

        # Trigger result event
        event = call_config.caller + orig_event + self.result_append
        self._trigger_event(event, call_config, result)

        # Trigger the additional events with the input of this result
        if call_config == self.active_call_config:
            for event in call_config.events[orig_event]:
                key = event.keys()[0]
                self._trigger_event(key, call_config._replace(events=event),
                                    {call_config.result_args:
                                     getattr(data, call_config.result_args)})

    def _trigger_event(self, event, call_config, data):
        try:
            listener_functions = self._events[event]
        except KeyError:
            logging.warn("Events: event '" + event + "' has no listeners")
            return

        for function in listener_functions:
            function(config=call_config, event=event, **data)
