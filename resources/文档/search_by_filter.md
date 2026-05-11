# 概述
/api/knowledge/doc/v2/search_by_filter 接口用于通过标签过滤检索文档
> 支持通过指定 pipeline_name 参数，来实现通过标签过滤某个实验版本下的文档
> 适用于文档级别的标量标签，不适用于结构化知识库中的表结构标量字段

# **前提条件**
完成"签名鉴权方式"页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现从知识库删除文档的功能。
# **请求接口**
| **URI** | /api/knowledge/doc/v2/search_by_filter | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | 子参数 | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| collection_name | -- | string | 否 | -- | **知识库名称** |
| project | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 默认为 default 项目，若需要操作指定项目下的知识库，需正确配置该字段 |
| resource_id | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| filter | -- | json | 是 | -- | **标签过滤条件** <br> 支持对 int64，string，list<int64>，list<string>，float32，bool，data_time 和 geo_point 类型的标签进行条件筛选，使用方式见[filter表达式](https://www.volcengine.com/docs/84313/1419289#filter-%E8%A1%A8%E8%BE%BE%E5%BC%8F) |
| limit | -- | int | 否 | -1 | **返回的文档数量** <br> 默认值为 -1，表示返回 100 条文档；若实际文档数量不足 100，则按实际数量返回；单次返回文档数最大为 5000 |
| pipeline_name | -- | string | 否 | -- | **实验版本名称** <br> 用于根据标签过滤实验版本下的文档列表 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | * collection_name：知识库的名字 <br> * total_num：该知识库下的文档总数 <br> * count：本次查询返回的文档总数 <br> * doc_list：查询的文档信息列表，里面每一个元素代表一篇文档的信息，单篇文档信息格式参考[响应消息](https://www.volcengine.com/docs/84313/1254615?lang=zh#%E5%93%8D%E5%BA%94%E6%B6%88%E6%81%AF) |
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
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/doc/v2/search_by_filter \
  -d '{
    "collection_name": "Tag_test",
    "project": "default",
    "filter": {
      "op": "must",
      "field": "subject",
      "conds": ["数学"]
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
  "code": 0,
  "message": "success",
  "request_id": "021775046751409fd00ffffffff002a0000000000001695",
  "data": {
    "collection_name": "Tag_test",
    "total_num": 3,
    "count": 3,
    "doc_list": [
      {
        "collection_name": "Tag_test",
        "doc_id": "test_1",
        "doc_name": "test_1",
        "doc_hash": "16071591840965547236",
        "add_type": "url",
        "doc_type": "mp4",
        "doc_size": 21145830,
        "added_by": "user_001",
        "create_time": 1772623580,
        "update_time": 1772623826,
        "title": "小学数学五年级下册知识点总结",
        "url": "https://example-bucket.tos-cn-beijing.volces.com/videos/test_1.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Expires=3600&X-Tos-Signature=xxxxxx",
        "video_frame": "https://example-bucket.tos-cn-beijing.volces.com/frames/test_1/frame_1.jpg?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Expires=600&X-Tos-Signature=xxxxxx",
        "point_num": 9,
        "is_wiki": false,
        "full_directory_path": [],
        "doc_summary": "",
        "brief_summary": "",
        "status": {
          "process_status": 0
        },
        "meta": "[{\"field_name\":\"subject\",\"field_type\":\"string\",\"field_value\":\"数学\"}]",
        "video_outline": {
          "title": "小学数学五年级下册知识点总结",
          "summary": "李老师对五年级下册8个章节的知识点进行系统回顾。",
          "chapters": [
            {
              "title": "课程开场与整体介绍",
              "content": "李老师自我介绍，说明本次对五年级下册8个章节进行回顾总结。",
              "start_time": 0,
              "end_time": 18630,
              "element_content": [
                "知画教育李老师[00:00-00:59]：今天我们对小学数学五年级下册的知识点进行回顾总结。",
                "..."
              ]
            },
            "..."
          ]
        },
        "statistics": {
          "pages": 0,
          "lines": 0,
          "cells": 0,
          "chars": 6522,
          "images": 0,
          "tables": 0
        }
      },
      "..."
    ]
  }
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Type: application/json

{"code":1000003,"message":"One or more parameters specified in the request are not valid. check doc_filter failed, err:field[subject] not in collection config","request_id":"021775046886297fd00ffffffff002a000000000000169596698e"}
```

