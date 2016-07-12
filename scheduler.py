import threading
import pygit2

from cache import EventCache


# TODO implement keeping track of active thread and implement
# queue (need to be thought out more)
# Handle module requests
class Scheduler():
    def __init__(self, git_dir, event_manager, events):
        self.repo = pygit2.Repository(git_dir)
        self.event_manager = event_manager
        self.events = events
        self.cache = EventCache()

        for event in self.events:
            self.event_manager.register_for_call_event(event,
                                                       self.call_git_module)

    def call_git_module(self, config, event, **args):
        args["callback_cache"] = self.module_callback_cache
        args["callback_result"] = self._trigger_result_event
        args["repo"] = self.repo
        args["config"] = config
        args["event"] = event

        git_module = self.events[event](**args)

        result_data = git_module.get_result_from_cache(self.cache.get(event))

        # If the result of the command is not yet in the cache, compute it
        if result_data:
            self._trigger_result_event(config, result_data)
        else:
            thread = threading.Thread(target=git_module.execute,
                                      args=()).start()

    def _trigger_result_event(self, config, data):
        self.event_manager.trigger_result_event(config, data)

    def module_callback_cache(self, event, key, result_data):
        self.cache.store(event, key, result_data)
