import unittest

from blocks import BlockType, markdown_to_blocks, block_to_block_type


class TestBlocks(unittest.TestCase):
    # Test converting markdown text to blocks
    def test_markdown_to_blocks_empty(self):
        text = ""
        res = markdown_to_blocks(text)
        expected = []
        self.assertEqual(expected, res)

    def test_markdown_to_blocks(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        res = markdown_to_blocks(text)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(expected, res)

    # Test determining type of markdown block
    def test_block_type_none(self):
        block = """
This block has no format.
It should be of type \"paragraph\""""
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    # TODO: Finish unit tests
    def test_block_type_heading(self):
        pass

    def test_block_type_code(self):
        pass

    def test_block_type_quote(self):
        pass

    def test_block_type_ul(self):
        pass

    def test_block_type_ol(self):
        pass


if __name__ == "__main__":
    unittest.main()
