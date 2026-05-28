from src.textnode import Inline, TextNode
from src.htmlnode import HTMLNode, LeafNode, ParentNode
import unittest
from src.main import split_nodes_delimiter


class TestDelimiterSplit(unittest.TestCase):
    def test_1(self):
        node = TextNode("This is text with a `code block` word", Inline.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", Inline.CODE)
        self.assertEqual(new_nodes, [
    TextNode("This is text with a ", Inline.TEXT),
    TextNode("code block", Inline.CODE),
    TextNode(" word", Inline.TEXT),
])
    def test_2(self):
        node = TextNode("This is text with a `code block`", Inline.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", Inline.CODE)
        self.assertEqual(new_nodes, [
    TextNode("This is text with a ", Inline.TEXT),
    TextNode("code block", Inline.CODE),
    
])
    def test_3(self):
        node = TextNode("`code block`", Inline.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", Inline.CODE)
        self.assertEqual(new_nodes, [

    TextNode("code block", Inline.CODE),
    
])
    def test_error(self):
        node = TextNode("`code block", Inline.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", Inline.CODE)

    def test_4(self):
        node = TextNode("````````", Inline.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", Inline.CODE)
        self.assertEqual(new_nodes, [])