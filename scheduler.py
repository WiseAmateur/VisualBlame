from modules.modules import module_list
from modules.modulebase import GitModuleBase
from cache import Cache
import threading
import pygit2

# Handle module requests
class Scheduler():
  events = module_list

  def __init__(self, git_dir, event_manager):
    self.event_manager = event_manager
    self.repo = pygit2.Repository(git_dir)
    self.cache = Cache()

    for event in self.events:
      self.event_manager.registerForEvent(event, self.callGitModule)

  def callGitModule(self, **kwargs):
    event = kwargs["event"]
    args = kwargs["data"]

    event_id = event
    for arg in args.values():
      event_id += str(arg)

    # If the result of the command is not yet in the cache, compute it
    if not self.cache.get(event_id):
      args["intermediate_data"] = self.cache.get(event)
      args["callback"] = self.moduleCallback
      args["repo"] = self.repo
      args["event"] = event
      args["event_id"] = event_id

      try:
        git_module = self.events[event](**args)

        thread = threading.Thread(target=git_module.execute, args=()).start()
      # Shouldn't happen, but is possible due to a user implementation fault in module_list or a module
      except:
        pass
    else:
      self.event_manager.triggerEvent(event + "_result", self.cache.get(event_id))

  def moduleCallback(self, cache_key, result_event, result_data, is_final_result=True):
    self.cache.store(cache_key, result_data)

    if is_final_result:
      self.event_manager.triggerEvent(result_event, result_data)