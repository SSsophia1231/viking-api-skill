## **概述**
/api/knowledge/service/rerank 接口用于重新批量计算输入文本与检索到的文本之间的 score 值，以对召回结果进行重排序。判断依据为 chunk content 能回答 query 的概率，分数越高即模型认为该文本片段能回答 query 的概率越大。
## **请求接口**
* 请求向量数据库 VikingDB 的 OpenAPI 接口时，需要构造签名进行鉴权，详细的 OpenAPI 签名调用方法请参见 [API签名调用指南](https://www.volcengine.com/docs/6369/67265)。

| **URI** | /api/knowledge/service/rerank | 统一资源标识符 |
| --- | --- | --- |
| **方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
## **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| datas | list[map] | 是 | -- | **待重排的数据列表** <br> 每个元素为一个 map，数组长度不超过 200，支持以下参数： <br>  <br> * query（必选）：用于排序的查询内容，string 或 object <br>    * string：纯文本查询内容，重排模型通用 <br>    * object：文或图的查询内容，**仅适用于 doubao-seed-rerank 模型**，示例如下： <br>  <br> ```Python <br> "query": { <br>     "text":"xxx", <br>     "image":"xxx" <br> } <br> ``` <br>  <br>  <br> * content（可选）：待排序的文本内容，string <br> * image（可选）：待排序的图片内容，string（单张） 或 array（多张），**仅适用于 doubao-seed-rerank 模型** <br>    * 支持传入公开访问的 http/https 链接 <br>    * 支持 jpeg、png、webp、bmp 格式的 base64 编码，单张图片小于 3 MB，请求体不能超过 4 MB，遵循 data:{mime_type};base64,{base64_data} 或 base64://{base64_image} 格式拼接传入 <br>       * {mime_type}：文件的媒体类型，支持 image/jpeg、image/png、image/webp、image/bmp <br>       * {base64_data}：文件经过 base64 编码后的字符串 <br> * title（可选）：文档的标题 |
| rerank_model | string | 否 | "base-multilingual-rerank" | **rerank 模型** <br> 可选模型： <br>  <br> * "doubao-seed-rerank"（即 doubao-seed-1.6-rerank）：字节自研多模态重排模型、支持文本 / 图片 / 视频 混合重排、精细语义匹配、可选阈值过滤与指令设置**（推荐）** <br> * "base-multilingual-rerank"：速度快、长文本、支持 70+ 种语言 <br> * "m3-v2-rerank"：常规文本、支持 100+ 种语言 |
| rerank_instruction | string | 否 | -- | **重排指令** <br> **仅当 rerank_model=="doubao-seed-rerank" 时生效**，用于提供给模型一个明确的排序指令，提升重排效果。字符串长度不超过 1024 <br> <span style="color: rgb(100, 106, 115)"><em>如，</em></span>*Whether the document answers the query or matches the content retrieval intent* |
## **响应消息**
| **字段** | **类型** | **子字段** | **子字段类型** | **说明** |
| --- | --- | --- | --- | --- |
| code | integer | -- | -- | 状态码 |
| message | string | -- | -- | 错误信息 |
| request_id | string | -- | -- | 请求的唯一标识符 |
| data | object | scores | array | float64 数组，与输入 datas 数组一一对应，表示每个文档与 query 的相关性得分 |
|  |  | token_usage | integer | 本次 rerank 调用消耗的总 token 数量 |
### **状态码说明**
| **状态码** | **http 状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 403 | VolcanoErrUnauthorized | 鉴权失败 |
| 1000002 | 400 | VolcanoErrInvalidRequest | 请求参数无效（当 query 缺失，或 datas 中所有文档都未提供任一媒体/文本内容时触发） |
| 300004 | 429 | VolcanoErrQuotaLimiter | 账户的 rerank 调用已达到配额限制 |
| 1000028 | 500 | VolcanoErrInternal | 服务内部错误，rerank 模型过载 |
## 完整示例
### 请求消息
```Shell
curl --location --request POST 'http://<your-host>/api/knowledge/service/rerank' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <your-auth-token>' \
--data-raw '{
    "rerank_model": "doubao-seed-rerank",
    "datas": [
        {
            "query": "展示一张系统架构图",
            "title": "系统架构设计文档",
            "image": "https://<your-domain>/path/to/arch-diagram.png"
        },
        {
            "query": "展示一张系统架构图",
            "title": "会议纪要",
            "content": "讨论了下个季度的 OKR。"
        }
    ]
}'
```

### 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: <content-length>
Content-Type: application/json
{
    "message":"success",
    "code":0,
    "request_id":"02170427320284800000000000000000000ffff0a0060861f847c",
    "data":{
        "scores":[0.17574862881497047,0.7583029228400268],
        "token_usage":123
    }
}
```

执行失败返回：
```Shell
HTTP/1.1 403 Forbidden
Content-Length: <content-length>
Content-Type: application/json
 
{
    "message":"check sign error, please check your ak, sk",
    "code":1000001,
    "request_id":"02170427372421200000000000000000000ffff0a006086784460"
}
```


