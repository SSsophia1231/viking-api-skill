# viking-api-skill

Viking 知识库 HTTP API 参考文档，覆盖知识库、文档、切片、知识服务、下载、Pipeline 等全部模块，可集成到各类 AI Agent 工具中使用。

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
/viking-api 如何调用 search_knowledge 接口？
/viking-api 签名鉴权怎么做？
/viking-api Pipeline create 接口的参数有哪些？
```

skill 每次调用时会自动检查并同步最新版本的文档。

## 在其他 Agent 中使用

本仓库的文档以 Markdown 格式存放在 `resources/` 目录下，导引入口为 `resources/index.md`。

任何支持读取文件或 GitHub 内容的 Agent，均可直接引用 `resources/index.md` 作为 Viking 知识库 API 的导航起点。

## License

Apache-2.0
