api/knowledge/pipeline/list：查看一个知识库下的所有[实验版本](https://www.volcengine.com/docs/84313/1510752)列表
# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现查看一个知识库下所有实验版本信息的功能
# **请求接口**
| **URI** | api/knowledge/pipeline/list | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对知识库服务端请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: token=********** | 鉴权 |
# **请求参数**
| 参数 | 类型 | 必选 | 默认值 | 备注 |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | *  | **知识库名称** |
| project | string | 否 | default | **项目名** |
| resource_id | string | 否 | *  | **知识库唯一 ID** <br>  <br> * 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| data | // 返回 pipeline 的配置信息 <br> { <br> collection_name: 知识库名称 <br> pipeline_list: <br> [ { // 和 pipeline info 返回的内容一致 <br> }, <br> ] <br> } |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 403 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request: %s | 非法参数 <br>  <br> * 缺失必选参数 <br> * collection_name 命名不符合规范 <br> * 字段类型与相关字段属性不满足约束条件 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
-H 'Content-Type: application/json' \
-H 'Authorization: token=****' \
https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/pipeline/list \
-d '{
"collection_name": "test_collection_name",
"project": "default"
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 1024
Content-Type: application/json

{
  "code": 0,
  "message": "success",
  "request_id": "021695029537650fd001de666660000000000000000000230da93",
  "data": {
    "collection_name": "test_collection_name",
    "pipeline_list": [
      {
        "pipeline_name": "default",
        "data_type": "unstructured_data",
        "index": {
          "vector_index": {
            "dimension": 1536,
            "metric": "cosine"
          }
        },
        "preprocessing": {
          "chunk_strategy": {
            "chunk_type": "fixed_size",
            "chunk_size": 800,
            "chunk_overlap": 400
          }
        },
        "auto_sync_doc": true,
        "create_time": "2024-11-01T10:30:00Z",
        "update_time": "2024-11-01T10:31:00Z"
      },
      {
        "pipeline_name": "custom_pipeline_01",
        "data_type": "unstructured_data",
        "index": {
          "vector_index": {
            "dimension": 1536,
            "metric": "cosine"
          }
        },
        "preprocessing": {
          "chunk_strategy": {
            "chunk_type": "fixed_size",
            "chunk_size": 1000,
            "chunk_overlap": 200
          }
        },
        "auto_sync_doc": false,
        "create_time": "2024-12-01T15:20:00Z",
        "update_time": "2024-12-01T15:21:00Z"
      }
    ]
  }
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 95
Content-Type: application/json

{
"code": 1000003,
"message": "invalid request: collection not found",
"request_id": "021695029757920fd001de6666600000000000000000002569b8f"
}
```


