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
        else:
            raise ValueError(f"Unknown orchestration_type: {typ}")
    else:
        # Одиночный агент
        agent_name = config.get("single", config["agent_sequence"][0])
        agent_mod = importlib.import_module(f"agents.{agent_name}")
        input_data = config.get("input", None)        return agent_mod.run(input_data, config)