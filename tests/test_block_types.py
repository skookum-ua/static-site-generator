import unittest
from src.textnode import Block
from src.main import block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_block_type_heading(self):
        md = "# This is **bolded** paragraph"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, Block.HEADING)
    def test_block_type_paragraph(self):
        md = "This is **bolded** paragraph"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, Block.PARAGRAPH)
    def test_block_type_heading2(self):
        md = "###### This is **bolded** paragraph"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, Block.HEADING)
    def test_block_type_quote1(self):
        md = "> This is **bolded** paragraph"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, Block.QUOTE)
    def test_block_type_unordered_list(self):
        md = """- This is **bolded** paragraph
- This is **bolded** paragraph
- This is **bolded** paragraph
- This is **bolded** paragraph"""
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, Block.UNORDERED_LIST)
    def test_block_type_ordered_list(self):
        md = """1. This is **bolded** paragraph
2. This is **bolded** paragraph
3. This is **bolded** paragraph
4. This is **bolded** paragraph"""
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, Block.ORDERED_LIST)
    def test_block_type_code(self):
        md = """```This is **bolded** paragraph
- This is **bolded** paragraph
- This is **bolded** paragraph
- This is **bolded** paragraph```"""
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, Block.CODE)
    def test_block_type_quote(self):
        md = """> This is **bolded** paragraph
> This is **bolded** paragraph
> This is **bolded** paragraph
> This is **bolded** paragraph"""
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, Block.QUOTE)
