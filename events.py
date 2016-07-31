from collections import namedtuple
import logging


# Result namedtuple, making sure the callers are in a list and optional
class ResultConfig(namedtuple('ResultConfig', 'event callers')):
    def __new__(cls, event, callers=[""]):
        if type(callers) is not list:
            callers = [callers]

        return super(ResultConfig, cls).__new__(cls, event, callers)


# Call namedtuple, making sure the events are in a dict
class CallConfig(namedtuple('CallConfig', 'event caller args')):
    def __new__(cls, event, caller, args={}):
        return super(CallConfig, cls).__new__(cls, event, caller, args)


# Class that allows for events to be registered and triggered
class EventManager():
    def __init__(self):
        self._events = {}
        self.result_append = "_"

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
        # Assumes the call config is valid and adds the args to it
        self._trigger_event(call_config.event, call_config._replace(args=args),
                            args)

    def trigger_result_event(self, call_config, data):
        result = {"data": data}

        # Trigger result event
        event = call_config.caller + call_config.event + self.result_append
        self._trigger_event(event, call_config, result)

    def _trigger_event(self, event, call_config, data):
        try:
            listener_functions = self._events[event]
        except KeyError:
            logging.warn("Events: event '" + event + "' has no listeners")
            return

        for function in listener_functions:
            function(config=call_config, event=event, **data)
