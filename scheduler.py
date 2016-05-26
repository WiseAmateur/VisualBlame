from cache import Cache
import threading
import pygit2

# TODO implement keeping track of active thread and implement queue (need to be thought out more)
# Handle module requests
class Scheduler():
  def __init__(self, git_dir, event_manager, events):
    self.repo = pygit2.Repository(git_dir)
    self.event_manager = event_manager
    self.events = events
    self.cache = Cache()

    for event in self.events:
      self.event_manager.registerForCallEvent(event, self.callGitModule)

  def callGitModule(self, **kwargs):
    event = kwargs["event"]
    args = kwargs["args"]
    caller = kwargs["caller"]

    event_id = event
    for arg in args.values():
      event_id += str(arg)

    # If the result of the command is not yet in the cache, compute it
    if not self.cache.get(event_id):
      args["intermediate_data"] = None#self.cache.get(event)
      args["callback"] = self.moduleCallback
      args["repo"] = self.repo
      args["event"] = event
      args["event_id"] = event_id
      args["caller"] = caller

      git_module = self.events[event](**args)

      thread = threading.Thread(target=git_module.execute, args=()).start()
      # Shouldn't happen, but is possible due to a user implementation fault in module_list or a module
      # except:
        # pass
    else:
      self.event_manager.triggerResultEvent(event, self.cache.get(event_id), caller)

  def moduleCallback(self, caller, cache_key, result_event, result_data, is_final_result=True):
    self.cache.store(cache_key, result_data)


    if is_final_result:
      self.event_manager.triggerResultEvent(result_event, result_data, caller)
      # TODO Check if the active event is a dict, if it is fire up new events after returning results.
