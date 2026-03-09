import io
import fitz  # PyMuPDF
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentParser:
    CHUNK_SIZE = 2000    # approx characters (~500 tokens)
    CHUNK_OVERLAP = 200  # approx characters (~50 tokens)

    @staticmethod
    def get_splitter():
        return RecursiveCharacterTextSplitter(
            chunk_size=DocumentParser.CHUNK_SIZE,
            chunk_overlap=DocumentParser.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    @staticmethod
    def parse_pdf(file_bytes: bytes, filename: str) -> list[dict]:
        """Parse PDF into chunks with page numbers using PyMuPDF."""
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        chunks = []
        splitter = DocumentParser.get_splitter()
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            if not text.strip():
                continue
                
            page_chunks = splitter.split_text(text)
            for chunk_idx, chunk_text in enumerate(page_chunks):
                chunks.append({
                    "text": chunk_text,
                    "doc_name": filename,
                    "page_number": page_num + 1,
                    "chunk_index": chunk_idx,
                })
        return chunks

    @staticmethod
    def parse_docx(file_bytes: bytes, filename: str) -> list[dict]:
        """Parse DOCX into chunks. DOCX doesn't have reliable page numbers, so we use 1."""
        doc = docx.Document(io.BytesIO(file_bytes))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        
        text = "\n".join(full_text)
        splitter = DocumentParser.get_splitter()
        text_chunks = splitter.split_text(text)
        
        chunks = []
        for chunk_idx, chunk_text in enumerate(text_chunks):
            chunks.append({
                "text": chunk_text,
                "doc_name": filename,
                "page_number": 1,
                "chunk_index": chunk_idx,
            })
        return chunks

    @staticmethod
    def parse_txt(file_bytes: bytes, filename: str) -> list[dict]:
        """Parse plain text into chunks."""
        text = file_bytes.decode("utf-8")
        splitter = DocumentParser.get_splitter()
        text_chunks = splitter.split_text(text)
        
        chunks = []
        for chunk_idx, chunk_text in enumerate(text_chunks):
            chunks.append({
                "text": chunk_text,
                "doc_name": filename,
                "page_number": 1,
                "chunk_index": chunk_idx,
            })
        return chunks

    @classmethod
    def parse(cls, file_bytes: bytes, filename: str) -> list[dict]:
        """
        Route to the correct parser based on file extension.
        Returns list of chunks: {text, doc_name, page_number, chunk_index}
        """
        ext = filename.lower().split('.')[-1]
        if ext == 'pdf':
            return cls.parse_pdf(file_bytes, filename)
        elif ext == 'docx':
            return cls.parse_docx(file_bytes, filename)
        elif ext in ['txt', 'md']:
            return cls.parse_txt(file_bytes, filename)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
