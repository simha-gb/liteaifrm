import importlib


def run_reflective(config):
    """Run agents sequentially with a reflection step after each agent.

    The reflection agent can request a single retry by returning a dictionary
    with ``redo`` set to True and an optional ``input`` field to replace the
    previous result.
    """
    agent_sequence = config.get("agent_sequence", [])
    reflection_agent = config.get("reflection_agent", "reviewer")
    input_data = config.get("input", None)

    result = input_data
    reflection_mod = importlib.import_module(f"agents.{reflection_agent}")
    reflection_cfg = dict(config)
    reflection_cfg.update(config.get("agent_settings", {}).get(reflection_agent, {}))
    if "prompt_path" not in reflection_cfg:
        reflection_cfg["prompt_path"] = f"prompts/{reflection_agent}.txt"

    for agent_name in agent_sequence:
        agent_mod = importlib.import_module(f"agents.{agent_name}")
        agent_config = dict(config)
        agent_config.update(config.get("agent_settings", {}).get(agent_name, {}))
        if "prompt_path" not in agent_config:
            agent_config["prompt_path"] = f"prompts/{agent_name}.txt"
        result = agent_mod.run(result, agent_config)

        # Reflection step
        feedback = reflection_mod.run(result, reflection_cfg)
        if isinstance(feedback, dict) and feedback.get("redo"):
            new_input = feedback.get("input", result)
            result = agent_mod.run(new_input, agent_config)
    return result
