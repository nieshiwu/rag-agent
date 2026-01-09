import json
from typing import Any, Dict, List, Optional
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult

class AgentCallbackHandler(BaseCallbackHandler):
    """Callback handler for printing agent execution steps in real-time."""

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        # print("\n🤔 [Agent Thinking] ...")
        pass

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Run when tool starts running."""
        tool_name = serialized.get("name") if serialized else "Unknown Tool"
        print(f"\n🤖 [Agent Decision]")
        print(f"   Tool: {tool_name}")
        
        # Optimize display: show default top_k if not present for knowledge_base_search
        if tool_name == "knowledge_base_search":
            try:
                # Handle cases where input_str is a JSON string
                if input_str.strip().startswith("{"):
                    inputs = json.loads(input_str)
                    # if "top_k" not in inputs:
                    #     inputs["top_k"] = "3 (default)"
                    print(f"   Input: {inputs}")
                else:
                    print(f"   Input: {input_str}")
            except:
                print(f"   Input: {input_str}")
        else:
            print(f"   Input: {input_str}")

    def on_tool_end(self, output: Any, **kwargs: Any) -> None:
        """Run when tool ends running."""
        # Check if we should suppress logging for specific tools or if LangChain is triggering multiple events
        # For now, let's keep it simple. If we see duplication, it might be because the tool itself prints AND the callback prints.
        # But we already removed prints from tools.
        
        # The issue might be that 'output' is sometimes the full ToolMessage object and sometimes the string content,
        # and LangGraph might be emitting events for both the tool execution and the node update.
        
        # However, looking at the user log:
        # One output is raw text: "Result: 今天..."
        # One output is JSON: "Result: [ { "content": ... } ]"
        
        # This suggests that maybe the AgentCallbackHandler is printing the raw output,
        # AND the tool itself was printing something before we cleaned it up?
        # OR, maybe LangChain's default verbose=True is on?
        
        print(f"\n🛠️  [Tool Output]")
        
        # Extract string content from output
        content_str = ""
        if isinstance(output, str):
            content_str = output
        elif hasattr(output, 'content'):
            content_str = str(output.content)
        else:
            content_str = str(output)
            
        # Truncate output if too long
        display_content = content_str[:300] + "..." if len(content_str) > 300 else content_str
        print(f"   Result: {display_content}")

    def on_agent_action(self, action: Any, **kwargs: Any) -> Any:
        """Run on agent action."""
        pass
        
    def on_chain_error(self, error: BaseException, **kwargs: Any) -> Any:
        """Run when chain errors."""
        print(f"\n❌ [Error] {str(error)}")
