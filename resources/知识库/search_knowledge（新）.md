
---


本节将说明如何基于一个已创建的知识库或某个[实验版本](https://www.volcengine.com/docs/84313/1510752)进行语义检索。
> 支持通过指定 pipeline_name 参数，来实现仅检索某个实验版本下的切片

# 概述
/api/knowledge/collection/search_knowledge 接口用于对知识库进行检索和前后处理，当前会默认对原始文本加工后的知识内容进行检索。
# **前提条件**

* 知识库创建完成、文档导入且处理完成后，即代表可以进行在线检索
* 调用接口前请先完成 [签名鉴权与调用示例](/docs/84313/1254485) 页面的注册账号、实名认证、AK/SK 密钥获取和签名获取
* search 和 search_knowledge 接口的区别：search_knowledge 接口是知识库在线链路升级后的最新接口，在原本 search 接口的基础上支持了多轮改写、文档聚合排序等新功能，与 chat_completions 接口联动，可以完成标准的检索生成链路

# **请求接口**
| **URI** | /api/knowledge/collection/search_knowledge | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| name | -- | string | 否 | -- | **知识库名称** |
| project | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在 default 项目下检索。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 name 和 project 作为知识库的唯一标识 |
| query | -- | string | 是 | -- | **检索文本** <br>  <br> * 最大可输入长度为 8000，query 长度 > 8000 时，接口报错 <br> * 所选 embedding 模型输入最大长度 < query 长度 < 8000 时，query 按所选模型自动截断 <br> * query 长度 < 所选 embedding 模型输入最大长度时，正常检索返回目标切片 |
| image_query | -- | string | 否 | -- | **检索图片** <br> 支持图片 URL 或 Base64 编码，详细要求见[图片像素说明](https://www.volcengine.com/docs/82379/1409291?lang=zh#7a10f532)和[图片文件格式](https://www.volcengine.com/docs/82379/1409291?lang=zh#5c068efa) <br>  <br> * 图片 URL 传入：适用于图片文件已存在公网可访问 URL 的场景，单张图片小于 10 MB <br> * Base64 编码传入：适用于图片文件较小的场景，支持 **JPEG、PNG、WebP、BMP** 四种格式的 Base64 编码，单张图片小于 3 MB，请求体不能超过 4 MB |
| limit | -- | int | 否 | 10 | **检索结果数量** <br>  <br> * 数量要求：[1, 1000] |
| query_param |  | json | 否 | -- | **检索的过滤和返回设置** |
|  | doc_filter | map | 否 | -- | **检索过滤条件** <br>  <br> * 支持对 doc 的 meta 信息过滤 <br> * 详细使用方式和支持字段见[filter表达式](https://www.volcengine.com/docs/84313/1419289#filter-%E8%A1%A8%E8%BE%BE%E5%BC%8F)，可支持对 doc_id 做筛选 <br> * 此处用过过滤的字段，需要在 collection/create 时添加到 index_config 的 fields 上 <br>  <br> 例如： <br> 单层 filter： <br> ```JSON <br> doc_filter = { <br>     "op": "must", // 查询算子 must/must_not/range/range_out <br>     "field": "doc_id", <br>     "conds": ["tos_doc_id_123", "tos_doc_id_456"] <br> } <br> query_param = { <br>     "doc_filter": doc_filter <br> } <br> ``` <br>  <br> 多层 filter： <br> ```JSON <br> doc_filter = { <br>   "op": "and",   // 逻辑算子 and/or <br>   "conds": [     // 条件列表，支持嵌套逻辑算子和查询算子 <br>     { <br>       "op": "must", <br>       "field": "type", <br>       "conds": [1] <br>     }, <br>     { <br>         ...         // 支持>=1的任意数量的条件进行组合 <br>     } <br>   ] <br> } <br>  <br> query_param = { <br>     "doc_filter": doc_filter <br> } <br> ``` <br>  |
| dense_weight | -- | float | 否 | 0.5 | **混合检索中稠密向量的权重** <br>  <br> * 1 表示纯稠密检索，0 表示纯字面检索，范围 [0.2, 1] <br> * 只有在请求的知识库使用的是混合检索时有效，即索引算法为 hnsw_hybrid |
| pre_processing |  | json |  |  | **检索预处理** |
|  | need_instruction | bool | 否 | false | **是否拼接 instruction 进行检索** |
|  | return_token_usage | bool | 否 | false | **是否返回 search 流程中各阶段的 token 使用量** |
|  | rewrite | bool | 否 | false | **是否对 query 进行改写** <br> 根据 messages 字段传入的历史对话信息进行改写，最多 3 轮 <br> **注：​**只有在 messages 字段长度大于 2 且不为空时，设置参数值为 true，才能返回有效的 rewrite_query； <br> ```JSON <br> "messages": [ <br>     {"role": "user", "content": "prompt 1"}, <br>     {"role": "assistant", "content": "prompt2"}, <br>     {"role": "user", "content": "prompt 3"}, <br> ] <br> ``` <br>  |
|  | messages | json | 是 | -- | **多轮对话信息** <br> 仅**开启改写**时需要上传，可根据历史对话内容进行问题改写，注意上传对话轮数需 >= 1 <br> 发出消息的对话参与者角色，可选值包括： <br>  <br> * user：User Message 用户消息 <br> * assistant：Assistant Message 对话助手消息 <br>  <br> ```JSON <br> [ <br>     {"role": "user", "content": "知识库支持哪些文档格式？"}, <br>     {"role": "assistant", "content": "知识库支持结构化和非结构化文档，其中结构化文档支持 excel、csv、jsonl 等常见格式，非结构化文档支持 pdf、docx、ppt 等常见格式。"}, <br>     {"role": "user", "content": "那大小呢？"}, <br> ] <br> ``` <br>  |
| post_processing |  | json |  |  | **检索后处理** |
|  | rerank_switch | bool | 否 | false | **自动对结果做 rerank** <br> 打开后，会自动请求 rerank 模型排序 |
|  | retrieve_count | int | 否 | 25 | **进入重排的切片数量，默认为 25** <br> 只有在 rerank_switch 为 true 时生效。retrieve_count 需要大于等于 limit，否则会抛出错误 |
|  | chunk_diffusion_count | int | 否 | 0 | **检索阶段返回命中切片的上下几片邻近切片** <br> 默认为 0，表示不进行 chunk diffusion。范围 [0, 5] |
|  | chunk_group | bool | 否 | false | **文本聚合** <br> 默认不聚合，对于非结构化文件，考虑到原始文档内容语序对大模型的理解，可开启文本聚合。开启后，会根据文档及文档顺序，对切片进行重新聚合排序返回 |
|  | rerank_model | string | 否 | "base-multilingual-rerank" | **rerank 模型选择** <br> 仅在 "rerank_switch" == true 的时候生效 <br> 可选模型： <br>  <br> * "doubao-seed-rerank"（即 doubao-seed-1.6-rerank）：字节自研多模态重排模型、支持文本 / 图片 / 视频混合重排、精细语义匹配、可选阈值过滤与指令设置 <br> * "base-multilingual-rerank"：速度快、长文本、支持 70+ 种语言 <br> * "m3-v2-rerank"：常规文本、支持 100+ 种语言 |
|  | enable_rerank_threshold | bool | 否 | false | **是否开启阈值过滤** <br> **仅当 rerank_model=="doubao-seed-rerank" 时生效**，为 true 时 rerank_threshold 生效 |
|  | rerank_threshold | float | 否 | -- | **阈值过滤** <br> **仅当 rerank_model=="doubao-seed-rerank" 时生效**，用于设置重排分数的过滤阈值，低于阈值的结果将不会被返回，取值范围为 0 到 1 |
|  | rerank_instruction | string | 否 | -- | **rerank 指令** <br> **仅在 "rerank_switch" == true 且 "rerank_model" == "doubao-seed-rerank" 时生效**，用于提供给模型一个明确的排序指令，提升重排效果。字符串长度不超过 1024 <br> *如：Whether the document answers the query or matches the content retrieval intent* |
|  | rerank_only_chunk | bool | 否 | false | **是否仅根据 chunk 内容计算重排分数** <br> 可选值： <br>  <br> * true： 只根据 chunk 内容计算分 <br> * false：根据 chunk title + 内容 一起计算排序分 |
|  | get_attachment_link | bool | 否 | false | **是否获取切片中图片的临时下载链接** |
| pipeline_name | -- | string | 否 | -- | **实验版本名称** <br>  <br> * 指定当前参数可查询具体实验版本下的切片列表 <br> * 不指定默认查询知识库主版本下的切片列表 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | 检索召回切片信息 |
data 返回值
| **字段** | **子字段** | **字段类型** | **说明** |
| --- | --- | --- | --- |
| collection_name | -- | string | 检索知识库名字 |
| count | -- | int | 检索返回的切片数量 |
| rewrite_query | -- | string | 改写的 query |
| token_usage |  | json | token 用量信息 |
|  | embedding_token_usage | json | 检索向量化阶段的 token 用量 <br> ```JSON <br> { <br>     "prompt_tokens": 16, <br>     "completion_tokens": 0, <br>     "total_tokens": 16 <br> } <br> ``` <br>  |
|  | rerank_token_usage | int | 重排阶段的 token 用量 |
|  | rewrite_token_usage | int | query 改写阶段的 token 用量 |
| result_list |  | list | 返回切片信息 |
|  | id | string | 索引的主键 |
|  | content | string | 切片内容 <br> 1、非结构化文件：content 返回切片内容 <br> 2、faq 文件：content 返回答案 <br> 3、结构化文件：content 返回参与索引的字段和取值，以 K:V 对拼接，使用 \n 区隔 <br> 4、音视频文件：content 返回音视频切片说话人，起始和结束时间单位 ms，通过 asr 转换的文本内容，如： <br> ```Plain <br> 说话人1[620,4160]：xxxxxx\n 说话人2[7660,19830]：xxxxxx\n <br> ``` <br>  |
|  | md_content | string | markdown 格式的解析结果 <br> 对于非结构化文档中的表格切片，可以额外返回 markdown 格式解析结果，保留更多表格原始信息 <br> 表格切片可以通过 chunk_type == table 判断 |
|  | html_content | string | html 格式的解析结果 <br> 对于非结构化文档中的表格切片，可以额外返回 html 格式解析结果，保留更多表格原始信息 <br> 表格切片可以通过 chunk_type == table 判断 |
|  | description | string | 若创建知识库时开启切片内容分析，即enable_slice_analysis=true，此字段则返回切片内容分析结果 |
|  | table_chunk_fields | list | 结构化数据检索返回单行全量数据 |
|  | original_question | string | faq 数据检索召回答案对应的原始问题 |
|  | score | float | 向量化语义检索得分 |
|  | point_id | string | 切片 id |
|  | chunk_title | string | 切片标题 |
|  | chunk_id | int | 切片位次 id <br> 代表在原始文档中的位次顺序 |
|  | process_time | int | 检索耗时（s） |
|  | rerank_score | float | 重排得分 |
|  | doc_info | list | 切片所属文档信息 <br> ```JSON <br> { <br>     "doc_id": "_sys_auto_gen_doc_id-134144883689", //文档 id <br>     "doc_name": "2404.08817v2.pdf", //文档名字 <br>     "create_time": 1727333117, //文档的创建时间 <br>     "doc_type": "pdf", //知识所属原始文档的类型 <br>     "doc_meta": "[{\"field_name\":\"doc_id\",\"field_type\":\"string\",\"field_value\":\"_sys_auto_gen_doc_id-13411829101044883689\"}]", //文档相关元信息（此处是一个包含文档 id 信息的列表形式的字符串） <br>     "source": "url", //知识来源类型：tos、lark、tos_fe <br>     "title": "Revisiting Code Similarity Evaluation with Abstract Syntax Tree Edit Distance", //知识所属文档的标题 <br>     "url": "***" //原始文档的公开下载链接或飞书文档链接 <br> } <br> ``` <br>  |
|  | recall_position | int | 向量化语义检索召回位次 |
|  | rerank_position | int | 重排位次 |
|  | chunk_type | string | 切片类型 <br> 部分返回值类型有：doc-image、image、video、audio、table、mixed-table、text、structured、faq等 |
|  | chunk_attachment | list | 检索召回附件的临时下载链接，有效时间 10 分钟 <br> chunk_type 为 image/doc_image 且 get_attachment_link 为 true 时，返回原始图片下载链接 <br> chunk_type 为 video 且 get_attachment_link 为 true 时，该字段会返回视频切片所抽取的关键帧图片列表，图片按照时间从小到大排序 <br> chunk_type 为 table/mixed-table 且 get_attachment_link 为 true 时，该字段会返回表格的图片或表格中所包含的图片列表 |
|  | original_coordinate |  | 切片在原文中的位置坐标 <br> 目前仅支持 pdf 和 ppt 文档，返回示例如下： <br> ```Plain <br> { <br>   "page_no": [0, 2], <br>   "bbox": [ <br>               [0.43075400818407467, 0.05201688247011952, 0.8814365734218823, 0.06268848178713717], <br>               [0.1144293768909557, 0.08121951665355412, 0.8790083028120703, 0.7626920876297637] <br>   ] <br> } <br> ``` <br>  |
|  | audio_start_time | long | 音频切片开始毫秒 |
|  | audio_end_time | long | 音频切片结束毫秒 |
|  | video_start_time | long | 视频切片开始毫秒 |
|  | video_end_time | long | 视频切片结束毫秒 |
table_chunk_fields 返回值
| 字段 | 字段类型 | 说明 |
| --- | --- | --- |
| field_name | string | 结构化数据的表字段名称 |
| field_value | -- | 结构化数据的表字段取值 <br> 字段类型以创建知识库时表字段定义为准 |
chunk_attachment 返回值
| 字段 | 字段类型 | 说明 |
| --- | --- | --- |
| uuid | string | 附件的唯一标识 |
| caption | string | 图片所属标题，若未识别到标题则值为"\n" |
| type | string | image 等 |
| link | string | "get_attachment_link" == true 时返回图片或视频抽帧图列或表格包含图片的临时下载链接，有效期 10 分钟 |
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
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/collection/search_knowledge \
  -d '{
        "name": "your_collection",
        "query": "test",
        "limit": 2,
        "query_param": {
            "doc_filter": {
                "op": "must",
                "field": "doc_id",
                "conds": ["tos_doc_id_123", "tos_doc_id_456"]
            }
        },
        "dense_weight": 0.5,
        "pre_processing": {
            "need_instruction": true,
            "rewrite": true,
            "messages": [
                {
                    "role": "system",
                    "content": "prompt template"
                },
                {
                    "role": "user",
                    "content": "history content"
                },
                {
                    "role": "assistant",
                    "content": "history content"
                },
                {
                    "role": "user",
                    "content": "history content"
                },
                {
                    "role": "assistant",
                    "content": "history content"
                }
                
            ],
            "return_token_usage": true
        },
        "post_processing": {
            "rerank_switch": false,
            "rerank_model": "base-multilingual-rerank",
            "rerank_only_chunk": false,
            "retrieve_count": 25,
            "chunk_group": false,
            "get_attachment_link": false
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
        "collection_name": "example",
        "count": 2,
        "rewrite_query": "xxx",
        "token_usage": {
            "embedding_token_usage": {
                "prompt_tokens": 16,
                "completion_tokens": 0,
                "total_tokens": 16
            },
            "rerank_token_usage": 0
        },
        "result_list": [
            {
                "id": "_sys_auto_gen_doc_id-13411829101044883689-15",
                "content": "content",
                "score": 0.2639991044998169,
                "point_id": "_sys_auto_gen_doc_id-13411829101044883689-15",
                "chunk_title": "title",
                "chunk_id": 15,
                "process_time": 1,
                "doc_info": {
                    "doc_id": "_sys_auto_gen_doc_id-13411829101044883689",
                    "doc_name": "2404.08817v2.pdf",
                    "create_time": 1727333117,
                    "doc_type": "pdf",
                    "doc_meta": "[{\"field_name\":\"doc_id\",\"field_type\":\"string\",\"field_value\":\"_sys_auto_gen_doc_id-13411829101044883689\"}]",
                    "source": "tos_fe",
                    "title": "title"
                },
                "recall_position": 1,
                "chunk_type": "text"
            },
            {
                "id": "_sys_auto_gen_doc_id-13411829101044883689-7",
                "content": "content",
                "score": 0.2583845257759094,
                "point_id": "_sys_auto_gen_doc_id-13411829101044883689-7",
                "chunk_title": "title",
                "chunk_id": 7,
                "process_time": 1,
                "doc_info": {
                    "doc_id": "_sys_auto_gen_doc_id-13411829101044883689",
                    "doc_name": "2404.08817v2.pdf",
                    "create_time": 1727333117,
                    "doc_type": "pdf",
                    "doc_meta": "[{\"field_name\":\"doc_id\",\"field_type\":\"string\",\"field_value\":\"_sys_auto_gen_doc_id-13411829101044883689\"}]",
                    "source": "tos_fe",
                    "title": "title"
                },
                "recall_position": 2,
                "chunk_type": "text"
            }
        ]
    },
    "message": "success",
    "request_id": "02172740884343900000000000000000000ffff0a00406f8a8861"
}
```

执行失败返回：
```Shell
HTTP/1.1 400 OK
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


