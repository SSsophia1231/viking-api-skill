本节将说明如何查询某个账户下的所有知识库信息。
# 概述
/api/knowledge/collection/list 接口用于查询某个账户下的所有知识库信息，默认按照知识库的创建时间从晚到早排序。
# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现查看知识库列表的功能。
# **请求接口**
| **URI** | /api/knowledge/collection/list | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对知识库服务请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数（旗舰版、标准版通用）**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| project | string | 否 | -- | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定，则返回所有项目下的知识库 <br> 若需要操作指定项目下的知识库，则需正确配置该字段。 <br>  |
| brief | bool | 否 | false | **是否查询和返回索引状态** <br> false 代表查询和返回索引状态 <br> true 代表不查询和返回索引状态 |

# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | * total_num : 列表里的知识库总数 <br> * collection_list : 知识库详细信息列表，数组型，每个元素是一个知识库的详细信息，具体参数形式见[info](/docs/84313/1254602) <br> * collection_name：知识库名称 <br> * version：知识库版本，标准版值为 2；旗舰版值为 4 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection 不存在 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/collection/list \
  -d '{
    "project": "abc",
    "brief": false
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
        "total_num": 200,
        "collection_list": [
            {
                "collection_name": "apiexample",
                "description": "test",
                "create_time": 1724747158,
                "update_time": 1724747158,
                "creator": "xxx",
                "pipeline_list": [
                    {
                        "pipeline_type": "user_define",
                        "pipeline_stat": {
                            "doc_num": 0,
                            "finish_doc_num": 0,
                            "point_num": 0,
                            "success_doc_num": 0
                        },
                        "index_list": [
                            {
                                "index_type": "hnsw_hybrid",
                                "index_config": {
                                    "vector_field": {
                                        "field_name": "_sys_auto_content_vector",
                                        "field_type": "vector",
                                        "dim": 2048
                                    },
                                    "sparse_vector_field": {
                                        "field_name": "_sys_auto_content_sparse_vector",
                                        "field_type": "sparse_vector"
                                    },
                                    "cpu_quota": 1,
                                    "distance": "ip",
                                    "quant": "int8",
                                    "embedding_model": "doubao-embedding-and-m3",
                                    "embedding_dimension": 2048,
                                    "need_instruction": true,
                                    "fields": [
                                        {
                                            "field_name": "_sys_auto_id",
                                            "field_type": "string"
                                        },
                                        {
                                            "field_name": "_sys_auto_doc_id",
                                            "field_type": "string"
                                        },
                                        {
                                            "field_name": "_sys_auto_chunk_id",
                                            "field_type": "int64"
                                        },
                                        {
                                            "field_name": "_sys_auto_doc_type",
                                            "field_type": "string"
                                        },
                                        {
                                            "field_name": "_sys_auto_add_type",
                                            "field_type": "string"
                                        }
                                    ]
                                },
                                "primary_key": "",
                                "status": -1
                            }
                        ],
                        "preprocessing_list": [
                            {
                                "chunking_strategy": "default",
                                "chunking_identifier": null,
                                "chunk_length": 2000
                            }
                        ],
                        "table_config_list": [
                            {
                                "table_type": "row",
                                "table_pos": 1,
                                "start_pos": 2,
                                "table_fields": [
                                    {
                                        "field_name": "讲解模块",
                                        "field_type": "string",
                                        "if_embedding": true,
                                        "if_filter": false
                                    },
                                    {
                                        "field_name": "子模块",
                                        "field_type": "string",
                                        "if_embedding": true,
                                        "if_filter": false
                                    },
                                    {
                                        "field_name": "问题示例",
                                        "field_type": "string",
                                        "if_embedding": true,
                                        "if_filter": false
                                    },
                                    {
                                        "field_name": "记忆化 ————讲解要点",
                                        "field_type": "string",
                                        "if_embedding": true,
                                        "if_filter": false
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "data_type": "structured_data",
                "resource_id": "kb-be6833502748aaef",
                "project": "default"
            }
        ]
    },
    "message": "success",
    "request_id": "02172474869381600000000000000000000ffff0a005049697e42"
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


