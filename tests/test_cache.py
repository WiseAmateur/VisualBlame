import unittest
from cache import Cache

# Only test public functions, only use public functions in tests
class TestCache(unittest.TestCase):
  def setUp(self):
    self.cache = Cache()

  def test_store(self):
    self.cache.store("key1", "value1")
    self.cache.store("key2", "value2")

    self.assertEqual(2, len(self.cache))
    self.assertEqual("value2", self.cache.get("key2"))

  def test_get(self):
    self.cache.store("key1", "value1")

    self.assertEqual("value1", self.cache.get("key1"))
    self.assertIsNone(self.cache.get("key2"))

if __name__ == '__main__':
    unittest.main()