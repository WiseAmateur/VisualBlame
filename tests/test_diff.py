import unittest
from modules.diff import Diff
from mock import Mock
import pygit2

class TestDiff(unittest.TestCase):
  def setUp(self):
    self.mock = Mock()
    self.args = {}
    self.args["callback"] = self.mock.method
    self.args["event"] = "diff"
    self.args["event_id"] = "diff594ce03e25bcb2105d65011978b14ece128d5802"
    self.args["repo"] = pygit2.Repository(".")
    self.args["file"] = "main.py"

  def test_execute_normal_args(self):
    self.args["intermediate_data"] = None
    self.args["commit_id"] = "594ce03e25bcb2105d65011978b14ece128d5802"

    diff_obj = Diff(**self.args)
    diff_obj.execute()

if __name__ == '__main__':
    unittest.main()