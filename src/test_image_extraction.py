import unittest

from extract_markdown_images import extract_markdown_images

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

if __name__ == "__main__":
    unittest.main()
