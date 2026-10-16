import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore

def get_qdrant_vector_store(collection_name: str = "study_materials"):
    # Kết nối tới Qdrant đang chạy qua Docker (với port 6333 REST)
    client = qdrant_client.QdrantClient(host="localhost", port=6333)
    
    # Khởi tạo Vector Store của LlamaIndex
    vector_store = QdrantVectorStore(
        client=client, 
        collection_name=collection_name
    )
    return vector_store