I will implement **Query Expansion (Query Rewriting)** to improve knowledge base retrieval quality.

### Plan

1.  **Analyze Current Limitation**:
    *   Currently, if a user asks "leave rules" but the KB contains "Annual leave entitlement", a simple keyword search might miss it or rank it low.
    *   The Agent passes the raw query directly to the tool (or with minimal changes).

2.  **Implement Query Expansion**:
    *   **Goal**: Before calling the search tool, generate 2-3 variations of the query to cover synonyms and related terms.
    *   **Action**: Modify `src/tools/rag_tool.py`.
        *   Instead of directly sending `query` to the mock server, I will first use the LLM (via a small internal chain) to generate expanded queries.
        *   Example: "leave rules" -> ["leave policy", "vacation days", "time off regulations"].
    *   **Mock Server Update**: Update `src/api/mock_server.py` to handle multiple queries or simply search for each expanded term and aggregate results (deduplicating them).
    *   **Decision**: For simplicity and stability in this demo, I will implement **Query Rewriting** inside the `KnowledgeBaseTool._run` method (or creating a helper function). It will rewrite the user's natural language question into a more precise "search engine friendly" query before sending it to the API.

3.  **Refine Mock Search Logic**:
    *   **Action**: Update `src/api/mock_server.py` to perform a "fuzzy match" on keywords if exact match fails, simulating a better vector search.

4.  **Verification**:
    *   Query: "vacation" (KB has "annual leave").
    *   Expectation: The rewritten query should include "annual leave", successfully finding the record.
