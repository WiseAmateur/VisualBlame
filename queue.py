from time import sleep
# from blame import Blame
import threading
# import pygit2

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
    threading.Thread(target=self.test, args=()).start()

  # temporary function to demonstrate workings
  def test(self):
    # repo = Repository('.git')
    # blame = Blame(repo, 'main.py')
    sleep(2)
    print("test")
