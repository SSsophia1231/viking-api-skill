# 概述
/api/knowledge/search_collection 接口支持根据知识库描述关键词检索知识库，支持模糊匹配。
# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现知识库信息查看的功能。
# **请求接口**
| **URI** | /api/knowledge/search_collection | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对知识库服务请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数（旗舰版、标准版通用）**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| project | string | 否 | -- | 不传时表示检索所有项目下的全部知识库 |
| query | string | 是 | -- | 要匹配的知识库描述关键词 <br> 长度限制 [1, 64) 个字符 |
# 返回结果
| 字段 | 备注 |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| data | 返回的详细信息 <br> { <br> "collection_list": [ { "collection_name": "xx" // 知识库的名字 <br> "project": "xxx" // 知识库所属项目 <br> "resource_id":"xxx" // 知识库id <br> "description":"xxx" // 知识库描述 <br> } <br> ] <br> } |

