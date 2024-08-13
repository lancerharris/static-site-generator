import unittest

from extract_markdown_links import extract_markdown_links

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

if __name__ == "__main__":
    unittest.main()
