import unittest
import requests
import os

class TestBot(unittest.TestCase):
  def test_connection(self):
    response = requests.get(os.environ.get("url"))
    if response.status_code !=200:
      self.fail("Unable to connect")
