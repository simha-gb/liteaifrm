import importlib

def run_planner(config):
    # Первый агент — planner, он возвращает план (например, список задач/агентов)
    planner_name = config.get("planner_agent", "planner")
    planner_mod = importlib.import_module(f"agents.{planner_name}")
    plan = planner_mod.run(config.get("input", None), config)
    # plan — например, ["summarizer", "researcher", "coder"]
    result = config.get("input", None)
    for agent_name in plan:
        agent_mod = importlib.import_module(f"agents.{agent_name}")
        agent_config = dict(config)
        agent_config.update(config.get("agent_settings", {}).get(agent_name, {}))
        result = agent_mod.run(result, agent_config)
    return result

