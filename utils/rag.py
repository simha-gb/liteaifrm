import pickle
import numpy as np
import faiss
from utils.openai_client import get_client


def load_faiss(cfg):
    """Load FAISS index and metadata according to retriever config."""
    index_path = cfg.get("faiss_index_path", "memories/rag_faiss.index")
    meta_path = cfg.get("faiss_meta_path", "memories/rag_faiss_meta.pkl")
    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        meta = pickle.load(f)
    return index, meta


def search(query, retriever_cfg, config):
    """Search FAISS index using OpenAI embeddings."""
    index, meta = retriever_cfg.get("_loaded", (None, None))
    if index is None or meta is None:
        index, meta = load_faiss(retriever_cfg)
        retriever_cfg["_loaded"] = (index, meta)

    openai = get_client(config)
    resp = openai.embeddings.create(
        model="text-embedding-3-small",
        input=query,
    )
    emb = np.array(resp.data[0].embedding, dtype=np.float32).reshape(1, -1)

    top_k = retriever_cfg.get("top_k", 3)
    _, I = index.search(emb, top_k)
    return [meta[i] for i in I[0]]
