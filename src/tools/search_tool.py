import json
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper # Import Wrapper
from langchain_core.tools import Tool

def ddg_search(query: str) -> str:
    """
    Perform a search using DuckDuckGo and return structured results.
    """
    try:
        # Configure DDG to search in Simplified Chinese (region="cn-zh")
        wrapper = DuckDuckGoSearchAPIWrapper(region="cn-zh", max_results=3)
        search = DuckDuckGoSearchRun(api_wrapper=wrapper)
        
        print(f"  [DDG Search] Searching for: {query}")
        # DDG returns a string summary directly
        result_text = search.invoke(query)
        
        # Wrap in our standard JSON format
        formatted_results = [{
            "content": f"Summary: {result_text}",
            "metadata": {
                "confidence_score": "N/A (Web Search)",
                "source": "internet (duckduckgo)",
                "link": "N/A"
            }
        }]
        
        return json.dumps(formatted_results, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps([{"error": str(e)}])

def get_search_tool():
    # Return a custom Tool that uses the ddg_search function
    return Tool(
        name="internet_search",
        description="用于在互联网上搜索公开信息（使用 DuckDuckGo）。当用户询问中国相关内容、天气、新闻或明确提到搜索时使用。",
        func=ddg_search
    )

