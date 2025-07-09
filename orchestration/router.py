import importlib


def run_router(config):
    """Route input to one or more agents based on ``router_map``.

    ``router_map`` is a mapping from route keys to agent names or lists of
    agents. The key is resolved from ``input_data['task']`` or
    ``input_data['route']``.
    """
    router_map = config.get("router_map", {})
    default_route = config.get("default_route", [])
    input_data = config.get("input", None)
    if isinstance(input_data, dict):
        route_key = input_data.get("task") or input_data.get("route")
    else:
        route_key = None

    agent_names = router_map.get(route_key, default_route)
    if isinstance(agent_names, str):
        agent_names = [agent_names]

    result = input_data
    for agent_name in agent_names:
        agent_mod = importlib.import_module(f"agents.{agent_name}")
        agent_config = dict(config)
        agent_config.update(config.get("agent_settings", {}).get(agent_name, {}))
        if "prompt_path" not in agent_config:
            agent_config["prompt_path"] = f"prompts/{agent_name}.txt"
        result = agent_mod.run(result, agent_config)
    return result
