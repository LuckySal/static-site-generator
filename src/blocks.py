import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text):
    blocks_list = text.split("\n\n")
    return [block.strip() for block in blocks_list if block]


def block_to_block_type(block):
    if re.search(r"^(#{1,6} ).+", block):
        return BlockType.HEADING
    if re.search(r"^```[\s\S]+```$", block):
        return BlockType.CODE
    if block[0] == ">":
        if is_quote(block):
            return BlockType.QUOTE
    if block[0:2] == "- ":
        if is_ul(block):
            return BlockType.UNORDERED_LIST
    if block[0:3] == "1. ":
        if is_ol(block):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def is_quote(block):
    lines = [x.strip() for x in block.split("\n") if x]
    for line in lines:
        if line[0] != ">":
            return False
    return True


def is_ul(block):
    lines = [x.strip() for x in block.split("\n") if x]
    for line in lines:
        if line[0:2] != "- ":
            return False
    return True


def is_ol(block):
    lines = [x.strip() for x in block.split("\n") if x]
    for i, line in enumerate(lines):
        if line[0:3] != f"{i + 1}. ":
            return False
    return True
