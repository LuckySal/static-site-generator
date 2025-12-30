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
    return [x.strip() for x in blocks_list if x]


def block_to_block_type(block):
    if re.search(r"^(#{1-6} ).+", block):
        return BlockType.HEADING
    if re.search(r"^```[\s.]+```$", block):
        return BlockType.CODE
    if block[0] == ">":
        return is_quote(block)
    if block[0:2] == "- ":
        return is_ul(block)
    if block[0:3] == "1. ":
        return is_ol(block)
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
