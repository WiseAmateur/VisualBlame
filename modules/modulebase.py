from abc import ABCMeta, abstractmethod

class ModuleBase:
  __metaclass__ = ABCMeta

  @abstractmethod
  def execute(self):
    pass