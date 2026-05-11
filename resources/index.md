# Viking 知识库 API 参考导引

本文件是 `viking-api` skill 的统一导引首页。

处理本 skill 相关的任何需求时，优先从这里按模块选择对应的 API 文档，再进入具体文档阅读。

## 使用方式

- 需要查询某个 API 接口时，按模块找到对应文档并阅读。
- 需要鉴权、签名、私网接入等基础配置时，进入"基础配置"部分。
- 如果用户问题涉及已下线或即将下线的接口，优先推荐新版接口，同时告知旧接口状态。

---

## 基础配置

| 文档 | 说明 |
|------|------|
| [签名鉴权与调用示例](签名鉴权与调用示例.md) | AK/SK 获取、签名计算方式、多语言调用示例 |
| [知识库私网连接方式](知识库私网连接方式.md) | 私网接入配置 |

---

## 知识库（Collection）

管理知识库实例的增删改查及检索、问答能力。

| 文档 | 接口 | 说明 |
|------|------|------|
| [create](知识库/create.md) | CreateCollection | 创建知识库 |
| [delete](知识库/delete.md) | DeleteCollection | 删除知识库 |
| [info](知识库/info.md) | GetCollection | 查询知识库详情 |
| [list](知识库/list.md) | ListCollections | 查询知识库列表 |
| [update](知识库/update.md) | UpdateCollection | 更新知识库配置 |
| [search_collection](知识库/search_collection.md) | SearchCollection | 在知识库中检索（推荐） |
| [search_knowledge（新）](知识库/search_knowledge（新）.md) | SearchKnowledge | 知识检索新版接口（推荐） |
| [chat_completions（新）](知识库/chat_completions（新）.md) | ChatCompletions | 知识库对话补全新版接口（推荐） |
| [search（即将下线）](知识库/search（即将下线）.md) | Search | 旧版检索接口，即将下线 |
| [search_and_generate（即将下线）](知识库/search_and_generate（即将下线）.md) | SearchAndGenerate | 旧版检索+生成接口，即将下线 |

### 知识库使用样例

| 文档 | 说明 |
|------|------|
| [图文问答样例](知识库/知识库图文问答样例.md) | 图文混合内容问答示例 |
| [多轮检索问答样例](知识库/知识库多轮检索问答样例.md) | 多轮对话检索问答示例 |
| [视频问答样例](知识库/知识库视频问答样例.md) | 视频内容问答示例 |
| [输出图文混排样例](知识库/知识库输出图文混排样例.md) | 图文混排输出示例 |

---

## 文档（Doc）

管理知识库中文档的上传、查询、更新与删除。

| 文档 | 接口 | 说明 |
|------|------|------|
| [add（新）](文档/add（新）.md) | AddDoc v2 | 上传文档新版接口（推荐） |
| [add](文档/add.md) | AddDoc | 上传文档旧版接口 |
| [delete](文档/delete.md) | DeleteDoc | 删除文档 |
| [info](文档/info.md) | GetDoc | 查询文档详情 |
| [list（新）](文档/list（新）.md) | ListDocs v2 | 查询文档列表新版接口（推荐） |
| [list](文档/list.md) | ListDocs | 查询文档列表旧版接口 |
| [update](文档/update.md) | UpdateDoc | 更新文档内容 |
| [update_meta](文档/update_meta.md) | UpdateDocMeta | 更新文档元数据 |
| [search_by_filter](文档/search_by_filter.md) | SearchDocsByFilter | 按过滤条件检索文档 |
| [文档处理报错处理手册](文档/文档处理报错处理手册.md) | — | 文档解析与处理常见错误排查 |

---

## 切片（Point）

管理文档切片的增删改查。

| 文档 | 接口 | 说明 |
|------|------|------|
| [add](切片/add.md) | AddPoint | 添加切片 |
| [delete](切片/delete.md) | DeletePoint | 删除切片 |
| [info](切片/info.md) | GetPoint | 查询切片详情 |
| [list（新）](切片/list（新）.md) | ListPoints v2 | 查询切片列表新版接口（推荐） |
| [list](切片/list.md) | ListPoints | 查询切片列表旧版接口 |
| [update](切片/update.md) | UpdatePoint | 更新切片 |

---

## 知识服务（Service）

管理知识服务实例及对话能力。

| 文档 | 接口 | 说明 |
|------|------|------|
| [chat（推荐）](知识服务/chat（推荐）.md) | Chat | 知识服务对话接口（推荐） |
| [list](知识服务/list.md) | ListServices | 查询知识服务列表 |

---

## 下载

| 文档 | 接口 | 说明 |
|------|------|------|
| [download](下载/download.md) | Download | 下载文件 |
| [info](下载/info.md) | GetDownloadInfo | 获取下载信息 |

---

## 实验版本（新）

Pipeline 相关的实验性新接口，功能持续迭代中。

| 文档 | 接口 | 说明 |
|------|------|------|
| [create](实验版本（新）/create.md) | CreatePipeline | 创建 Pipeline |
| [delete](实验版本（新）/delete.md) | DeletePipeline | 删除 Pipeline |
| [info](实验版本（新）/info.md) | GetPipeline | 查询 Pipeline 详情 |
| [list](实验版本（新）/list.md) | ListPipelines | 查询 Pipeline 列表 |
| [update](实验版本（新）/update.md) | UpdatePipeline | 更新 Pipeline |
| [re-process](实验版本（新）/re-process.md) | ReProcess | 重新处理 |
| [batch-to-pipeline](实验版本（新）/batch-to-pipeline.md) | BatchToPipeline | 批量导入到 Pipeline |
| [set-default-pipeline](实验版本（新）/set-default-pipeline.md) | SetDefaultPipeline | 设置默认 Pipeline |

---

## 其他能力

| 文档 | 说明 |
|------|------|
| [Rerank 重排](Rerank重排.md) | 检索结果重排序 API |
