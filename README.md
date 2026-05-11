# viking-api-skill

Viking 知识库 HTTP API 参考文档，覆盖知识库、文档、切片、知识服务、下载、实验版本 等全部模块，可集成到各类 AI Agent 工具中使用，帮助快速撰写脚本，完成知识库能力集成。

## 包含内容

- 签名鉴权与 AK/SK 配置
- 知识库（Collection）增删改查、检索、对话补全
- 文档（Doc）上传、查询、更新、按条件检索
- 切片（Point）增删改查
- 知识服务（Service）对话接口
- 文件下载
- Pipeline 实验版本接口
- Rerank 重排

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

## License

Apache-2.0
