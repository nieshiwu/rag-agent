# Agentic RAG System (智能 RAG 检索助手)

这是一个基于 LangGraph 和 LangChain 构建的智能 Agent 系统，旨在演示如何通过 Agent 决策来实现企业级 RAG（检索增强生成）与联网搜索的混合检索。

该系统能够理解用户的自然语言问题，自动判断应该查询内部知识库（模拟）还是搜索互联网（DuckDuckGo），并返回结构化的数据结果。

## 🌟 核心特性

*   **智能路由**：自动判断用户意图，选择合适的工具（Knowledge Base 或 Internet Search）。
*   **混合检索**：支持关键词检索、语义检索和混合检索模式（由 LLM 自动决策）。
*   **业务感知**：内置业务规则，自动将问题映射到正确的知识库（Finance, Tech, HR, General）。
*   **结构化输出**：直接返回 JSON 格式的原始数据，包含置信度、来源、检索方式等元数据，便于下游系统集成。
*   **Mock 知识库**：内置一个模拟的向量数据库 API，用于演示 RAG 流程，无需复杂的本地向量库部署。
*   **Langfuse 监控**：集成了 Langfuse Tracing，可实时监控 Agent 的思考过程和 Latency。

## 🛠️ 技术栈

*   **框架**: LangGraph, LangChain
*   **LLM**: 兼容 OpenAI 接口的模型 (默认配置为 Qwen-Max)
*   **搜索**: DuckDuckGo (优先简体中文)
*   **监控**: Langfuse (OpenTelemetry based)
*   **语言**: Python 3.10+

## 🚀 快速开始

### 1. 环境准备

确保你已经安装了 Python 3.10 或更高版本。

```bash
# 克隆项目（如果适用）
# git clone ...

# 安装依赖
pip install -r requirements.txt
```

*(注意：如果 `requirements.txt` 不存在，请手动安装以下核心包)*
```bash
pip install langgraph langchain-openai langchain-community duckduckgo-search python-dotenv uvicorn fastapi langfuse langfuse-langchain
```

### 2. 配置环境变量

在项目根目录创建一个 `.env` 文件，并填入以下配置：

```ini
# LLM 配置 (示例使用阿里云 DashScope)
OPENAI_API_KEY=sk-your-api-key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-max

# Langfuse 监控配置 (可选，如不需要可忽略或注释代码)
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 3. 运行系统

直接运行 `main.py` 启动交互式终端：

```bash
python main.py
```

系统会自动启动后台的 Mock 知识库服务，并初始化 Agent。

## 💬 使用示例

在终端中输入问题，Agent 会自动处理：

**场景 1：查询内部知识库 (HR)**
```text
User: 公司的年假有多少天？

🤖 [Agent Decision] Tool: knowledge_base_search (library='hr')
...
Result: [
  {
    "content": "服务满1年以上的员工享有15天年假。",
    "confidence_score": 0.95,
    "source": "knowledge_base (hr)",
    "retrieval_method": "hybrid"
  }
]
```

**场景 2：查询内部知识库 (Tech)**
```text
User: 错误码 500 是什么意思？

🤖 [Agent Decision] Tool: knowledge_base_search (library='tech', method='keyword')
...
Result: [
  {
    "content": "错误码500通常表示内部服务器错误，请检查日志。",
    "confidence_score": 0.99,
    "source": "knowledge_base (tech)",
    "retrieval_method": "keyword"
  }
]
```

**场景 3：联网搜索 (Fallback)**
```text
User: 帮我查一下北京今天的天气

🤖 [Agent Decision] Tool: internet_search
...
Result: [
  {
    "content": "Summary: 北京今日天气晴朗，气温 5~15度...",
    "confidence_score": "N/A",
    "source": "internet (duckduckgo)",
    "retrieval_method": "from web"
  }
]
```

## 📂 项目结构

```
rag_agent/
├── main.py                 # 入口文件，负责启动 Mock Server 和 Agent Loop
├── .env                    # 配置文件
├── src/
│   ├── api/
│   │   └── mock_server.py  # 模拟的知识库 API (FastAPI)
│   ├── core/
│   │   ├── agent.py        # Agent 定义与 Graph 构建
│   │   ├── callbacks.py    # 自定义控制台日志回调
│   │   └── prompts/        # 所有 Prompt 模板
│   │       ├── agent_prompts.py
│   │       └── tool_prompts.py
│   └── tools/
│       ├── rag_tool.py     # 知识库检索工具
│       └── search_tool.py  # 联网搜索工具 (DuckDuckGo)
```

## 📝 许可证

MIT License
