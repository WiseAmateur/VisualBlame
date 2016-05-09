from modules.modules import module_list
from modules.modulebase import ModuleBase
import threading
import pygit2

# Handle module requests
class Scheduler():
  events = module_list

  def __init__(self, git_dir, event_manager):
    self.event_manager = event_manager
    self.repo = pygit2.Repository(git_dir)

    for event in self.events:
      self.event_manager.registerForEvent(event, self.callModule)

  def callModule(self, **kwargs):
    obj = self.events[kwargs["event"]](self.repo, self.triggerEvent, **kwargs["data"])
    if isinstance(obj, ModuleBase):
      threading.Thread(target=obj.execute, args=()).start()

  def triggerEvent(self, event, data):
    self.event_manager.triggerEvent(event, data)