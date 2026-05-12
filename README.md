# 自强书院后端

## 项目概述

这是一个基于 Django + DRF 的后端项目，当前已经实现三条主线：

- 用户系统 `user`
  - 本地注册登录
  - 个人资料管理
  - 学生 / 教师 / 管理员角色
- 项目与申请系统 `event`
  - 教师发布项目、管理项目
  - 学生提交申请
  - 教师审批申请
- 文件系统 `file`
  - 使用 `UUID` 管理文件
  - 文件上传、下载、删除
  - 模板文件管理

另外已经预留了站内通知系统 `notification`，但当前默认关闭，不会主动触发通知。

## 技术栈

- Python 3.9
- Django 4.2.26
- Django REST Framework
- SQLite3
  - 仅建议用于当前开发阶段
  - 后续推荐迁移到 PostgreSQL

## 开发环境要求

请使用 conda 的 `py39` 虚拟环境，不要直接使用 `base` 环境。

```bash
conda activate py39
```

环境变量模板见 [`.env.example`](/e:/involuntary/works/ziqiangPlatform/.env.example)。

## 当前 App 说明

### `apps.user`

提供：

- 注册验证码
- 用户注册
- 登录 / 登出
- 个人资料查询与修改
- 修改密码
- 修改邮箱

说明：

- `role` 当前支持 `student`、`teacher`、`admin`
- 普通注册仅允许 `student` / `teacher`
- `admin` 不允许前端自注册
- `me/profile` 会返回 `email`，但 `email` 只读，修改邮箱必须走单独接口

### `apps.event`

提供：

- 项目公开列表 / 详情
- 教师项目管理
- 项目发布 / 关闭 / 删除草稿
- 学生申请
- 教师审批申请
- 项目和申请的筛选查询

说明：

- 草稿项目可以删除
- 已发布但未开始的项目可以关闭
- 已开始或历史项目不能删除 / 关闭
- 历史项目统一视为 `closed`
- 申请不可撤回
- 教师只能逐条审批，不能批量批准

### `apps.file`

提供：

- 文件上传
- 文件详情
- 受权限保护的文件下载
- 我的文件列表
- 模板文件列表
- 管理员模板管理

说明：

- 文件主键使用 `UUID`
- 文件不直接暴露原始 `media` 路径
- `file_url` 返回的是后端下载接口
- 已被引用的文件不能删除

### `apps.notification`

提供：

- 我的通知列表
- 通知详情
- 单条已读
- 全部已读

说明：

- 当前默认关闭通知触发
- 通过 `ENABLE_NOTIFICATIONS=True` 可启用

## 文件系统设计

文件系统当前有两个核心模型：

- `ManagedFile`
  - 统一文件中心
  - 用 `UUID` 管理文件
  - 记录分类、原始文件名、大小、类型、上传者等信息
- `FileTemplate`
  - 固定模板文件
  - 例如申请表模板
  - 只允许管理员管理

文件分类目前为：

- `event_attachment`
- `application_resume`
- `template`
- `other`

## 上传规则

### 文件类型与大小白名单

- `event_attachment`
  - 允许：`.zip`、`.rar`、`.7z`、`.pdf`、`.doc`、`.docx`
  - 最大：`100MB`
- `application_resume`
  - 允许：`.pdf`、`.doc`、`.docx`、`.zip`
  - 最大：`20MB`
- `template`
  - 允许：`.pdf`、`.doc`、`.docx`、`.zip`
  - 最大：`20MB`
- `other`
  - 允许：`.zip`、`.rar`、`.7z`、`.pdf`、`.doc`、`.docx`、`.txt`、`.md`、`.png`、`.jpg`、`.jpeg`
  - 最大：`50MB`

### 文件引用关系

当前文件会被这些地方引用：

- 项目附件 `Event.attachment`
- 申请简历 `EventApplication.resume`
- 模板文件 `FileTemplate.file`

只要文件被以上任一对象引用，就不能删除。

## 通知系统说明

通知代码已经存在，但当前默认不启用。

配置项：

```env
ENABLE_NOTIFICATIONS=False
```

启用后，会触发以下通知：

- 学生提交申请 -> 通知老师
- 教师审批通过 / 拒绝 -> 通知学生

## 测试

建议在 `py39` 环境中运行：

```bash
conda activate py39
python manage.py test apps.user --verbosity=2
python manage.py test apps.event --verbosity=2
python manage.py test apps.file --verbosity=2
python manage.py test apps.notification --verbosity=2
```

## 下一步建议

- 前端对接现有接口
- 评估并准备从 SQLite 迁移到 PostgreSQL
- 如果要启用消息提示，再打开 `ENABLE_NOTIFICATIONS`
- 视需要补接口审计和存储统计命令

## 相关文档

- [QUICKSTART.md](/e:/involuntary/works/ziqiangPlatform/QUICKSTART.md)
- [API_SIMPLE.md](/e:/involuntary/works/ziqiangPlatform/API_SIMPLE.md)
