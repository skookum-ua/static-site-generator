import unittest
from src.textnode import Inline, TextNode
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.main import split_nodes_image, split_nodes_link

class TestTextToSplitImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            Inline.TEXT,
        )
        new_nodes = split_nodes_image([node])

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

    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            Inline.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", Inline.TEXT),
                TextNode("image", Inline.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", Inline.TEXT),
                TextNode(
                    "second image", Inline.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )