from llama_index.readers.file import PyMuPDFReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from app.services.vector_store import get_qdrant_vector_store
import os
from dotenv import load_dotenv

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

Settings.embed_model = GeminiEmbedding(model_name="models/gemini-embedding-001", api_key=gemini_key)

def parse_and_chunk(file_path: str, filename: str):
    loader = PyMuPDFReader()
    documents = loader.load_data(file_path=file_path)
    
    # Giữ lại metadata số trang cho tính năng click vào trích dẫn
    for doc in documents:
        doc.metadata["filename"] = filename
        doc.metadata["page_number"] = doc.metadata.get("source", 1)
        
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    return splitter.get_nodes_from_documents(documents)

def process_document_pipeline(file_path: str, doc_id: str, filename: str):
    print(f"[{doc_id}] Trạng thái: Parsing... Đang cắt tài liệu.")
    nodes = parse_and_chunk(file_path, filename)
    
    # Bổ sung document_id vào từng vector để sau này dễ dàng lọc (Filter)
    for node in nodes:
        node.metadata["document_id"] = doc_id

    print(f"[{doc_id}] Trạng thái: Indexing... Đang đẩy vào Qdrant.")
    vector_store = get_qdrant_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Upsert vector lên DB
    index = VectorStoreIndex(nodes=nodes, storage_context=storage_context)
    
    print(f"[{doc_id}] Trạng thái: Ready! Xử lý hoàn tất.")
    # Bước tiếp theo: Chỗ này sẽ gọi hàm Update DB (Postgres) sang trạng thái Ready