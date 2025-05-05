import unittest
from unittest.mock import Mock, patch
from src.pdf_reader import PDFReader


class TestPDFReader(unittest.TestCase):
    @patch("src.pdf_reader.PdfReader")
    def setUp(self, mock_pdf_reader):
        # Mock the PDF reader
        self.mock_reader = mock_pdf_reader.return_value
        self.mock_reader.pages = [Mock(), Mock()]  # Mock two pages
        self.mock_reader.pages[0].extract_text.return_value = "Page 1 content"
        self.mock_reader.pages[1].extract_text.return_value = "Page 2 content"

        # Create a test PDF path
        self.test_pdf_path = "test.pdf"
        # Patch os.path.exists to return True for our test file
        with patch("os.path.exists", return_value=True):
            self.pdf_reader = PDFReader(self.test_pdf_path)

    def test_initialization(self):
        """Test that PDFReader initializes correctly"""
        self.assertEqual(self.pdf_reader.file_path, self.test_pdf_path)
        self.assertEqual(self.pdf_reader.num_pages, 2)

    def test_invalid_file_path(self):
        """Test that PDFReader raises error for non-existent file"""
        with self.assertRaises(FileNotFoundError):
            PDFReader("nonexistent.pdf")

    def test_invalid_file_extension(self):
        """Test that PDFReader raises error for non-PDF file"""
        with patch("os.path.exists", return_value=True):
            with self.assertRaises(ValueError):
                PDFReader("test.txt")

    def test_get_page_text(self):
        """Test getting text from a specific page"""
        self.assertEqual(self.pdf_reader.get_page_text(0), "Page 1 content")
        self.assertEqual(self.pdf_reader.get_page_text(1), "Page 2 content")

    def test_get_page_text_invalid_page(self):
        """Test that getting an invalid page raises error"""
        with self.assertRaises(ValueError):
            self.pdf_reader.get_page_text(2)

    def test_get_all_pages_text(self):
        """Test getting text from all pages"""
        expected = ["Page 1 content", "Page 2 content"]
        self.assertEqual(self.pdf_reader.get_all_pages_text(), expected)


if __name__ == "__main__":
    unittest.main()
