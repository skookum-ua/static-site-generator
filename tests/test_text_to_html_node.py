import unittest
from src.textnode import Inline, TextNode
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.main import text_node_to_html_node

class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a paragraph of text.", Inline.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a paragraph of text.")
    
    def test_bold(self):
        node = TextNode("This is a text node", Inline.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link(self):
        node = TextNode("This is a text node", Inline.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
