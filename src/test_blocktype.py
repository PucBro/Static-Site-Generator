import unittest
from blocktype import block_to_block_type, BlockType

class TestBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_code_block(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote_block(self):
        quote = "> This is a quote\n> Another line"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        not_quote = "> Quote\nNormal line"
        self.assertEqual(block_to_block_type(not_quote), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        ul = "- item 1\n- item 2"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)
        not_ul = "- item 1\nitem 2"
        self.assertEqual(block_to_block_type(not_ul), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        ol = ". item 1\n. item 2"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)
        not_ol = ". item 1\nitem 2"
        self.assertEqual(block_to_block_type(not_ol), BlockType.PARAGRAPH)

    def test_paragraph(self):
        para = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(para), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
