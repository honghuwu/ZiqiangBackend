# API 简表

本文档只描述当前后端已实现接口。

## 基础说明

- 认证方式：SessionAuthentication
- 除明确标注 `AllowAny` 的接口外，默认都需要登录
- 响应默认分页，列表接口通常返回：

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": []
}
```

## 1. 用户系统 `api/user`

### 注册与登录

| 接口 | 方法 | 说明 | 权限 |
|---|---|---|---|
| `/api/user/send-register-code/` | `POST` | 发送注册验证码 | `AllowAny` |
| `/api/user/register/` | `POST` | 注册账号 | `AllowAny` |
| `/api/user/login/` | `POST` | 登录 | `AllowAny` |
| `/api/user/logout/` | `POST` | 登出 | 已登录 |

### 个人资料

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/user/me/profile/` | `GET` | 获取当前用户资料 |
| `/api/user/me/profile/` | `PUT/PATCH` | 修改当前用户资料 |

当前返回字段：

```json
{
  "id": 1,
  "name": "张三",
  "student_id": "2023001",
  "class_name": "自强书院2023级1班",
  "phone": "13800138000",
  "wechat_id": "zhangsan_wechat",
  "bio": "个人简介",
  "role": "student",
  "email": "student@example.com"
}
```

只读字段：

- `student_id`
- `role`
- `email`

### 密码与邮箱

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/user/change-password/` | `POST` | 修改密码 |
| `/api/user/send-change-email-code/` | `POST` | 发送改邮箱验证码 |
| `/api/user/change-email/` | `POST` | 修改邮箱 |

### 角色说明

- `student`
- `teacher`
- `admin`

说明：

- 普通注册仅允许 `student` / `teacher`
- `admin` 由后端 / 管理后台配置

## 2. 项目系统 `api/event`

### 公开项目接口

| 接口 | 方法 | 说明 | 权限 |
|---|---|---|---|
| `/api/event/events/` | `GET` | 项目公开列表 | `AllowAny` |
| `/api/event/events/<id>/` | `GET` | 项目公开详情 | `AllowAny` |

说明：

- 草稿项目不会公开
- 已关闭 / 历史项目可见，但草稿仅教师本人和管理员可见

### 教师项目管理

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/event/teacher/events/` | `GET` | 教师 / 管理员项目列表 |
| `/api/event/teacher/events/` | `POST` | 创建草稿项目 |
| `/api/event/teacher/events/<id>/` | `GET` | 查看项目详情 |
| `/api/event/teacher/events/<id>/` | `PUT/PATCH` | 更新项目 |
| `/api/event/teacher/events/<id>/` | `DELETE` | 删除草稿项目 |
| `/api/event/teacher/events/<id>/publish/` | `POST` | 发布项目 |
| `/api/event/teacher/events/<id>/close/` | `POST` | 关闭项目 |

### 项目状态规则

- `draft`
  - 草稿
  - 可删除
  - 可发布
- `published`
  - 已发布且未开始
  - 可接收申请
  - 可关闭
- `ongoing`
  - 已开始进行中
  - 不可关闭
- `closed`
  - 手动关闭或历史项目
  - 不可编辑

### 项目返回字段示例

```json
{
  "id": 1,
  "title": "后端招新项目",
  "event_type": "科研",
  "start_time": "2026-03-10T10:00:00+08:00",
  "end_time": "2026-03-20T18:00:00+08:00",
  "location": "主楼101",
  "description": "项目简介",
  "attachment": {
    "id": "2c6db4a1-20f0-4e6a-b89e-1aa9b9d4d48d",
    "original_name": "project-material.zip",
    "category": "event_attachment",
    "file_url": "http://127.0.0.1:8000/api/file/uploads/2c6db4a1-20f0-4e6a-b89e-1aa9b9d4d48d/download/"
  },
  "expected_participants": 10,
  "current_participants": 3,
  "status": "published",
  "teacher": 2,
  "teacher_name": "李老师",
  "can_delete": false,
  "can_publish": false,
  "can_close": true,
  "pending_applications_count": 5
}
```

### 创建 / 更新项目请求示例

```json
{
  "title": "后端招新项目",
  "event_type": "科研",
  "start_time": "2026-03-10T10:00:00+08:00",
  "end_time": "2026-03-20T18:00:00+08:00",
  "location": "主楼101",
  "description": "项目简介",
  "expected_participants": 10,
  "attachment_id": "2c6db4a1-20f0-4e6a-b89e-1aa9b9d4d48d"
}
```

### 项目列表筛选

适用于：

- `/api/event/events/`
- `/api/event/teacher/events/`

支持参数：

- `status=draft|published|ongoing|closed`
- `teacher_name=<keyword>`
- `can_recruit=true|false`

## 3. 申请系统 `api/event`

