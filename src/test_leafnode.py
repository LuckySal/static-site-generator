import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_empty_leaf(self):
        with self.assertRaises(TypeError):
            node = LeafNode()

    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="p", value=None)
            res = node.to_html()

    def test_leaf_no_tag(self):
        test_value = "This is a test"
        node = LeafNode(tag=None, value=test_value)
        self.assertEqual(node.to_html(), test_value)


if __name__ == "__main__":
    unittest.main()
