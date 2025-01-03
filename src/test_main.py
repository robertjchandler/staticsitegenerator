import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_missing_title(self):
        markdown = "Hello"
        self.assertRaises(Exception)
