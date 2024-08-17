import unittest

from src.block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # makrdown string must be fully left aligned here for the test to pass
        # this is so the string trimming in the function can be tested
        markdown = """
# This is a heading



                #### this has too much whitespace


This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
        """
        self.assertListEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading",
                "#### this has too much whitespace",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# This is a heading"), "heading")
        self.assertEqual(block_to_block_type("## This is a heading"), "heading")
        self.assertEqual(block_to_block_type("###### This is a heading"), "heading")

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nThis is ## a code block\n```"), "code-block")

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote block"), "quote-block")
        self.assertEqual(block_to_block_type("> This is a quote block\n>another quote\n>yet another quote"), "quote-block")
    
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* This is a list item"), "unordered-list")
        self.assertEqual(block_to_block_type("* This is a list item\n* This is another list item"), "unordered-list")
        self.assertEqual(block_to_block_type("* This is a list item\n- This is a dash list item"), "unordered-list")

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. This is a list item"), "ordered-list")
        self.assertEqual(block_to_block_type("1. This is a list item\n2. This is another list item"), "ordered-list")

    def test_not_ordered_list(self):
        self.assertEqual(block_to_block_type("1. This is a list item\n* This is another list item"), "paragraph")
        self.assertEqual(block_to_block_type("1. This is a list item\n3. This is another list item"), "paragraph")

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), "paragraph")
        self.assertEqual(block_to_block_type("This is a paragraph\n```unclosed code block"), "paragraph")
        self.assertEqual(block_to_block_type("> This would be a quote block\nif not for the missing '>' on this line"), "paragraph")
        self.assertEqual(block_to_block_type("- This is a paragraph\nsince there isn't a * or - on this line"), "paragraph")
        self.assertEqual(block_to_block_type("* This is a paragraph\n```unclosed code block"), "paragraph")

    def test_markdown_to_html_node(self):
        markdown = """
# This is a heading

## This is another heading h2 this time

### This is a heading h3

####### This is a paragraph since too many hashes 

# this counts as a heading
## since there is no empty line between the hashes and the text

```
    This is a code block
```

> This is a quote block
> This is another line in the quote block

* This is an unordered list item
- This is another unordered list item

1. This is an ordered list item
2. This is another ordered list item
4. This is a list item with the wrong number and should be treated as a paragraph

1. This is an ordered list item
2. This is another ordered list item

This is a paragraph

This is a paragraph with **bold** and *italic* text

"""

        self.assertListEqual(
            str(markdown_to_html_node(markdown)).split(),
            ['HTMLNode(div,', 'None,', 'children:', '[HTMLNode(h1,', 'None,', 'children:', '[HTMLNode(None,', 'This', 'is', 'a', 'heading,', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(h2,', 'None,', 'children:', '[HTMLNode(None,', 'This', 'is', 'another', 'heading', 'h2', 'this', 'time,', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(h3,', 'None,', 'children:', '[HTMLNode(None,', 'This', 'is', 'a', 'heading', 'h3,', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(p,', 'None,', 'children:', '[HTMLNode(None,', '#######', 'This', 'is', 'a', 'paragraph', 'since', 'too', 'many', 'hashes,', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(h1,', 'None,', 'children:', '[HTMLNode(None,', 'this', 'counts', 'as', 'a', 'heading', '##', 'since', 'there', 'is', 'no', 'empty', 'line', 'between', 'the', 'hashes', 'and', 'the', 'text,', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(pre,', 'None,', 'children:', '[HTMLNode(code,', 'This', 'is', 'a', 'code', 'block', ',', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(blockquote,', 'None,', 'children:', '[HTMLNode(None,', 'This', 'is', 'a', 'quote', 'block', 'This', 'is', 'another', 'line', 'in', 'the', 'quote', 'block,', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(ul,', 'None,', 'children:', '[HTMLNode(li,', 'None,', 'children:', '[HTMLNode(None,', 'This', 'is', 'an', 'unordered', 'list', 'item,', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(li,', 'None,', 'children:', '[HTMLNode(None,', 'This', 'is', 'another', 'unordered', 'list', 'item,', 'children:', 'None,', 'None)],', 'None)],', 'None),', 'HTMLNode(p,', 'None,', 'children:', '[HTMLNode(None,', '1.', 'This', 'is', 'an', 'ordered', 'list', 'item', '2.', 'This', 'is', 'another', 'ordered', 'list', 'item', '4.', 'This', 'is', 'a', 'list', 'item', 'with', 'the', 'wrong', 'number', 'and', 'should', 'be', 'treated', 'as', 'a', 'paragraph,', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(ol,', 'None,', 'children:', '[HTMLNode(li,', 'None,', 'children:', '[HTMLNode(None,', 'This', 'is', 'an', 'ordered', 'list', 'item,', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(li,', 'None,', 'children:', '[HTMLNode(None,', 'This', 'is', 'another', 'ordered', 'list', 'item,', 'children:', 'None,', 'None)],', 'None)],', 'None),', 'HTMLNode(p,', 'None,', 'children:', '[HTMLNode(None,', 'This', 'is', 'a', 'paragraph,', 'children:', 'None,', 'None)],', 'None),', 'HTMLNode(p,', 'None,', 'children:', '[HTMLNode(None,', 'This', 'is', 'a', 'paragraph', 'with', ',', 'children:', 'None,', 'None),', 'HTMLNode(b,', 'bold,', 'children:', 'None,', 'None),', 'HTMLNode(None,', 'and', ',', 'children:', 'None,', 'None),', 'HTMLNode(i,', 'italic,', 'children:', 'None,', 'None),', 'HTMLNode(None,', 'text,', 'children:', 'None,', 'None)],', 'None)],', 'None)']
        )

if __name__ == "__main__":
    unittest.main()

