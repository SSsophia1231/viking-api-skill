api/knowledge/pipeline/info 接口用以查看某个具体知识库的[实验版本](https://www.volcengine.com/docs/84313/1510752)信息。
# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名计算后，可调用 API 接口实现查看知识库下某个实验版本信息的功能。
# **请求接口**
| **URI** | api/knowledge/pipeline/info | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: token=********** | 鉴权 |
# **请求参数**
| 参数 | 类型 | 必选 | 默认值 | 备注 |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | *  | **知识库名称** |
| project | string | 否 | default | **项目名** |
| resource_id | string | 否 | *  | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| name | string | 是 | *  | **实验版本名称** <br>  <br> * 不能使用系统默认值“default” <br> * 实验版本由字母、数字、下划线组成，且只能以字母开头 <br> * 长度不超过 32 个字符 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| data | 返回 pipeline 的配置信息 <br> { <br> collection_name: 当前 pipeline 所属知识库名称 <br> pipeline_info: pipeline 的完整配置信息（包含解析策略、索引配置、存储等） <br> pipeline_name：当前返回信息对应的实验版本名称 <br> auto_sync_doc：表示该 pipeline 是否自动同步新导入的文档 <br> } |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 403 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 <br>  <br> * 缺失必选参数 <br> * collection 命名不符合规范 <br> * 字段类型与相关字段属性不满足约束条件 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
-H 'Content-Type: application/json' \
-H 'Authorization: token=****' \
https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/pipeline/info \
-d '{
"collection_name": "test_collection_name",
"project": "default",
"name": "custom_pipeline_01"
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 486
Content-Type: application/json

{
  "code": 0,
  "message": "success",
  "request_id": "021695029537650fd001de666660000000000000000000230da93",
  "data": {
    "collection_name": "test_collection_name",
    "pipeline_info": {
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
          "chunk_size": 800,
          "chunk_overlap": 400
        }
      },
      "auto_sync_doc": true,
      "create_time": "2024-12-01T10:30:00Z",
      "update_time": "2024-12-01T10:30:00Z"
    }
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
"message": "invalid request: pipeline not found",
"request_id": "021695029757920fd001de6666600000000000000000002569b8f"
}
```


