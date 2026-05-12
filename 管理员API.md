# 管理员管理 API 文档

## 概述

管理员管理 API 提供唯一管理员账号的后台管理能力，包括用户管理、项目管理、文件管理等。

- 基础路径: `/api/admin/`
- 认证方式: Session 认证（Cookie + CSRF Token）
- 权限要求: 仅 `role=admin` 的用户可访问

---

## 0. 首次初始化管理员账号

管理员账号通过 `.env` 文件配置，通过管理命令创建。

### 0.1 配置凭据

编辑项目根目录下的 `.env` 文件：

```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123456
ADMIN_EMAIL=admin@example.com
```

### 0.2 创建管理员

```bash
python manage.py createsuperadmin
```

如果管理员账号已存在，该命令会**重置密码并确保角色为 admin**。

### 0.3 登录

```
POST /api/admin/login/
```

```json
{
    "student_id": "admin",
    "password": "admin123456"
}
```

---

## 1. 认证接口

### 1.1 管理员登录

```
POST /api/admin/login/
```

**Request:**
```json
{
    "student_id": "admin001",
    "password": "admin_password",
    "remember_me": false
}
```

**Response (200):**
```json
{
    "detail": "Login successful",
    "role": "admin"
}
```

**Response (400):**
```json
{
    "detail": "Invalid credentials or insufficient permissions"
}
```

说明: 只有 `role=admin` 的用户才能通过此接口登录成功。普通用户调用此接口会被拒绝。

---

### 1.2 管理员登出

```
POST /api/admin/logout/
```

**Response (200):**
```json
{
    "detail": "Logged out"
}
```

---

### 1.3 获取 CSRF Token

```
GET /api/admin/csrf/
```

**Response (200):**
```json
{
    "csrfToken": "<token>"
}
```

---

## 2. 仪表盘

### 2.1 获取统计数据

```
GET /api/admin/dashboard/
```

**Response (200):**
```json
{
    "total_users": 150,
    "total_students": 120,
    "total_teachers": 29,
    "total_admins": 1,
    "total_events": 45,
    "events_by_status": {
        "draft": 5,
        "published": 20,
        "ongoing": 10,
        "closed": 10
    },
    "total_applications": 200,
    "applications_by_status": {
        "pending": 50,
        "approved": 100,
        "rejected": 30,
        "cancelled": 20
    },
    "total_files": 80
}
```

---

## 3. 用户管理

### 3.1 用户列表

```
GET /api/admin/users/
```

**Query Parameters:**
| 参数      | 类型   | 说明                                  |
| --------- | ------ | ------------------------------------- |
| role      | string | 按角色筛选: student / teacher / admin |
| search    | string | 按姓名/学号/邮箱模糊搜索              |
| page      | int    | 页码（默认1）                         |
| page_size | int    | 每页数量（默认20）                    |

**Response (200):**
```json
{
    "count": 150,
    "next": "http://.../api/admin/users/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "2023001",
            "email": "student@example.com",
            "name": "张三",
            "student_id": "2023001",
            "class_name": "计算机2301",
            "phone": "13812345678",
            "wechat_id": "wx_zhangsan",
            "bio": "简介内容",
            "role": "student",
            "is_active": true,
            "date_joined": "2024-01-01T00:00:00Z",
            "events_count": 0,
            "applications_count": 3
        }
    ]
}
```

---

### 3.2 用户详情

```
GET /api/admin/users/{id}/
```

**Response (200):**
```json
{
    "id": 1,
    "username": "2023001",
    "email": "student@example.com",
    "name": "张三",
    "student_id": "2023001",
    "class_name": "计算机2301",
    "phone": "13812345678",
    "wechat_id": "wx_zhangsan",
    "bio": "简介内容",
    "role": "student",
    "is_active": true,
    "date_joined": "2024-01-01T00:00:00Z",
    "events_count": 0,
    "applications_count": 3
}
```

---

### 3.3 创建用户

```
POST /api/admin/users/
```

**Request:**
```json
{
    "username": "2024001",
    "email": "new_student@example.com",
    "password": "password123",
    "name": "李四",
    "student_id": "2024001",
    "class_name": "软件2401",
    "phone": "13900001111",
    "wechat_id": "wx_lisi",
    "bio": "新同学",
    "role": "student"
}
```

**Response (201):**
```json
{
    "id": 2,
    "username": "2024001",
    "email": "new_student@example.com",
    "name": "李四",
    "student_id": "2024001",
    "class_name": "软件2401",
    "phone": "13900001111",
    "wechat_id": "wx_lisi",
    "bio": "新同学",
    "role": "student",
    "is_active": true,
    "date_joined": "2024-06-01T00:00:00Z",
    "events_count": 0,
    "applications_count": 0
}
```

