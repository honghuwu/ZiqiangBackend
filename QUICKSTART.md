# 快速启动指南

## 1. 进入正确环境

请使用 conda 的 `py39` 虚拟环境，不要直接使用 `base`。

```bash
conda activate py39
```

如果本地没有该环境：

```bash
conda create --name py39 python=3.9
conda activate py39
```

## 2. 初始化项目

```bash
# 进入项目目录
cd path/to/ziqiangPlatform

# 安装依赖
pip install -r requirements.txt

# 复制环境变量模板
# Windows PowerShell:
Copy-Item .env.example .env

# 运行迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

开发地址：

- `http://127.0.0.1:8000`
- `http://localhost:8000`

## 3. 环境变量

最小可用配置：

```env
DJANGO_ENV=local
DJANGO_SECRET_KEY=replace-with-your-own-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=True
ENABLE_NOTIFICATIONS=False
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

说明：

- `ENABLE_NOTIFICATIONS=False`
  - 当前默认关闭通知触发
- 如果要启用通知触发：

```env
ENABLE_NOTIFICATIONS=True
```

## 4. 用户系统调试

### 发送注册验证码

```bash
curl -X POST http://127.0.0.1:8000/api/user/send-register-code/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

### 注册

```bash
curl -X POST http://127.0.0.1:8000/api/user/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "2023001",
    "name": "张三",
    "email": "test@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "code": "123456",
    "class_name": "自强书院2023级1班",
    "phone": "13800138000",
    "wechat_id": "zhangsan_wechat",
    "role": "student"
  }'
```

### 登录

```bash
curl -X POST http://127.0.0.1:8000/api/user/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "2023001",
    "password": "password123"
  }'
```

## 5. 文件上传与 UUID 流程

### 第一步：上传文件

项目附件：

```bash
curl -X POST http://127.0.0.1:8000/api/file/uploads/ \
  -H "Cookie: sessionid=your_session_id" \
  -F "file=@project-material.zip" \
  -F "category=event_attachment" \
  -F "description=项目附件"
```

学生简历：

```bash
curl -X POST http://127.0.0.1:8000/api/file/uploads/ \
  -H "Cookie: sessionid=your_session_id" \
  -F "file=@resume.pdf" \
  -F "category=application_resume" \
  -F "description=学生简历"
```

返回示例：

```json
{
  "id": "2c6db4a1-20f0-4e6a-b89e-1aa9b9d4d48d",
  "original_name": "project-material.zip",
  "category": "event_attachment",
  "file_url": "http://127.0.0.1:8000/api/file/uploads/2c6db4a1-20f0-4e6a-b89e-1aa9b9d4d48d/download/",
  "is_referenced": false,
  "can_delete": true
}
```

### 第二步：业务接口中传 UUID

创建项目时传 `attachment_id`：

```bash
curl -X POST http://127.0.0.1:8000/api/event/teacher/events/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your_session_id" \
  -d '{
    "title": "后端招新项目",
    "event_type": "科研",
    "start_time": "2026-03-10T10:00:00+08:00",
    "end_time": "2026-03-20T18:00:00+08:00",
    "location": "主楼101",
    "description": "项目简介",
    "expected_participants": 10,
    "attachment_id": "2c6db4a1-20f0-4e6a-b89e-1aa9b9d4d48d"
  }'
```

提交申请时传 `resume_id`：

```bash
curl -X POST http://127.0.0.1:8000/api/event/events/1/apply/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your_session_id" \
  -d '{
    "statement": "我想参加这个项目",
    "resume_id": "1d838e1e-98f8-42c0-9cf0-3b7de35cf6ec"
  }'
```

### 下载文件

文件下载统一走后端接口：

```text
GET /api/file/uploads/<uuid>/download/
```

### 模板文件

查看模板：

```text
GET /api/file/templates/
GET /api/file/templates/<key>/
```

管理员管理模板：

```text
GET    /api/file/admin/templates/
POST   /api/file/admin/templates/
GET    /api/file/admin/templates/<key>/
PATCH  /api/file/admin/templates/<key>/
DELETE /api/file/admin/templates/<key>/
```

## 6. 项目与申请流程

### 教师创建草稿项目

```bash
curl -X POST http://127.0.0.1:8000/api/event/teacher/events/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=teacher_session" \
  -d '{
    "title": "科研项目A",
    "event_type": "科研",
    "start_time": "2026-03-10T10:00:00+08:00",
    "end_time": "2026-03-20T18:00:00+08:00",
    "location": "主楼101",
    "description": "项目简介",
    "expected_participants": 5
  }'
```

### 发布项目

```text
POST /api/event/teacher/events/<id>/publish/
```

### 关闭项目

```text
POST /api/event/teacher/events/<id>/close/
```

规则：

- 草稿可删除
- 已发布但未开始可关闭
- 进行中 / 历史项目不可删除或关闭

### 学生提交申请

```text
POST /api/event/events/<event_id>/apply/
```

规则：

- 只能申请已发布且未开始的项目
- 满员项目不能提交新申请
- 同一学生不能重复提交待审核 / 已通过申请
- 学生不能撤回申请

### 教师审批

```text
GET  /api/event/teacher/applications/
POST /api/event/teacher/applications/<id>/approve/
POST /api/event/teacher/applications/<id>/reject/
```

规则：

- 只能逐条审批
- 项目开始前可以改判
- 项目开始后不能再改判

## 7. 筛选参数

### 项目列表筛选

适用于：

- `GET /api/event/events/`
- `GET /api/event/teacher/events/`

支持：

- `status`
  - `draft`
  - `published`
  - `ongoing`
  - `closed`
- `teacher_name`
- `can_recruit=true|false`

### 申请列表筛选

适用于：

- `GET /api/event/my-applications/`
- `GET /api/event/teacher/applications/`

支持：

- `event=<event_id>`
- `status=pending|approved|rejected|cancelled`

### 通知列表筛选

适用于：

- `GET /api/notification/my/`

支持：

- `is_read=true|false`

## 8. 测试

```bash
conda activate py39
python manage.py test apps.user --verbosity=2
python manage.py test apps.event --verbosity=2
python manage.py test apps.file --verbosity=2
python manage.py test apps.notification --verbosity=2
```

## 9. 常见问题

### `ModuleNotFoundError: No module named 'django'`

说明当前没进入 `py39` 环境：

```bash
conda activate py39
```

### 上传文件被拒绝

检查：

- 文件扩展名是否在白名单内
- 文件大小是否超过分类上限
- 上传分类是否正确

### 通知没有生成

检查 `.env`：

```env
ENABLE_NOTIFICATIONS=False
```

如果要启用：

```env
ENABLE_NOTIFICATIONS=True
```
