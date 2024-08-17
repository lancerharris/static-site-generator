import unittest
from src.page_generation import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Heading"
        self.assertEqual(extract_title(markdown), "Heading")

    def test_extract_title_no_heading(self):
        markdown = "No heading"
        self.assertIsNone(extract_title(markdown))
    
    def test_extract_title_whitespace(self):
        markdown = "#        Heading with whitespace "
        self.assertEqual(extract_title(markdown), "Heading with whitespace")

    def test_extract_title_empty_string(self):
        markdown = ""
        self.assertIsNone(extract_title(markdown))

    def test_extract_title_no_space_after_hash(self):
        markdown = "#Heading"
        self.assertIsNone(extract_title(markdown))

    def test_extract_title_multi_headings(self):
        markdown = "# First heading\n# Second heading"
        self.assertEqual(extract_title(markdown), "First heading")

    def test_extract_title_not_first_line(self):
        markdown = "Some text\n# Heading"
        self.assertEqual(extract_title(markdown), "Heading")

    def test_extract_title_newline_after_hash(self):
        markdown = "#\nHeading"
        self.assertEqual(extract_title(markdown), "Heading")

if __name__ == '__main__':
    unittest.main()

