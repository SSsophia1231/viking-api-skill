# **概述**
/api/knowledge/point/delete 接口用于删除一个知识库下的某个切片，或删除某个[实验版本](https://www.volcengine.com/docs/84313/1510752)下的某个切片
> 通过指定 pipeline_name 实现在知识库下的指定实验版本内删除切片

# **前置条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现删除知识库下某个切片的功能。
# **请求接口**
| **URI** | /api/knowledge/point/delete | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **类型** | **必选** | **默认值** | **备注** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空 <br> * 长度要求：[1, 64] |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则默认在 default 项目下操作。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库唯一 id** <br>  <br> * 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| point_id | string | 是 | -- | **要删除的切片 id** |
| pipeline_name | string | 否 | -- | **实验版本名称** <br>  <br> * 指定当前参数可删除具体实验版本下的切片 <br> * 不指定默认删除知识库主版本下的切片 |
# **响应消息**
| 字段 | 备注 |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
# **完整示例**
## 请求消息
```bash
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/point/delete \
  -d '{
    "resource_id": "kb_xxxxxx",
    "point_id": "_sys_xxxxx"
}'
```

## 响应消息
执行成功返回：
```JSON
HTTP/1.1 200 OK 
Content-Length: 43 
Content-Type: application/json 
  
{"code":0,"message":"success","request_id":"021695029537650fd001de666660000000000000000000230da93"}
```

执行失败返回：
```Plain
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request: %s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


