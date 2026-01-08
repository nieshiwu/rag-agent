from langchain_core.prompts import ChatPromptTemplate

QUERY_REWRITE_TEMPLATE = (
    "请将以下问题改写为一个适合搜索引擎查询的陈述句。\n"
    "问题: {question}\n"
    "陈述句:"
)

QUERY_REWRITE_PROMPT = ChatPromptTemplate.from_template(QUERY_REWRITE_TEMPLATE)
