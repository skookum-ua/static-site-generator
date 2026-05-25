from textnode import Inline, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
def main():

    new_node = TextNode("value", Inline.BOLD )
    
    print(repr(new_node))

def text_node_to_html_node(text_node):
    if text_node.text_type == Inline.TEXT:
        return LeafNode(None,text_node.text)
    elif text_node.text_type == Inline.BOLD:
        return LeafNode("b",text_node.text)
    elif text_node.text_type == Inline.ITALIC:
        return LeafNode("i",text_node.text)
    elif text_node.text_type == Inline.CODE:
        return LeafNode("code",text_node.text)
    elif text_node.text_type == Inline.LINK:
        return LeafNode("a",text_node.text, {"href": text_node.url})
    elif text_node.text_type == Inline.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("not supported tag")


main()