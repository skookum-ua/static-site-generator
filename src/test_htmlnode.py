import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_node(self):
        node = HTMLNode()
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
    def test_props_to_html(self):
        props = {"href": "https://www.google.com","target": "_blank",}
        child = HTMLNode("tag")
        children = []
        children.append(child)
        node = HTMLNode("tag", "value", children, props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    def test_repr(self):
        props = {"href": "https://www.google.com","target": "_blank",}
        child = HTMLNode("tag")
        children = []
        children.append(child)
        node = HTMLNode("tag", "value", children, props)
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, "value")



if __name__ == "__main__":
    unittest.main()