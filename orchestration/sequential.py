import importlib

def run_sequence(config):
    agent_sequence = config.get("agent_sequence", [])
    input_data = config.get("input", None)
    result = input_data
    for agent_name in agent_sequence:        agent_mod = importlib.import_module(f"agents.{agent_name}")  # ← сначала импорт
        agent_config = dict(config)
        agent_config.update(config.get("agent_settings", {}).get(agent_name, {}))
        if "prompt_path" not in agent_config:
            agent_config["prompt_path"] = f"prompts/{agent_name}.txt"
        result = agent_mod.run(result, agent_config)  # ← потом вызов
    return result