---

### 3.4 更新用户

```
PUT /api/admin/users/{id}/
```

**Request:**
```json
{
    "email": "updated@example.com",
    "name": "张三(修改)",
    "student_id": "2023001",
    "class_name": "计算机2301",
    "phone": "13800000000",
    "wechat_id": "wx_zhangsan_new",
    "bio": "更新后的简介",
    "role": "student",
    "is_active": true,
    "password": ""
}
```

说明:
- `password` 为空字符串时保留原密码，填写新密码则重置
- `username` 不可修改（与 student_id 关联）
- 如果修改的是当前管理员自己，`role` 不可修改

---

### 3.5 删除用户

```
DELETE /api/admin/users/{id}/
```

**Response (204):** 无内容

说明:
- 管理员不能删除自己的账号
- 删除用户会级联删除其相关的项目、申请等数据（取决于 on_delete 设置）

---

## 4. 项目管理

### 4.1 项目列表

```
GET /api/admin/events/
```

**Query Parameters:**
| 参数         | 类型   | 说明                                             |
| ------------ | ------ | ------------------------------------------------ |
| status       | string | 按状态筛选: draft / published / ongoing / closed |
| teacher_name | string | 按发布教师姓名搜索                               |
| search       | string | 按项目名称模糊搜索                               |
| page         | int    | 页码                                             |
| page_size    | int    | 每页数量                                         |

**Response (200):**
```json
{
    "count": 45,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "科研项目A",
            "event_type": "科研",
            "start_time": "2024-09-01T09:00:00Z",
            "end_time": "2024-12-31T18:00:00Z",
            "location": "实验室301",
            "description": "项目描述...",
            "attachment": null,
            "expected_participants": 10,
            "current_participants": 5,
            "status": "published",
            "teacher": 3,
            "teacher_name": "王老师",
            "can_delete": true,
            "can_publish": false,
            "can_close": true,
            "pending_applications_count": 2,
            "created_at": "2024-08-01T00:00:00Z",
            "updated_at": "2024-08-15T00:00:00Z"
        }
    ]
}
```

---

### 4.2 项目详情

```
GET /api/admin/events/{id}/
```

---

### 4.3 创建项目

```
POST /api/admin/events/
```

**Request:**
```json
{
    "teacher_id": 3,
    "title": "新科研项目",
    "event_type": "科研",
    "start_time": "2024-10-01T09:00:00Z",
    "end_time": "2025-01-31T18:00:00Z",
    "location": "实验室302",
    "description": "项目描述...",
    "attachment_id": null,
    "expected_participants": 15
}
```

说明: `teacher_id` 必填，管理员可以替任意教师创建项目。

---

### 4.4 更新项目

```
PUT /api/admin/events/{id}/
```

**Request:** 同创建项目

---

### 4.5 删除项目

```
DELETE /api/admin/events/{id}/
```

**Response (204):** 无内容

---

### 4.6 修改项目状态

```
POST /api/admin/events/{id}/publish/     -- 发布草稿项目
POST /api/admin/events/{id}/close/       -- 关闭项目
```

**Response (200):**
```json
{
    "detail": "Event published successfully"
}
```

---

## 5. 申请管理

### 5.1 申请列表

```
GET /api/admin/applications/
```

**Query Parameters:**
| 参数   | 类型   | 说明                                                  |
| ------ | ------ | ----------------------------------------------------- |
| event  | int    | 按项目ID筛选                                          |
| status | string | 按状态筛选: pending / approved / rejected / cancelled |
| page   | int    | 页码                                                  |

---

### 5.2 审核申请

```
POST /api/admin/applications/{id}/approve/
POST /api/admin/applications/{id}/reject/
```

**Request:**
```json
{
    "review_note": "审核意见"
}
```

---

## 6. 文件管理

### 6.1 文件列表

```
GET /api/admin/files/
```

**Query Parameters:**
| 参数     | 类型   | 说明         |
| -------- | ------ | ------------ |
| category | string | 按分类筛选   |
| search   | string | 按文件名搜索 |
| page     | int    | 页码         |

---

### 6.2 删除文件

```
DELETE /api/admin/files/{id}/
```

---

## 错误响应格式

所有接口错误返回统一格式:

```json
{
    "detail": "错误描述信息"
}
```

或字段级错误:

```json
{
    "student_id": ["This student_id is already registered"],
    "email": ["This email is already registered"]
}
```

HTTP 状态码:
- 200: 成功
- 201: 创建成功
- 204: 删除成功（无返回内容）
- 400: 请求参数错误
- 401: 未登录
- 403: 无管理员权限
- 404: 资源不存在
