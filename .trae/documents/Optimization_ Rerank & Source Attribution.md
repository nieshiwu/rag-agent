I will simulate the Knowledge Base returning a confidence score, as requested. The "confidence score" will be part of the metadata returned by the Knowledge Base API itself.

### Plan

1.  **Update Mock Knowledge Base (Server-Side)**:
    *   **Goal**: Simulate a real vector database or search engine that returns a similarity/confidence score along with the content.
    *   **Action**: Modify `src/api/mock_server.py`.
        *   For each result item, calculate/assign a `confidence_score` (0.0 - 1.0).
        *   Since this is a mock, I will simulate the score based on keyword overlap matches to make it look realistic (more matching words = higher score).
        *   Return this score in the JSON response.

2.  **Update RAG Tool (Client-Side)**:
    *   **Goal**: Pass this server-provided score through to the Agent.
    *   **Action**: Modify `src/tools/rag_tool.py`.
        *   Ensure the tool preserves the `confidence_score` field from the API response.
        *   Add a `source: "knowledge_base"` tag to clearly distinguish it from web search.

3.  **Update Search Tool (Client-Side)**:
    *   **Goal**: For consistency, web search results (which usually don't have a score) should be marked clearly or given a placeholder score.
    *   **Action**: Modify `src/tools/search_tool.py`.
        *   Since Baidu doesn't give a confidence score, we will either omit it or calculate a simple local proxy (like keyword match ratio) just so the data format is consistent, but label it clearly as "estimated_score".
        *   Add `source: "internet"` tag.

4.  **Update Agent Prompt**:
    *   **Goal**: Instruct the Agent to report these scores.
    *   **Action**: Update `src/core/prompts/agent_prompts.py` to ask the Agent to mention the `confidence_score` provided by the knowledge base when citing information.
