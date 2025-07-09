import gradio as gr
from utils.config_loader import load_config
from orchestration.controller import run

# Загружаем конфиг 1 раз при старте
config = load_config("config/agent_profile.yml")

def chat_gradio(message, history):
    config_for_call = dict(config)
    config_for_call["input"] = message
    result = run(config_for_call)

    # Ищем разумный вывод — лучше всего stdout из code_result, потом summary
    if isinstance(result, dict):
        if "code_result" in result and isinstance(result["code_result"], dict):
            out = result["code_result"].get("stdout", "").strip()
            if out:
                return out
        if "summary" in result:
            return result["summary"]
        if "research" in result:
            return result["research"]
        if "code" in result:
            return result["code"]
        if "output_text" in result:
            return result["output_text"]
        # иначе — просто показываем всё содержимое как текст
        return str(result)
    return str(result)


if __name__ == "__main__":
    gr.ChatInterface(fn=chat_gradio).launch()

    # Дополнительно: простой REPL в консоли (опционально)
    while True:
        message = input("Ты: ")
        if message.lower() in {"выход", "exit", "quit"}:
            break
        bot_reply = chat_gradio(message, history=[])
        print("Бот:", bot_reply)

