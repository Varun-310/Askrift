"""
Document parser service.
Converts PDF, DOCX, and TXT files into text chunks with page metadata.
"""


class DocumentParser:
    CHUNK_SIZE = 500    # tokens per chunk
    CHUNK_OVERLAP = 50  # token overlap between chunks

    @staticmethod
    def parse_pdf(file_bytes: bytes) -> list[dict]:
        """Parse PDF into chunks with page numbers using PyMuPDF."""
        # TODO: Phase 3 implementation
        pass

    @staticmethod
    def parse_docx(file_bytes: bytes) -> list[dict]:
        """Parse DOCX into chunks with page numbers using python-docx."""
        # TODO: Phase 3 implementation
        pass

    @staticmethod
    def parse_txt(file_bytes: bytes) -> list[dict]:
        """Parse plain text into chunks."""
        # TODO: Phase 3 implementation
        pass

    @classmethod
    def parse(cls, file_bytes: bytes, filename: str) -> list[dict]:
        """
        Route to the correct parser based on file extension.
        Returns list of chunks: {text, doc_name, page_number, chunk_index}
        """
        # TODO: Phase 3 implementation
        pass
