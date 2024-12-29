import unittest

from textnode import TextNode, TextType
from markdown_to_blocks import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
)

from split_delimiter import (
    split_nodes_image,
    split_nodes_link,
    split_nodes_delimiter,
    text_to_textnodes,
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
        
if __name__ == "__main__":
    unittest.main()
