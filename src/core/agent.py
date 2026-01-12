from langchain.agents import create_agent
from src.llm.model import get_llm
from src.tools.rag_tool import KnowledgeBaseTool
from src.tools.search_tool import get_search_tool
from src.core.prompts.agent_prompts import AGENT_SYSTEM_PROMPT

def create_rag_agent():
    # 1. Initialize LLM
    llm = get_llm(0.9)

    # 2. Define Tools
    rag_tool = KnowledgeBaseTool(llm=llm) 
    search_tool = get_search_tool()
    
    tools = [rag_tool, search_tool]

    # 3. Create Agent (LangGraph)
    # This creates a prebuilt ReAct-style agent (using tool calling)
    # It returns a CompiledGraph
    agent = create_agent(model=llm, tools=tools, system_prompt=AGENT_SYSTEM_PROMPT)
    
    return agent
