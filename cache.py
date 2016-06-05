class Cache():
  def __init__(self):
    self.cache = {}
    self.default = None

  def __len__(self):
    return len(self.cache)

  def store(self, key, value):
    self.cache[key] = value

  def get(self, key):
    try:
      return self.cache[key]
    except KeyError:
      return self.default


class EventCache(Cache):
  def store(self, event, key, value):
    try:
      self.cache[event][key] = value
    except KeyError:
      self.cache[event] = {}
      self.cache[event][key] = value
