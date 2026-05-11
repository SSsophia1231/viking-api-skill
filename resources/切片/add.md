# **概述**
/api/knowledge/point/add 接口用于新增一个知识库或某个[实验版本](https://www.volcengine.com/docs/84313/1510752)下文档的一个切片。
> 通过指定 pipeline_name 实现在知识库下的指定实验版本内新增切片

# **前置条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现新增一个知识库下某个文档的一个切片的功能。
# **请求接口**
| **URI** | /api/knowledge/point/add | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对知识库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **类型** | **必选** | **默认值** | **备注** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在 default 项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库唯一 id** <br>  <br> * 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| doc_id | string | 是 | -- | **表示新增切片所属的文档** <br>  <br> * 不存在时会报错。 |
| chunk_type | string | 是 | -- | **要添加的切片类型** <br>  <br> * 和知识库支持的类型不匹配时会报错 <br> * 结构化知识库：“structured”， <br> * 非结构化知识库： <br>    * “text”： 纯文本切片 <br>    * “faq”： faq 类型切片 |
| content | string |  | -- | **新增切片文本内容** <br> 当 chunk_type 为 text、faq 时必传 <br> 1、text：content 对应切片原文内容 <br> 2、faq：content 对应**答案字段**内容 |
| chunk_title | string | 否 | -- | **切片标题** <br> 只有非结构化文档支持修改切片的标题。 |
| question | string | 否 | -- | **新增 faq 切片中的问题字段** <br> 当 chunk_type 为 faq 时必传 <br>  <br> * 字段长度范围为 [1，{Embedding模型支持的最大长度}] |
| fields | list | 否 | -- | **表示传入的结构化数据** <br> 当 chunk_type 为 structured 时必传。 <br> [ <br> { "field_name": "xxx" // 字段名称 <br> "field_value": xxxx // 字段值 <br> }, <br> ] <br>  <br> * field_name 必须已在所属知识库的表字段里配置，否则会报错 <br> * 和文档导入时的向量字段长度校验保持一致，拼接后的做 embedding 的文本长度不超过 65535 |
| pipeline_name | string | 否 | -- | **实验版本名称** <br>  <br> * 指定当前参数可向具体实验版本下新增切片 <br> * 不指定默认向知识库主版本下新增切片 |
# **响应消息**
| **字段** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | { <br> "collection_name": 知识库的名字， <br> "resource_id": 知识库唯一标识， <br> "project": 项目名， <br> "doc_id": 文档id， <br> "chunk_id": 整型，切片在文档下的 id，文档下唯一， <br> "point_id": 切片 id，知识库下唯一 <br> } |
# **完整示例**
## 请求消息
```bash
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/point/add \
  -d '{
    "resource_id": "kb_XXX",
    "doc_id": "_sys_XXXX",
    "chunk_type": "text",
    "content": "test content"
}'
```

## 响应消息
执行成功返回：
```JSON
HTTP/1.1 200 OK 
Content-Length: 43 
Content-Type: application/json 
  
{
    "code": 0,
    "data": {
        "collection_name": "lzm_test2",
        "project": "default",
        "resource_id": "kb-a638e4045e9708f0",
        "doc_id": "_sys_auto_gen_doc_id-9744689384778553745",
        "chunk_id": 7,
        "point_id": "_sys_auto_gen_doc_id-9744689384778553745-7"
    },
    "message": "success",
    "request_id": "02173431739184000000000000000000000ffff0a0078dc15a2fe"
}
```

执行失败返回：
```Plain
HTTP/1.1 400 Bad Request 
Content-Length: 43 
Content-Type: application/json 
  
{"code":1000003, "message":"invalid request: %s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"} 
```


