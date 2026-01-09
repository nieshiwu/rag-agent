from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class SearchRequest(BaseModel):
    library_name: str
    search_method: str = "hybrid"
    query: str
    top_k: int = 3

@app.post("/search")
async def search_knowledge_base(request: SearchRequest):
    print(f"Received search request: {request}")
    
    # Simulate database results
    mock_data = {
        "finance": [
            {"content": "第三季度收入同比增长15%。", "metadata": {"filename": "Q3_Financial_Report.pdf", "page": 12, "keywords": ["revenue", "growth"]}},
            {"content": "2024财年的预算已获董事会批准。", "metadata": {"filename": "FY24_Budget_Approval.docx", "page": 1, "keywords": ["budget", "board"]}},
            {"content": "由于市场波动，股票表现保持稳定。", "metadata": {"filename": "Market_Analysis_2023.pdf", "page": 45, "keywords": ["stock", "market"]}},
            {"content": "第四季度的财务审计将于下周开始。", "metadata": {"filename": "Audit_Schedule_Q4.xlsx", "page": "Sheet1", "keywords": ["audit", "schedule"]}}
        ],
        "tech": [
            {"content": "API服务器目前运行时间为99.9%。", "metadata": {"filename": "Server_Health_Dashboard.html", "page": "N/A", "keywords": ["uptime", "api"]}},
            {"content": "新的人工智能模型'Alpha-X'正在部署中。", "metadata": {"filename": "AI_Deployment_Plan_v2.pdf", "page": 3, "keywords": ["AI", "deployment"]}},
            {"content": "由于维护，数据库将在周日停机。", "metadata": {"filename": "Maintenance_Notice_DB.txt", "page": 1, "keywords": ["database", "downtime"]}},
            {"content": "前端团队已将React版本升级至18.0。", "metadata": {"filename": "Frontend_Changelog.md", "page": 102, "keywords": ["react", "upgrade"]}},
            {"content": "错误码500通常表示内部服务器错误，请检查日志。", "metadata": {"filename": "Error_Codes_Manual.pdf", "page": 88, "keywords": ["error 500", "troubleshooting"]}}
        ],
        "general": [
            {"content": "公司野餐定于下周五举行。", "metadata": {"filename": "Company_Events_Calendar.ics", "page": "N/A", "keywords": ["picnic", "event"]}},
            {"content": "关于远程办公的新HR政策将于下月生效。", "metadata": {"filename": "Remote_Work_Policy_Update.pdf", "page": 2, "keywords": ["remote work", "policy"]}}
        ],
        "hr": [
            {"content": "服务满1年以上的员工享有15天年假。", "metadata": {"filename": "Employee_Handbook_2024.pdf", "page": 25, "keywords": ["leave", "vacation"]}},
            {"content": "病假超过3天需提供医生证明。", "metadata": {"filename": "Sick_Leave_Policy.docx", "page": 4, "keywords": ["sick leave", "medical certificate"]}},
            {"content": "绩效考核每半年进行一次，分别在6月和12月。", "metadata": {"filename": "Performance_Review_Guidelines.pdf", "page": 7, "keywords": ["performance", "review"]}}
        ]
    }
    
    results = mock_data.get(request.library_name.lower())
    
    if not results:
        # Default fallback if library not found
        return {"results": [], "message": f"No data found for library '{request.library_name}'"}
    
    # Simple filtering simulation
    # Handle both string (legacy) and dict items
    filtered_results = []
    for r in results:
        text = r if isinstance(r, str) else r.get("content", "")
        if any(word.lower() in text.lower() for word in request.query.split()):
            filtered_results.append(r)
    
    # If no keyword match, return all (mocking semantic search returning something relevant)
    raw_results = filtered_results if filtered_results else results
    
    # Calculate confidence scores and add metadata
    enriched_results = []
    query_words = set(request.query.lower().split())
    
    for item in raw_results:
        # Extract content string
        content = item if isinstance(item, str) else item.get("content", "")
        item_metadata = {} if isinstance(item, str) else item.get("metadata", {})
        
        # Simulate confidence score based on keyword overlap
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
            "library": request.library_name,
            "metadata": item_metadata
        })
    
    # Sort by confidence score descending
    enriched_results.sort(key=lambda x: x["confidence_score"], reverse=True)
    
    # Apply top_k limit
    final_results = enriched_results[:request.top_k]
    
    return {
        "query": request.query,
        "results": final_results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
