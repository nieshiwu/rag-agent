import json
import requests
import re
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.core.prompts.tool_prompts import QUERY_REWRITE_PROMPT, RELEVANCE_SCORE_PROMPT

# 定义输入参数的 Schema
class RAGToolInput(BaseModel):
    query: str = Field(description="用户的原始问题或查询字符串。")
    library_name: str = Field(description="要搜索的具体知识库名称（例如：'kb_flfg'金融法律法规 ,'kb_jr_book'金融书籍包括金融制度、金融理论等，或'kb_rmyh'人民银行相关）。")
    search_method: str = Field(description="使用的搜索方式，如'vector'向量, 或 'vector-graph'向量+图。", default="vector-graph")
    top_k: int = Field(description="期望返回的结果数量（默认为3，调研类问题建议5-10，事实类问题建议1）。", default=3)

class KnowledgeBaseTool(BaseTool):
    name: str = "knowledge_base_search"
    description: str = "使用此工具搜索内部知识库（财务、金融条例）。必须指定知识库名称和搜索方式。"
    args_schema: Type[BaseModel] = RAGToolInput
    
    api_url: str = "http://192.168.0.197:28011/kb/search" 
    # api_url: str = "http://localhost:6666/search"
    llm: Optional[ChatOpenAI] = None

    def __init__(self, api_url: str = api_url, llm: Optional[ChatOpenAI] = None):
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

    def _calculate_relevance(self, query: str, content: str) -> float:
        """
        Uses LLM to calculate relevance score between query and content.
        """
        try:
            chain = RELEVANCE_SCORE_PROMPT | self.llm | StrOutputParser()
            score_str = chain.invoke({"query": query, "document": content})
            # Clean up string to ensure it's a float
            match = re.search(r"(\d+(\.\d+)?)", score_str)
            if match:
                score = float(match.group(1))
                return min(1.0, max(0.0, score))
            return 0.5 # Fallback
        except Exception:
            return 0.5

    def _run(self, query: str, library_name: str, search_method: str = "hybrid", top_k: int = 3) -> str:
        """Use the tool."""
        try:
            # 1. Query Rewriting (Optional, for better recall)
            # In a real system, you might use an LLM to rewrite "it" to "annual leave policy"
            # Here we just use the raw query or simple rule-based modification
            
            payload = {
                "library_name": library_name,
                "search_method": search_method,
                "query": query,
                "top_k": top_k
            }
            
            response = requests.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            # print(data) # Reduce console noise
            
            # Format output with clear confidence scores
            # Handle both "data" (new API) and "results" (old/mock API) keys
            results = data.get("data") or data.get("results") or []
            
            # Ensure results is a list. If API returns a single dict object, wrap it in a list.
            if isinstance(results, dict):
                results = [results]
            elif not isinstance(results, list):
                # Fallback for unexpected types (e.g. None or str), though .get([], []) handles None -> []
                results = []

            if not results:
                return "No results found in knowledge base."
            
            formatted_output = []
            
            for item in results:
                # Basic type check
                if isinstance(item, str):
                    content = item
                    raw_metadata = {}
                    score_source = "llm_eval"
                    score = self._calculate_relevance(query, content)
                else:
                    content = item.get("content", "")
                    raw_metadata = item.get("metadata", {})

                    # Extract Confidence Score (Priority: Metadata > LLM Eval)
                    if "confidence_score" in raw_metadata:
                        score = raw_metadata["confidence_score"]
                        score_source = "knowledge_base"
                    else:
                        score = self._calculate_relevance(query, content)
                        score_source = "llm_eval"
                
                # Extract Source Type & Library (Priority: Metadata > Defaults)
                source_type = raw_metadata.get("source_type", "knowledge_base")
                library = raw_metadata.get("library", library_name)
                
                # Format Score Display
                if score_source == "llm_eval":
                    final_score_display = f"{score} (AI Eval)"
                else:
                    final_score_display = score
                
                # Construct Final Metadata
                final_metadata = {
                    "confidence_score": final_score_display,
                    "source": f"{source_type} ({library})",
                    "filename": raw_metadata.get("filename", "N/A"),
                    "page": raw_metadata.get("page", "N/A"),
                    "keywords": raw_metadata.get("keywords", "N/A")
                }
                
                formatted_output.append({
                    "content": content,
                    "metadata": final_metadata
                })
            
            resp_str = json.dumps(formatted_output, ensure_ascii=False, indent=2)
            
            return resp_str
        except Exception as e:
            error_msg = f"Error connecting to knowledge base: {str(e)}"
            return error_msg

    async def _arun(self, query: str, library_name: str, search_method: str = "hybrid", top_k: int = 3) -> str:
        """Use the tool asynchronously."""
        # For simplicity, calling sync implementation here, but in production should be async
        return self._run(query, library_name, search_method, top_k)
