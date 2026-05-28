import unittest
from src.textnode import TextNode, Inline

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", Inline.BOLD)
        node2 = TextNode("This is a text node", Inline.BOLD)
        self.assertEqual(node, node2)
    def test_none(self):
        node = TextNode("This is a text node", Inline.BOLD, None)
        node2 = TextNode("This is a text node", Inline.BOLD, None)
        self.assertEqual(node, node2)
    def test_not_equal_types(self):
        node = TextNode("This is a text node", Inline.LINK, None)
        node2 = TextNode("This is a text node", Inline.ITALIC, None)
        self.assertNotEqual(node, node2)
    def test_not_equal_url(self):
        node = TextNode("This is a text node", Inline.LINK)
        node2 = TextNode("This is a text node", Inline.ITALIC, None)
        self.assertNotEqual(node, node2)
    def test_not_equal_url2(self):
        node = TextNode("This is a text node", Inline.LINK, "None")
        node2 = TextNode("This is a text node", Inline.ITALIC, None)
        self.assertNotEqual(node, node2)
    

if __name__ == "__main__":
    unittest.main()