### 学生申请

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/event/events/<event_id>/apply/` | `POST` | 提交项目申请 |
| `/api/event/my-applications/` | `GET` | 我的申请列表 |
| `/api/event/my-applications/<id>/` | `GET` | 我的申请详情 |

说明：

- 学生不能撤回申请
- 满员项目不能提交新申请
- 同一学生不能重复提交待审核 / 已通过申请

### 教师审批

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/event/teacher/applications/` | `GET` | 教师 / 管理员查看申请列表 |
| `/api/event/teacher/applications/<id>/approve/` | `POST` | 审批通过 |
| `/api/event/teacher/applications/<id>/reject/` | `POST` | 审批拒绝 |

说明：

- 只能逐条审批
- 项目开始前可改判
- 项目开始后不能再改判
- 教师不能删除申请，只能拒绝

### 申请状态

- `pending`
- `approved`
- `rejected`
- `cancelled`

### 提交申请请求示例

```json
{
  "statement": "我想参加这个项目",
  "resume_id": "1d838e1e-98f8-42c0-9cf0-3b7de35cf6ec"
}
```

### 申请对象示例

```json
{
  "id": 1,
  "event": 1,
  "event_title": "后端招新项目",
  "student": 3,
  "student_name": "张三",
  "student_id": "2023001",
  "student_email": "student@example.com",
  "statement": "我想参加这个项目",
  "resume": {
    "id": "1d838e1e-98f8-42c0-9cf0-3b7de35cf6ec",
    "original_name": "resume.pdf",
    "category": "application_resume",
    "file_url": "http://127.0.0.1:8000/api/file/uploads/1d838e1e-98f8-42c0-9cf0-3b7de35cf6ec/download/"
  },
  "status": "pending",
  "review_note": "",
  "reviewed_at": null,
  "created_at": "2026-03-01T10:00:00+08:00",
  "updated_at": "2026-03-01T10:00:00+08:00"
}
```

### 申请列表筛选

适用于：

- `/api/event/my-applications/`
- `/api/event/teacher/applications/`

支持参数：

- `event=<event_id>`
- `status=pending|approved|rejected|cancelled`

## 4. 文件系统 `api/file`

### 文件上传与读取

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/file/uploads/` | `POST` | 上传文件 |
| `/api/file/my-files/` | `GET` | 我的文件列表 |
| `/api/file/uploads/<uuid>/` | `GET` | 文件详情 |
| `/api/file/uploads/<uuid>/` | `DELETE` | 删除文件 |
| `/api/file/uploads/<uuid>/download/` | `GET` | 下载文件 |

### 模板文件

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/file/templates/` | `GET` | 可用模板列表 |
| `/api/file/templates/<key>/` | `GET` | 模板详情 |

### 管理员模板管理

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/file/admin/templates/` | `GET` | 模板管理列表 |
| `/api/file/admin/templates/` | `POST` | 创建模板绑定 |
| `/api/file/admin/templates/<key>/` | `GET` | 模板详情 |
| `/api/file/admin/templates/<key>/` | `PATCH` | 更新模板 |
| `/api/file/admin/templates/<key>/` | `DELETE` | 停用模板 |

### 文件分类

- `event_attachment`
- `application_resume`
- `template`
- `other`

### 文件删除规则

- 文件使用 `UUID`
- 未被引用可删除
- 被以下对象引用时不可删除：
  - `FileTemplate`
  - `Event.attachment`
  - `EventApplication.resume`

### 文件返回示例

```json
{
  "id": "2c6db4a1-20f0-4e6a-b89e-1aa9b9d4d48d",
  "original_name": "project-material.zip",
  "category": "event_attachment",
  "content_type": "application/zip",
  "file_size": 10240,
  "description": "项目附件",
  "file_url": "http://127.0.0.1:8000/api/file/uploads/2c6db4a1-20f0-4e6a-b89e-1aa9b9d4d48d/download/",
  "is_referenced": false,
  "can_delete": true,
  "created_at": "2026-03-01T10:00:00+08:00",
  "updated_at": "2026-03-01T10:00:00+08:00"
}
```

## 5. 通知系统 `api/notification`

说明：

- 通知代码已实现
- 当前默认不触发通知，除非开启：

```env
ENABLE_NOTIFICATIONS=True
```

### 通知接口

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/notification/my/` | `GET` | 我的通知列表 |
| `/api/notification/my/<id>/` | `GET` | 通知详情 |
| `/api/notification/my/<id>/read/` | `POST` | 单条标记已读 |
| `/api/notification/my/read-all/` | `POST` | 全部标记已读 |

### 通知类型

- `event_application_submitted`
- `event_application_approved`
- `event_application_rejected`

### 通知筛选

支持参数：

- `is_read=true|false`
