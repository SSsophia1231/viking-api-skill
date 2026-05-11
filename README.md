# viking-api-skill

Viking 知识库 HTTP API 参考文档的 Claude Code Skill，覆盖知识库、文档、切片、知识服务、下载、Pipeline 等全部模块。

## 安装

```bash
npm install -g viking-api-skill
```

安装后 skill 自动复制到 `~/.claude/skills/viking-api/`，在 Claude Code 中直接使用 `/viking-api` 触发。

## 使用

在 Claude Code 中：

```
/viking-api 如何调用 search_knowledge 接口？
/viking-api 签名鉴权怎么做？
/viking-api Pipeline create 接口的参数有哪些？
```

## 更新

文档随版本迭代。skill 每次被调用时会自动检查并同步最新版本。

也可手动更新：

```bash
npm update -g viking-api-skill
```

## 发版说明（维护者）

每次文档更新后：

```bash
# 1. 更新 resources/ 下的文档文件
# 2. 生成版本元数据
python3 scripts/build_release.py 1.x.x
# 3. 同步 package.json 版本号后提交
git add -A
git commit -m "docs: v1.x.x"
git tag v1.x.x
git push origin main --tags
# 4. 发布到 npm
npm version 1.x.x
npm publish
```
