import importlib

def run_tree(config):
    tree = config.get("agent_tree")
    input_data = config.get("input", None)
    # Допустим, tree описан так:
    # {
    #   "root": ["summarizer", "researcher"],
    #   "summarizer": [],
    #   "researcher": ["coder"],
    #   "coder": ["runner"],
    #   "runner": []
    # }
    results = {}

    def run_node(agent_name, inp):
        agent_mod = importlib.import_module(f"agents.{agent_name}")
        agent_config = dict(config)
        agent_config.update(config.get("agent_settings", {}).get(agent_name, {}))
        result = agent_mod.run(inp, agent_config)
        results[agent_name] = result
        for child in tree.get(agent_name, []):
            run_node(child, result)
    # Запускаем с "root" — можешь поменять под свой вариант
    for agent in tree["root"]:
        run_node(agent, input_data)
    return results  # dict всех результатов
