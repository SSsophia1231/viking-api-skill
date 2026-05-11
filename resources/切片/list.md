# 概述
/api/knowledge/point/list 接口用于查看知识库或某个[实验版本](https://www.volcengine.com/docs/84313/1510752)下的切片列表，默认按 point_id 从小到大排序。
> 支持通过指定 pipeline_name 参数，来实现仅查询某个实验版本下的切片列表

# **前提条件**
完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现查看知识库下的切片列表的功能。
# **请求接口**
| **URI** | /api/knowledge/point/list | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对知识库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| collection_name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则默认在 default 项目下查询。 <br> 若需要查询指定项目下的知识库，需正确配置该字段。 <br>  |
| resource_id | string | 否 | -- | **知识库唯一 id** <br> 可选择直接传 resource_id，或同时传 collection_name 和 project 作为知识库的唯一标识 |
| offset | int | 否 | 0 | **用于分页** <br> 表示从结果的第几个开始取，需要大于等于 0 |
| limit | int | 否 | -1 | **返回切片个数** <br> -1 表示获取所有，最大值不超过 100，每次返回最多不超过 100 |
| doc_ids | list | 否 | -- | **按文档 id 筛选** <br> 指定文档返回对应切片列表，不传或为 null 表示不筛选，传入的 size 为 0 将返回空结果。限制 list 长度，最大长度为 100 |
| point_ids | list | 否 | -- | **按照切片 id 筛选** <br> 指定一个或多个切片 id 返回对应切片内容，不传或为 null 表示不筛选，传入的 size 为 0 将返回空结果。限制切片 id 列表长度，最大长度为 100 |
| get_attachment_link | bool | 否 | false | **是否获取切片中图片的临时下载链接** <br> 10 分钟有效期 |
| pipeline_name | string | 否 | -- | **实验版本名称** <br>  <br> * 指定当前参数可查询具体实验版本下的切片列表 <br> * 不指定默认查询知识库主版本下的切片列表 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | 切片内容，返回值说明同 info 接口 [响应消息](/docs/84313/1386606#6d03f9d3) <br> ```text <br> { <br>     "collection_name": 知识库名称 <br>     "total_num": 总共有多少个结果 <br>     "count": 本次返回的结果数量 <br>     "point_list": [ <br>         { <br>           "collection_name": 知识库名称 <br>           "point_id": 切片 id //每个知识库版本下唯一 <br>           "doc_info": { <br>               "doc_id": 所属文档 id <br>               "doc_name": 所属文档名字 <br>               "create_time": 切片创建时间 <br>               "doc_type": 所属原始文档类型 <br>               "description": 文档描述（当前仅支持图片文档） <br>               "doc_meta": 所属文档的 meta 信息 <br>               "source": 所属文档知识来源（url，tos 等） <br>               "title": 所属文档标题 <br>               "original_coordinate": 切片在所属文档的原始位置坐标   // 仅支持 pdf 和 ppt 文档 <br>           } <br>         "process_time": 切片处理完成的时间 <br>         "video_start_time": 视频切片的起始时间，单位 ms，其中第一个视频切片起始时间默认不返回起始时间 <br>         "video_end_time": 视频切片的结束时间，单位 ms <br>         "audio_start_time": 音频切片的起始时间，单位 ms <br>         "audio_end_time": 音频切片的结束时间，单位 ms <br>         "chunk_title": 切片标题，是由解析模型识别出来的上一层级的标题。若没有上一层级标题则为空 <br>         "content": 切片内容 <br>         "md_content": 切片 markdown 解析结果，保留更多的原始表格信息，当前只有 chunk_type 为 table 的切片会返回该字段 <br>         "html_content": 切片 html 解析结果，保留更多的原始表格信息，当前只有 chunk_type 为 table 的切片会返回该字段 <br>       } <br>   ] <br> } <br> ``` <br>  |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
| 1000005 | 400 | collection not exist | collection不存在 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/point/list \
  -d '{
    "collection_name": "test_collection_name",
    "project": "default"
}'
```

## 响应消息
执行成功返回：
```Shell
{
    "code": 0,
    "data": {
        "collection_name": "api0828",
        "total_num": 1,
        "count": 1,
        "point_list": [
            {
                "collection_name": "api0828",
                "point_id": "_sys_auto_gen_doc_id-17691607628519396693-0",
                "process_time": 1724848725,
                "content": "讲解模块:讲解模块：xxxxxx\n子模块:子模块：xxxxx\n问题示例:问题示例：xxxxxx\n记忆化 —— 讲解要点:\n□ 要点1\n□ 要点2\n□ 要点3",
                "chunk_id": 0,
                "doc_info": {
                    "doc_id": "_sys_auto_gen_doc_id-17691607628519396693",
                    "doc_name": "演示表格.xlsx",
                    "create_time": 1724848720,
                    "doc_type": "xlsx",
                    "source": "tos_fe"
                },
                "chunk_type": "structured",
                "table_chunk_fields": [
                    {
                        "field_name": "讲解模块",
                        "field_value": "讲解模块：xxxxxx"
                    },
                    {
                        "field_name": "子模块",
                        "field_value": "子模块：xxxxx"
                    },
                    {
                        "field_name": "问题示例",
                        "field_value": "问题示例：xxxxxx"
                    },
                    {
                        "field_name": "记忆化 —— 讲解要点",
                        "field_value": "□ 要点1\n□ 要点2\n□ 要点3"
                    }
                ]
            }
        ]
    },
    "message": "success",
    "request_id": "02172484891424400000000000000000000ffff0a00705414b331"
}
```

执行失败返回：
```Shell
HTTP/1.1 400 OK
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


