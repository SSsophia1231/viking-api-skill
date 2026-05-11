# 概述
/api/knowledge/doc/update_meta 接口用于更新知识库或某个[实验版本](https://www.volcengine.com/docs/84313/1510752)上文档信息，文档 meta 信息更新会自动触发索引中的数据更新。
> 支持通过指定 pipeline_name 参数，来实现编辑某个实验版本下的文档 meta 信息。

# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现更新文档信息的功能。
# **请求接口**
| **URI** | /api/knowledge/doc/update_meta | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对知识库服务端请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| collection_name | -- | string | 否 | -- | **知识库名称** |
| project | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| doc_id | -- | string | 是 | -- | **待更新文档的 id** |
| meta |  | array 或 array 对应的 JSON 字符串 | 否 | -- | **meta 信息** |
|  | field_name | string | 否 | -- | **要更新的字段名** |
|  | field_type | string | 否 | -- | **要更新的字段类型** <br>  <br> * 仅当新增知识库未配置过的标签字段时生效，且新增字段不能用于标量过滤，仅可作为当前文档的描述信息存储 <br> * 支持 "int64"，"float32"，"string"，"bool"，"list<string>" 类型，限制参考[VikingDB的field_type规则和说明](https://www.volcengine.com/docs/84313/1254542#field-type-%E5%8F%AF%E9%80%89%E5%80%BC) |
|  | field_value | 与 field_type 指定类型一致 | 否 | -- | **要更新的字段值** <br> 字段值需保证类型符合字段定义，如 "int64"，"float32"，"string" 等 |
| pipeline_name | -- | string | 否 | -- | **实验版本名称** <br>  <br> * 不指定时，默认更新知识库主版本下的文档信息 <br> * 当指定时，更新特定实验版本内的文档信息 |
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
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/doc/update_meta \
  -d '{
    "collection_name": "test_collection_name",
    "project": "",
    "doc_id": "test123",
    "meta": [
      {"field_name": "行业", "field_type": "string", "field_value": "企业服务"},
      {"field_name": "是否公开", "field_type": "bool", "field_value": true}
    ]
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
HTTP/1.1 400 OK
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


