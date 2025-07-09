from utils.config_loader import load_config
from orchestration.controller import run

config = load_config("config/agent_profile.yml")
result = run(config)
print("Результат пайплайна:", result)