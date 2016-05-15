import unittest
from modules.blame import Blame
from mock import Mock

class TestBlame(unittest.TestCase):
  def setUp(self):
    self.mock = Mock()
    self.args = {}
    self.args["callback"] = self.mock.method
    self.args["event"] = "blame"
    self.args["event_id"] = "blame7main.py"
    self.args["repo"] = None
    self.args["file"] = None

  def test_execute_normal_args(self):
    self.args["intermediate_data"] = {"asd87y": [1,2,3,8,9,10,23,25,38,39,40],
      "9usdfo": [4,5,6,7,15,16,17,18,28,29,30]}
    self.args["line"] = 10
    expected_result = {"asd87y": self.args["intermediate_data"]["asd87y"]}

    blame_obj = Blame(**self.args)
    blame_obj.execute()
    self.mock.method.assert_called_with(self.args["event_id"], "blame_result", expected_result)

    self.args["line"] = 29
    expected_result = {"9usdfo": self.args["intermediate_data"]["9usdfo"]}

    blame_obj = Blame(**self.args)
    blame_obj.execute()
    self.mock.method.assert_called_with(self.args["event_id"], "blame_result", expected_result)

if __name__ == '__main__':
    unittest.main()