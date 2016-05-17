import unittest
from gui.codelistview import CodeListView

class TestCodeListView(unittest.TestCase):
  def test_format_line_data_normal_args(self):
    listview = CodeListView()
    data = listview._format_line_data(["test"])

    self.assertEqual(data, [{"index": "1  ", "line": "test"}])

if __name__ == '__main__':
    unittest.main()