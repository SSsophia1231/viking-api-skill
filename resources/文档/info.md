# 概述
/api/knowledge/doc/info 接口用于查看知识库或某个[实验版本](https://www.volcengine.com/docs/84313/1510752)下的文档信息。
> 支持通过指定 pipeline_name 参数，来实现查看某个实验版本下的文档状态

# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口查看知识库下某个文档的信息。
# **请求接口**
| **URI** | /api/knowledge/doc/info | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档** [API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在 default 项目下查询。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| doc_id | string | 是 | -- | **要查询的文档 id** |
| return_token_usage | bool | 否 | false | **是否返回文档向量化和文档生成摘要所消耗的 tokens** |
| pipeline_name | string | 否 | -- | **实验版本名称** <br>  <br> * 不指定时，默认查询知识库主版本下的文档信息 <br> * 当指定时，查询特定实验版本内的文档信息 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | 文档信息 |
data 返回值
| 字段 | 子字段 | 字段类型 | 说明 |
| --- | --- | --- | --- |
| collection_name | -- | string | 知识库名称 |
| doc_name | -- | string | 文档名称 |
| doc_hash | -- | string | 文档内容的唯一 hash 值 |
| doc_id | -- | string | 文档唯一标识 |
| add_type | -- | string | 文档导入方式 |
| doc_type | -- | string | 文档类型 |
| create_time | -- | number | 文档创建时间，毫秒级时间戳 |
| added_by | -- | string | 文档上传人 |
| update_time | -- | number | 文档更新时间，毫秒级时间戳 |
| url | -- | string | 文档的 URL 地址 |
| meta | -- | string | 文档元信息，JSON 字符串格式 |
| point_num | -- | number | 文档切片数量 |
| status |  | object | 文档处理状态对象 |
|  | process_status | number | 文档处理状态 <br> 0：成功 <br> 1：失败 <br> 2：排队中 <br> 3：更新中 <br> 5：删除中 <br> 6：处理中 |
| doc_summary | -- | string | 文档全文摘要 |
| brief_summary | -- | string | 文档精简摘要 |
| title | -- | string | 文档或视频标题 |
| video_outline |  | object | 视频大纲信息（音视频知识库且 enable_smart_summary == true 时返回） |
|  | title | string | 视频全部智能大纲标题 |
|  | summary | string | 视频全部智能大纲内容 |
|  | chapters | array | 视频章节列表，单个元素结构如下： <br> ```JSON <br> { <br>   "title": "xxx", // 智能大纲标题 <br>   "content": "xxx", // 智能大纲内容 <br>   "start_time": 0, // 章节开始时间（毫秒） <br>   "end_time": 296000, // 章节结束时间（毫秒） <br>   "element_content": [ // 章节内的详细句子列表 <br>     "说话人1[00:00:23.72]：xxx", <br>     "说话人1[00:00:25.48]：xxx", <br>     ... <br>   ] <br> } <br> ``` <br>  |
| video_frame | -- | string | 视频帧 URL 地址 |
| audio_outline |  | object | 音频大纲信息（仅在音视频知识库且 enable_audio_smart_summary == true 时返回） |
|  | title | string | 音频全部智能大纲标题 |
|  | summary | string | 音频全部智能大纲内容 |
|  | chapters | array | 音频章节列表，单个元素结构如下： <br> ```JSON <br> { <br>   "title": "xxx", // 智能大纲标题 <br>   "content": "xxx", // 智能大纲内容 <br>   "start_time": 0, // 章节开始毫秒 <br>   "end_time": 296000, // 章节结束毫秒 <br>   "element_content": [ // 章节详细句子列表 <br>     "说话人1[00:00-00:28]：xxx" <br>     "说话人1[00:29-00:35]：xxx" <br>     ... <br>   ] <br> } <br> ``` <br>  |
| doc_size | -- | number | 文档大小（字节） |
| full_directory_path | -- | array | 文档所在目录路径 |
| is_wiki | -- | boolean | 是否为 wiki 类型文档 |
| statistics |  | object | 文档统计信息对象 |
|  | pages | number | 页数 |
|  | lines | number | 行数 |
|  | cells | number | 单元格数量 |
|  | chars | number | 提取文本字符数 |
|  | images | number | 图片数量 |
|  | tables | number | 表格数量 |
## failed_code 报错码：
| **failed_code** | **错误描述** | **处理建议** |
| --- | --- | --- |
| 10001 | 文档下载超时 | 请上传重试。如果问题仍然存在，请联系我们 |
| 10003 | URL 校验失败，请确认 URL 链接 | 请确认 URL 链接正确后重试。如果问题仍然存在，请联系我们 |
| 10005 | 飞书文档获取异常，请确认有效且已授权 | 请确认飞书文档权限，并通过飞书开放平台 OpenAPI [飞书开放平台](https://open.larkoffice.com/document/server-docs/docs/docs-overview)确认授权 |
| 30001 | 超过知识库文件限制大小 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 35001 | 超过知识库切片数量限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 35002 | FAQ 文档解析为空 | FAQ 文档解析结果为空，切片数为 0。请确保文档中包含有效数据 |
| 35004 | 超过知识库 FAQ 文档 sheet 数量限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 36003 | 结构化文档表头不匹配 | 结构化文档表头不匹配，请确保上传文档中每个 sheet 的表头与预定义的知识库表结构完全一致 |
| 36004 | 结构化文档数据类型转换失败 | 结构化文档数据类型转换失败，请确保上传文档中每个 sheet 的单元格的内容格式与预定义的知识库表结构数据类型完全一致 |
| 36005 | 超过知识库结构化文档 sheet 数量限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 36006 | 超过知识库结构化文档有效行数限制 | 超过知识库配额限制。[配额说明参考](https://www.volcengine.com/docs/84313/1339026) |
| 36007 | 结构化文档解析为空 | 结构化文档解析结果为空，切片数为 0。请确保文档中包含有效数据 |
| 36008 | embedding 的列组合长度超出限制 | 缩短待 embedding 原始文本长度 |
| 其他错误码 | 未知错误，请联系我们 | 未知错误，请联系我们 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection 不存在 |
| 1001001 | 400 | doc not exist | doc 不存在 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/doc/info \
  -d '{
    "collection_name": "test_collection_name",
    "project": "",
    "doc_id": "test123",
    "return_token_usage": true
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 1234
Content-Type: application/json
 
{
  "code": 0,
  "message": "success",
  "request_id": "021695029757920fd001de6666600000000000000000002569b8f",
  "data": {
    "collection_name": "video_collection",
    "doc_name": "会议视频.mp4",
    "doc_hash": "xxxxxxxxxxxxxxxx",
    "doc_id": "_sys_auto_gen_doc_id-xxxx",
    "add_type": "tos_fe",
    "doc_type": "mp4",
    "create_time": 1768804541257,
    "added_by": "user@example.com",
    "update_time": 1768804640273,
    "meta": "[]",
    "point_num": 11,
    "status": {
      "process_status": 0
    },
    "doc_summary": "",
    "brief_summary": "",
    "title": "项目交付与竞品分析会议",
    "video_outline": {
      "title": "项目交付与竞品分析会议大纲",
      "summary": "会议围绕项目进度、重点事项以及竞品分析方式展开。",
      "chapters": [
        {
          "title": "项目交付计划与重点事项",
          "content": "讨论项目时间节点与需要优先推进的关键事项。",
          "start_time": 0,
          "end_time": 76000,
          "element_content": [
            "说话人1: 讨论项目整体时间安排。[00:00:00]",
            "说话人1: 确认需要优先处理的事项。[00:00:09]",
            "说话人2: 补充相关技术方向建议。[00:00:19]"
          ]
        },
        {
          "title": "公司复盘与阶段总结",
          "content": "回顾阶段性成果，并讨论改进方向。",
          "start_time": 76000,
          "end_time": 169000,
          "element_content": [
            "说话人1: 提出阶段复盘的必要性。[00:01:23]",
            "说话人1: 讨论如何系统总结经验。[00:02:23]"
          ]
        },
        {
          "title": "分阶段竞品分析策略",
          "content": "明确不同阶段的竞品范围与分析重点。",
          "start_time": 169000,
          "end_time": 317000,
          "element_content": [
            "说话人2: 说明竞品需按阶段区分。[00:03:00]",
            "说话人1: 当前阶段聚焦核心竞品。[00:04:31]",
            "说话人2: 提出补充竞品条目的建议。[00:05:01]"
          ]
        }
      ],
      "video_frame": "USER_VIDEO/xxx/fragment_0_frame_1.jpg"
    },
    "video_frame": "xxx",
    "doc_size": 29964057,
    "full_directory_path": [],
    "is_wiki": false,
    "statistics": {
      "pages": 0,
      "lines": 0,
      "cells": 0,
      "chars": 6127,
      "images": 0,
      "tables": 0
    }
  }
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


