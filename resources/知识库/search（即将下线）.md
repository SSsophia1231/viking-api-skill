**注意**：该接口预计下线，不再更新支持新功能。建议用户选择 search_knowledge 使用，新增功能和模型会优先适配新接口。

---


本节将说明如何基于一个已创建的知识库做在线检索。
* 知识库创建完成、文档导入且处理完成后，即代表可以进行在线检索了。
* 调用接口前请先完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取。

# 概述
/api/knowledge/collection/search 接口用于对知识库进行检索，当前会默认对原始文本加工后的知识内容进行检索。
# **前提条件**

* 知识库创建完成。
* 文档导入且处理完成。
* 完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现知识库的检索查询功能。

# **请求接口**
| **URI** | /api/knowledge/collection/search | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| name | -- | string | 否 | -- | **知识库名称** <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空 <br> * 长度要求：[1, 64] |
| project | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在 default 项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 name 和 project 作为知识库的唯一标识 |
| query | -- | string | 是 | -- | **检索文本**，最大可输入长度为 8000： <br>  <br> * query 长度 > 8000 时，接口报错 <br> * 所选 embedding 模型输入最大长度 < query 长度 < 8000 时，query 按所选模型自动截断 <br> * query 长度 < 所选 embedding 模型输入最大长度 时，正常检索并返回结果 |
| limit | -- | int | 否 | 10 | **检索结果数量** <br>  <br> * 数量要求：[1, 200] |
| **query_param** |  | **json** | 否 |  | **检索的过滤和返回设置** |
|  | doc_filter | map | 否 | -- | **检索过滤条件**，支持对 doc 的 meta 信息过滤 <br>  <br> * 使用方式和支持字段见[filter 表达式](/docs/84313/1254563#2f7e9f83) <br> * 此处用作过滤的字段，需要在 collection/create 时添加到 index_config 的 fields 上 |
| rerank_switch | -- | bool | 否 | false | **自动对结果做 rerank** <br> 说明：打开后，会自动请求 rerank 模型排序 |
| retrieve_count | -- | int | 否 | 25 | **进入重排的切片数量**，默认为 25 <br> 只有在 rerank_switch 为 true 时生效。retrieve_count 需要大于等于 limit，否则会抛出错误 |
| dense_weight | -- | float | 否 | 0.5 | **混合检索中稠密向量的权重** <br> 1 表示纯稠密检索，0 表示纯字面检索，范围 [0.2, 1] <br> 只有在请求的知识库使用的是混合检索时有效，即索引算法为 hnsw_hybrid |
| rerank_model | -- | string | 否 | "m3-v2-rerank" | **rerank 模型选择** <br> 仅在 "rerank_switch" == true 的时候生效 <br> 可选模型： <br>  <br> * "m3-v2-rerank"：轻量小模型，具有强大的多语言能力，推理速度快 |
| rerank_only_chunk | -- | bool | 否 | false | **是否仅根据 chunk 内容计算重排分数** <br> 可选值： <br>  <br> * true： 只根据 chunk 内容计算分 <br> * false：根据 chunk title + 内容 一起计算排序分 |
| get_attachment_link | -- | bool | 否 | false | **是否获取 attachment 的临时下载链接** <br> 用于获取检索召回的原始图片 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | 检索返回内容 |
data 返回值
| 字段 | 子字段 | 字段类型 | 说明 |
| --- | --- | --- | --- |
| collection_name | -- | string | 检索知识库名字 |
| count | -- | int | 检索返回的结果数量 |
| **result_list** |  | **list** | 检索返回切片列表 |
|  | id | string | 索引的 primary_key |
|  | content | string | 切片内容，当文档类型为 faq 时，content为问题对应的答案 |
|  | original_question | string | 文本片为 faq 时，返回原始问题 |
|  | score | float | 检索召回得分 |
|  | point_id | string | 知识点 id <br> 知识点唯一标识符 |
|  | chunk_title | string | 切片标题 |
|  | chunk_id | int | 切片 id，代表切片在对应文档里的位序，不同文档可能重复 |
|  | process_time | int | 知识处理完成时间 |
|  | rerank_score | float | rerank 得分，仅当 "rerank_switch" == true 时出现 |
|  | doc_info | object | * "doc_id"：文档 id <br> * "doc_name"：文档名称 <br> * "create_time"：文档创建时间 <br> * "doc_type"：文档类型 <br> * "source"：文档上传来源，"tos_fe", "tos", "url" <br> * "title"：知识库所属文档标题 |
|  | recall_position | int | 召回位次，整数，从 1 开始，仅当 "rerank_switch" == true 时出现 |
|  | rerank_position | int | 重排位次，整数，从 1 开始，仅当 "rerank_switch" == true 时出现 |
|  | chunk_type | string | 切片所属类型, "text", "table", "image" 等 |
|  | table_chunk_fields | list | 结构化数据检索返回单行全量数据 |
|  | **chunk_attachment** | **list** | 检索召回附件（原始图片等）的临时下载链接，chunk_type 为 image 时有效 |
chunk_attachment 返回值
| 字段 | 字段类型 | 说明 |
| --- | --- | --- |
| link | string | type 为 image 时表示图片的临时下载链接，有效期 10 分钟 |
| type | string | image 等 |
## **状态码说明**
| **状态码** | **HTTP 状态码** | **返回信息** | **状态码说明** |
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
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/collection/search \
  -d '{
    "name": "test_name",
    "project": "default",
    "query": "introduce a new document level structure",
    "retrieve_count": 25,
    "limit": 2,
    "query_param": {
        "doc_filter": {
          "op": "must",
          "field": "doc_id",
          "conds": ["tos_doc_id_123", "tos_doc_id_456"]
        }
    },
    "rerank_switch": true,
    "dense_weight": 0.5
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 43
Content-Type: application/json
 
{
    "code":0,
    "data": {
          "collection_name": "test_name",
          "count": 2,
          "result_list": [
            {
                "id": "tos_doc_id_456",
                "chunk_title": "Conclusion",
                "content": "In this paper, we discussed the task of document level structure parsing. This task is more intricate compared to the traditional page level scenario. This complexity arises because we need to consider connecting paragraphs across pages and linking paragraphs into sections. To address these challenges, we introduced a transition-based parser as a solution. Alongside this, we introduced a new dataset called DocTree to support this task.",
                "score": 0.7119365930557251,
                "recall_position": 1,
                "point_id": "tos_doc_id_2_1-217-6834848478902922598",
                "process_time": 1709097567,
                "rerank_score": 0.877777,
                "rerank_position": 1,
                "doc_info": {        
                    "doc_id": "tos_doc_id_456",
                    "doc_name": "DLSP: A Document Level Structure Parser for Multi-Page Digital Documents.pdf",
                    "create_time": 1677561567,
                    "doc_type": "pdf",
                    "doc_meta": "[{\"field_name\": \"author\", \"field_type\": \"string\", \"field_value\": \"Mike\"}, {\"field_name\": \"category\", \"field_type\": \"string\", \"field_value\": \"Mike\"}]",
                    "source": "tos",
                    "title": "DLSP: A Document Level Structure Parser for Multi-Page Digital Documents"
               }
            },
            {
                "id": "tos_doc_id_456",
                "chunk_title": "Conclusion",
                "content": "We also introduce a new document level structure parsing dataset called DocTree. It comprises 1,298 manually annotated documents with document level structural information. In contrast to previous datasets focusing on single page, the maximum page number in DocTree reaches 85 while the average is 7.2.",
                "score": 0.711473822593689,
                "recall_position": 1,
                "point_id": "tos_doc_id_2_1-37-3242137170643999406",
                "process_time": 1709097567,
                "rerank_score": 0.5874546,
                "rerank_position": 2,
                "doc_info": {        
                    "doc_id": "tos_doc_id_456",
                    "doc_name": "DLSP: A Document Level Structure Parser for Multi-Page Digital Documents.pdf",
                    "create_time": 1677561593,
                    "doc_type": "pdf",
                    "doc_meta": "[{\"field_name\": \"author\", \"field_type\": \"string\", \"field_value\": \"Mike\"}, {\"field_name\": \"category\", \"field_type\": \"string\", \"field_value\": \"Mike\"}]",
                    "source": "tos",
                    "title": "DLSP: A Document Level Structure Parser for Multi-Page Digital Documents"
               }
            }
        ]
    },
    "message": "success",
    "request_id": "02170910041086600000000000000000000ffff0a00609d26d25e"
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


