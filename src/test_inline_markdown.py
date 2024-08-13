import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,

    text_bold_delimiter,
    text_italic_delimiter,
    text_code_delimiter,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_text_node(self):
        node = TextNode("This is a text node", text_type_text)
        nodes = [node]
        new_nodes = split_nodes_delimiter(nodes, text_code_delimiter, text_type_code)
        self.assertListEqual(
            [
                TextNode("This is a text node", text_type_text)
            ],
            new_nodes
        )

    def test_single_code_node(self):
        node = TextNode("This is a `code` node", text_type_text)
        nodes = [node]
        new_nodes = split_nodes_delimiter(nodes, text_code_delimiter, text_type_code)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, text_type_code)
        self.assertEqual(new_nodes[2].text, " node")
        self.assertListEqual(
            [
                TextNode("This is a ", text_type_text),
                TextNode("code", text_type_code),
                TextNode(" node", text_type_text)
            ],
            new_nodes
        )
    
    def test_single_code_node2(self):
        node = TextNode("This is a `code` node with `code2`", text_type_text)
        nodes = [node]
        new_nodes = split_nodes_delimiter(nodes, text_code_delimiter, text_type_code)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, text_type_code)
        self.assertEqual(new_nodes[2].text, " node with ")
        self.assertEqual(new_nodes[3].text, "code2")
        self.assertEqual(new_nodes[3].text_type, text_type_code)
        self.assertListEqual(
            [
                TextNode("This is a ", text_type_text),
                TextNode("code", text_type_code),
                TextNode(" node with ", text_type_text),
                TextNode("code2", text_type_code)
            ],
            new_nodes
        )

    def test_single_bold_node(self):
        node = TextNode("This is a **bold** node", text_type_text)
        nodes = [node]
        new_nodes = split_nodes_delimiter(nodes, text_bold_delimiter, text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" node", text_type_text),
            ],
            new_nodes
        )

    def test_single_italic_node(self):
        node = TextNode("This is an *italic* node", text_type_text)
        nodes = [node]
        new_nodes = split_nodes_delimiter(nodes, text_italic_delimiter, text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" node", text_type_text),
            ],
            new_nodes
        )

    def test_double_code_node(self):
        node1 = TextNode("This is a `code` node", text_type_text)
        node2 = TextNode("This is a `code2` node", text_type_text)
        nodes = [node1, node2]
        new_nodes = split_nodes_delimiter(nodes, text_code_delimiter, text_type_code)
        self.assertListEqual(
            [
                TextNode("This is a ", text_type_text),
                TextNode("code", text_type_code),
                TextNode(" node", text_type_text),
                TextNode("This is a ", text_type_text),
                TextNode("code2", text_type_code),
                TextNode(" node", text_type_text),
            ],
            new_nodes
        )

    def test_multi_distinct_nodes(self):
        node1 = TextNode("This is a `code` node", text_type_text)
        node2 = TextNode("This is a **bold** node", text_type_text)
        node3 = TextNode("This is a basic text node", text_type_text)
        nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(nodes, text_code_delimiter, text_type_code)
        self.assertListEqual(
            [
                TextNode("This is a ", text_type_text),
                TextNode("code", text_type_code),
                TextNode(" node", text_type_text),
                TextNode("This is a **bold** node", text_type_text),
                TextNode("This is a basic text node", text_type_text),
            ],
            new_nodes
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )
    
    def test_missing_closing_delimiter(self):
        node = TextNode("This is a broken `code node", text_type_text)
        nodes = [node]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, text_code_delimiter, text_type_code)

class TestLinkExtraction(unittest.TestCase):
    def test_valid_link(self):
        text = "This is text with a link [click here](https://www.example.com)"
        tuples_extracted = extract_markdown_links(text)
        self.assertListEqual(
            [("click here", "https://www.example.com")],
            tuples_extracted
        )

    def test_valid_links(self):
        text = "This is text with a link [click here](https://www.example.com) and [to youtube](https://www.youtube.com/)"
        tuples_extracted = extract_markdown_links(text)
        self.assertListEqual(
            [("click here", "https://www.example.com"), ("to youtube", "https://www.youtube.com/")],
            tuples_extracted
        )

    def test_no_valid_links1(self):
        text = "This is text with no links"
        tuples_extracted = extract_markdown_links(text)
        self.assertListEqual(
            [],
            tuples_extracted
        )
    
    def test_no_valid_links2(self):
        text = "This is text with no links []"
        tuples_extracted = extract_markdown_links(text)
        self.assertListEqual(
            [],
            tuples_extracted
        )
    
    def test_no_valid_links3(self):
        text = "This is text with no links ()"
        tuples_extracted = extract_markdown_links(text)
        self.assertListEqual(
            [],
            tuples_extracted
        )

    def test_no_text(self):
        text = ""
        tuples_extracted = extract_markdown_links(text)
        self.assertListEqual(
            [],
            tuples_extracted
        )

class TestImgExtraction(unittest.TestCase):
    def test_valid_img(self):
        text = "This is text with a image ![click here](https://www.example.com)"
        tuples_extracted = extract_markdown_images(text)
        self.assertListEqual(
            [("click here", "https://www.example.com")],
            tuples_extracted
        )

    def test_valid_imgs(self):
        text = "This is text with an img ![click here](https://www.example.com) and ![to youtube](https://www.youtube.com/)"
        tuples_extracted = extract_markdown_images(text)
        self.assertListEqual(
            [("click here", "https://www.example.com"), ("to youtube", "https://www.youtube.com/")],
            tuples_extracted
        )

    def test_no_valid_imgs1(self):
        text = "This is text with no imgs"
        tuples_extracted = extract_markdown_images(text)
        self.assertListEqual(
            [],
            tuples_extracted
        )
    
    def test_no_valid_imgs2(self):
        text = "This is text with no imgs []()"
        tuples_extracted = extract_markdown_images(text)
        self.assertListEqual(
            [],
            tuples_extracted
        )
    
    def test_no_valid_imgs3(self):
        text = "This is text with no imgs ()"
        tuples_extracted = extract_markdown_images(text)
        self.assertListEqual(
            [],
            tuples_extracted
        )

    def test_no_text(self):
        text = ""
        tuples_extracted = extract_markdown_images(text)
        self.assertListEqual(
            [],
            tuples_extracted
        )
