本节将说明如何更新一个已创建的知识库信息。
* 当前仅支持更新知识库的 description、cpu_quota、 fields（文档标签）和 vlm_prompt（视频切片规则）
   * 旗舰版支持 description、cpu_quota、 fields（文档标签）、vlm_prompt（视频切片规则）修改
   * 标准版仅支持 description 修改
* 当前通过 collection/update 接口成功更新 fields（文档标签）字段后，前端会自动同步并**覆盖**为更新后的内容

# 概述
/api/knowledge/collection/update 接口用于更新知识库信息。
# **前提条件**
完成 “签名鉴权方式” 页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现知识库信息更新的功能。
# **请求接口**
| **URI** | /api/knowledge/collection/update | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数（旗舰版）**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在 default 项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库 id** <br> 可选择直接传 resource_id ，或同时传 name 和 project 作为知识库的唯一标识。 |
| description | string | 否 | -- | **知识库描述信息** <br>  <br> * 长度要求：[1, 65535] |
| cpu_quota | int | 否 | -- | **cpu 配额** |
| fields | list | 否 | -- | **文档标签** <br> 文档标签修改逻辑为**覆盖更新**，例如创建知识库时设置了标签 A、B、C <br>  <br> * 若想新增文档标签 D，此时 update 应传入 A、B、C、D <br> * 若想删除文档标签 A，此时 update 应传入 B、C、D <br>  <br> ```Plain <br> [ <br>   { <br>     "field_name": "xxx" // 文档标签名称，最大长度为 128 字符 <br>     "field_type": "xxx" //文档标签类型 <br>     "default_val": xxxx // 文档标签值 <br>   }, <br> ] <br> ``` <br>  |
| vlm_prompt | string | 否 | -- | **视频切片规则** <br> 要求：字数不超过 5000，且必须包含 start_time 和 end_time 以及格式说明，否则会直接造成视频分段失败 <br> ```SQL <br> { <br>   "name": "demo_video", <br>   "project": "default", <br>   "vlm_prompt": "### 任务：视频智能切片\n\t\t你需要仅基于提供的视频分镜抽帧将视频拆分若干个小切片。要求每个切片满足：\n\t\t1. 时长：每个小片段时长控制在60秒左右,但不要超过300秒\n\t\t2. 第一个片段的start_time从0开始，最后一个片段的end_time为视频结尾时间\n\t\t3. 所有小片段连贯无间隔（end_time = 下一段start_time）,每个片段必须满足 start_time < end_time（起始早于结束）\n\t\t4. 拆分断点选择在分镜切换处\n\t\t5. content_summary 直接显示\"自定义caption\"\n\t\t\t### 输出要求（JSON格式）,紧凑排列、无多余空格：\n\t\t\t请输出一个JSON数组，每个元素代表一个切片，包含：\n\t\t\t- `start_time`：切片开始时间(格式：)。\n\t\t\t- `end_time`：切片结束时间(格式：)。\n\t\t\t- `content_summary`\n\t\t\t例如：\n\t\t\t[{{\"start_time\":\"00:00:00.000\",\"end_time\":\"00:00:10.000\",\"content_summary\":\"自定义caption\"}},{{\"start_time\":\"00:00:10.000\",\"end_time\":\"00:00:20.000\",\"content_summary\":\"自定义caption\"}}]\n\t\t\t即使音频ASR文本或分镜抽帧有缺失，也尽量根据视频内容进行切片。" <br> } <br> ``` <br>  |
# 请求参数（标准版）
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在 default 项目下创建。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库 id** <br> 可选择直接传 resource_id ，或同时传 name 和 project 作为知识库的唯一标识。 |
| description | string | 否 | -- | **知识库描述信息** <br>  <br> * 长度要求：[1, 65535] |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection 不存在 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/collection/update \
  -d '{
    "name": "test_collection_name",
    "project": "",
    "description": "这是一个测试知识库",
    "cpu_quota": 1
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 43
Content-Type: application/json
 
{"code":0,"message":"success","request_id":"021695029537650fd001de666660000000000000000000230da93"}
```

执行失败返回：
```Shell
HTTP/1.1 400 OK
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


