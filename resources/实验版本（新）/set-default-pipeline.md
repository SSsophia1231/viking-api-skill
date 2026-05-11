# 概述
api/knowledge/collection/set-default-pipeline 接口用于将 [实验版本](https://www.volcengine.com/docs/84313/1510752)（pipeline）设置为正式版本，此接口仅供前端调用。
**前提条件**

1. 完成“签名鉴权方式”页面的注册账号、实名认证、AK/SK 密钥获取和签名获取后，可调用 API 接口实现知识库的创建功能。
2. **实验版本的文档数需与正式版本一致才能设置为正式版本**

# **请求接口**
| **URI** | /api/knowledge/collection/set-default-pipeline | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端向服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: token=********** | 鉴权 |
# **请求参数**
| **参数** | **类型** | **是否必选** | **默认值** | **参数说明** |
| --- | --- | --- | --- | --- |
| name | string | 否 | -- | **知识库名称** |
| project | string | 否 | default | **知识库所属项目名称** <br> 获取方式参见文档[API 接入与技术支持](/docs/84313/1606319#1ab381b9) |
| resource_id | string | 否 | -- | **知识库的唯一 ID** <br> 可选择直接传 resource_id，或同时传 name 和 project 作为知识库的唯一标识 |
| new_default_pipeline_name | string | 是 | -- | 设置对应名称的实验版本为正式版本 |
| old_pipeline_name | string | 是 | -- | 为原正式版本设置新名称 <br>  <br> * 新名称不能设置为系统的默认值“default” <br> * 实验版本名称由字母、数字、下划线组成，并只能以字母开头 <br> * 长度不超过 128 个字符 |
# **响应消息**
| **参数** | **参数说明** |
| --- | --- |
| code | 状态码 |
| message | 返回信息 |
## **状态码说明**
| **状态码** | **返回信息** | **状态码说明** |
| --- | --- | --- |
| 0 | success | 成功 |
| 1000001 | unauthorized | 鉴权失败 |
| 1000002 | no permission | 权限不足 |
| 1000003 | invalid request：%s | **非法参数** <br>  <br> * 缺失必选参数 <br> * collection 命名不符合规范 <br> * 字段类型与相关字段属性不满足约束条件 |

