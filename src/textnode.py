import re
from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    """An enum of supported text types"""

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """A class containing basic information abaout a section of text"""

    def __init__(self, text, text_type, url=None):
        """TextNode constructor

        Args:
            text (string, required): Contents of the text.
            text_type (TextType, required): The type of the text. Used to convert to HTML. See TextType enum for accepted types.
            url (string, optional): URL destination for link and image text types. Defaults to None.
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    """Converts a text node to the corresponding LeafNode

    Args:
        text_node (TextNode, required): A text node to convert

    Raises:
        TypeError: Raised if text type is missing or incorrect

    Returns:
        LeafNode: Leaf node containing HTML properties
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise TypeError("Node is not a recognized type.")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
        else:
            count = node.text.count(delimiter)
            if count == 0:
                new_nodes.append(node)
            elif count % 2 == 0:
                text_list = node.text.split(delimiter)
                for i, val in enumerate(text_list):
                    if val != "":
                        if i % 2 == 0:
                            new_nodes.append(TextNode(val, TextType.TEXT))
                        else:
                            new_nodes.append(TextNode(val, text_type))
            else:
                raise ValueError(
                    f'"{node.text}" does not contain valid markdown.'
                )
    return new_nodes


def extract_markdown_links(text):
    rx = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(rx, text)
    return matches


def extract_markdown_images(text):
    rx = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(rx, text)
    return matches


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            temp = [node.text]
            matches = extract_markdown_links(node.text)
            for match in matches:
                temp = temp[-1].split(f"[{match[0]}]({match[1]})", 1)
                if len(temp[0]) > 0:
                    new_nodes.append(TextNode(temp[0], node.text_type))
                new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            if len(temp[-1]) > 0:
                new_nodes.append(TextNode(temp[-1], node.text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            temp = [node.text]
            matches = extract_markdown_images(node.text)
            for match in matches:
                temp = temp[-1].split(f"![{match[0]}]({match[1]})", 1)
                if len(temp[0]) > 0:
                    new_nodes.append(TextNode(temp[0], node.text_type))
                new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            if len(temp[-1]) > 0:
                new_nodes.append(TextNode(temp[-1], node.text_type))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text.replace("\n", " "), TextType.TEXT)
    nodes_list = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes_list = split_nodes_delimiter(nodes_list, "_", TextType.ITALIC)
    nodes_list = split_nodes_delimiter(nodes_list, "`", TextType.CODE)
    nodes_list = split_nodes_link(nodes_list)
    nodes_list = split_nodes_image(nodes_list)
    return nodes_list
