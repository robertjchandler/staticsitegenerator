import re
from textnode import text_node_to_html_node
from htmlnode import ParentNode
from split_delimiter import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks = []
    for block in split_markdown:
        if block != "":
            blocks.append(block.rstrip().lstrip())
    return blocks

def block_to_block_type(markdown):
    if(re.match(r"^#{1,6} ", markdown) is not None):
        return "heading"
    elif(re.match(r"^`{3}[\w\W\s]*`{3}$", markdown) is not None):
        return "code"
    elif(re.match(r"^> ", markdown, re.MULTILINE) is not None):
        return "quote"
    elif(re.match(r"^[*|-] ", markdown, re.MULTILINE) is not None):
        return "unordered_list"
    elif(re.match(r"^\d\. ", markdown, re.MULTILINE) is not None):
        return "ordered_list"
    else:
        return "paragraph"

def markdown_to_html_node(markdown):
    block_type = block_to_block_type(markdown)
    if block_type == block_type_paragraph:
        return paragraph_helper(markdown)
    if block_type == block_type_heading:
        return heading_helper(markdown)
    if block_type == block_type_code:
        return code_helper(markdown)
    if block_type == block_type_olist:
        return ordered_list_helper(markdown)
    if block_type == block_type_ulist:
        return unordered_list_helper(markdown)
    if block_type == block_type_quote:
        return quote_helper(markdown)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def heading_helper(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_helper(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def quote_helper(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def unordered_list_helper(block):
    list_items = []
    split_block = block.split("\n")
    for item in split_block:
        text = item[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)

def ordered_list_helper(block):
    list_items = []
    split_block = block.split("\n")
    for item in split_block:
        text = item[3:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)

def paragraph_helper(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)
