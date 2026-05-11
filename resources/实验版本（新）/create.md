api/knowledge/pipeline/create 创建一个新的[实验版本](https://www.volcengine.com/docs/84313/1510752)
> pipeline： 对应知识库控制台的“实验版本”功能，每个 pipeline 拥有一条独立的离线数据处理流水线，可以通过多个 pipeline 对比同一批数据的不同处理策略，并择优发布成正式版本。

pipeline 相关控制台操作介绍：https://www.volcengine.com/docs/84313/1510752

> 注：

> * 单个知识库**最多创建 10 个 pipeline**
> * 仅旗舰版知识库支持使用实验版本 API

# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现从知识库创建一个新实验版本的功能。
# **请求接口**
| **URI** | api/knowledge/pipeline/create | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端向向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: token=********** | 鉴权 |
# **请求参数**
| 参数 | 子参数 | 类型 | 必选 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| collection_name | *  | string | 否 | *  | **知识库名称** |
| project | *  | string | 否 | default | **项目名** |
| resource_id | *  | string | 否 | *  | **知识库唯一 id** <br>  <br> * 可选择直接传 resource_id ，或同时传 name 和 project 作为知识库的唯一标识 |
| name | *  | string | 是 | *  | **实验版本名称** <br>  <br> * 不能使用已有系统的默认值 “default” <br> * 实验版本由字母、数字、下划线组成，并只能以字母开头 <br> * 长度不超过 128 个字符 |
| index |  | object | 否 |  | **索引配置** |
|  | index_config | object | 否 | *  | ```JSON <br> { <br>     "fields": [ <br>         { <br>             "field_name": "type", <br>             //标签名 <br>             "field_type": "string", <br>             //标签类型 <br>             "default_val": "instruction" <br>             //标签默认值 <br>          }, <br>          {...} <br>     ], <br>     "cpu_quota": 1, <br>     // cpu 配额，整数型，大于 0， 默认值为 1 <br>     "embedding_model": "doubao-embedding-and-m3", <br>     // 指定向量化模型 <br>     "embedding_dimension": 2048, <br>     // 向量维度 <br>     "quant": "int8" <br>     // 向量的量化方式 <br>  <br>     // "embedding_model"、"embedding_dimension"和"quant"可选范围参考 <br> } <br> ``` <br>  <br> 注： <br>  <br> * fields 即“标签”，数量限制为 180 个，且名称不可重复，可用于检索时对文档进行过滤。 <br> * fields 的名字不能以 "_sys_auto" 开头，否则会创建失败。 <br> * 对于 fields，如果不传或 value 为空，将不会加入任何的筛选字段。 <br> * 如果 field 设置为 “doc_id” 且 字段类型为 “string” 类型，这时系统会将后续上传文档的 doc_id 值写入 |
|  | index_type | string | 否 | hnsw_hybrid | **指定索引算法** <br> 支持 hnsw_hybrid、hnsw 和 flat <br> 推荐选择 “hnsw_hybrid”，能够兼具对关键词和语义的理解，综合提高检索精度 <br> 向量化模型和索引算法的对照关系参考 [向量化模型及索引算法对照表](https://www.volcengine.com/docs/84313/1254593#6e312068) |
| preprocessing |  | object | 否 |  | **非结构化文档处理策略** <br>  <br> * 当 data_type 为 “unstructured_data” 时生效，为 “structured_data” 时无效。 |
|  | chunking_strategy | string | 否 | *  | **选用的切片策略**，枚举值：["custom_balance", "custom"] <br>  <br> * “custom_balance” 是方舟知识库系统提供的最新默认文档处理策略，该策略： <br>    1. 升级了对 PDF, DOCX 等复杂文档的解析和理解能力，对复杂文档版面结构、语义结构的解析能力获得大幅提升；特别优化了图片内容及其上下文的理解和加工能力，支持将图片和文本 chunk 混合编排，增强上下文一致性；特别优化了表格内容的理解加工能力，对长表格解析和切片更具优势；结合 VikingDB 语义和关键词融合检索算法，提高了多模态内容的检索能力，大幅提升相关信息的召回能力；提高了切片算法信噪比，无关信息更少，语义损失更小。 <br>    2. 选用此策略后，可生效的文档处理策略子参数包括： <br>    * "chunk_length" (仅当“chunking_identifier”为空时生效） <br>    * "merge_small_chunks" (仅当“chunking_identifier”为空时生效） <br>    * "multi_mode" (仅当“chunking_identifier”为空时生效） <br> * “custom” 是使用自定义分隔符的文档处理策略，选用此策略后，可生效的文档处理策略子参数包括： <br>    * “chunking_identifier” <br>    * "chunk_length" (仅当“chunking_identifier”为空时生效） <br>    * "merge_small_chunks" (仅当“chunking_identifier”为空时生效） <br>    * "multi_mode" (仅当“chunking_identifier”为空时生效） <br> * 请注意原 “default” 策略目前仅用于兼容存量知识库，不再维护，**新建知识库建议采用 “custom_balance”** |
|  | chunking_identifier | list | 否 | *  | **自定义分隔符号** |
|  | chunk_length | int | 否 | 500 | **切片最大长度** <br> 取值范围见 [向量化模型及索引算法对照表](https://www.volcengine.com/docs/84313/1254593#6e312068) |
|  | merge_small_chunks | bool | 否 | true | **是否合并短文本片** <br> 配置是否对短文本片进行合并，且合并后的文本片会限制不超过切片最大长度 |
|  | multi_modal | *  | 否 | *  | **图片召回策略** <br> 枚举值： <br>  <br> * "image_ocr"：图片 ocr <br>  <br> 传参示例： <br>  <br> * 当 `"multi_modal": ["image_ocr"]` 时，开启图片 ocr，不传值即代表不开启图片 ocr <br>  <br> 使用旧参数命名“multi_mode”创建的库仍保留原命名，但新创建知识库不推荐继续使用。 |
| data_type | *  | string | 是 | *  | **知识库内的数据类型** <br>  <br> * unstructured_data：非结构化数据 <br> * structured_data：结构化数据 |
| table_config | *  | object | 否 | *  | **结构化知识库表字段定义** <br> 当 data_type 为 “structured_data” 时生效 <br> ```JSON <br> { <br>   "table_type": "row", <br>   // 可选值：row（从行开始解析）、col（从列开始解析） <br>   "table_pos": "int", <br>   // 字段位于第几行或第几列, <br>   "start_pos": "int", <br>   // 起始数据在第几行, <br>   "table_fields": [ <br>       { "field_name": "xxx", //字段名称 <br>           "field_type": "int64", //字段类型, 支持string, int64, float32, bool <br>           "if_embedding": true, //是否参与索引 <br>           "default_value":"xxx", //默认值 <br>           "if_filter": false //设置为过滤字段 <br>     }, <br>     ..... <br>   ] <br> } <br> ``` <br>  |
| auto_sync_doc | *  | bool | 否 | *  | **是否自动同步新增文档** <br> 打开后调用 add_doc 接口向知识库上传文档时，自动同步到当前实验版本 |
| doc_summary_config |  | object | 否 | -- | **知识库摘要配置** |
|  | enabled | bool | 否 | false | **是否开启文档 AI 摘要功能** <br> 配置知识库是否开启文档 AI 生成摘要功能，开启后，该知识库将自动为每篇文档生成摘要并保存结果到文档元信息中 <br> 注：此功能仅对当知识库类型为非结构化知识库时生效，即 data_type 为 “unstructured_data” 时生效 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 403 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 <br>  <br> * 缺失必选参数 <br> * collection_name 命名不符合规范 <br> * 字段类型与相关字段属性不满足约束条件 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
-H 'Content-Type: application/json' \
-H 'Authorization: token=****' \
https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/pipeline/create \
-d '{
  "collection_name": "test_collection_name",
  "project": "default",
  "name": "custom_pipeline_01",
  "data_type": "unstructured_data",
  "index_type": "hnsw_hybrid",
  "index_config": {
    "embedding_dimension": 2048,
    "quant": "int8",
    "cpu_quota": 1,
    "fields": [
      {
        "field_name": "type",
        "field_type": "string",
        "default_val": "instruction"
      }
    ]
  },
  "preprocessing": {
    "chunking_strategy": "custom_balance",
    "chunk_length": 800,
    "merge_small_chunks": true,
    "multi_modal": ["image_ocr"]
  },
  "auto_sync_doc": true
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 78
Content-Type: application/json

{"code":0,"message":"success","request_id":"021695029537650fd001de666660000000000000000000230da93"}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 105
Content-Type: application/json

{
"code": 1000003,
"message": "invalid request: pipeline name cannot be 'default'",
"request_id": "021695029757920fd001de6666600000000000000000002569b8f"
}
```


