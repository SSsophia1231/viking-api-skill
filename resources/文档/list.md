# 概述
/api/knowledge/doc/list 接口用于查询知识库或某个[实验版本](https://www.volcengine.com/docs/84313/1510752)上文档的列表，默认按照文档上传时间倒序排列。
> 支持通过指定 pipeline_name 参数，来实现查询某个实验版本下的文档列表

# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现查询某个知识库下的所有文档信息的功能。
# **请求接口**
| **URI** | /api/knowledge/doc/list | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | 子参数 | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| collection_name | -- | string | 否 | -- | **知识库名称** |
| project | -- | string | 否 | default | **知识库所属项目，获取方式参见文档** [API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在 default 项目下查询。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| filter |  | json | 否 | -- | **过滤条件** <br> 用于对返回结果进行过滤，支持使用 doc_id 过滤 |
|  | doc_id_list | list | 否 | -- | **指定 doc_id 过滤条件** <br> 只返回列表中指定的文档信息 |
| offset | -- | int | 否 | 0 | **查询起始位置** <br> 表示从结果的第几个文档后开始取，需要大于等于 0 <br> 注：如果设置 offset ≥ 100，需同时传入 limit 参数才能生效 |
| limit | -- | int | 否 | -1 | **查询文档数** <br> -1 表示获取所有，最大值不超过 100，每次返回最多不超过 100 |
| doc_type | -- | list | 否 | -- | **文档类型筛选** |
| return_token_usage | -- | bool | 否 | false | **是否返回文档向量化和文档摘要生成所消耗的 tokens** |
| pipeline_name | -- | string | 否 | -- | **实验版本名称** <br>  <br> * 不指定时，默认查询知识库主版本下的文档列表 <br> * 指定时，查询特定实验版本内的文档列表 |
| detailed | -- | bool | 否 | false | **是否展示文档详细信息** <br> 详细信息：文档摘要 <br> 注：摘要相关字段返回内容较多，可能导致请求耗时较长，建议仅在需要时单独调用 doc/info 接口获取 |
**响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | * collection_name：知识库的名字 <br> * total_num：该知识库下的文档总数 <br> * count：本次查询返回的文档总数 <br> * doc_list：查询的文档信息列表，里面每一个元素代表一篇文档的信息，单篇文档信息格式参考[响应消息](/docs/84313/1254615#b10aaec1) |
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
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/doc/list \
  -d '{
    "collection_name": "test_collection_name",
    "project": "",
    "filter": {
            "doc_id_list": ["test0123", "test1111"]
        },
    "return_token_usage": true
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 43
Content-Type: application/json
 
{
    "code": 0,
    "data": {
        "collection_name": "test_collection_name",
        "total_num": 2,
        "count": 2,
        "doc_list":[
            {
                "collection_name": "test_collection_name",
                "doc_name" :"张某某盗窃案",
                "doc_id": "test0123",
                "add_type": "url",
                "doc_type": "pdf",
                "doc_summary": "这篇论文提出了基于注意力机制的 Transformer 模型,...", // 全文摘要
                "brief_summary": "这篇论文提出了基于注意力机制的 Transformer 模型,...", // 精简摘要
                "create_time": 1711367027,
                "added_by": "username",
                "update_time": 1711367030,
                "url": "https://fwh-my-test-bucket.tos-cn-beijing.volces.com/%E6%96%B0%E6%A9%99%E7%A7%91%E6%8A%80/%E5%91%A8%E6%9D%A8%E7%9B%97%E7%AA%83%E6%A1%88.pdf?X-Tos-Algorithm=TOS4-HMAC-SHA256\u0026X-Tos-Content-Sha256=UNSIGNED-PAYLOAD\u0026X-Tos-Credential=YOUR_ACCESS_KEY_ID%2F20240325%2Fcn-beijing%2Ftos%2Frequest\u0026X-Tos-Date=20240325T114024Z\u0026X-Tos-Expires=3600\u0026X-Tos-SignedHeaders=host\u0026X-Tos-Security-Token=nCgdqdEROend3.ChsKBzNzX056d3cSEGBgA9av-UtVs7ClfMkXS4oQk8WFsAYYo-GFsAYgle7V6QcoAjCSkLEJOhx6aGFpeXVqaWEuMDMyMkBieXRlZGFuY2UuY29tQgN0b3NSHHpoYWl5dWppYS4wMzIyQGJ5dGVkYW5jZS5jb21YBGAB.Nur_XCwZ_1LHmSsfeWGjDUn8SEOo3c6op5hx3lUgLZuxtHN_sqs-Kd0KbKw-51CT6wXKQo3AbmidScqVTu6gLQ\u0026X-Tos-Signature=5c3dff2f8cd67daae99476d54188033cc32932d87f1ff85f4f1afd5862fa35cd",
                "point_num": 53,
                "status":{
                    "process_status":0
                },
                "total_tokens":345390,
                "doc_summary_tokens": 120742,
                "doc_premium_status": {
                    "doc_summary_status_code": 0  // 摘要生成的状态码
                }
            },
            {
                "collection_name": "test_collection_name",
                "doc_name" :"测试文档",
                "doc_id": "test1111",
                "add_type": "url",
                "doc_type": "doc",
                "create_time": 1711367010,
                "added_by": "username",
                "update_time": 1711367010,
                "url": "https://fwh-my-test-bucket.tos-cn-beijing.volces.com/%E6%B3%95%E5%BE%8B%E8%A1%8C%E4%B8%9A/%E5%8F%B8%E6%B3%95%E8%A7%A3%E9%87%8A/%20%E6%9C%80%E9%AB%98%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2%E5%85%B3%E4%BA%8E%E5%AE%A1%E7%90%86%E6%9C%9F%E8%B4%A7%E7%BA%A0%E7%BA%B7%E6%A1%88%E4%BB%B6%E8%8B%A5%E5%B9%B2%E9%97%AE%E9%A2%98%E7%9A%84%E8%A7%84%E5%AE%9A%EF%BC%88%E4%BA%8C%EF%BC%89%20-%20%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E6%9C%80%E9%AB%98%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2%E5%85%AC%E6%8A%A5.docx?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Content-Sha256=UNSIGNED-PAYLOAD&X-Tos-Credential=YOUR_ACCESS_KEY_ID%2F20240325%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20240325T122115Z&X-Tos-Expires=3600&X-Tos-SignedHeaders=host&X-Tos-Security-Token=nCgdqdEROend3.ChsKBzNzX056d3cSEGBgA9av-UtVs7ClfMkXS4oQk8WFsAYYo-GFsAYgle7V6QcoAjCSkLEJOhx6aGFpeXVqaWEuMDMyMkBieXRlZGFuY2UuY29tQgN0b3NSHHpoYWl5dWppYS4wMzIyQGJ5dGVkYW5jZS5jb21YBGAB.Nur_XCwZ_1LHmSsfeWGjDUn8SEOo3c6op5hx3lUgLZuxtHN_sqs-Kd0KbKw-51CT6wXKQo3AbmidScqVTu6gLQ&X-Tos-Signature=08f26c395dfccb934f990fbc7acdb23eecc2b7441abaa74305f4e67433cdfeec",
                "point_num": 100,
                "status":{
                    "process_status":0
                },
                "total_tokens":345390
            }
        ]
    },
    "message": "success",
    "request_id": "02171136497331800000000000000000000ffff0a00601688694f"
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


