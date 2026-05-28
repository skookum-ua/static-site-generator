import unittest
from src.textnode import *
from src.htmlnode import *
from src.main import *

class TestEverything(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_headings(self):
        md = """
# Heading 1

## Heading 2 with **bold**

### Heading 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2><h3>Heading 3</h3></div>",
        )

    def test_unordered_list(self):
        md = """
- First item with `code`
- Second **bold** item
- Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item with <code>code</code></li><li>Second <b>bold</b> item</li><li>Third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with _italics_
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italics</i></li><li>Third item</li></ol></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote
> across multiple lines
> with **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote across multiple lines with <b>bold</b> text</blockquote></div>",
        )

    def test_mixed_blocks(self):
        md = """
# My Blog Post

This is the introduction.

- Bullet 1
- Bullet 2

> A wise quote here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<h1>My Blog Post</h1>"
            "<p>This is the introduction.</p>"
            "<ul><li>Bullet 1</li><li>Bullet 2</li></ul>"
            "<blockquote>A wise quote here</blockquote>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_empty_and_whitespace(self):
        md = """
   
   
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")