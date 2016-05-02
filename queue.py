from time import sleep
import thread

class Queue():
  def __init__(self):
    self.data = None
    self.is_executing = False

  def __len__(self):
    if self.data:
      return 1
    else:
      return 0

  def addData(self, data):
    self.data = data
    self.executeData()

  def executeData(self):
    thread.start_new_thread(self.test, ())

  def test(self):
    sleep(2)
    print("testin testin")
