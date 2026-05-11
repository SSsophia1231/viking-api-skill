# 概述
/api/knowledge/doc/delete 接口用于删除知识库或某个[实验版本](https://www.volcengine.com/docs/84313/1510752)下的文档。
> 支持通过指定 pipeline_name 参数，来实现仅删除某个实验版本下的文档

# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现从知识库删除文档的功能。
# **请求接口**
| **URI** | /api/knowledge/doc/delete | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在 default 项目下操作。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| doc_id | string | 是 | -- | **要删除的文档 id** |
| pipeline_name | string | 否 | -- | **实验版本名称** <br>  <br> * 不指定时，默认会删除当前知识库及所有关联实验版本下的文档 <br> * 指定时，仅删除该实验版本下的文档，不影响知识库及其他版本 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection 不存在 |
| 1001001 | 400 | doc not exist | doc 不存在 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/doc/delete  \
  -d '{
    "collection_name": "test_collection_name",
    "project": "",
    "doc_id": "test123"
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 43
Content-Type: application/json
 
{"code":0,"message":"success","request_id":"021695029537650fd001de666660000000000000000000230da93"}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


