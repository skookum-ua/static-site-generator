import unittest
from src.htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_tag_p(self):
        node = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
    def test_tag_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(repr(node), "LeafNode(a, Click me!, {'href': 'https://www.google.com'})")
