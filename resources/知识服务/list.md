本节将说明如何查询某个知识库下的知识服务信息。
# 概述
/api/knowledge/service/list 接口用于查询某个知识库下的知识服务信息。
# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现查看知识服务列表的功能。
# **请求接口**
| **URI** | /api/knowledge/service/list | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对知识库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数（旗舰版、标准版通用）**
| **参数** | 子参数 | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| filter |  | json | 是 | -- | **过滤条件** |
|  | collection_resource_ids | list | 是 | -- | 知识库 ID 列表，目前仅支持一个 |
|  | service_type | int | 否 | 2 | **知识服务类型** <br> 1 代表检索服务 <br> 2 代表问答服务 |
| page_number |  | int | 否 | 1 | 页数 |
| page_size |  | int | 否 | 100 | 每页条数 |

# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | * total_count : 返回的知识服务个数 <br> * page_size：每页条数 <br> * page_number：页数 <br> * knowledge_services <br>    * name：知识服务名称 <br>    * description：知识服务描述 <br>    * service_type：知识服务类型 <br>    * service_resource_id：知识服务 id |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection不存在 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/service/list \
  -d '{
    "filter":{
        "collection_resource_ids": ["kb_xxx"],
        "service_type": 2
    }
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 43
Content-Type: application/json
 
{
    "request_id": "0217734150**********4692d",
    "message": "success",
    "code": 0,
    "data": {
        "total_count": 2,
        "page_size": 100,
        "page_number": 1,
        "knowledge_services": [
            {
                "name": "test01",
                "description": "",
                "service_type": 2,
                "service_resource_id": "kb-service-**********c78e"
            },
            {
                "name": "test02",
                "description": "",
                "service_type": 2,
                "service_resource_id": "kb-service-**********cbcb"
            }
        ]
    }
}
```

执行失败返回：
```Shell
HTTP/1.1 400 OK
Content-Length: 43
Content-Type: application/json
 
{"code":1000005, "message":"collection not exist , please check your parameter", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


