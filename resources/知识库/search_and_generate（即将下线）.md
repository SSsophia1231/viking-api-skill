**注意**：该接口预计下线，不再更新支持新功能。建议用户选择 search_knowledge + chat_completion 串联使用，新增功能和模型会优先适配这两个接口。

---


由于大模型底层架构升级，知识库同步兼容适配，search_and_generate API 用法和影响如下：
1、若原本使用公共接入点调用 Doubao 模型，无影响
2、若原本使用私有接入点调用 Doubao 模型，需要额外上传 API key 参数，否则会自动调度到**公共 EP 上（此时计费项和折扣会走知识库商品）**

本节将说明如何基于一个已创建的知识库做在线检索，并使用大语言模型整合生成回答。
* 知识库创建完成、文档导入且处理完成后，即代表可以进行在线检索了
* 调用接口前请先完成“对接指南”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取

# 概述
/api/knowledge/collection/search_and_generate 接口用于对知识库进行检索，并将检索到的文本片和用户问题组装到 prompt 当中，调用大语言模型生成问题的回答。
# **前提条件**

* 知识库创建完成。
* 文档导入且处理完成。
* 完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现知识库的检索查询并调用大模型整合生成回答的功能。

# **请求接口**
| **URI** | /api/knowledge/collection/search_and_generate | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **子参数** | **类型** | **必选** | **默认值** | **备注** |
| --- | --- | --- | --- | --- | --- |
| name | -- | string | 否 | -- | **知识库名称** <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空 <br> * 长度要求：[1, 64] |
| project | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 name 和 project 作为知识库的唯一标识 |
| query | -- | string | 是 | -- | **检索文本**，最大可输入长度为 8000： <br>  <br> * query 长度 > 8000 时，接口报错 <br> * 所选 embedding 模型输入最大长度 < query 长度 < 8000 时，query 按所选模型自动截断 <br> * query 长度 < 所选 embedding 模型输入最大长度时，正常检索返回。 |
| stream | -- | bool | 否 | false | **响应内容是否流式返回** <br>  <br> * false：模型生成完所有内容后一次性返回结果 <br> * true：按 SSE 协议逐块返回模型生成内容，最后一个信息流显示 usage 及 "end" : true 参数 |
| **query_param** |  | json | 否 | -- | **检索的过滤和返回设置** |
|  | doc_filter | map | 否 | -- | **检索过滤条件**，支持对 doc 的 meta 信息过滤 <br>  <br> * 使用方式和支持字段见 [filter 表达式说明](https://www.volcengine.com/docs/84313/1419289#filter-%E8%A1%A8%E8%BE%BE%E5%BC%8F)，可支持对 doc_id 做筛选 <br> * 此处用过过滤的字段，需要在 collection/create 时添加到 index_config 的fields 上 <br>  <br> 例如： <br> ```Plain <br> doc_filter = { <br>     "op": "must", <br>     "field": "doc_id", <br>     "conds": ["tos_doc_id_123", "tos_doc_id_456"] <br> } <br> query_param = { <br>     "doc_filter": doc_filter <br> } <br> ``` <br>  |
| **retrieve_param** |  | map | 否 |  | **检索召回参数配置** |
|  | rerank_switch | bool | 否 | false | **自动对结果做 rerank** <br> 说明：打开后，会自动请求 rerank 模型排序 |
|  | retrieve_count | int | 否 | 25 | **进入重排的切片数量**，默认为 25 <br> 只有在 rerank_switch 为 true 时生效。retrieve_count 需要大于等于 limit，否则会抛出错误 |
|  | limit | int | 否 | 10 | **最终返回的文本片数量**，取值范围 [1, 200] |
|  | dense_weight | float | 否 | 0.5 | **混合检索中稠密向量的权重** <br> 1 表示纯稠密检索 ，0 表示纯字面检索，范围 [0.2, 1] <br> 只有在请求的知识库使用的是混合检索时有效，即索引算法为 hnsw_hybrid |
|  | chunk_diffusion_count | int | 否 | 0 | **检索阶段返回命中文本片上下几片文本片。**默认为 0，表示不进行 chunk diffusion。范围 [0, 5] |
|  | rerank_model | string | 否 | "m3-v2-rerank" | **rerank 模型选择** <br> 仅在 "rerank_switch" == true 的时候生效 <br> 可选模型： <br>  <br> * "m3-v2-rerank"：轻量小模型，具有强大的多语言能力，推理速度快 |
|  | rerank_only_chunk | bool | 否 | false | **是否仅根据 chunk 内容计算重排分数** <br> 可选值： <br>  <br> * true： 只根据 chunk 内容计算分 <br> * false：根据 chunk title + 内容 一起计算排序分 |
|  | get_attachment_link | bool | 否 | false | **是否获取 attachment 的临时下载链接** <br> 用于获取检索召回的原始图片 |
| **llm_param** |  | map | 否 |  | **大语言模型参数配置** |
|  | model | string | 否 | "Doubao-pro-32k" | **生成使用的大语言模型** <br> 可选模型： <br>  <br> * Doubao-pro-32k**（默认值）** <br> * Doubao-pro-128k <br> * Doubao-pro-256k <br> * Doubao-lite-32k <br> * Doubao-lite-128k |
|  | model_version | string | 否 |  | Doubao-pro-32k 可选的模型版本 <br>  <br> * 240828（默认） <br>  <br> Doubao-pro-128k 可选的模型版本 <br>  <br> * 240628 <br>  <br> Doubao-pro-256k 可选的模型版本 <br>  <br> * 240828 <br>  <br> Doubao-lite-32k 可选的模型版本 <br>  <br> * 240828 <br>  <br> Doubao-lite-128k 可选的模型版本 <br>  <br> * 240828 <br> * 240515 |
|  | max_new_tokens | int | 否 | 2000 | **最多生成多少个新 token** |
|  | temperature | float | 否 | 0.7 | **生成温度** |
|  | top_p | float | 否 | 0.9 | **用于控制输出 tokens 的多样性** <br> top_p 值越大输出的 tokens 类型越丰富，取值范围 [0, 1]。 |
|  | top_k | int | 否 | 0 | **选择预测值最大的 k 个 token 进行采样** <br> 取值范围 [0, 1000]，0 表示不生效。 |
|  | prompt | string | 否 | "使用以下的信息作为你学习到的知识，这些信息在 XML tags 之内。 <br> {{ .retrieved_chunks }} <br> 回答用户的问题，用户的问题在 XML tags 之内 <br> 回答问题时，如果 context 不能回答用户提出的问题，请直接说明你不知道。此外，回答问题时应该精简干练但又完整地回答用户的问题，避免过冗余的回答。 <br> {{ .user_query }} <br> " | {{ .retrieved_chunks }}和{{ .user_query }}是占位符，由后端传入检索到的文本片和用户的问题。 <br> prompt 中必须有且只有上述两个占位符，否则会抛出错误。 |
|  | prompt_extra_context | map | 否 | -- | **组装模型 prompt 时，检索到的文本片包含哪些信息** <br> 会将self_define_fields和system_fields的字段按先后拼接 <br>  <br> * self_define_fields：**用户自定义的元数据** <br>    * list类型，所有用户自定义的元数据名（可选） <br>    * **列表顺序=拼接顺序** <br> * system_fields：**可供选择的元数据** <br>    * 系统预设字段： <br>       * "doc_name": 文档名字（文档名称，可选） <br>       * "title"：知识所属文档的标题（文档标题，可选） <br>       * "chunk_title":文本片所属副标题（文本片副标题，可选） <br>       * "content": 原始文本加工后的知识内容（内容，必选） <br>    * **列表顺序=拼接顺序** |
|  | endpoint_id | string | 否 | -- | **大语言模型私有接入点** <br> 更多操作可参考[模型推理接入点保障 QPS](/docs/84313/1321481) <br> 需要传入 api_key 配合使用 |
|  | api_key | string | 否 | -- | **接入点 API Key** <br> 当需要使用私有模型接入点时，需传入对应 API key 进行鉴权 |
# **响应消息**
## 流式调用响应信息
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | 检索及流式生成内容 |
data 返回值
| 字段 | 子字段 | 字段类型 | 说明 |
| --- | --- | --- | --- |
| collection_name | -- | string | 检索知识库名字 |
| count | -- | int | 检索返回的结果数量 |
| **result_list** |  | list | 检索返回切片列表 |
|  | id | string | 索引的 primary_key |
|  | content | string | 切片内容，当文档类型为faq时，content为问题对应的答案 |
|  | score | float | 检索召回得分 |
|  | point_id | string | 知识点 id <br> 知识点唯一标识符 |
|  | chunk_title | string | 切片标题 |
|  | chunk_id | int | 切片 id，代表切片在对应文档里的位序，不同文档可能重复 |
|  | process_time | int | 知识处理完成时间 |
|  | rerank_score | float | rerank 得分，仅当 "rerank_switch" == true时出现 |
|  | doc_info | list | * "doc_id"：文档 id <br> * "doc_name"：文档名称 <br> * "create_time"：文档创建时间 <br> * "doc_type"：文档类型 <br> * "source"：文档上传来源，"tos_fe", "tos", "url" <br> * "title"：知识库所属文档标题 |
|  | recall_position | int | 召回位次，整数，从 1 开始，仅当 "rerank_switch" == true时出现 |
|  | chunk_type | string | 切片所属类型, "text", "table", "image" 等 |
|  | table_chunk_fields | list | 结构化数据检索返回单行全量数据 |
|  | **chunk_attachment** | **`list<object>`** | 检索召回附件（原始图片等）的临时下载链接，chunk_type 为 image 时有效 |
| generated_answer | -- | string | 生成回答，"stream" == true 时为空 |
| usage | -- | string | 大模型输入输出消耗 token 量，"stream" == true 时为空 |
| prompt | -- | string | 组装系统 prompt 和检索到的文本片后最终调用 LLM 时的完整 prompt |
chunk_attachment 返回值
| 字段 | 字段类型 | 说明 |
| --- | --- | --- |
| link | string | type 为 image 时表示图片的临时下载链接，有效期 10 分钟 |
| type | string | image 等 |
流式生成 data
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| generated_answer | string | 流式生成回答 |
流式结束标识 data
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| generated_answer | string | 为空 |
| usage | string | "completion_tokens"：大模型生成消耗 tokens <br> "prompt_tokens"：大模型输入消耗 tokens <br> "total_tokens"：大模型总计消耗 tokens |
| end | bool | "end" == true，表示流式返回结束 |
## 非流式调用响应信息
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | 检索及非流式生成内容 |
非流式生成 data
| 字段 | 子字段 | 说明 |
| --- | --- | --- |
| collection_name | -- | 检索知识库名字 |
| count | -- | 检索返回的结果数量 |
| **result_list** |  | 检索返回切片列表 |
|  | id | 索引的 primary_key |
|  | content | 切片内容 |
|  | score | 检索召回得分 |
|  | point_id | 知识点 id：doc_id 拼接 chunk_id，唯一 |
|  | chunk_title | 切片标题 |
|  | chunk_id | 切片 id，不同文档可能重复 |
|  | process_time | 知识处理完成时间 |
|  | rerank_score | rerank 得分 |
|  | doc_info | * "doc_id"：文档 id <br> * "doc_name"：文档名称 <br> * "create_time"：文档创建时间 <br> * "doc_type"：文档类型 <br> * "source"：文档上传来源，"tos_fe", "tos", "url" <br> * "title"：知识库所属文档标题 |
|  | recall_position | 召回位次，整数，从 1 开始 |
|  | chunk_type | 切片所属类型, "text", "table", "image" |
| generated_answer | -- | 生成回答 <br> 如 "在**创建知识库**页面填写相关参数时，可以在配置知识库页面下设置知识库使用的切片规则与使用的向量化模型，以及知识库的元信息定义和索引 CPU 限额等信息。并且展开高级设置，可以设置知识库的索引算法和量化方式。" |
| usage | -- | 大模型输入输出消耗 token 量 <br> 如 {"prompt_tokens":2000,"completion_tokens":2040,"total_tokens":4040} |
| prompt | -- | 组装系统 prompt 和检索到的文本片后最终调用 LLM 时的完整 prompt |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 缺乏鉴权信息 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection 不存在 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/collection/search_and_generate \
  -d '{
  "name": "我的知识库",
  "project": "",
  "query": "首次创建知识库要配置哪些参数？",
  "stream": true, #开启流式返回
  "query_param": {
  },
  "retrieve_param": {
    "rerank_switch": true,
    "retrieve_count": 30,
    "dense_weight": 0.7,
    "limit": 15,
    "chunk_diffusion_count": 1    
  },
  "llm_param": {
    "model": "Doubao-pro-32k",
    "max_new_tokens": 2500,
    "min_new_tokens": 5,
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 10,
    "prompt": "使用以下的信息作为你学习到的知识，这些信息在 <context></context> XML tags 之内.\n\n<context>\n{{.retrieved_chunks}}\n</context>\n\n回答用户的问题，用户的问题在<query></query> XML tags 之内\n回答问题时，如果你不知道，请直接说明你不知道。\n\n<query>\n{{.user_query}}\n</query> ",
    "prompt_extra_context": {
      "self_define_fields": ["自定义元数据1", "自定义元数据2"],
      "system_fields": ["doc_name", "title", "chunk_title", "content"]
    }
  }
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 209
Content-Type: application/json
 
{
    "code": 0,
    "data": {
        "collection_name": "knowledge_base_instruction", #检索知识库名字
        "count": 2, #检索返回的结果数量
        "result_list": [
            {
            "id": "help-1", #索引的 primary_key
            "content": "在**创建知识库**页面填写相关参数。在配置知识库页面下可以设置知识库使用的切片规则与使用的向量化模型，以及知识库的元信息定义和索引 CPU 限额等信息。展开高级设置，可以设置知识库的索引算法和量化方式。", #原始文本加工后的知识内容
            "score": 0.71294925212860107 , #检索得分
            "chunk_title": "首次创建知识库", #该 chunk 的父标题
            "chunk_id": 5, #该 chunk 在所属文档中的排序位置
            "process_time": 1720773416, #知识处理完成的时间
            "rerank_score": 0.71294925212860107 , #rerank得分
            "doc_info": {
                "doc_id": "help", #文档id
                "doc_name": "知识库帮助中心.docx", #文档名字
                "create_time": 1720773416, #文档的创建时间
                "doc_type": "docx", #知识所属原始文档的类型
                "source": "tos", #知识来源, "tos","url"
                "title": "创建知识库", #知识所属文档的标题
                },
            "recall_position": 13, #召回位次，整数，从 1 开始
            "rerank_position": 2, #重排后在结果列表的位次，整数，从 1 开始
            "chunk_type": "text", #切片所属类型, "text","table","image"等
            },
            {...},
        ],
        "generated_answer": "", #使用大模型生成的内容，仅非流式下有返回
        "usage": "", #大模型输入输出消耗 token 量，仅非流式下有返回
        "prompt": "\n使用以下的信息作为你学习到的知识，这些信息在 <context></context> XML tags 之内.\n\n<context>\n\ndoc_name:知识库帮助中心.docx\n", #组装系统 prompt 和检索到的文本片后最终调用 LLM 时的完整 prompt
        },
    "message":"success",
    "request_id":"02172182782007500000000000000000000ffff0a0040acf7106c"
}

{"code":0,"data":{"generated_answer":"知识库页面下设置知识库使用的切片规则与使用的"},"message":"success","request_id":"02172182782007500000000000000000000ffff0a0040acf7106c"}
{...}

{"code":0,"data":{"generated_answer":"","usage":"{\"completion_tokens\":2,\"prompt_tokens\":939,\"total_tokens\":941}\n","end":true},"message":"success","request_id":"02172182782007500000000000000000000ffff0a0040acf7106c"}
```

执行失败返回：
```Shell
HTTP/1.1 400 OK
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


