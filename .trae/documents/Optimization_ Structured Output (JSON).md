I will modify the Agent's System Prompt to output a structured JSON list where `content` corresponds to the **original retrieved text** (verbatim).

### Plan

1.  **Update Agent System Prompt**:
    *   **Goal**: Instruct the LLM to return a JSON list of retrieved items, preserving the original text in the `content` field.
    *   **Action**: Modify `src/core/prompts/agent_prompts.py`.
    *   **New Instructions**:
        *   "Output a JSON list only. Do not summarize."
        *   "Each item must contain: `content` (the verbatim retrieved text), `confidence_score`, `source`, `retrieval_method`."
        *   Explicitly warn the model **not to rewrite or summarize** the `content` field, but to copy it from the tool output.

2.  **Verify Output**:
    *   Run `main.py` with a query.
    *   Check that the output is a JSON list and the `content` field matches the mock data or web search snippets exactly.
