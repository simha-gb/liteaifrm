# MIT License
#
# Copyright (c) 2025 simha-gb
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from utils.openai_client import get_client

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

    # История для Responses API (можно усложнить, если надо)
    local_history = [
        {"role": "system", "content": [{"type": "input_text", "text": instructions}]},
        {"role": "user", "content": [{"type": "input_text", "text": message}]}
    ]

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
