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