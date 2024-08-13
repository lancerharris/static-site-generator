import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_bold_delimiter,
    text_italic_delimiter,
    text_code_delimiter,
    text_node_to_html_node,
    split_nodes_delimiter
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bolded text node", text_type_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bolded text node")

    def test_italic(self):
        node = TextNode("This is an italicized text node", text_type_italic)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italicized text node")

    def test_code(self):
        node = TextNode("print('Hello, world!')", text_type_code)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello, world!')")
        

    def test_link(self):
        node = TextNode("Google", text_type_link, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
    
    def test_image(self):
        node = TextNode("An image", text_type_image, "https://www.test.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.test.com/image.png", "alt": "An image"}
        )

    def test_invalid_text_type(self):
        node = TextNode("An unknown node", "unknown")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_no_text_type(self):
        node = TextNode("A missing text_type node", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

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

if __name__ == "__main__":
    unittest.main()
