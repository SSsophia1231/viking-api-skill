# 概述
/api/knowledge/doc/add 接口用于向已创建的知识库添加文档。
* 文档类型限制参考 [支持的文档类型及规格](/docs/84313/1339026#685f54dd)

# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现导入文档到知识库功能。
# **请求接口**
| **URI** | /api/knowledge/doc/add | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对知识库服务请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| collection_name | -- | string | 否 | -- | **知识库名称** |
| project | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | -- | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| add_type | -- | string | 是 | -- | **文档添加的方式**，可为以下枚举值： <br>  <br> * url ：提供了可以直接公开下载的 url 链接 <br> * tos ：tos 的已授权目录，目前只支持华北区域 <br> * lark：上传飞书文档时，此参数传 lark |
| doc_id | -- | string | 否 | -- | **知识库下的文档唯一标识** <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母或下划线开头，不能为空 <br> * 长度要求：[1, 128] <br>  <br> 注： <br>  <br> * 多次上传，重复的 doc_id 会进行覆盖（新上传的覆盖旧的） <br> * "add_type" == "url" 时，该字段必传 <br> * "add_type" == "tos" 时，该字段无效，系统会自动从 tos 文件的 “x-tos-meta-doc_id” 中获取 <br> * "add_type" == "lark" 时，该字段为可选。若未传，会自动生成 doc_id |
| doc_name | -- | string | 否 | -- | **文档名称** <br>  <br> * 长度要求：[1, 256] <br> * "add_type" == "url" 时，该字段必传 <br> * "add_type" == "tos" 时，该字段无效，系统会自动从 tos 中获取，自动以文件名作为 doc_name <br> * "add_type" == "lark" 时，该字段无效，系统会自动获取对应飞书文档的标题或本地上传文件名 |
| doc_type | -- | string | 否 | -- | **上传文档的类型** <br>  <br> * 非结构化文档支持类型：txt, doc, docx, pdf, markdown, pptx, ppt, jpeg, png, webp, bmp, mp4, mp3, wav, aac, flac, ogg； <br>  <br> <span style="color: rgb(100, 106, 115)"><em>（.jpg .jpeg 文件 doc_type 均为 jpeg）（.md .markdown 文件 doc_type 均为 markdown）</em></span> <br>  <br> * 结构化文档支持类型：xlsx, csv, jsonl <br> * 飞书文档支持类型：wiki, docx, sheet, bitable, folder, file(本地上传文件) <br>  <br> 注： <br>  <br> * add_type 为 url 时，该字段必传 <br> * add_type 为 tos 时，该字段无效，系统会自动从 tos 文件的扩展名中获取 <br> * add_type 为 lark 时，该字段必传 |
| description | -- | string | 否 | -- | **文档描述** <br> 描述会参与对图片的检索，如电商场景下，描述可以用于存放图片对应的详细商品说明，售卖亮点，价格等 <br> 注： <br>  <br> * 暂**只在** doc_type 为**图片类型文档时支持**，其他类型文档设置无效。 <br> * 长度 [0，4000] |
| lark_file | -- | json | 否 | -- | **待上传的飞书文档地址** <br> 仅当 "add_type" == "lark" 时，该字段必传 <br> 参考示例1： <br> { <br> "url": "链接", // 支持文档、电子表格、文件夹、wiki、多维表格、本地上传文档的 URL 链接 <br> "obj_type": "docx", // 枚举：wiki / docx / folder / sheet(电子表格) / space / bitable(多维表格) / file(本地上传文档) <br> "obj_token": "xx", // 对应 obj_type 的 token，可从飞书[开放平台获取](https://open.larkoffice.com/document/server-docs/docs/faq#08bb5df6) <br> "include_child": false, // 是否导入子文档，默认为 false <br> } <br> 注： <br>  <br> * url 或 obj_type + obj_token 两种用法可以二选一 |
| tos_path | -- | string | 否 | -- | **待上传的 tos 目录或指定文件路径** <br> 需要在*`控制台/上传文档/tos 上传`* 页面完成授权，仅当 "add_type" == "tos" 时，该字段必传 <br>  <br> * 正确示例： <br>    * `tos_path="your_tos/path/"` <br>    * `tos_path="your_tos/path/知识库手册.pdf"` <br> * 错误示例： <br>    * `tos_path="tos://your_tos/path/"` <br>    * `tos_path="tos://your_tos/path/知识库手册.pdf"` <br>  <br> 注： <br>  <br> * 导入目录下的文档是一次性的，后续目录下的文档变更不会被自动同步到知识库 <br> * 导入目录时只会扫描当前目录下的文件，而不会递归查看子目录 <br> * tos 目录下文档的 doc_id 取值若重复，最终导入知识库只会保留最后一个上传的文档，即 doc_id 唯一 <br> * 如果目录下文件内容的变更需求，有以下两种方式： <br>    * 单文件变更：通过 url 方式导入，并指定要替换文档的 doc_id （相对比较快） <br>    * 批量变更：再次导入 tos 目录，这种方式会对目录下所有的文档做变更检查，并将新文档替换旧文档。由于需要做文件校验，这种方式耗时较长 <br> * 文件大小限制参考：[知识库配额说明](/docs/84313/1339026) |
| url | -- | string | 否 | -- | **待上传的文件 url 链接** <br> 仅当 "add_type" == "url" 时，该字段必传，字段长度范围是[1, 1024] <br>  <br> * 文件大小限制参考：[知识库配额说明](/docs/84313/1339026) |
| **meta** |  | array 或 array 对应的 JSON 字符串 | 否 | -- | **标签信息** <br>  <br> * "add_type" 为 "url" 或 "lark" 时，该字段有效 <br> * "add_type" == "tos" 时，该字段无效。系统会自动获取 tos 上的文件元信息，您可在[对象存储控制台](https://console.volcengine.com/tos/bucket?projectName=default)中可以针对文档指定元数据信息，参数类型选择“x-tos-meta-”，参数名即为标签名，参数值即为标签值。由于 x-tos-meta-* 的类型限制，此时标签值字段类型只能是 **string** |
|  | field_name | string | 否 | -- | **标签名** <br>  <br> * 不能为 “doc_id” <br> * 需对齐创建知识库时的 field_name <br>    * 需在创建知识库时先初始化标签索引，再在上传文档时打标，以用于检索时实现标签过滤能力 <br>    * 若需新增过滤标签，请先编辑知识库新增标签后，再进行文档打标 |
|  | field_type | string | 否 | -- | **标签类型** <br>  <br> * 支持 "int64"，"float32"，"string"，"bool"，"list<string>"，"list<int64>" 类型 <br> * 需对齐创建知识库时的 field_type |
|  | field_value | 与 field_type 指定类型一致 | 否 | -- | **标签值** |
| **dedup** |  |  | 否 | -- | 如果任一子参数为 true，表示需要去重，此时如果库中没有重复文档，会当做新文档导入。 <br> 当 **content_dedup** 和 **doc_name_dedup** 均为 **true** 时： <br> （C 和 D 分别表示库中相同内容和相同 doc_name 的文档数量） <br>  <br> * C + D = 0 时，当做新文档导入 <br> * C + D = 1 时，根据 auto_skip 参数配置，给出不同处理策略。 <br> * C = 1 ，D = 1 且 C 和 D 指向同一篇文档时，返回重复文档 ID 和错误码 <br> * 其他情况， 返回对应的文档列表，并提示用户去重后重新导入 <br>  <br> 注：只会检查 content 和 doc_name，其他信息的变更不会检查，覆盖或当做新文档导入以上述标准为准。 |
|  | content_dedup | bool | 否 | false | **内容去重** <br> 覆盖相同内容的文档，此时会查找库中相同 doc hash 的文档，查询到的数量为 C。当 **content_dedup** 为 **true**，**doc_name_dedup** 为 **false** 时： <br>  <br> * C = 0 时，当做新文档导入，规则参考 dedup 说明 <br> * C = 1 时，根据 auto_skip 参数配置，给出不同处理策略。 <br> * C > 1 时，提示报错信息。 |
|  | doc_name_dedup | bool | 否 | false | **文档名称去重** <br> 覆盖相同 doc_name 的文档。此时会查找库中相同 doc_name 的文档，查询到的数量为 D。当 **doc_name_dedup** 为 **true**，**content_dedup** 为 **false**时： <br>  <br> * D = 0 时，当做新文档导入，规则参考 dedup 说明 <br> * D = 1 时，根据 auto_skip 参数配置，给出不同处理策略。 <br> * D > 1 时，提示报错信息。 |
|  | auto_skip | bool | 否 | false | **重复文档处理策略** <br> 当 auto_skip 参数设置为 true 时，系统会自动跳过重复文档，并返回原始文档 ID；当 auto_skip 参数设置为 false 时，将覆盖后文档，并返回新文档 ID。 |
# **响应消息**
| **参数** | **参数说明** | **备注** |
| --- | --- | --- |
| code | 状态码 |  |
| message | 返回信息 |  |
| request_id | 标识每个请求的唯一标识符 |  |
| data | { <br> "collection_name": 知识库的名字， <br> "resource_id": 知识库唯一标识， <br> "project": 项目名， <br> "doc_id": 文档唯一标识， <br> "dedup_info": { // 当 dedup 任一子参数为 true 时返回该参数 <br> "skip": true, <br> "same_doc_ids":[ ] <br> } <br> } |  |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection不存在 |
| 1001010 | 400 | doc num is exceed 3000000 | doc数量已满。点击详情查看[知识库配额限制](https://www.volcengine.com/docs/84313/1339026) |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/doc/add \
  -d '{
    "collection_name": "test_collection_name",
    "project": "default",
    "add_type": "url",
    "doc_id": "test0123",
    "doc_name": "张某某盗窃案",
    "doc_type": "pdf",
    "url": "https://fwh-my-test-bucket.tos-cn-beijing.volces.com/%E6%96%B0%E6%A9%99%E7%A7%91%E6%8A%80/%E5%91%A8%E6%9D%A8%E7%9B%97%E7%AA%83%E6%A1%88.pdf?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Content-Sha256=UNSIGNED-PAYLOAD&X-Tos-Credential=YOUR_ACCESS_KEY_ID%2F20240325%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20240325T114024Z&X-Tos-Expires=3600&X-Tos-SignedHeaders=host&X-Tos-Security-Token=nCgdqdEROend3.ChsKBzNzX056d3cSEGBgA9av-UtVs7ClfMkXS4oQk8WFsAYYo-GFsAYgle7V6QcoAjCSkLEJOhx6aGFpeXVqaWEuMDMyMkBieXRlZGFuY2UuY29tQgN0b3NSHHpoYWl5dWppYS4wMzIyQGJ5dGVkYW5jZS5jb21YBGAB.Nur_XCwZ_1LHmSsfeWGjDUn8SEOo3c6op5hx3lUgLZuxtHN_sqs-Kd0KbKw-51CT6wXKQo3AbmidScqVTu6gLQ&X-Tos-Signature=5c3dff2f8cd67daae99476d54188033cc32932d87f1ff85f4f1afd5862fa35cd",
    "meta":[
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
        "collection_name": "test_collection_name",
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
 
{"code":1000003, "message":"invalid request：%s", 
"request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


