from typing import List
from pypdf import PdfReader
import os.path


class PDFReader:
    def __init__(self, pdf_path: str):
        """Initialize the PDF reader with a path to a PDF file.

        Args:
            pdf_path (str): Path to the PDF file

        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a PDF
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if not pdf_path.lower().endswith(".pdf"):
            raise ValueError(f"File must be a PDF: {pdf_path}")

        self._pdf_path = pdf_path
        self._reader = PdfReader(pdf_path)
        self._num_pages = len(self._reader.pages)

    @property
    def num_pages(self) -> int:
        """Get the total number of pages in the PDF.

        Returns:
            int: Number of pages
        """
        return self._num_pages

    @property
    def file_path(self) -> str:
        """Get the path to the PDF file.

        Returns:
            str: Path to the PDF file
        """
        return self._pdf_path

    def get_page_text(self, page_num: int) -> str:
        """Get the text content of a specific page.

        Args:
            page_num (int): Page number (0-based index)

        Returns:
            str: Text content of the page

        Raises:
            ValueError: If page number is invalid
        """
        if not 0 <= page_num < self._num_pages:
            raise ValueError(
                f"Invalid page number: {page_num}. Must be between 0 and {self._num_pages - 1}"
            )

        return self._reader.pages[page_num].extract_text()

    def get_all_pages_text(self) -> List[str]:
        """Get text content from all pages in the PDF.

        Returns:
            Dict[int, str]: Dictionary mapping page numbers (1-based) to their text content
        """
        return [self.get_page_text(i) for i in range(self._num_pages)]
