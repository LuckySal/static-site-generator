import unittest

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    text_node_to_html_node,
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    # TextNode
    def test_text_empty(self):
        with self.assertRaises(TypeError):
            node = TextNode()

    def test_text_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_diff_type(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_text_set_link(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode(
            "This is a url node", TextType.LINK, "https://google.com"
        )
        self.assertEqual(node1.url, None)
        self.assertEqual(node2.url, "https://google.com")

    def test_text_no_type(self):
        with self.assertRaises(TypeError):
            node = TextNode("Text node with no type", None)
            html_node = text_node_to_html_node(node)

    def test_text_wrong_type(self):
        with self.assertRaises(AttributeError):
            node = TextNode("Text node with invalid type", TextType.BOOK)

    # text_node_to_html_node
    def test_text_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_image_to_html(self):
        node = TextNode("Image alt text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        expected = '<img src="image.png" alt="Image alt text"></img>'
        self.assertEqual(html_node.to_html(), expected)

    # split_nodes_delimiter
    def text_split_markdown(self):
        node = TextNode("This contains **bold** text.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes[1].text, "bold")
        self.assertEqual(split_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(split_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(len(split_nodes), 3)

    def test_split_md_beginning(self):
        node = TextNode("_The_ italic text is at the beginning", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(split_nodes[0].text, "The")
        self.assertEqual(split_nodes[0].text_type, TextType.ITALIC)
        self.assertEqual(split_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(len(split_nodes), 2)

    def test_split_md_end(self):
        node = TextNode("The italic text is at the _end_", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(split_nodes[1].text, "end")
        self.assertEqual(split_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(split_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(len(split_nodes), 2)

    def test_split_no_md(self):
        node = TextNode("This text contains no markdown.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(split_nodes[0].text, "This text contains no markdown.")
        self.assertEqual(len(split_nodes), 1)

    def test_split_other_text_type(self):
        node = TextNode("This whole node is bold.", TextType.BOLD)
        split_nodes_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        split_nodes_italic = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(split_nodes_bold), 1)
        self.assertEqual(split_nodes_bold[0].text, "This whole node is bold.")
        self.assertEqual(split_nodes_bold[0].text_type, TextType.BOLD)
        self.assertEqual(len(split_nodes_italic), 1)
        self.assertEqual(split_nodes_italic[0].text, "This whole node is bold.")
        self.assertEqual(split_nodes_italic[0].text_type, TextType.BOLD)

    def test_split_multiple_nodes(self):
        node1 = TextNode("This node has **bold** text.", TextType.TEXT)
        node2 = TextNode("This node has _italic_ text.", TextType.TEXT)
        split_nodes_bold = split_nodes_delimiter(
            [node1, node2], "**", TextType.BOLD
        )
        self.assertEqual(len(split_nodes_bold), 4)
        self.assertEqual(split_nodes_bold[1].text_type, TextType.BOLD)
        self.assertEqual(split_nodes_bold[3].text_type, TextType.TEXT)

        split_nodes_both = split_nodes_delimiter(
            split_nodes_bold, "_", TextType.ITALIC
        )
        self.assertEqual(len(split_nodes_both), 6)
        self.assertEqual(split_nodes_both[4].text_type, TextType.ITALIC)
        self.assertEqual(split_nodes_both[4].text, "italic")
        self.assertEqual(split_nodes_both[3].text_type, TextType.TEXT)

    # Extract links and images
    def test_extract_markdown_images(self):
        matches1 = extract_markdown_images(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)."
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches1
        )

        matches2 = extract_markdown_images("This text contains no images")
        self.assertListEqual([], matches2)

        matches3 = extract_markdown_images(
            "This text contains a [link](https://google.com)."
        )
        self.assertListEqual([], matches3)

        matches4 = extract_markdown_images(
            "This text contains an ![image](image.png) and a [link](link.com)."
        )
        self.assertListEqual([("image", "image.png")], matches4)

        matches5 = extract_markdown_images(
            "This text contains ![image1](image1.png) and ![image2](image2.jpg)."
        )
        self.assertListEqual(
            [("image1", "image1.png"), ("image2", "image2.jpg")], matches5
        )

    def test_extract_markdown_links(self):
        matches1 = extract_markdown_links(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)."
        )
        self.assertListEqual([], matches1)

        matches2 = extract_markdown_links("This text contains no links")
        self.assertListEqual([], matches2)

        matches3 = extract_markdown_links(
            "This text contains a [link](https://google.com)."
        )
        self.assertListEqual([("link", "https://google.com")], matches3)

        matches4 = extract_markdown_links(
            "This text contains an ![image](image.png) and a [link](link.com)."
        )
        self.assertListEqual([("link", "link.com")], matches4)

        matches5 = extract_markdown_links(
            "This text contains [link1](link1.org) and [link2](link2.edu)."
        )
        self.assertListEqual(
            [("link1", "link1.org"), ("link2", "link2.edu")], matches5
        )

    # Split text nodes by links and images
    def test_split_node_link_none(self):
        node = TextNode("This node contains no links.", TextType.TEXT)
        res = split_nodes_link([node])
        expected = [node]
        self.assertListEqual(expected, res)

    def test_split_node_link_multiple(self):
        text1 = (
            "This node contains two links and one image: "
            "[link1](link1.com), "
            "![image1](image1.png), and "
            "[link1_5](link1_5.com). "
            "That is all."
        )
        node = TextNode(text1, TextType.TEXT)
        res = split_nodes_link([node])
        expected = [
            TextNode(
                "This node contains two links and one image: ", TextType.TEXT
            ),
            TextNode("link1", TextType.LINK, "link1.com"),
            TextNode(", ![image1](image1.png), and ", TextType.TEXT),
            TextNode("link1_5", TextType.LINK, "link1_5.com"),
            TextNode(". That is all.", TextType.TEXT),
        ]
        self.assertListEqual(expected, res)

    def test_split_nodes_link_beginning(self):
        node = TextNode("[link](link.com) for example", TextType.TEXT)
        res = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "link.com"),
            TextNode(" for example", TextType.TEXT),
        ]
        self.assertListEqual(expected, res)

    def test_split_image_multiple(self):
        node = TextNode(
            (
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
                "and another ![second image](https://i.imgur.com/3elNhQu.png)"
            ),
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_list(self):
        node1 = TextNode("This node contains no images.", TextType.TEXT)
        node2 = TextNode("![image1](image1.png) for example", TextType.TEXT)
        node3 = TextNode(
            (
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
                "and another ![second image](https://i.imgur.com/3elNhQu.png)"
            ),
            TextType.TEXT,
        )
        res = split_nodes_image([node1, node2, node3])
        expected = [
            TextNode("This node contains no images.", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "image1.png"),
            TextNode(" for example", TextType.TEXT),
            TextNode("This is text with an ", TextType.TEXT),
            TextNode(
                "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
            ),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image",
                TextType.IMAGE,
                "https://i.imgur.com/3elNhQu.png",
            ),
        ]
        self.assertListEqual(expected, res)

    # Convert text to textnodes
    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word "
            "and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        res = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, res)

    def test_text_to_textnodes_no_md(self):
        text = "This text has no markdown whatsoever."
        res = text_to_textnodes(text)
        expected = [
            TextNode("This text has no markdown whatsoever.", TextType.TEXT)
        ]
        self.assertListEqual(expected, res)


if __name__ == "__main__":
    unittest.main()
