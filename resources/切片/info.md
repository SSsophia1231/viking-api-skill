# 概述
/api/knowledge/point/info 接口用于查看知识库或某个[实验版本](https://www.volcengine.com/docs/84313/1510752)下指定切片的信息。
> 通过指定 pipeline_name 查看知识库下指定实验版本的切片信息。

# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，即可调用 API 接口查看知识库下指定切片的信息。
# **请求接口**
| **URI** | /api/knowledge/point/info | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档** [API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则默认在 default 项目下查询。 <br> 若需要操作指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| point_id | string | 是 | -- | **切片唯一 id** |
| get_attachment_link | bool | 否 | False | **是否获取切片中图片的临时下载链接** <br> 有效期 10 分钟 |
| pipeline_name | string | 否 | -- | **实验版本名称** <br>  <br> * 指定当前参数可查询具体实验版本下的切片信息 <br> * 不指定默认查询知识库主版本下的切片信息 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | 返回内容 |
data 返回值
| 字段 | 子字段 | 字段类型 | 说明 |
| --- | --- | --- | --- |
| collection_name | -- | string | 知识库名称 |
| point_id | -- | string | 切片唯一 id |
| process_time | -- | int | 知识处理完成的时刻（Unix 时间戳，秒） |
| update_time | -- | int | 切片更新的时刻（Unix 时间戳，秒） |
| content | -- | string | 切片内容 <br> 1、非结构化文件：content 返回切片原文内容 <br> 2、faq 文件：content 返回答案字段内容 <br> 3、结构化文件：content 返回参与索引的字段和取值，以 K:V 对拼接，使用 \n 区隔 |
| md_content | -- | string | markdown 格式的解析结果 <br> 对于非结构化文档中的表格切片，可以额外返回 markdown 格式解析结果，保留更多表格原始信息 <br> 表格切片可以通过 chunk_type == table 判断 |
| html_content | -- | string | html 格式的解析结果 <br> 对于非结构化文档中的表格切片，可以额外返回 html 格式解析结果，保留更多表格原始信息 <br> 表格切片可以通过 chunk_type == table 判断 |
| table_chunk_fields | -- | list | 结构化数据检索返回单行全量数据 |
| description | -- | string | 图片描述或视频画面总结 <br>  <br> * 图片描述：图片上传时传入的描述信息 <br> * 视频画面总结：视频切片的画面总结 <br> * 长度[0，4000] |
| chunk_id | -- | int | 切片在原文档中的顺序位次 |
| chunk_status | -- | string | 切片状态 |
| chunk_title | -- | string | 该文本片的父标题，是由解析模型识别出来的上一层级的标题。若没有上一层级标题则为空 |
| chunk_type | -- | string | 切片类型 <br> 返回值类型有：doc-image、image、video、audio、table、text、structured、faq、mixed-table等 |
| chunk_source | -- | string | 切片来源 <br> 来源于文档解析切片或者手动新增切片，对应值分别为 document 和 user |
| chunk_attachment | -- | list | 检索召回附件，chunk_type 为 image 和 video 时有效 |
| doc_info | -- | list | 切片所属文档信息 |
|  | doc_id | string | 所属文档 id |
|  | doc_name | string | 文档名称 |
|  | create_time | int | 文档创建的时刻 |
|  | doc_type | string | 文档类型 |
|  | doc_meta | string | 文档 meta 信息 |
|  | source | string | 文档导入来源 |
|  | title | string | 仅视频切片返回，即当前视频所有大纲标题 |
|  | status | object | process_status 为文档处理状态 <br> 0：成功 <br> 1：失败 <br> 2：排队中 <br> 3：更新中 <br> 5：删除中 <br> 6：处理中 |
| video_frame | -- | string | 仅视频切片返回 <br> 视频切片关键帧 |
| video_start_time | -- | long | 仅视频切片返回 <br> 视频切片的起始时间，单位 ms |
| video_end_time | -- | long | 仅视频切片返回 <br> 视频切片的结束时间，单位 ms |
| audio_start_time | -- | long | 仅音频切片返回 <br> 音频切片的起始时间，单位 ms |
| audio_end_time | -- | long | 仅音频切片返回 <br> 音频切片的结束时间，单位 ms |
| original_coordinate | -- | -- | 仅 pdf 和 ppt 返回，知识点原始坐标信息 |
|  | page_no | list | 知识点坐标页码 |
|  | bbox | list | 知识点在原文页的 bbox 坐标位置 |
chunk_attachment 返回值
| 字段 | 字段类型 | 说明 |
| --- | --- | --- |
| uuid | string | 附件的唯一标识 |
| caption | string | 图片所属标题，若未识别到标题则值为"\n" |
| type | string | image、video、mixed-table、table 等 |
| info_link | string | "get_attachment_link" == true 时返回图片、视频抽帧图列或表格所包含图片的临时下载链接，有效期 10 分钟 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection不存在 |
| 1001001 | 400 | doc not exist | doc不存在 |
| 1002001 | 400 | point not exist | point_id不存在 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/point/info \
  -d '{
    "resource_id": "xxx",
    "point_id": "_sys_auto_gen_lark_doc_id-29175896809570851-0"
}'
```

## 响应消息
执行成功返回：
```JSON
{
    "code":0,
    "data":{
        "collection_name":"test",
        "point_id":"_sys_auto_gen_lark_doc_id-29175896809570851-0",
        "process_time":1731054363,
        "content":"a:4\nb:5\nc:6",
        "chunk_id":0,
        "doc_info":{
            "doc_id":"_sys_auto_gen_lark_doc_id-29175896809570851",
            "doc_name":"表格",
            "create_time":1731054262,
            "doc_type":"lark_sheet",
            "doc_meta":"[{\"field_name\":\"doc_id\",\"field_type\":\"string\",\"field_value\":\"_sys_auto_gen_lark_doc_id-291758968095705851\"}]",
            "source":"lark"
            },
        "chunk_type":"structured",
        "table_chunk_fields":[{"field_name":"a","field_value":"4"},{"field_name":"b","field_value":"5"},{"field_name":"c","field_value":"6"}]
        },
    "message":"success",
    "request_id":"02173217505951900000000000000000000ffff0a00787e6d6662"
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


