# 知识库对接接口需求文档

本文档描述了 RAG Agent 与外部知识库服务交互的 API 接口规范。当前系统使用 Mock Server 进行模拟，后续对接真实知识库时，需遵循此规范。

## 1. 接口概述

*   **用途**: 根据用户查询检索相关的知识片段。
*   **通信协议**: HTTP/HTTPS
*   **请求方法**: POST
*   **建议路径**: `/search` (可配置)
*   **Content-Type**: `application/json`

## 2. 请求格式 (Request)

Agent 将以 `application/json` 格式发送检索请求。

### 参数说明

| 字段名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `query` | string | 是 | - | 用户的原始查询或重写后的查询字符串。 | "2024年第一季度财报" |
| `library_name` | string | 是 | - | 目标知识库的标识符。 | "finance", "tech", "hr", "general" |
| `search_method` | string | 否 | `hybrid` | 建议的检索策略。可选值：`keyword`, `semantic`, `hybrid`。 | "keyword" |
| `top_k` | int | 否 | `3` | 期望返回的最大结果数量。 | 5 |

### 请求示例

```json
{
  "query": "错误码 500 代表什么？",
  "library_name": "tech",
  "search_method": "keyword",
  "top_k": 3
}
```

## 3. 响应格式 (Response)

知识库服务应返回 JSON 格式的数据，其中核心数据位于 `results` 数组中。

### 字段说明

**响应根对象：**

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `query` | string | 回显请求中的查询词。 |
| `results` | Array | 检索到的知识片段列表，按置信度降序排列。如果无结果，返回空数组 `[]`。 |
| `message` | string | (可选) 状态消息或调试信息。 |

**Result 对象 (`results` 数组元素)：**

| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `content` | string | 是 | 检索到的文本内容片段。 |
| `confidence_score` | float | 是 | 相关性评分 (0.0 - 1.0)。 |
| `source_type` | string | 是 | 来源类型标识，通常为 "knowledge_base"。 |
| `library` | string | 是 | 来源库标识，用于回显。 |
| `metadata` | object | 否 | 扩展元数据信息（详见下表）。 |

**Metadata 对象 (位于 `results[].metadata`)：**

| 字段名 | 类型 | 说明 | 缺失处理 |
| :--- | :--- | :--- | :--- |
| `filename` | string | 来源文件名称。 | 建议返回 "N/A" |
| `page` | int/string | 所在页码或位置。 | 建议返回 "N/A" |
| `keywords` | list/string | 关联关键词。 | 建议返回 "N/A" |

### 响应示例

```json
{
  "query": "错误码 500 代表什么？",
  "results": [
    {
      "content": "错误码 500 通常表示内部服务器错误，建议检查应用日志。",
      "confidence_score": 0.98,
      "source_type": "knowledge_base",
      "library": "tech",
      "metadata": {
        "filename": "Error_Codes_Manual.pdf",
        "page": 88,
        "keywords": ["error 500", "troubleshooting"]
      }
    },
    {
      "content": "遇到 500 错误时，请尝试重启服务。",
      "confidence_score": 0.75,
      "source_type": "knowledge_base",
      "library": "tech",
      "metadata": {
        "filename": "Service_Restart_Guide.docx",
        "page": 12,
        "keywords": ["restart", "service"]
      }
    }
  ]
}
```

## 4. 错误处理

*   **200 OK**: 请求成功。
*   **400 Bad Request**: 请求参数缺失或格式错误。
*   **500 Internal Server Error**: 知识库内部服务异常。
