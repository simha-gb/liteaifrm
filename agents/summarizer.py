from utils.openai_client import get_client
from utils.rag import search

def run(input_data, config):
    openai = get_client(config)

    # Инструкция — из prompt_path или из config["instructions"]
    instructions = config.get("instructions", "Summarize the following text.")
    prompt_path = config.get("prompt_path")
    if prompt_path:
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                instructions = f.read()
        except Exception as e:
            print(f"Не удалось прочитать промт {prompt_path}: {e}")

    # Извлекаем message из input_data (строка или dict)
    if isinstance(input_data, str):
        message = input_data
    elif isinstance(input_data, dict):
        message = input_data.get("message", "") or str(input_data)
    else:
        message = str(input_data)

    # Поддержка кастомных параметров модели/температуры/tools
    model = config.get("model", "gpt-4o")
    temperature = config.get("temperature", 0.3)
    tools = config.get("tools", [])

    # Фикс для tools: приводим к Responses API формату (dict, а не str)
    def fix_tool(tool):
        if isinstance(tool, str):
            return {"type": tool}
        return tool
    if tools and isinstance(tools[0], str):
        tools = [fix_tool(t) for t in tools]

    # --- RAG context ---
    retriever_cfg = config.get("retriever", {})
    context_text = ""
    if retriever_cfg.get("enabled"):
        chunks = search(message, retriever_cfg, config)
        context_text = "\n".join([c["content"] for c in chunks])

    # История для Responses API (можно усложнить, если надо)
    local_history = [{"role": "system", "content": [{"type": "input_text", "text": instructions}]}]
    if context_text:
        local_history.append({"role": "system", "content": [{"type": "input_text", "text": f"Контекст:\n{context_text}"}]})
    local_history.append({"role": "user", "content": [{"type": "input_text", "text": message}]})

    # Запрос к Responses API
    response = openai.responses.create(
        model=model,
        instructions=instructions,  # Responses API это допускает, но можно убрать если system prompt
        input=local_history,
        tools=tools,
        temperature=temperature,
    )

    summary = getattr(response, "output_text", None) or getattr(response, "text", "")
    print("[summarizer] summary:", summary)
    return {"summary": summary}
