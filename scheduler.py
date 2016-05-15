from modules.modules import module_list
from modules.modulebase import ModuleBase
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
      self.event_manager.registerForEvent(event, self.callModule)

  def callModule(self, **kwargs):
    cache_key = kwargs["event"]
    for key in kwargs["data"]:
      cache_key += str(kwargs["data"][key])

    data = self.cache.get(cache_key)

    # TODO give function that takes the data, puts it in the cache if necessary and then triggers the event
    obj = self.events[kwargs["event"]](self.repo, self.triggerEvent, **kwargs["data"])
    # TODO use try except instead? (wrapped around the obj instantiation too
    if isinstance(obj, ModuleBase):
      thread = threading.Thread(target=obj.execute, args=())
      thread.start()

  def triggerEvent(self, event, data):
    self.event_manager.triggerEvent(event, data)