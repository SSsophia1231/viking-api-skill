# 概述
api/knowledge/doc/re-process 接口用以将指定文档同步到一个[实验版本](https://www.volcengine.com/docs/84313/1510752)中。
# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现将指定文档同步到实验版本的功能。
# **请求接口**
| **URI** | /api/knowledge/doc/re-process | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: token=********** | 鉴权 |
# **请求参数**
| 参数 | 类型 | 必选 | 默认值 | 备注 |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在 default 项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识。 |
| pipeline_name | string | 是 | -- | **实验版本名称** |
| doc_id | string | 是 | -- | **要导入的文档 ID** |
| auto_skip | bool | 否 | false | **是否去重** <br> 开启后，会自动跳过实验版本内已存在的 doc_id |
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
| 1000003 | 400 | invalid request: %s | 非法参数 <br>  <br> * 缺失必选参数 <br> * collection 命名不符合规范 <br> * 字段类型与相关字段属性不满足约束条件 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
-H 'Content-Type: application/json' \
-H 'Authorization: token=****' \
https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/doc/re-process \
-d '{
"collection_name": "test_collection_name",
"project": "default",
"pipeline_name": "custom_pipeline",
"doc_id": "test_doc_123",
"auto_skip": true
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
Content-Length: 95
Content-Type: application/json

{
"code": 1000003,
"message": "invalid request: missing required parameter doc_id",
"request_id": "021695029757920fd001de6666600000000000000000002569b8f"
}
```


