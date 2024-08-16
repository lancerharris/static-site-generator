import re

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown):
    blocks = re.split(r'\n{2,}', markdown.strip())
    blocks = [block.strip() for block in blocks]
    return blocks

def block_to_block_type(block: str) -> str:
    heading_match = re.match(r"^(#{1,6})\s", block)
    if heading_match:
        return f"heading"

    if block.startswith("```") and block.endswith("```"):
        return "code-block"

    if all(line.startswith(">") for line in block.splitlines()):
        return "quote-block"

    if all(line.startswith(("* ", "- ")) for line in block.splitlines()):
        return "unordered-list"

    lines = block.splitlines()
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return "ordered-list"

    return "paragraph"

def markdown_heading_to_html_node(block):
    num_hashes = len(re.match(r"^#+", block).group(0))
    text = re.sub(r"^#+\s*", "", block)
    return ParentNode(f"h{num_hashes}", markdown_to_html_children(text))

def markdown_quote_block_to_html_node(block):
    lines = block.splitlines()
    text = "\n".join([re.sub(r"^> ", "", line) for line in lines])
    return ParentNode("blockquote", markdown_to_html_children(text))

def markdown_list_to_html_node(block, list_type):
    lines = block.splitlines()
    list_items = []
    for line in lines:
        if list_type == "ul":
            text = re.sub(r"^[*-] ", "", line)
        if list_type == "ol":
            text = re.sub(r"^\d+\. ", "", line)
        list_items.append(ParentNode("li", markdown_to_html_children(text)))
    return ParentNode(list_type, list_items)

def markdown_code_block_to_html_node(block):
    code_text = re.sub(r"^```|```$", "", block)
    return ParentNode("pre", [LeafNode("code", code_text)])

def markdown_to_html_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    sibling_blocks = []
    block_functions = {
        "heading": markdown_heading_to_html_node,
        "quote-block": markdown_quote_block_to_html_node,
        "unordered-list": lambda block: markdown_list_to_html_node(block, list_type="ul"),
        "ordered-list": lambda block: markdown_list_to_html_node(block, list_type="ol"),
        "code-block": markdown_code_block_to_html_node,
    }

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type in block_functions:
            sibling_blocks.append(block_functions[block_type](block))
        else:
            sibling_blocks.append(ParentNode("p", markdown_to_html_children(block)))
            
    return ParentNode("div", sibling_blocks)
            