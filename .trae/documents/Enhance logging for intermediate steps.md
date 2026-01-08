I will modify the code to print the intermediate steps, including tool invocations and internal library calls.

### Plan

1.  **Enhance Tool Logs (`src/tools/rag_tool.py`)**:
    *   Add detailed print statements to show the internal process of the RAG tool:
        *   Query Rewriting result.
        *   HTTP Request payload (Input to the "Library").
        *   HTTP Response data (Output from the "Library").

2.  **Visualize Agent Execution (`main.py`)**:
    *   Update the `main` loop to parse the `response['messages']` history.
    *   Iterate through the messages to display the chain of thought:
        *   **Agent Decision**: Show which tool the agent decided to call and with what arguments (from `AIMessage.tool_calls`).
        *   **Tool Output**: Show the result returned by the tool (from `ToolMessage`).

This will provide a clear, step-by-step view of:
`User Input` -> `Agent Decision (Tool Call)` -> `Tool Internal Logs (Library Call)` -> `Tool Output` -> `Agent Final Answer`.
