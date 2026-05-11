# viking-api-skill

帮助开发者快速接入 Viking 知识库 HTTP API。内置完整 API 参考文档，覆盖 Viking 知识库、文档、切片、知识服务、下载、实验版本 等全部模块，可直接生成调用脚本，无需手查文档。

产品官方文档：https://www.volcengine.com/docs/84313/2117716?lang=zh

## 能做什么

- 根据需求生成完整的调用脚本（Python / Go / Java / curl 等）
- 处理签名鉴权，补全请求参数，避免手查文档
- 覆盖知识库创建、文档上传与解析、向量检索、RAG 问答等端到端流程
- 定位接口报错、解释响应字段、给出修复建议

## 在 Claude Code 中使用

```bash
npm install -g viking-api-skill
```

安装后在 Claude Code 中直接输入 `/viking-api` 触发，例如：

```
/viking-api 帮我用 Python 写一个上传文档并轮询解析状态的脚本
/viking-api 用 Go 实现签名鉴权，并调用 search_knowledge 接口
/viking-api 写一个 curl 脚本，创建知识库并批量上传文档
/viking-api 帮我封装一个 Python 类，覆盖知识库的增删改查
```

skill 每次调用时会自动检查并同步最新版本的文档。
