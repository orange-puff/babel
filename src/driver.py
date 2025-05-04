from pdf_reader import PDFReader


if __name__ == "__main__":
    pdf_reader = PDFReader("books/art-of-controversy.pdf")
    print(pdf_reader.get_page_text(pdf_reader.num_pages - 5))
