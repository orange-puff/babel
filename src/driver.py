from pdf_reader import PDFReader
from semantic_search import SemanticSearch

if __name__ == "__main__":
    pdf_reader = PDFReader("books/art-of-controversy.pdf")
    semantic_search = SemanticSearch()
    semantic_search.add_pages(pdf_reader.get_all_pages_text())
    for idx, page, score in semantic_search.search(
        "The act of making a decision means you can no longer proceed with many other paths."
    ):
        print(f"{idx}: {score}")
        print(page)
        print("-" * 100)
