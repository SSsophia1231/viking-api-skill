# 概述
/api/knowledge/collection/create 接口用于创建一个新的知识库。创建成功后，可以导入数据。
# **前提条件**
完成"签名鉴权方式"页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现知识库的创建功能。
# **请求接口**
| **URI** | /api/knowledge/collection/create | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数（旗舰版）**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| name | -- | string | 是 | -- | **知识库名称** <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空 <br> * 长度要求：[1-64] <br> * 知识库名称不能重复 |
| project | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要在指定项目下创建知识库，则需正确配置该字段。 <br>  |
| description | -- | string | 否 | "" | **知识库描述信息** <br>  <br> * 长度要求：[1, 65535] |
| version | -- | int | 否 | 4 | 2: 标准版 <br> 4: 旗舰版 <br> 当前版本下该值为 4 *（仅旗舰版支持结构化知识库和音视频模态）* |
| data_type |  | string | 否 | unstructured_data | **知识库内的数据类型** <br>  <br> * unstructured_data：全模态数据（同时支持上传结构化文件，如 pdf、 doc、csv、xlsx、png、mp4 等） <br> * structured_data：结构化数据（仅支持上传结构化文件，如 csv、xlsx、jsonl） |
| **preprocessing** |  | object | 否 |  | **非结构化文档处理策略** <br> 当 data_type 为 “unstructured_data” 时生效，为 “structured_data” 时无效。 |
|  | chunking_strategy | string | 否 | -- | **文档切片策略**，枚举值：["custom_balance", "custom"] <br>  <br> * “custom_balance” 是知识库系统提供的最新默认文档处理策略，该策略： <br>    1. 升级了对 pdf、docx 等复杂文档的解析和理解能力，对复杂文档版面结构、语义结构的解析能力获得大幅提升；特别优化了图片内容及其上下文的理解和加工能力，支持将图片和文本 chunk 混合编排，增强上下文一致性；特别优化了表格内容的理解加工能力，对长表格解析和切片更具优势；结合 VikingDB 语义和关键词融合检索算法，提高了多模态内容的检索能力，大幅提升相关信息的召回能力；提高了切片算法信噪比，无关信息更少，语义损失更小。 <br>    2. 选用此策略后，可生效的文档处理策略子参数包括： <br>    * "chunk_length" (仅当 "chunking_identifier" 为空时生效） <br>    * "merge_small_chunks" (仅当 "chunking_identifier" 为空时生效） <br>    * "multi_modal" (仅当 "chunking_identifier" 为空时生效） <br> * “custom” 是使用自定义分隔符的文档处理策略，选用此策略后，可生效的文档处理策略子参数包括： <br>    * "chunking_identifier" <br>    * "chunk_length" (仅当 "chunking_identifier" 为空时生效） <br>    * "merge_small_chunks" (仅当 "chunking_identifier" 为空时生效） <br>    * "multi_modal" (仅当 "chunking_identifier" 为空时生效） <br> * 请注意原“default”策略目前仅用于兼容存量知识库，不再维护，**新建知识库建议采用“custom_balance”** |
|  | chunking_identifier | list | 否 | -- | **自定义分隔符号** <br> chunking_strategy == “custom” 时，需要指定自定义分隔符 |
|  | chunk_length | int | 否 | 500 | **文档类型切片最大长度** <br> 取值范围见 [向量化模型及索引算法对照表](/docs/84313/1254593#6e312068) |
|  | merge_small_chunks | bool | 否 | true | **是否合并短切片（文档、音视频通用）** <br> 配置是否对短切片进行合并，且合并后的文本/音视频片会限制不超过设置的切片最大长度限制 |
|  | multi_modal | list | 否 | -- | **图片理解策略** <br> 枚举值： <br>  <br> * "image_ocr"：图片 ocr <br>  <br> 传参示例： <br>  <br> * 当 `"multi_modal": ["image_ocr"]` 时，开启图片 ocr，不传值即代表不开启图片 ocr <br>  <br> 使用旧参数命名“multi_mode”创建的库仍保留原命名，但新创建知识库不推荐继续使用 |
|  | video_chunking_strategy | string | 否 | smart_slice | **视频切片策略** <br> 当选择创建音视频知识库时生效（即 **embedding_model** 参数为 doubao-embedding-vision-and-m3或 doubao-embedding-vision，**embedding_model_version** 参数为 250615 时），参数值如下： <br>  <br> * smart_slice: 智能内容切片 <br> * voice_slice: 语音语义切片 |
|  | vlm_prompt | string | 否 | 连续剪裁分段模板的 prompt | **视频切片规则** <br> 仅当 video_chunking_strategy == “smart_slice” 时生效，字数不超过5000，必须包含 start_time 和 end_time 以及格式说明，否则直接造成视频分段失败 <br> ```JSON <br>   "preprocessing": { <br>     "chunk_length": 2000, <br>     "chunking_strategy": "custom_balance", <br>     "enable_smart_summary": true, <br>     "keep_raw_text": true, <br>     "merge_small_chunks": true, <br>     "multi_modal": [ <br>       "image_ocr" <br>     ], <br>     "video_chunking_strategy": "smart_slice", <br>     // 视频切片规则（自定义prompt） <br>     "vlm_prompt": "### 任务：视频智能切片\n\t\t你需要仅基于提供的视频分镜抽帧将视频拆分若干个小切片。要求每个切片满足：\n\t\t1. 时长：每个小片段时长控制在60秒左右,但不要超过300秒\n\t\t2. 第一个片段的start_time从0开始，最后一个片段的end_time为视频结尾时间\n\t\t3. 所有小片段连贯无间隔（end_time = 下一段start_time）,每个片段必须满足 start_time < end_time（起始早于结束\n\t\t4. 拆分断点选择在分镜切换处\n\t\t5. content_summary 直接显示\"自定义caption\"\n\t\t\t### 输出要求（JSON格式）,紧凑排列、无多余空格：\n\t\t\t请输出一个JSON数组，每个元素代表一个切片，包含：\n\t\t\t- `start_time`：切片开始时间(格式：HH:MM:SS.sss)。\n\t\t\t- `end_time`：切片结束时间(格式：HH:MM:SS.sss)。\n\t\t\t- `content_summary`\n\t\t\t例如：\n\t\t\t[{{\"start_time\":\"00:00:00.000\",\"end_time\":\"00:00:10.000\",\"content_summary\":\"自定义caption\"}},{{\"start_time\":\"00:00:10.000\",\"end_time\":\"00:00:20.000\",\"content_summary\":\"自定义caption\"}}]\n\t\t\t即使音频ASR文本或分镜抽帧有缺失，也尽量根据视频内容进行切片。" <br>   } <br> ``` <br>  |
|  | enable_smart_summary | bool | 否 | true | **视频是否开启大纲智能总结** <br> 配置是否开启大纲，开启后支持使用大模型对视频内容进行智能大纲总结 |
|  | video_max_length | int | 否 | 30 | **视频最大切片长度** <br> 仅当 video_chunking_strategy == “voice_slice” 时生效，取值范围 [1, 60] ，单位 s |
|  | audio_chunk_length | int | 否 | 2000 | **音频文本切片最大长度** |
|  | enable_audio_smart_summary | bool | 否 | false | **音频是否开启大纲智能总结** <br> 配置是否开启大纲，开启后支持使用大模型对音频内容进行智能大纲总结 |
| table_config | -- | object | 否 | -- | **结构化知识库表字段配置** <br> 当 data_type == “structured_data” 时生效 <br> ```JSON <br> { <br>   "table_type": "row", <br>   // row 表示从行开始解析，col 表示从列开始解析, <br>   "table_pos": "int", <br>   // 字段位于第几行或第几列, <br>   "start_pos": "int", <br>   // 起始数据在第几行或第几列, <br>   "table_fields": [ <br>       { "field_name": "xxx", //字段名称 <br>           "field_type": "int64", //字段类型, 支持 string, int64, float32, bool，list<string> <br>           "if_embedding": true, //是否参与向量索引 <br>           "default_value": "xxx", //默认值 <br>           "if_filter": false //是否为标签过滤字段 <br>     }, <br>     ..... <br>   ] <br> } <br> ``` <br>  |
| **index** |  | object | 否 | -- | **索引配置** |
|  | index_config | object | 否 | -- | 知识库索引配置 <br> ```JSON <br> { <br>     "fields": [ <br>         { <br>             "field_name": "type", <br>             //标签名 <br>             "field_type": "string", <br>             //标签类型 <br>             "default_val": "instruction" <br>             //标签默认值 <br>          }, <br>          {...} <br>     ], <br>     "cpu_quota": 1, <br>     // cpu 配额，整数型 [1, 100]， 默认值为 1 <br>     "embedding_model": "doubao-embedding-vision", <br>     // 指定向量化模型，创建知识库的类型由所选模型决定 <br>     "embedding_model_version": "250328", <br>     //指定向量化模型版本，非必填，不填会默认使用版本 <br>     //注：若需要创建视频知识库，此字段必填且需指定为250615 <br>     "embedding_dimension": 2048, <br>     // 向量维度 <br>     "quant": "int8" <br>     // 向量的量化方式 <br>  <br>     // "embedding_model"、"embedding_model_version"、"embedding_dimension"和"quant"可选范围参考 <br> } <br> ``` <br>  <br> 注： <br>  <br> * 每个知识库最多可定义 **180 个**标签字段，字段名称不可重复 <br> * 字段名称不能以 _sys_auto 开头，否则创建将会失败 <br> * 支持的字段类型（field_type）：string、int64、list<int64>、list<string>、float32、bool、date_time、geo_point <br> * 创建知识库时仅需定义标签字段结构，文档的实际打标操作通过上传时调用 doc/add 接口完成 <br> * 若不传 fields 或 value 为空，则该文档不会附加任何标签，也不参与标签过滤 <br> * 若将某字段的 field_name 设为 "doc_id" 且 field_type 为 "string"，系统将在文档上传后自动写入对应的 doc_id 值 |
|  | index_type | string | 否 | hnsw_hybrid | **指定索引算法**，支持 hnsw_hybrid、hnsw 和 flat <br> 推荐选择 “hnsw_hybrid”，能够兼具对关键词和语义的理解，综合提高检索精度 <br> 向量化模型和索引算法的对照关系参考 [向量化模型及索引算法对照表](https://www.volcengine.com/docs/84313/1254593#6e312068) |
| doc_summary_config |  | object | 否 | -- | **知识库摘要配置** |
|  | enabled | bool | 否 | false | **是否开启文档 AI 摘要功能** <br> 配置知识库是否开启文档 AI 生成摘要功能，开启后，该知识库将自动为每篇文档生成摘要并保存结果到文档元信息中 <br> 注：此功能仅对当知识库类型为非结构化知识库时生效，即 data_type 为 “unstructured_data” 时生效 |
# 请求参数（标准版）
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| name | -- | string | 是 | -- | **知识库名称** <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空 <br> * 长度要求：[1-64] <br> * 知识库名称不能重复 |
| project | -- | string | 否 | default | **知识库所属项目，获取方式参见文档**[API 接入与技术支持](/docs/84313/1606319#1ab381b9) <br> 若不指定该字段，则在default项目下创建。 <br> 若需要在指定项目下创建知识库，则需正确配置该字段。 <br>  |
| description | -- | string | 否 | "" | **知识库描述信息** <br>  <br> * 长度要求：[1, 65535] |
| version | -- | int | 否 | 4 | 2: 标准版 <br> 4: 旗舰版 <br> 当前版本下该值为 2 |
| **preprocessing** |  | object | 否 |  | **非结构化文档处理策略** <br> 当 data_type 为 “unstructured_data” 时生效，为 “structured_data” 时无效。 |
|  | chunking_strategy | string | 否 | -- | **文档切片策略**，枚举值：["custom_balance", "custom"] <br>  <br> * “custom_balance” 是知识库系统提供的最新默认文档处理策略，该策略： <br>    1. 升级了对 pdf、docx 等复杂文档的解析和理解能力，对复杂文档版面结构、语义结构的解析能力获得大幅提升；特别优化了图片内容及其上下文的理解和加工能力，支持将图片和文本 chunk 混合编排，增强上下文一致性；特别优化了表格内容的理解加工能力，对长表格解析和切片更具优势；结合 VikingDB 语义和关键词融合检索算法，提高了多模态内容的检索能力，大幅提升相关信息的召回能力；提高了切片算法信噪比，无关信息更少，语义损失更小。 <br>    2. 选用此策略后，可生效的文档处理策略子参数包括： <br>    * "chunk_length" (仅当 "chunking_identifier" 为空时生效） <br>    * "merge_small_chunks" (仅当 "chunking_identifier" 为空时生效） <br>    * "multi_modal" (仅当 "chunking_identifier" 为空时生效） <br> * “custom” 是使用自定义分隔符的文档处理策略，选用此策略后，可生效的文档处理策略子参数包括： <br>    * "chunking_identifier" <br>    * "chunk_length" (仅当 "chunking_identifier" 为空时生效） <br>    * "merge_small_chunks" (仅当 "chunking_identifier" 为空时生效） <br>    * "multi_modal" (仅当 "chunking_identifier" 为空时生效） <br> * 请注意原“default”策略目前仅用于兼容存量知识库，不再维护，**新建知识库建议采用“custom_balance”** |
|  | chunking_identifier | list | 否 | -- | **自定义分隔符号** |
|  | chunk_length | int | 否 | 500 | **文档类型切片最大长度** <br> 取值范围见 [向量化模型及索引算法对照表](https://arcosite.bytedance.net/sites/1712806259465/661759fdfb491202fff58f9d/editor/661f2f7dcc137203042cdffc/?docLang=zh#6e312068) |
|  | merge_small_chunks | bool | 否 | true | **是否合并短文本片** <br> 配置是否对短文本片进行合并，且合并后的文本片会限制不超过切片最大长度 |
|  | multi_modal | list | 否 | -- | **图片理解策略** <br> 枚举值： <br>  <br> * "image_ocr"：图片 ocr <br>  <br> 传参示例： <br>  <br> * 当 "multi_modal": ["image_ocr"] 时，开启图片 ocr，不传值即代表不开启图片 ocr <br>  <br> 使用旧参数命名“multi_mode”创建的库仍保留原命名，但新创建知识库不推荐继续使用。 |
| **doc_summary_config** |  | object | 否 | -- | **知识库摘要配置** |
|  | enabled | bool | 否 | false | **是否开启文档 AI 摘要功能** <br> 配置知识库是否开启文档 AI 生成摘要功能，开启后，该知识库将自动为每篇文档生成摘要并保存结果到文档元信息中 |
# 向量化模型及索引算法对照表
| **创建知识库类型** | **向量化模型** | **模型版本** | **产出类型** | **索引类型** | **向量维度** | **量化方式** | **chunk_length 取值** | **检索类型** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 音视频知识库、 <br> 图像/富文本知识库 | doubao-embedding-vision | 250615（音视频知识库）、250328（图像/富文本知识库） | 稠密向量 | hnsw（默认）、flat | 1024、2048 <br> 默认2048 | int8（默认）、float、fix16 | [100, 4000] <br> 默认 2000 | 语义检索（字节自研模型） |
|  | doubao-embedding-vision-and-m3 | 250615（音视频知识库）、250328（图像/富文本知识库） | 稠密向量和稀疏向量 | hnsw_hybrid（默认） | 1024、2048 <br> 默认2048 | int8（默认）、float、fix16 | [100, 4000] <br> 默认 2000 | 混合检索（兼顾语义检索和关键词匹配） |
| 结构化知识库、 <br> 纯文本知识库 | bge-large-zh | -- | 稠密向量 | hnsw（默认）、flat | 1024 | int8（默认）、float、fix16 | [100, 500] <br> 默认 500 | 语义检索 |
|  | bge-m3 | -- | 稠密向量和稀疏向量 | hnsw_hybrid（默认） | 1024 | int8（默认）、float、fix16 | [100, 8000] <br> 默认 2000 | 混合检索（兼顾语义检索和关键词匹配） |
|  |  | -- |  | hnsw（默认）、flat | 1024 | int8（默认）、float、fix16 | [100, 8000] <br> 默认 2000 | 语义检索（此时稀疏向量被忽略，适用于只需要长文本窗口、多语言检索的纯语义检索场景） |
|  | bge-large-zh-and-m3 | -- | 稠密向量和稀疏向量 | hnsw_hybrid（默认） | 1024 | int8（默认）、float、fix16 | [100, 500] <br> 默认 500 | 混合检索（兼顾语义检索和关键词匹配） |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| data | 返回的详细信息 <br> { <br> "resource_id": 知识库 id <br> } |
| request_id | 标识每个请求的唯一标识符 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 403 | unauthorized | 鉴权失败 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request: %s | 非法参数 <br>  <br> * 缺失必选参数 <br> * collection 命名不符合规范 <br> * 字段类型与相关字段属性不满足约束条件 |
| 1000004 | 400 | collection exist | collection 已存在 |
# 完整示例
## 请求消息
创建结构化知识库
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/collection/create \
  -d '{
    "name": "apiexample",
    "description": "test",
    "index": {
        "index_type": "hnsw_hybrid",
        "index_config": {
            "fields": [],
            "quant": "int8",
            "cpu_quota": 1,
            "embedding_model": "doubao-embedding-and-m3",
            "embedding_dimension": 2048
        }
    },
    "table_config": {
        "table_type": "row",
        "table_pos": 1,
        "start_pos": 2,
        "table_fields": [
            {
                "field_type": "string",
                "field_name": "讲解模块",
                "if_embedding": true,
                "if_filter": false
            },
            {
                "field_type": "string",
                "field_name": "子模块",
                "if_embedding": true,
                "if_filter": false
            },
            {
                "field_type": "string",
                "field_name": "问题示例",
                "if_embedding": true,
                "if_filter": false
            },
            {
                "field_type": "string",
                "field_name": "记忆化 ————讲解要点",
                "if_embedding": true,
                "if_filter": false
            }
            

        ]
    },
    "data_type": "structured_data",
    "project": "default"
  }'
```

创建视频知识库
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/collection/create \
  -d '{
      "data_type": "unstructured_data",
      "description": "Video_XXX",
      "index": {
        "index_config": {
          "chunk_title_entity_extraction": false,
          "cpu_quota": 1,
          "embedding_dimension": 2048,
          "embedding_model": "doubao-embedding-vision-and-m3",
          "embedding_model_version": "250615",
          "field_enumerated_list": "{}",
          "fields": [
            {
              "field_name": "doc_id",
              "field_type": "string"
            }
          ],
          "quant": "int8"
        },
        "index_type": "hnsw_hybrid"
      },
      "name": "Video_XXX",
      "preprocessing": {
        "chunk_length": 2000,
        "chunking_strategy": "custom_balance",
        "enable_slice_analysis": true,
        "enable_smart_summary": true,
        "merge_small_chunks": true,
        "video_chunking_strategy": "smart_slice",
        "video_max_length": 180
      }
    }
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
    "data": {
        "resource_id": "kb-8349ef57441ab57"
    },
    "request_id":"021695029537650fd001de666660000000000000000000230da93"
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request: %s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


