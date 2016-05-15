from abc import ABCMeta, abstractmethod

# TODO not abstract class but parent class that already implements the basic functions of the execute/callback handling
class ModuleBase:
  __metaclass__ = ABCMeta

  @abstractmethod
  def execute(self):
    pass