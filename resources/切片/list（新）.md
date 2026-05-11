# 概述
/api/knowledge/point/v2/list 接口用于查看知识库或某个[实验版本](https://www.volcengine.com/docs/84313/1510752)下的切片列表，默认按 point_id 从小到大排序。
> 支持通过指定 pipeline_name 参数，来实现仅查询某个实验版本下的切片列表

* point/v2/list 接口的改进
   * 精简接口参数，提升易用性
   * 统一使用 `uri` 参数指定文档来源（支持 URL 或 TOS 路径）
   * 支持在通过 TOS 导入文件时设置标签信息
   * 采用统一的内容去重规则，检测到重复文档时将报错


# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现查看知识库下的切片列表的功能。
# **请求接口**
| **URI** |  | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对知识库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则默认在 default 项目下查询。 <br> 若需要查询指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| pipeline_name | string | 否 | -- | **实验版本名称** <br>  <br> * 指定当前参数可查询具体实验版本下的切片列表 <br> * 不指定默认查询知识库主版本下的切片列表 |
| limit | int | 否 | 100 | **每次返回切片数量** <br> 取值范围 [1, 100]，即单次请求最多返回 100 条切片数据 |
| next_token | string | 否 | -- | **翻页游标** <br> 当数据总量较大时，接口不会一次性返回所有数据，而是将数据拆分为若干批次，每次请求只返回其中一批。这种方式通常称为"分页"，每一批数据即为"一页" <br> next_token 是游标，用于标记当前的读取位置。每次请求返回的 next_token 指向下一批数据的起始位置，传入后即可获取接下来的数据，以此实现连续翻页 <br>  <br> * **首次请求：** 不传 next_token，从第一条数据开始返回 <br> * **获取后续数据：** next_token 由接口自动生成，无需解析或构造，直接将返回值传入下次请求即可，接口将从上次结束处继续返回 <br> * **数据读取完毕：** 当响应中 next_token 为空时，表示所有数据已返回完毕 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | * collection_name：知识库的名字 <br> * count：本次查询返回的文档总数 <br> * point_list：查询的切片信息列表，里面每一个元素代表一个切片的信息，单个切片的信息格式参考[响应消息](https://www.volcengine.com/docs/84313/1386606?lang=zh#%E5%93%8D%E5%BA%94%E6%B6%88%E6%81%AF) |
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
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/point/v2/list \
  -d '{
    "collection_name": "test_collection_name",
    "limit": 1,
    "next_token": "eyJtb2RlIjoicG9pbnRfaWQiLCJwb2ludF9pZCI6Il9zeGFya19kb2NfaWQtNDk5MDMwOTAyMjE2MjIzNjM5NC0wIn0"
}'
```

## 响应消息
执行成功返回：
```Shell
{
    "code": 0,
    "data": {
        "collection_name": "api0828",
        "count": 1,
        "point_list": [
            {
                "collection_name": "api0828",
                "point_id": "_sys_auto_gen_doc_id-17691607628519396693-0",
                "process_time": 1724848725,
                "content": "讲解模块:讲解模块：xxxxxx\n子模块:子模块：xxxxx\n问题示例:问题示例：xxxxxx\n记忆化 —— 讲解要点:\n□ 要点1\n□ 要点2\n□ 要点3",
                "chunk_id": 0,
                "doc_info": {
                    "doc_id": "_sys_auto_gen_doc_id-17691607628519396693",
                    "doc_name": "演示表格.xlsx",
                    "create_time": 1724848720,
                    "doc_type": "xlsx",
                    "source": "tos_fe"
                },
                "chunk_type": "structured",
                "table_chunk_fields": [
                    {
                        "field_name": "讲解模块",
                        "field_value": "讲解模块：xxxxxx"
                    },
                    {
                        "field_name": "子模块",
                        "field_value": "子模块：xxxxx"
                    },
                    {
                        "field_name": "问题示例",
                        "field_value": "问题示例：xxxxxx"
                    },
                    {
                        "field_name": "记忆化 —— 讲解要点",
                        "field_value": "要点1\n 要点2\n 要点3"
                    }
                ]
            }
        ],
        "has_more": true,
        "next_token": "eyJtb2RlIjoicG9pbnRfaWQiLCJwb2ludF9pZCI6Il9zeXNfYXV0b19nZW5fbGFya19kb2NfaWQtNDk5MDMwOTAyMjE2MjIzNjM5NC0wIn0"
    },
    "message": "success",
    "request_id": "02172484891424400000000000000000000ffff0a00705414b331"
}
```

执行失败返回：
```Shell
HTTP/1.1 400 OK
Content-Length: 43
Content-Type: application/json

{"code": 1000003, "message": "One or more parameters specified in the request are not valid. req parse to json failed","request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


