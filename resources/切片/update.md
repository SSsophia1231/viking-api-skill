# **概述**
/api/knowledge/point/update 接口用于更新知识库或某个[实验版本](https://www.volcengine.com/docs/84313/1510752)下的切片内容。
> 支持通过指定 pipeline_name 参数，来实现仅更新某个实验版本下的切片内容

# **前置条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现更新知识库下的切片内容的功能。
# **请求接口**
| URI | /api/knowledge/point/update | 统一资源标识符 |
| --- | --- | --- |
| 请求方法 | POST | 客户端向服务器请求的操作类型 |
| 请求头 | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| 参数 | 类型 | 必选 | 默认值 | 备注 |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| point_id | string | 是 | -- | **要更新的切片 id** |
| chunk_title | string | 否 | -- | **切片标题** <br> 只有非结构化文档支持修改切片的标题。 |
| content | string | 二者只传一个 | -- | **要更新的非结构化文档的切片内容** <br>  <br> * 1、非结构化文件：content 对应切片原文内容 <br> * 2、faq 文件：content 对应答案字段内容 <br> * 3、结构化文件：content 对应参与索引的字段和取值，以 K:V 对拼接，使用 \n 区隔 |
| fields | list |  | -- | **要更新的结构化文档的切片内容** <br> 一行数据全量更新 <br> [ <br> { "field_name": "xxx", // 字段名称 <br> "field_value": "xxxx" // 字段值 <br> }, <br> ] <br> field_name 必须已在所属知识库的表字段里配置，否则会报错 |
| question | string | 否 | -- | **要更新的非结构化 faq 文档切片的问题字段** |
| pipeline_name | string | 否 | -- | **实验版本名称** <br>  <br> * 指定当前参数可更新具体实验版本下的切片 <br> * 不指定默认更新知识库主版本下的切片 |
# **响应消息**
| 字段 | 备注 |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
## **状态码说明**
| code | message | 备注 | http status_code |
| --- | --- | --- | --- |
| 0 | success | 成功 | 200 |
| 1000001 | unauthorized | 缺乏鉴权信息 | 401 |
| 1000002 | no permission | 权限不足 | 403 |
| 1000003 | invalid request：%s | 非法参数 | 400 |
| 1000005 | collection not exist | collection不存在 | 400 |
# **完整示例**
## 请求消息
```bash
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/point/update \
  -d '{
    "resource_id": "kb_xxxxx",
    "point_id": "_sys_xxxx",
    "content": "test content"
}'
```

## 响应消息
执行成功返回：
```text
HTTP/1.1 200 OK
Content-Length: 43
Content-Type: application/json

{"code":0,"message":"success","request_id":"021695029537650fd001de666660000000000000000000230da93"}
```

执行失败返回：
```text
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json

{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"} 
```


