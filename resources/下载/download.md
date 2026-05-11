# 概述
/api/knowledge/task/download 接口用于创建一个新的视频下载任务
> 通过指定 pipeline_name 实现在知识库下的指定实验版本内创建一个新的视频下载任务

# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现创建一个新的视频下载任务。
# **请求接口**
| **URI** | /api/knowledge/task/download | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| doc_id | string | 是 | **要下载的视频文件 id** |
| collection_name | string | 否 | **知识库名称** |
| resource_id | string | 否 | 知识库唯一 id <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| project | string | 否 | 知识库所属项目，获取方式参见文档[API 接入与技术支持](https://www.volcengine.com/docs/84313/1606319#1ab381b9)。注意：若不指定该字段，则在 default 项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 |
| pipeline_name | string | 否 | **实验版本名称** <br>  <br> * 指定当前参数可查询具体实验版本下的切片信息 <br> * 不指定默认查询知识库主版本下的切片信息 |
# **响应消息**
| 字段 | 类型 | 子字段 | 子字段类型 | 描述 |
| --- | --- | --- | --- | --- |
| code | integer | -- | -- | 状态码 |
| message | string | -- | -- | 返回信息 |
| data | object | task_id | string | 任务ID |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection不存在 |
| 1001001 | 400 | doc not exist | doc不存在 |
| 1002001 | 400 | point not exist | point_id不存在 |
# 完整消息
## 请求消息
```bash
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/task/download \
  -d '{
    "doc_id": "xxx",
    "collection_name": "test_collection_name",
    "project": ""
}'
```

## 响应消息
执行成功返回：
```JSON
HTTP/1.1 200 OK 
Content-Length: 43 
Content-Type: application/json 
  
{"code":0,"data":{"task_id":"8154fd9998a346a0a417dd1b50cacb54"},"message":"success","request_id":"02176897682572100000000000000000000ffffac130a43c675fe"}
```

执行失败返回：
```JSON
HTTP/1.1 400 Bad Request 
Content-Length: 43 
Content-Type: application/json 
  
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"} 
```


