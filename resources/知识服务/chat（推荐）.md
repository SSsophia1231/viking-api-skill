本节将说明如何基于已创建好的一个知识服务进行检索或者问答。
# 概述
/api/knowledge/service/chat 接口支持基于一个已创建的知识服务进行检索/问答
> 使用 service/chat 接口有哪些优势？
> 1、无需串联拼接 search_knowledge 接口和 chat_completions 接口，在控制台前端调试在线参数并发布服务后，即可通过当前接口调用，获得与控制台前端完全一致的效果
> 2、无需生成复杂的 AKSK 签名，通过 API Key 即可调用

# **前提条件**
在您的知识库控制台界面发布知识服务，并关联相应的 API Key（用于权限校验）。
# **请求接口**
| **URI** | /api/knowledge/service/chat |  |
| --- | --- | --- |
| **请求方法** | POST |  |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | 'Authorization': 'Bearer {apikey}' | 该知识服务关联的 API Key，用于鉴权 |
|  | "Host": knowledge_base_domain | 知识库域名 |
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| service_resource_id | string | 是 | -- | **知识服务唯一 id** |
| messages | json | 是 | -- | **检索/问答多轮对话消息** <br> 格式为一问一答形式，发出消息的对话参与者角色，可选值包括： <br>  <br> * user：User Message 用户消息 <br> * assistant：Assistant Message 对话助手消息 <br>  <br> 其中 **最后一个元素 role == user ，content 为当前最新的提问 query** <br> **纯文本对话：** <br> 例如： <br> ```Python <br> [ <br>     {"role": "user", "content": "你好"}, <br>     {"role": "assistant", "content": "你好！有什么我可以帮助你的？"}, <br>     {"role": "user", "content": "当前轮次用户问题"} <br> ] <br> ``` <br>  <br> **图文对话**： <br> 例如： <br> ```JSON <br> [ <br>     { <br>         "role": "user", <br>         "content": [ <br>             { <br>                 "type": "text", <br>                 "text": "推荐一个类似的适合 3 岁小孩的玩具" <br>             }, <br>             { <br>                 "type": "image_url", <br>                 "image_url": { <br>                     "url": "https://ark-project.tos-cn-beijing.volces.XXX.jpeg" #客户上传的图片，支持 URL/base64 编码，协议详见：https://www.volcengine.com/docs/82379/1362931?lang=zh#477e51ce 和 https://www.volcengine.com/docs/82379/1362931?lang=zh#d86010f4 <br>                 } <br>             } <br>         ] <br>     } <br> ] <br> ``` <br>  |
| query_param | json | 否 | nil | **检索过滤条件** <br> 在创建知识服务时如果您已配置了过滤条件，那么和该附加过滤条件一起生效，逻辑为 and <br>  <br> * 支持对 doc 的 meta 信息过滤 <br> * 详细使用方式和支持字段见[filter表达式](https://www.volcengine.com/docs/84313/1419289#filter-%E8%A1%A8%E8%BE%BE%E5%BC%8F)，可支持对 doc_id 做筛选 <br> * 此处用到过滤的字段，需要在 collection/create 时添加到 index_config 的 fields 上 <br>  <br> 例如： <br> 单层 filter： <br> ```JSON <br> doc_filter = { <br>    "op": "must", // 查询算子 must/must_not/range/range_out <br>    "field": "doc_id", <br>    "conds": ["tos_doc_id_123", "tos_doc_id_456"] <br> } <br> query_param = { <br>     "doc_filter": doc_filter <br> } <br> ``` <br>  <br> 多层 filter： <br> ```JSON <br> doc_filter = { <br>   "op": "and",   // 逻辑算子 and/or <br>   "conds": [     // 条件列表，支持嵌套逻辑算子和查询算子 <br>     { <br>       "op": "must", <br>       "field": "type", <br>       "conds": [1] <br>     }, <br>     { <br>         ...         // 支持>=1的任意数量的条件进行组合 <br>     } <br>   ] <br> } <br>  <br> query_param = { <br>     "doc_filter": doc_filter <br> } <br> ``` <br>  |
| stream | bool | 否 | true | **是否采用流式返回** <br> 当创建的知识服务为问答类型服务时生效 |
# **响应消息**
目前知识服务主要分为两类：检索类型和问答类型。针对不同类型的知识服务，返回的消息格式也有所不同。
## 检索类知识服务
如果您请求的是检索类型的知识服务，返回结果如下：
| 字段 | 子字段 | 类型 | 备注 |
| --- | --- | --- | --- |
| code |  | int | 状态码 |
| message |  | string | 返回信息 |
| **data** |  | **json** | **返回数据详情** |
|  | count | int | 检索结果返回的条数 |
|  | rewrite_query | string | query 改写的结果 |
|  | token_usage | json | Token 使用信息 |
| ^^ |  | result_list | list |
|  | id | string | 索引的主键 |
|  | content | string | 切片内容 <br> 1、非结构化文件：content 返回切片内容 <br> 2、faq 文件：content 返回答案 <br> 3、结构化文件：content 返回参与索引的字段和取值，以 K:V 对拼接，使用 \n 区隔 |
|  | md_content | string | markdown 格式的解析结果 <br> 对于非结构化文档中的表格切片，可以额外返回 markdown 格式解析结果，保留更多表格原始信息 <br> 表格切片可以通过 chunk_type == table 判断 |
|  | html_content | string | html 格式的解析结果 <br> 对于非结构化文档中的表格切片，可以额外返回 html 格式解析结果，保留更多表格原始信息 <br> 表格切片可以通过 chunk_type == table 判断 |
|  | table_chunk_fields | `list<object>` | 结构化数据检索返回单行全量数据 |
|  | original_question | string | faq 数据检索召回答案对应的原始问题 |
|  | score | float | 向量化语义检索得分 |
|  | point_id | string | 切片 id |
|  | chunk_title | string | 切片标题 |
|  | chunk_id | int | 切片位次 id <br> 代表在原始文档中的位次顺序 |
|  | process_time | int | 切片处理完成的时刻（Unix 时间戳，秒） |
|  | rerank_score | float | 重排得分 |
|  | doc_info | json | 文档信息 <br> ```JSON <br> { <br>     "doc_id": "_sys_auto_gen_doc_id-134144883689", //文档 id <br>     "doc_name": "2404.08817v2.pdf", //文档名字 <br>     "create_time": 1727333117, //文档的创建时间 <br>     "doc_type": "pdf", //知识所属原始文档的类型 <br>     "doc_meta": "[{\"field_name\":\"doc_id\",\"field_type\":\"string\",\"field_value\":\"_sys_auto_gen_doc_id-13411829101044883689\"}]", //文档相关元信息（此处是一个包含文档 id 信息的列表形式的字符串） <br>     "source": "url", //知识来源类型：tos lark tos_fe <br>     "title": "Revisiting Code Similarity Evaluation with Abstract Syntax Tree Edit Distance", //知识所属文档的标题 <br>     "url": "***" //原始文档的公开下载链接或飞书文档链接 <br> } <br> ``` <br>  |
|  | recall_position | int | 向量化语义检索召回位次 |
|  | rerank_position | int | 重排位次 |
|  | chunk_type | string | 切片所属类型 <br> 部分返回值类型有：doc-image、image、video、table、mixed-table、text、structured、faq 等 |
|  | chunk_attachment | `list<object>` | 检索召回附件（原始图片等）的临时下载链接，chunk_type 为 image、video、table、mixed-table 时且 get_attachment_link 为 true 时有效 |
## 问答类知识服务-非流式
如果您请求的是问答类型的知识服务，并选择非流式回答，返回结果如下：
| 字段 | 子字段 | 类型 | 备注 |
| --- | --- | --- | --- |
| code |  | int | 状态码 |
| message |  | string | 返回信息 |
| **data** |  | **json** | **返回数据详情** |
|  | count | int | 检索结果返回的条数 |
|  | rewrite_query | string | query 改写的结果 |
|  | token_usage | json | Token 使用信息 |
|  | result_list | list | 检索返回的信息 |
|  | generated_answer | string | LLM 模型生成的回答 |
|  | reasoning_content | string | 推理模型生成的内容 |
## 问答类知识服务-流式
如果您请求的是问答类型的知识服务，并选择流式回答，检索的结果将会放在首个流中返回，token_usage 会放在尾流中返回，中间流按照 SSE 格式返回生成的结果（可参考[ chat_completions 接口](https://www.volcengine.com/docs/84313/1350013)）。
| 字段 |  | 类型 | 备注 |
| --- | --- | --- | --- |
| code |  | int | 状态码 |
| message |  | string | 返回信息 |
| **data** |  | **json** | **返回数据详情** |
|  | count | int | 检索结果返回的条数 **首流返回** |
|  | rewrite_query | string | query 改写的结果 **首流返回** |
|  | result_list | list | 检索返回的信息 **首流返回** |
|  | generated_answer | string | LLM 模型生成的回答 **中间流返回** |
|  | reasoning_content | string | 推理模型生成的内容 **中间流返回** |
|  | token_usage | json | Token 使用信息 **尾流返回** |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_api_key' \
  http://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/service/chat \
  -d '{
    "service_resource_id": "your_service_resource_id",
    "stream": false,
    "messages": [
        {
            "role": "user",
            "content": "注册抖音的方式有哪些"
        }
    ]
}'
```

## 响应消息
执行成功返回：
```Shell
{
    "code": 0,
    "data": {
        "count": 2,
        "token_usage": {
            "embedding_token_usage": {
                "prompt_tokens": 23,
                "completion_tokens": 0,
                "total_tokens": 23
            },
            "rerank_token_usage": 62,
            "llm_token_usage": {
                "prompt_tokens": 510,
                "completion_tokens": 52,
                "total_tokens": 562,
                "prompt_tokens_details": {
                    "cached_tokens": 0
                },
                "completion_tokens_details": {
                    "reasoning_tokens": 0
                }
            }
        },
        "result_list": [
            {
                "id": "_sys_auto_gen_doc_id-8423876736290680802-0",
                "content": "问题:注册抖音的方式有哪些\n答案:有手机号、邮箱等方式",
                "score": 0.6423748731613159,
                "point_id": "_sys_auto_gen_doc_id-8423876736290680802-0",
                "chunk_id": 0,
                "process_time": 1745475503,
                "rerank_score": 0.929823701560032,
                "doc_info": {
                    "doc_id": "_sys_auto_gen_doc_id-8423876736290680802",
                    "doc_name": "未命名表格.xlsx",
                    "create_time": 1745475499,
                    "doc_type": "xlsx",
                    "doc_meta":"[{\"field_name\":\"所属行业\",\"field_type\":\"list\<string\>\",\"field_value\":[\"医疗\"]},{\"field_name\":\"优先级\",\"field_type\":\"float32\",\"field_value\":\"10\"}]",
                    "source": "tos_fe",
                    "url": ""
                },
                "recall_position": 1,
                "rerank_position": 1,
                "chunk_type": "structured",
                "chunk_source": "document",
                "update_time": 1745475503,
                "table_chunk_fields": [
                    {
                        "field_name": "问题",
                        "field_value": "注册抖音的方式有哪些"
                    },
                    {
                        "field_name": "答案",
                        "field_value": "有手机号、邮箱等方式"
                    }
                ],
                "FromRecallQueue": "master_recall"
            },
            {
                "id": "_sys_auto_gen_doc_id-8423876736290680802-1",
                "content": "问题:注册微信有另外的方式吗\n答案:另外可以通过QQ注册微信",
                "score": 0.5205988883972168,
                "point_id": "_sys_auto_gen_doc_id-8423876736290680802-1",
                "chunk_id": 1,
                "process_time": 1745475503,
                "rerank_score": 0.3796083432458134,
                "doc_info": {
                    "doc_id": "_sys_auto_gen_doc_id-8423876736290680802",
                    "doc_name": "未命名表格.xlsx",
                    "create_time": 1745475499,
                    "doc_type": "xlsx",
                    "doc_meta":"[{\"field_name\":\"所属行业\",\"field_type\":\"list\<string\>\",\"field_value\":[\"医疗\"]},{\"field_name\":\"优先级\",\"field_type\":\"float32\",\"field_value\":\"10\"}]",
                    "source": "tos_fe"
                },
                "recall_position": 2,
                "rerank_position": 2,
                "chunk_type": "structured",
                "chunk_source": "document",
                "update_time": 1745475503,
                "table_chunk_fields": [
                    {
                        "field_name": "问题",
                        "field_value": "注册微信有另外的方式吗"
                    },
                    {
                        "field_name": "答案",
                        "field_value": "另外可以通过QQ注册微信"
                    }
                ],
                "FromRecallQueue": "master_recall"
            }
        ],
        "generated_answer": "您好，注册抖音有手机号、邮箱等方式<reference data-ref=\"_sys_auto_gen_doc_id-8423876736290680802-0\" data-img-ref=\"false\"></reference>。"
    }
    "message": "success",
    "request_id": "02174581251018800000000000000000000ffff0a007412e51bff"
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
{
    "code": 1000003,
    "message": "invalid request:messages role nil",
    "request_id": "02174581256280800000000000000000000ffff0a007412632e7a"
}
```


