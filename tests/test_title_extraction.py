from src.main import extract_title
import unittest

class TestTextToHTMLNode(unittest.TestCase):
    def test_title1(self):
        text = """# This is text with
This is text with
This is text with
This is text with"""
        self.assertEqual(extract_title(text), "This is text with")