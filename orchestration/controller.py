import importlib


def run(config):
    if config.get("orchestra_mode"):
        typ = config.get("orchestration_type", "sequential")
        if typ == "sequential":
            from .sequential import run_sequence
            return run_sequence(config)
        elif typ == "planner":
            from .planner import run_planner
            return run_planner(config)
        elif typ == "tree":
            from .tree import run_tree
            return run_tree(config)
        elif typ == "router":
            from .router import run_router
            return run_router(config)
        elif typ == "reflective":
            from .reflective import run_reflective
            return run_reflective(config)
        else:
            raise ValueError(f"Unknown orchestration_type: {typ}")
    else:
        # Single agent mode
        agent_name = config.get("single", config["agent_sequence"][0])
        agent_mod = importlib.import_module(f"agents.{agent_name}")
        input_data = config.get("input", None)
        return agent_mod.run(input_data, config)
