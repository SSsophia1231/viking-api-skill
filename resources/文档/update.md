# 概述
/api/knowledge/doc/update 接口用于更新某个文档信息，如文档标题等。文档信息更新会自动触发索引中的数据更新。
# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现更新文档信息的功能。
# **请求接口**
| **URI** | /api/knowledge/doc/update | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| collection_name | -- | string | 否 | -- | **知识库名称** |
| project | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| doc_id | -- | string | 是 | -- | **待更新文档的 id** |
| doc_name | -- | string | 是 | -- | **更新后的文档名称** |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | ```JSON <br> { <br> "doc_id": "1234567890", <br> "doc_name": "更新后的文档名称.docx", // 其他更新后的文档相关信息 <br> } <br> ``` <br>  |
## **状态码说明**
| **状态码** | **http 状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection 不存在 |
| 1001001 | 400 | doc not exist | doc 不存在 |
| 1000028 | 500 | internal error | 内部错误 |
# 完整示例
```JSON
{
    "message": "success",
    "code": 0,
    "request_id": "abc1234567890",
    "data": {
        "doc_id": "1234567890",
        "doc_name": "更新后的文档名称.docx" // 其他更新后的文档相关信息
    }
}
```


