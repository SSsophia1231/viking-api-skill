# 概述
/api/knowledge/doc/v2/add 接口用于向已创建的知识库添加文档。
* 文档类型限制参考 [支持的文档类型及规格](/docs/84313/1339026#685f54dd)
* doc/v2/add 接口的改进
   * 精简接口参数，提升易用性
   * 统一使用 `uri` 参数指定文档来源（支持 URL 或 TOS 路径）
   * 支持在通过 TOS 导入文件时设置标签信息
   * 采用统一的内容去重规则，检测到重复文档时将报错

# **前提条件**
完成《签名鉴权方式》页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现导入文档到知识库功能。
# **请求接口**
| **URI** | /api/knowledge/doc/v2/add | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **类型** | **是否必传** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | 知识库名称 |
| project | string | 否 | default | 知识库所属项目，获取方式参考文档 [API 接入与技术支持](https://www.volcengine.com/docs/84313/1606319?lang=zh#1ab381b9) <br> 若需要操作指定项目下的知识库，需正确配置该字段 <br>  |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| doc_id | string | 是 | -- | **知识库下的文档唯一标识** <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母或下划线开头，不能为空 <br> * 长度要求：[1, 128] |
| doc_name | string | 否 | -- | **文档名称** <br>  <br> * 对于 tos 导入的方式，未传入时直接使用 tos path 下面的文档名 <br> * 对于 url 导入的方式，先通过 url 提取带后缀的文档名，如果没有则返回错误码 400，要求用户再传 doc_name <br>  <br> 格式要求： <br>  <br> * 不能包含有特殊用途的字符(< > : " / \ <br> * 长度要求：[1, 255] |
| doc_type | string | 否 | -- | **上传文档的类型** <br>  <br> * 非结构化文档支持类型：txt, doc, docx, pdf, markdown, pptx, ppt, jpeg, png, webp, bmp, mp4, mp3, wav, aac, flac, ogg <br>    * .jpg 和 .jpeg 文件 doc_type 均为 jpeg <br>    * .markdown 和 .md 文件 doc_type 均为 markdown <br> * 结构化文档支持类型：xlsx, csv, jsonl <br>  <br> 优先使用传入的值；若未传入，将尝试自动提取；若自动提取失败，则接口返回错误 <br>  |
| description | string | 否 | -- | **文档描述** <br> 描述会参与对图片的检索，如电商场景下，描述可以用于存放图片对应的详细商品说明，售卖亮点，价格等 <br> 注： <br>  <br> * 暂**只在** doc_type 为**图片类型文档时支持**，其他类型文档设置无效。 <br> * 长度 [0, 4000] |
| tag_list | list | 否 | -- | Tag 为结构体，包含 <br>  <br> * field_name：标签名，类型为string <br>    * 不能为 "doc_id" <br>    * 需对齐创建知识库时的 field_name <br>       * 在创建知识库时先初始化标签索引，再在上传文档时打标，以用于检索时实现标签过滤能力 <br>       * 若需新增过滤标签，请先编辑知识库新增标签后，再进行文档打标 <br> * field_type：标签类型 <br>    * 支持 "int64"，"float32"，"string"，"bool"，"list"，"list" ，"date_time"，"geo_point" 类型 <br>    * 需对齐创建知识库时的 field_type <br> * field_value：标签值 <br>    * 与 field_type 指定类型一致 |
| uri | string | 是 | -- | 待上传的文件 uri 链接，示例： <br>  <br> * http://a/b/c.pdf <br> * tos://a/b/c.pdf |
# **响应消息**
| **参数** | **参数说明** | **备注** |
| --- | --- | --- |
| code | 状态码 |  |
| message | 返回信息 |  |
| request_id | 标识每个请求的唯一标识符 |  |
| data | { <br> "collection_name": 知识库的名字， <br> "resource_id": 知识库唯一标识， <br> "project": 项目名， <br> "doc_id": 文档唯一标识 <br> } |  |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection 不存在 |
| 1001002 | 400 | invalid request: doc_id:xxx is duplicated with doc_ids:xxx | 文档内容与现有文档重复 |
| 1001010 | 400 | doc num is exceed 3000000 | doc 数量已达限额，点击详情查看[知识库配额限制](https://www.volcengine.com/docs/84313/1339026) |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/doc/v2/add \
  -d '{
    "collection_name": "test_collection_name",
    "project": "default",
    "doc_id": "test0123",
    "doc_name": "test.mp4",
    "uri": "xxx",
    "tag_list": [
        {"field_name":"行业","field_type":"string", "field_value":"企业服务"},
        {"field_name":"是否公开","field_type":"bool", "field_value":true}
        ]
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 43
Content-Type: application/json
 
{
    "code":0,
    "message":"success",
    "request_id":"021695029537650fd001de666660000000000000000000230da93",
    "data":{
        "collection_name": "video_collection",
        "resource_id": "kb-8349ef57441ab57",
        "project": "default",
        "doc_id": "test0123"
        }
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request: %s", 
"request_id": "021695029757920fd001de666660000000000000000002569b8f"}
```


