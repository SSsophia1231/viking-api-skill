# 概述
/api/knowledge/task/info 接口用于查询指定下载任务的状态、进度和结果
> 通过指定 pipeline_name 实现在知识库下的指定实验版本内查询指定下载任务的状态、进度和结果

# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现查询指定下载任务的状态、进度和结果。
# **请求接口**
| **URI** | /api/knowledge/task/info | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对知识库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| task_id | string | 是 | 要查询的任务的唯一标识符。 |
# **响应消息**
| 字段 | 类型 | 子字段 | 子字段类型 | 描述 |
| --- | --- | --- | --- | --- |
| code | integer | -- | -- | 状态码 |
| message | string | -- | -- | 返回信息 |
| data | object | status | string | 任务状态 <br>  <br> * running <br> * success <br> * fail |
|  |  | percentage | integer | 任务进度，0 ~ 100 |
|  |  | attachment_link | string | 下载 TOS 链接 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
|  | 400 | task not exist | 任务不存在 |
# 完整消息
## 请求消息
```bash
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/task/info \
  -d '{
    "task_id": "xxx"
}'
```

## 响应消息
执行成功返回：
```JSON
HTTP/1.1 200 OK 
Content-Length: 43 
Content-Type: application/json 
  
{
  "code": 0,
  "data": {
    "status": "success",
    "percentage": 100,
    "attachment_link": "https://knowledgebase-video-boe.tos-cn-beijing.volces.com/USER_VIDEO_TEST/2100655893/112294/user_define/_sys_auto_gen_doc_id-6049498338074484299/_sys_auto_gen_doc_id-6049498338074484299.zip?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLT****%2F20251215%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20251215T083624Z&X-Tos-Expires=900&X-Tos-SignedHeaders=host&X-Tos-Signature=9c6627ebab6138399a437c80e6b4bfc6098b3c84e20fe84741054d40fd4f3d2f"
  },
  "message": "success",
  "request_id": "02176578783344000000000000000000000ffff0a007f1ef31bf2"
}
```

执行失败返回：
```JSON
HTTP/1.1 400 Bad Request
Content-Length: 43 
Content-Type: application/json 
  
{"code":1000003,"message":"invalid request:task not exist","request_id":"02176897909291000000000000000000000ffffac130abbfb5dbd"}
```


