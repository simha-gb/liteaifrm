import json
import pickle
import numpy as np
import faiss
from utils.openai_client import get_client


def run(input_data, config):
    # Сначала — всё, что нужно дальше!
    single_settings = config.get("single_settings", {})
    model = single_settings.get("model") or config.get("model", "gpt-4o-mini")
    temperature = single_settings.get("temperature") or config.get("temperature", 0.3)

    # Инструкции — из файла или из конфига:
    prompt_path = single_settings.get("prompt_path") or config.get("prompt_path")
    if prompt_path:
        with open(prompt_path, "r", encoding="utf-8") as f:
            instructions = f.read()
    else:
        instructions = single_settings.get("instructions") or config.get(
            "instructions",
            "Отвечай на вопрос пользователя используя предоставленный контекст.")

    tools = single_settings.get("tools") or config.get("tools", [])

    # --- RAG config ---
    retriever_cfg = config.get("retriever", {})
    if retriever_cfg.get("enabled", False):
        vector_db = retriever_cfg.get("vector_db", "chromadb")
        chunk_size = retriever_cfg.get("chunk_size", 500)
        top_k = retriever_cfg.get("top_k", 3)
        index_path = retriever_cfg.get("faiss_index_path", "memory/rag_faiss.index")
        meta_path = retriever_cfg.get("faiss_meta_path", "memory/rag_faiss_meta.pkl")

        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            meta = pickle.load(f)

        def get_embedding(text: str):
            openai = get_client(config)
            resp = openai.embeddings.create(
                model="text-embedding-3-small",
                input=text  # исправлено!
            )
            return np.array(resp.data[0].embedding, dtype=np.float32)

        def search_faiss(query: str, top_k=top_k):
            emb = get_embedding(query)
            emb = emb.reshape(1, -1)
            D, I = index.search(emb, top_k)
            results = [meta[i] for i in I[0]]
            return results
    else:
        search_faiss = None

    # --- Instructions, tools ---
    instructions = config.get("instructions", "Отвечай на вопрос пользователя используя предоставленный контекст.")
    tools = config.get("tools", [])

    # --- Input and history ---
    message = input_data if isinstance(input_data, str) else (input_data.get("message", "") if input_data else "")
    history = config.get("history", [])

    # --- Get context (RAG) ---
    context_text = ""
    if retriever_cfg.get("enabled", False) and search_faiss:
        context_chunks = search_faiss(message, top_k=top_k)
        context_text = "\n".join([chunk["content"] for chunk in context_chunks])
    else:
        context_text = config.get("context", "")

    local_history = history.copy() if history else []
    if context_text:
        local_history.append({
            "role": "system",
            "content": [{"type": "input_text", "text": f"Контекст для ответа:\n{context_text}"}]
        })
    local_history.append({
        "role": "user",
        "content": [{"type": "input_text", "text": message}]
    })

    # --- OpenAI Responses API ---
    openai = get_client(config)
    response = openai.responses.create(
        model=model,
        instructions=instructions,
        input=local_history,
        tools=tools,
        temperature=temperature
    )

    output = {
        "output_text": getattr(response, "output_text", None) or getattr(response, "text", ""),
        "history": local_history + [
            {"role": "assistant", "content": [{"type": "output_text", "text": getattr(response, "output_text", "")}]}
        ]
    }    return output
