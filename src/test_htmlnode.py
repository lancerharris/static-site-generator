import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_to_html_no_props(self):
        node = HTMLNode(
            "div",
            "No Modifications!",
        )
        self.assertEqual(
            node.props_to_html(),
            ""
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_to_html_no_children(self):
        leaf_node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            leaf_node.to_html(),
            "<p>Hello, world!</p>",
        )

    def test_to_html_no_children_no_tag(self):
        leaf_node = LeafNode(None, "I'm text!")
        self.assertEqual(
            leaf_node.to_html(),
            "I'm text!",
        )

    def test_no_children_leaf(self):
        leaf_node = LeafNode("p", "I'm alone!")
        self.assertEqual(
            leaf_node.children,
            None,
        )

    def test_parent_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "Hello, world!")])

    def test_parent_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

    def test_parent_children_not_htmlnode(self):
        parent_node = ParentNode("div", [LeafNode("p", "Hello, world!"), "I'm not a node"])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_no_children_to_html(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_nested_parents_to_html(self):
        parent = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("p", "Hello, world!"),
                        LeafNode("p", "Goodbye, world!"),
                    ],
                ),
                LeafNode("p", "I'm a leaf"),
            ],
        )
        self.assertEqual(
            parent.to_html(),
            "<div><div><p>Hello, world!</p><p>Goodbye, world!</p></div><p>I'm a leaf</p></div>",
        )

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "I'm a child!")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>I'm a child!</span></div>",
        )

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "I'm a grandchild!")
        child_node = ParentNode("p", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p><b>I'm a grandchild!</b></p></div>",
        )
    
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

   
    

if __name__ == "__main__":
    unittest.main()
