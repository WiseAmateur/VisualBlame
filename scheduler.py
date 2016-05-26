import threading
import pygit2

from cache import Cache


# TODO implement keeping track of active thread and implement queue (need to be thought out more)
# Handle module requests
class Scheduler():
  def __init__(self, git_dir, event_manager, events):
    self.repo = pygit2.Repository(git_dir)
    self.event_manager = event_manager
    self.events = events
    self.cache = Cache()

    for event in self.events:
      self.event_manager.register_for_call_event(event, self.call_git_module)

  def call_git_module(self, config, event, cache_only, **args):
    event_id = event
    for arg in args.values():
      event_id += str(arg)

    # If the result of the command is not yet in the cache, compute it
    if not self.cache.get(event_id):
      args["intermediate_data"] = self.cache.get(event)
      args["callback"] = self.module_callback
      args["repo"] = self.repo
      args["config"] = config
      args["event_id"] = event_id
      args["cache_only"] = cache_only

      git_module = self.events[event](**args)

      thread = threading.Thread(target=git_module.execute, args=()).start()
    elif not cache_only:
      self.event_manager.trigger_result_event(config, self.cache.get(event_id))

  def module_callback(self, cache_key, result_data, config=None, cache_only=False):
    self.cache.store(cache_key, result_data)

    if not cache_only:
      self.event_manager.trigger_result_event(config, result_data)
