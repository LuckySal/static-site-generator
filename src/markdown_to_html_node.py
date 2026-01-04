from htmlnode import ParentNode, LeafNode
from textnode import (
    TextType,
    TextNode,
    text_node_to_html_node,
    text_to_textnodes,
)
from blocks import BlockType, markdown_to_blocks, block_to_block_type


def markdown_to_html_node(markdown):
    blocks_list = markdown_to_blocks(markdown)
    nodes_list = blocks_to_nodes(blocks_list)
    return ParentNode("div", nodes_list)


def blocks_to_nodes(blocks_list):
    nodes_list = []
    for block in blocks_list:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            text_node = strip_code(block)
            html_node = text_node_to_html_node(text_node)
            wrapped_code_node = ParentNode("pre", [html_node])
            nodes_list.append(wrapped_code_node)
        elif block_type == BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(block)
            child_nodes = [text_node_to_html_node(node) for node in text_nodes]
            nodes_list.append(ParentNode("p", child_nodes))
        elif block_type == BlockType.HEADING:
            text, level = strip_heading(block)
            text_nodes = text_to_textnodes(text)
            child_nodes = [text_node_to_html_node(node) for node in text_nodes]
            nodes_list.append(ParentNode(f"h{level}", child_nodes))
        elif block_type == BlockType.QUOTE:
            text = strip_quotes(block)
            text_nodes = text_to_textnodes(text)
            child_nodes = [text_node_to_html_node(node) for node in text_nodes]
            nodes_list.append(ParentNode("blockquote", child_nodes))
        elif block_type == BlockType.UNORDERED_LIST:
            child_nodes = itemize(block, BlockType.UNORDERED_LIST)
            nodes_list.append(ParentNode("ul", child_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            child_nodes = itemize(block, BlockType.ORDERED_LIST)
            nodes_list.append(ParentNode("ol", child_nodes))
    return nodes_list


def strip_code(block):
    text = block.strip()[3:-3].lstrip()
    return TextNode(text, TextType.CODE)


def strip_heading(block):
    text, level = "", 0
    for i in range(len(block)):
        if block[i] == "#":
            text = block[i + 1 :]
            level += 1
            if block[i + 1] == " ":
                text = block[i + 2 :]
                break
    return text, level


def strip_quotes(block):
    lines = block.split("\n")
    new_lines = [line[1:] for line in lines]
    return "\n".join(new_lines)


def itemize(block, block_type):
    lines = block.split("\n")
    items = []
    if block_type == BlockType.UNORDERED_LIST:
        for line in lines:
            text_nodes = text_to_textnodes(line[2:])
            children = [text_node_to_html_node(child) for child in text_nodes]
            items.append(ParentNode("li", children))
    elif block_type == BlockType.ORDERED_LIST:
        if block_type == BlockType.UNORDERED_LIST:
            for line in lines:
                text_nodes = text_to_textnodes(line[3:])
                children = [
                    text_node_to_html_node(child) for child in text_nodes
                ]
                items.append(ParentNode("li", children))
    else:
        raise TypeError(f"{block_type} cannot be itemized")
    return items
