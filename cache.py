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
