from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class SearchRequest(BaseModel):
    library_name: str
    search_method: str
    query: str

@app.post("/search")
async def search_knowledge_base(request: SearchRequest):
    print(f"Received search request: {request}")
    
    # Simulate database results
    mock_data = {
        "finance": [
            "第三季度收入同比增长15%。",
            "2024财年的预算已获董事会批准。",
            "由于市场波动，股票表现保持稳定。",
            "第四季度的财务审计将于下周开始。"
        ],
        "tech": [
            "API服务器目前运行时间为99.9%。",
            "新的人工智能模型'Alpha-X'正在部署中。",
            "由于维护，数据库将在周日停机。",
            "前端团队已将React版本升级至18.0。",
            "错误码500通常表示内部服务器错误，请检查日志。"
        ],
        "general": [
            "公司野餐定于下周五举行。",
            "关于远程办公的新HR政策将于下月生效。"
        ],
        "hr": [
            "服务满1年以上的员工享有15天年假。",
            "病假超过3天需提供医生证明。",
            "绩效考核每半年进行一次，分别在6月和12月。"
        ]
    }
    
    results = mock_data.get(request.library_name.lower())
    
    if not results:
        # Default fallback if library not found
        return {"results": [], "message": f"No data found for library '{request.library_name}'"}
    
    # Simple filtering simulation
    filtered_results = [r for r in results if any(word.lower() in r.lower() for word in request.query.split())]
    
    # If no keyword match, return all (mocking semantic search returning something relevant)
    # Ensure final_results is a list of strings first
    raw_results = filtered_results if filtered_results else results
    
    # Calculate confidence scores and add metadata
    enriched_results = []
    query_words = set(request.query.lower().split())
    
    for content in raw_results:
        # Simulate confidence score based on keyword overlap
        # content is a string here
        content_words = set(content.lower().split())
        if not query_words:
            score = 0.5 # Default score if query is empty
        else:
            overlap = len(query_words.intersection(content_words))
            # Basic normalization: overlap / len(query)
            # Add base score of 0.6 to simulate vector search baseline
            score = min(0.99, 0.6 + (overlap / len(query_words)) * 0.4)
            
        enriched_results.append({
            "content": content,
            "confidence_score": round(score, 2),
            "source_type": "knowledge_base",
            "library": request.library_name
        })
    
    return {
        "query": request.query,
        "results": enriched_results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
