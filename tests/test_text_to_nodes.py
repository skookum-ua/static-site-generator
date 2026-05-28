import unittest
from src.textnode import Inline, TextNode
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.main import split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextToNode(unittest.TestCase):
    def test_text_to_images(self):
        node = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"

        new_nodes = text_to_textnodes(node)

        self.assertListEqual(
            [
                TextNode("This is text with an ", Inline.TEXT),
                TextNode("image", Inline.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", Inline.TEXT),
                TextNode(
                    "second image", Inline.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_text_to_nodes(self):

        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(node)

        self.assertListEqual(
            [
                TextNode("This is ", Inline.TEXT),
                TextNode("text", Inline.BOLD),
                TextNode(" with an ", Inline.TEXT),
                TextNode("italic", Inline.ITALIC),
                TextNode(" word and a ", Inline.TEXT),
                TextNode("code block", Inline.CODE),
                TextNode(" and an ", Inline.TEXT),
                TextNode("obi wan image", Inline.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", Inline.TEXT),
                TextNode("link", Inline.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )