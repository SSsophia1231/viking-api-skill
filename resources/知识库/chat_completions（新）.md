由于大模型底层架构升级，知识库同步兼容适配，chat_completions API 用法和影响如下：
1、若原本使用公共接入点调用 Doubao 模型，无影响
2、若原本使用私有接入点调用 Doubao 模型，需要额外上传 API key 参数，否则会自动调度到**公共 EP 上（此时计费项和折扣会走知识库商品）**

本节将说明如何基于多轮历史对话，使用大语言模型进行回答生成
# 概述
/api/knowledge/chat/completions 接口用于向大模型发起一次对话请求，需与新升级的 search_knowledge 接口配合使用，可以完成标准的检索生成链路。
本接口对 Doubao 大模型 chat/completions 接口全面兼容。
# **前提条件**

* 知识库创建完成。
* 文档导入且处理完成。
* 完成“对接指南”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现知识库检索查询并调用大模型整合生成回答的功能。
* 进行本地 Prompt 组装拼接

# **请求接口**
| **URI** | /api/knowledge/chat/completions | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对向量数据库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 鉴权 |
# **请求参数**
| **参数** | **子参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- | --- |
| model | -- | String | 是 | Doubao-1-5-pro-32k | **想要用于在线生成的大模型** <br>  <br> * 当指定为 doubao 系列模型时默认使用系统的公共推理接入点，适合调试场景，有 TPM 限流 <br> * 或指定为在方舟上创建的推理接入点 ID，适合生产场景，TPM 配置可在创建推理接入点时自行调整 <br>  <br> 公共推理接入点模型可选范围详见下表。 <br> 私有推理接入点 ID 形如： <br>  <br> * ep-202406040*****-***** <br>  <br> 注意当使用私有接入点时，需要配合传入 API key 进行鉴权 <br> > 注：默认值可能随版本更新而变化。为确保产品效果稳定，建议用户指定模型版本 |
| model_version | -- | string | 否 | -- | 对话模型和图像理解模型的可选范围详见下表。 |
| thinking | -- | json | 否 | enabled | **控制模型是否开启深度思考模式** <br> 取值范围： <br>  <br> * enabled：开启思考模式，模型一定先思考后回答。 <br> * disabled：关闭思考模式，模型直接回答问题，不会进行思考。 <br> * auto：自动思考模式，模型根据问题自主判断是否需要思考，简单题目直接回答。 <br>  <br> 当前支持的模型详情见：[thinking](https://www.volcengine.com/docs/82379/1449737#%E5%85%B3%E9%97%AD%E6%B7%B1%E5%BA%A6%E6%80%9D%E8%80%83) <br> **示例：** <br> ```Bash <br>  <br>     extra_body={ <br>         "thinking": { <br>             "type": "disabled",  # 不使用深度思考能力 <br>             # "type": "enabled", # 使用深度思考能力 <br>             # "type": "auto", # 模型自行判断是否使用深度思考能力 <br>         } <br>     } <br> ``` <br>  |
| api_key | -- | string | 否 | -- | **接入点 API Key** <br> 当需要使用私有模型接入点时，需传入对应 API key 进行鉴权 |
| messages | -- | json | 是 | -- | 发出消息的对话参与者角色，可选值包括： <br>  <br> * system：System Message 系统消息 <br> * user：User Message 用户消息 <br> * assistant：Assistant Message 对话助手消息 <br>  <br> **多轮文本问答**： 串联脚本示例可参考[知识库多轮检索问答样例](https://www.volcengine.com/docs/84313/1392553?lang=zh) <br> ```JSON <br> [ <br>     {"role": "system", "content": "你是一位在线客服，你的首要任务是通过巧妙的话术回复用户的问题，你需要根据「参考资料」来回答接下来的「用户问题」，这些信息在 <context></context> XML tags 之内，你需要根据参考资料给出准确，简洁的回答。"}, <br>     {"role": "user", "content": "推荐一个适合 3 岁小孩的玩具"}, <br>     {"role": "assistant", "content": "您好！3 岁宝宝正处于身体、智力、情感多方面快速发展的阶段，您可以看看以下几款类型的玩具：乐高积木、拼图、消防局与消防直升机套装、医疗玩具套装、儿童滑板车"} <br>     {"role": "user", "content": "详细介绍下乐高积木有哪些合适的系列"}, <br> ] <br> ``` <br>  <br> **多轮图文理解**：串联脚本示例可参考[知识库图文问答样例](https://www.volcengine.com/docs/84313/1403979?lang=zh) <br> ```Plain <br> [ <br>     { <br>         "role": "system", <br>         "content": "你是一位在线客服，你的首要任务是通过巧妙的话术回复用户的问题，你需要根据「参考资料」来回答接下来的「用户问题」，这些信息在 <context></context> XML tags 之内，你需要根据参考资料给出准确，简洁的回答。参考资料中可能会包含图片信息，图片的引用说明在<img></img>XML tags 之内，参考资料内的图片顺序与用户上传的图片顺序一致。" <br>     }, <br>     { <br>         "role": "user", <br>         "content": [ <br>             { <br>                 "type": "text", <br>                 "text": "推荐一个适合 3岁小孩的玩具" <br>             }, <br>             { <br>                 "type": "image_url", <br>                 "image_url": { <br>                     "url": "https://ark-project.tos-cn-beijing.volces.XXX.jpeg" #从知识库中召回的 top1 图片 url <br>                 } <br>             }, <br>             { <br>                 "type": "image_url", <br>                 "image_url": { <br>                     "url": "https://ark-project.tos-cn-beijing.volces.XXX.jpeg" #从知识库中召回的 top2 图片 url <br>                 } <br>             } <br>         ] <br>     } <br> ] <br> ``` <br>  |
| stream | -- | Boolean | 否 | False | **响应内容是否流式返回** <br>  <br> * false：模型生成完所有内容后一次性返回结果 <br> * true：按 SSE 协议逐块返回模型生成内容，并以一条 data: [DONE] 消息结束 |
| max_tokens | -- | Integer | 否 | 4096 | **模型可以生成的最大 token 数量** <br> > 注意 <br>  <br> > * **模型回复最大长度（单位 token），取值范围各个模型不同，详细见**[模型列表](https://www.volcengine.com/docs/82379/1330310)**。** <br> > * **输入 token 和输出 token 的总长度还受模型的上下文长度限制。** |
| return_token_usage | -- | Boolean | 否 | False | **是否返回token用量统计** |
| temperature | -- | Float | 否 | 0.1 | **采样温度** <br> 控制了生成文本时对每个候选词的概率分布进行平滑的程度。取值范围为 [0, 1]。当取值为 0 时模型仅考虑对数概率最大的一个 token。 <br> 较高的值（如 0.8）会使输出更加随机，而较低的值（如 0.2）会使输出更加集中确定。通常建议仅调整 temperature 或 top_p 其中之一，不建议两者都修改。 |
## **对话模型**
| 模型名称 | 可选版本 |
| --- | --- |
| Doubao-1-5-pro-32k | 250115, character-250715 |
| Doubao-1-5-lite-32k | 250115 |
## **图像理解模型**
| 模型名称 | 可选版本 |
| --- | --- |
| Doubao-seed-2-0-pro | 260215 |
| Doubao-seed-2-0-lite | 260215 |
| Doubao-seed-2-0-mini | 260215 |
| Doubao-seed-1-8 | 251228 |
| Doubao-seed-1-6-vision | 250815 |
| Doubao-seed-1-6 | 251015, 250615 |
| Doubao-seed-1-6-flash | 250828, 250615 |
| Doubao-1-5-vision-pro-32k | 250115 |
方舟模型下线说明：[https://www.volcengine.com/docs/82379/1350667?lang=zh](https://www.volcengine.com/docs/82379/1350667?lang=zh)
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
| request_id | 标识每个请求的唯一标识符 |
| data | 模型回答与token用量统计 |
data返回值
| 字段 | 子字段 | 字段类型 | 说明 |
| --- | --- | --- | --- |
| reasoning_content | -- | string | 模型处理问题的思维链内容 <br> > 支持返回此字段的模型：DeepSeek-R1 |
| generated_answer | -- | string | 大模型最终回答 |
| usage | -- | string | token用量统计 |
## **状态码说明**
| **状态码** | **http状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- | --- |
| 0 | 200 | success | 成功 |
| 1000001 | 401 | unauthorized | 缺乏鉴权信息 |
| 1000002 | 403 | no permission | 权限不足 |
| 1000003 | 400 | invalid request：%s | 非法参数 |
# 完整示例
## 请求消息
```Shell
curl -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'Authorization: HMAC-SHA256 ***' \
  https://api-knowledgebase.mlp.cn-beijing.volces.com/api/knowledge/chat/completions \
  -d '{
        "model": "Doubao-1-5-pro-32k",
        "max_tokens": 4096,
        "temperature": 0.1,
        "messages": [
                {
                    "role": "system",
                    "content": "prompt template"
                },
                {
                    "role": "user",
                    "content": "history content"
                },
                {
                    "role": "assistant",
                    "content": "history content"
                },
                {
                    "role": "user",
                    "content": "history content"
                },
                ...
           
                {
                    "role": "assistant",
                    "content": "history content"
                }         
            ],
        "stream": false,
        "return_token_usage": true
}'
```

## 响应消息
执行成功返回：
```Shell
HTTP/1.1 200 OK
Content-Length: 209
Content-Type: text/event-stream

{
    "code": 0,
    "data": {
        "generated_answer": "HNSW（Hierarchical Navigable Small World）是一种用于高效近似最近邻搜索的数据结构和算法。\n\n它具有以下特点和优势：\n1. **高效性**：能够在大规模数据集中快速找到近似最近邻。\n2. **可扩展性**：适用于处理海量数据。\n3. **准确性**：提供相对准确的最近邻搜索结果。\n4. **层次结构**：通过构建层次结构来加速搜索过程。\n5. **小世界特性**：利用数据的局部性和相似性，提高搜索效率。\n\nHNSW 在许多领域有广泛的应用，例如：\n1. **图像检索**：快速找到相似的图像。\n2. **推荐系统**：推荐相关的产品或内容。\n3. **数据挖掘**：发现相似的数据点。\n4. **机器学习**：在特征空间中进行相似性搜索。\n\n总之，HNSW 是一种强大的工具，用于解决大规模数据集中的最近邻搜索问题。",
        "usage": "{\"prompt_tokens\":13,\"completion_tokens\":217,\"total_tokens\":230}\n"
    },
    "message": "success",
    "request_id": "02172742276364600000000000000000000ffff0a00406fa14e0d"
    
}
```

执行失败返回：
```Shell
HTTP/1.1 400 Bad Request
Content-Length: 43
Content-Type: application/json
 
{"code":1000003, "message":"invalid request：%s", "request_id": "021695029757920fd001de6666600000000000000000002569b8f"}
```


