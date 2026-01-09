from langchain_core.prompts import ChatPromptTemplate

QUERY_REWRITE_TEMPLATE = (
    "请将以下问题改写为一个适合搜索引擎查询的陈述句。\n"
    "问题: {question}\n"
    "陈述句:"
)

QUERY_REWRITE_PROMPT = ChatPromptTemplate.from_template(QUERY_REWRITE_TEMPLATE)

RELEVANCE_SCORE_TEMPLATE = (
    "你是一个相关性评估专家。请评估以下文档内容与用户查询的相关性。\n"
    "\n"
    "评分标准：\n"
    "- 0.0-0.2 (不相关): 文档内容与查询主题完全无关，或仅仅是关键词偶然匹配但语义不符。\n"
    "- 0.3-0.5 (弱相关): 文档提到了查询中的部分概念，但并未提供直接答案，或信息过于宽泛/边缘化。\n"
    "- 0.6-0.8 (强相关): 文档直接回答了查询的核心问题，或提供了关键的支持性证据，信息有价值。\n"
    "- 0.9-1.0 (完美匹配): 文档准确、完整地包含了查询所需的所有信息，是理想的检索结果。\n"
    "\n"
    "查询: {query}\n"
    "文档: {document}\n"
    "\n"
    "请只输出一个 0.0 到 1.0 之间的浮点数（保留一位或两位小数），严禁输出任何解释或其他文本。"
)

RELEVANCE_SCORE_PROMPT = ChatPromptTemplate.from_template(RELEVANCE_SCORE_TEMPLATE)
