import re
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode

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
    elif(re.match(r"^>", markdown, re.MULTILINE) is not None):
        return "quote"
    elif(re.match(r"^[*|-] ", markdown, re.MULTILINE) is not None):
        return "unordered_list"
    elif(re.match(r"^\d\. ", markdown, re.MULTILINE) is not None):
        return "ordered_list"
    else:
        return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            return heading_helper(block)
        elif block_type == "code":
            return code_helper(block)
        elif block_type == "quote":
            return quote_helper(block)
        elif block_type == "unordered_list":
            pass
        elif block_type == "ordered_list":
            pass
        else:
            # block_type == "paragraph"
            return paragraph_helper(block)

def heading_helper(block):
    split_block = block.split(" ", maxsplit=1)
    heading_type = len(split_block[0])
    tag = f"h{heading_type}"
    return LeafNode(tag, split_block[1])

def code_helper(block):
    code = block.lstrip("``` ").rstrip(" ```")
    return LeafNode("code", str(LeafNode("pre", code)))

def quote_helper(block):
    quote = block.split("> ")
    return LeafNode("blockquote", quote)

def unordered_list_helper(block):
    pass

def ordered_list_helper(block):
    pass

def paragraph_helper(block):
    return LeafNode("p", block)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
