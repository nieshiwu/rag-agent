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
        print(f"   Input: {input_str}")

    def on_tool_end(self, output: Any, **kwargs: Any) -> None:
        """Run when tool ends running."""
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
