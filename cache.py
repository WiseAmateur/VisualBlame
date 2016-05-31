from threading import Lock


class Cache():
  def __init__(self):
    self.cache = {}
    self.default = None

  def __len__(self):
    return len(self.cache)

  def store(self, key, value):
    lock = Lock()

    lock.acquire()
    try:
      self.cache[key] = value
    finally:
      lock.release()

  def get(self, key):
    lock = Lock()

    lock.acquire()
    try:
      # print "get key:", "<<<<<" + key + ">>>>"
      # for key in self.cache:
        # print "key:", key
      try:
        return self.cache[key]
      except KeyError:
        return self.default
    finally:
      lock.release()
