# liteaifrm
Lite framework for Responses Api

## Configuration

The utilities expect an OpenAI API key to be available. Set the
`OPENAI_API_KEY` environment variable or specify `openai_api_key` in your
configuration file before running the agents.

### Memories

Vector indexes are stored in the `memories/` folder. Default paths in
`config/agent_profile.yml` point to `memories/rag_faiss.index` and
`memories/rag_faiss_meta.pkl`. The folder is ignored by git and will be
created automatically if missing.

### Retriever settings

Global retriever options are defined under the top level `retriever` section.
Each agent inside `agent_settings` may override these by providing its own
`retriever` subsection. Example:

```yaml
retriever:
  enabled: true
  top_k: 3
  faiss_index_path: memories/rag_faiss.index
  faiss_meta_path: memories/rag_faiss_meta.pkl

agent_settings:
  summarizer:
    prompt_path: "prompts/summarizer.txt"
    retriever:
      enabled: true
      top_k: 5
```

When `retriever.enabled` is true for an agent, the FAISS index will be loaded
and used to provide additional context during generation.


### Orchestration modes

Set `orchestra_mode` to `true` in `config/agent_profile.yml` and choose one of
five orchestration types via `orchestration_type`:
`sequential`, `planner`, `tree`, `router` or `reflective`.
The selected mode determines how agents are executed.

* **sequential** – run agents from `agent_sequence` one after another.
* **planner** – a `planner_agent` returns the list of agents to run.
* **tree** – spawn agents according to `agent_tree` starting from its `root` key.
* **router** – choose agents based on the `router_map` section and fields of the input.
* **reflective** – after each agent a `reflection_agent` may request a retry.

Switching the value in the YAML file allows quick experimentation with different
execution strategies.
