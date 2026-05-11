api/knowledge/pipeline/update 修改 [实验版本](https://www.volcengine.com/docs/84313/1510752) 配置
# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现更新 [实验版本](https://www.volcengine.com/docs/84313/1510752) 信息的功能。
# **请求接口**
| **URI** | /api/knowledge/pipeline/update | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: token=********** | 鉴权 |
# **请求参数**
| 参数 | 类型 | 必选 | 默认值 | 备注 |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | *  | **知识库名称** |
| project | string | 否 | default | **项目名** |
| resource_id | string | 否 | *  | **知识库唯一 id** <br> 可选择直接传 resource_id ，或同时传 name 和 project 作为知识库的唯一标识 |
| name | string | 是 | *  | **实验版本名称** <br>  <br> * 不能使用已有系统的默认值 “default” <br> * 实验版本由字母、数字、下划线组成，且只能以字母开头 <br> * 长度不超过 32 个字符 |
| cpu_quota | int | 否 | *  | **cpu 配额** |
| auto_sync_doc | bool | 否 | *  | **是否自动同步新增文档** <br> 打开后调用 add_doc 接口向知识库上传文档时，自动同步到当前实验版本 |
| vlm_prompt | string | 否 | *  | **视频切片规则** <br> 要求：字数不超过 5000，且必须包含 start_time 和 end_time 以及格式说明，否则会造成视频分段失败 <br> ```json <br> { <br>   "name": "demo_video", <br>   "project": "default", <br>   "vlm_prompt": "### 任务：视频智能切片\n\t\t你需要仅基于提供的视频分镜抽帧将视频拆分若干个小切片。要求每个切片满足：\n\t\t1. 时长：每个小片段时长控制在60秒左右,但不要超过300秒\n\t\t2. 第一个片段的start_time从0开始，最后一个片段的end_time为视频结尾时间\n\t\t3. 所有小片段连贯无间隔（end_time = 下一段start_time）,每个片段必须满足 start_time < end_time（起始早于结束\n\t\t4. 拆分断点选择在分镜切换处\n\t\t5. content_summary 直接显示\"自定义caption\"\n\t\t\t### 输出要求（JSON格式）,紧凑排列、无多余空格：\n\t\t\t请输出一个JSON数组，每个元素代表一个切片，包含：\n\t\t\t- `start_time`：切片开始时间(格式：)。\n\t\t\t- `end_time`：切片结束时间(格式：)。\n\t\t\t- `content_summary`\n\t\t\t例如：\n\t\t\t[{{\"start_time\":\"00:00:00.000\",\"end_time\":\"00:00:10.000\",\"content_summary\":\"自定义caption\"}},{{\"start_time\":\"00:00:10.000\",\"end_time\":\"00:00:20.000\",\"content_summary\":\"自定义caption\"}}]\n\t\t\t即使音频ASR文本或分镜抽帧有缺失，也尽量根据视频内容进行切片。" <br> } <br> ``` <br>  |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 403 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 <br>  <br> * 缺失必选参数 <br> * collection_name 命名不符合规范 <br> * 字段类型与相关字段属性不满足约束条件 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
-H 'Content-Type: application/json' \
-H 'Authorization: token=****' \
https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/pipeline/update \
-d '{
  "collection_name": "test_collection_name",
  "project": "default",
  "name": "custom_pipeline_01",
  "cpu_quota": 2,
  "auto_sync_doc": true
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 78
Content-Type: application/json

{"code":0,"message":"success","request_id":"021695029537650fd001de666660000000000000000000230da93"}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 120
Content-Type: application/json

{
"code": 1000003,
"message": "invalid request: cannot update default pipeline",
"request_id": "021695029757920fd001de6666600000000000000000002569b8f"
}
```


