import json
import requests
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.core.prompts.tool_prompts import QUERY_REWRITE_PROMPT

# 定义输入参数的 Schema
class RAGToolInput(BaseModel):
    query: str = Field(description="用户的原始问题或查询字符串。")
    library_name: str = Field(description="要搜索的具体知识库名称（例如：'finance'财务, 'tech'技术, 'general'通用, 'hr'人事）。")
    search_method: str = Field(description="使用的搜索方式，如 'keyword'关键词, 'semantic'语义, 或 'hybrid'混合。", default="hybrid")

class KnowledgeBaseTool(BaseTool):
    name: str = "knowledge_base_search"
    description: str = "使用此工具搜索内部知识库（财务、技术、通用、人事）。必须指定知识库名称和搜索方式。"
    args_schema: Type[BaseModel] = RAGToolInput
    
    api_url: str = "http://localhost:8000/search" # Default mock URL
    llm: Optional[ChatOpenAI] = None

    def __init__(self, api_url: str = "http://localhost:8000/search", llm: Optional[ChatOpenAI] = None):
        super().__init__()
        self.api_url = api_url
        self.llm = llm or ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    def _rewrite_query(self, query: str) -> str:
        """
        Converts a question into a declarative statement for better retrieval.
        """
        try:
            chain = QUERY_REWRITE_PROMPT | self.llm | StrOutputParser()
            return chain.invoke({"question": query})
        except Exception as e:
            # Fallback if LLM fails or is not configured
            return query

    def _run(self, query: str, library_name: str, search_method: str = "hybrid") -> str:
        """Use the tool."""
        print(f"\n  [RAG Internal] 1. Rewriting Query...")
        # 1. Rewrite Query
        rewritten_query = self._rewrite_query(query)
        print(f"  [RAG Internal]    Original: '{query}' -> Rewritten: '{rewritten_query}'")

        # 2. Call HTTP Interface
        payload = {
            "library_name": library_name,
            "search_method": search_method,
            "query": rewritten_query
        }
        print(f"  [RAG Internal] 2. Calling Knowledge Base API...")
        print(f"  [RAG Internal]    URL: {self.api_url}  Payload: {json.dumps(payload, ensure_ascii=False)}")

        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            print(f"  [RAG Internal] 3. API Response Received")
            print(f"  [RAG Internal]    Status: {response.status_code}")
            
            # Format output with clear confidence scores
            results = data.get("results", [])
            formatted_output = []
            
            if not results:
                return "No results found in knowledge base."
                
            for item in results:
                if isinstance(item, str):
                    # Handle legacy/fallback string format
                    content = item
                    score = 0.5 # Default fallback score
                    source_type = "knowledge_base"
                    library = library_name
                else:
                    # Handle new dict format
                    content = item.get("content", "")
                    score = item.get("confidence_score", 0.0)
                    source_type = item.get("source_type", "knowledge_base")
                    library = item.get("library", library_name)
                
                formatted_output.append({
                    "content": content,
                    "metadata": {
                        "confidence_score": score,
                        "source": f"{source_type} ({library})"
                    }
                })
            
            resp_str = json.dumps(formatted_output, ensure_ascii=False, indent=2)
            display_str = resp_str[:200] + "..." if len(resp_str) > 200 else resp_str
            # print(f"  [RAG Internal]    Data: {display_str}\n")
            
            return resp_str
        except Exception as e:
            error_msg = f"Error connecting to knowledge base: {str(e)}"
            print(f"  [RAG Internal] Error: {error_msg}")
            return error_msg

    async def _arun(self, query: str, library_name: str, search_method: str = "hybrid") -> str:
        """Use the tool asynchronously."""
        # For simplicity, calling sync implementation here, but in production should be async
        return self._run(query, library_name, search_method)
