import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from split_delimiter import (
    split_nodes_image,
    split_nodes_link,
    split_nodes_delimiter,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    heading_helper,
    code_helper,
    quote_helper,
    unordered_list_helper,
    ordered_list_helper,
    paragraph_helper,
    extract_markdown_images,
    extract_markdown_links,
)

class TestSplitDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bold")

    def test_italic(self):
        node = TextNode("This is text with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, "italic")

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[1].text, "code block")

class TestExtractMarkdownImagesLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

def test_split_image_single(self):
    node = TextNode(
        "![image](https://www.example.COM/IMAGE.PNG)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
        ],
        new_nodes,
    )

def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

def test_split_links(self):
    node = TextNode(
        "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
            TextNode(" with text that follows", TextType.TEXT),
        ],
        new_nodes,
    )
    
def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
        
def test_markdown_to_blocks(self):
     markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
     blocks = markdown_to_blocks(markdown)
     self.assertListEqual(
          [
               "# This is a heading",
               "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
               "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
          ],
          blocks,
     )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        markdown = "# This is a heading"
        self.assertEqual(block_to_block_type(markdown), "heading")

    def test_code(self):
        markdown = "``` This\n\tis\n\ta.\n\t(c0de)\n\t# block ```"
        self.assertEqual(block_to_block_type(markdown), "code")

    def test_quote(self):
        markdown = "> This\n> is\n> a\n> quote"
        self.assertEqual(block_to_block_type(markdown), "quote")

    def test_unordered_list(self):
        markdown = "* This\n* is\n* an\n- unordered\n- list"
        self.assertEqual(block_to_block_type(markdown), "unordered_list")

    def test_ordered_list(self):
        markdown = "1. This\n2. is\n3. an\n4. ordered\n5. list"
        self.assertEqual(block_to_block_type(markdown), "ordered_list")
        
    def test_paragraph(self):
        markdown = "This is a paragraph."
        self.assertEqual(block_to_block_type(markdown), "paragraph")
        
def test_heading_helper(self):
    block = "# This a a heading"
    self.assertEqual(heading_helper(block), LeafNode("h1", "This is a heading"))

def test_code_helper(self):
    block = "``` This\n\tis\n\ta.\n\t(c0de)\n\t# block ```"
    self.assertEqual(code_helper(block), LeafNode("code", str(LeafNode("pre", "This\n\tis\n\ta.\n\t(c0de)\n\t# block"))))

def test_quote_helper(self):
    block = "> This is a quote"
    self.assertEqual(quote_helper(block), LeafNode("blockquote", "This is a quote"))

def test_unordered_list_helper(self):
    block = "* This is an unordered list"
    self.assertEqual(unordered_list_helper(block), ParentNode("ul", [LeafNode("li", "This is an unordered list")]))

def test_ordered_list_helper(self):
    block = "1. This is an ordered list"
    self.assertEqual(ordered_list_helper(block), ParentNode("ol", [LeafNode("li", "This is an ordered list")]))

def test_paragraph_helper(self):
    block = "This is a paragraph."
    self.assertEqual(paragraph_helper(block), LeafNode("p", block))
