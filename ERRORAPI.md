# 错误码 API 文档

## 概述

所有 API 接口在出错时都会返回统一的 JSON 格式，包含 `detail`（错误描述）和 `error_code`（唯一识别码）。

---

## 通用响应格式

### 成功响应

```json
{
    "detail": "Login successful"
}
```

### 错误响应

```json
{
    "detail": "Invalid student_id or password",
    "error_code": "AUTH_001"
}
```

字段级校验错误：

```json
{
    "student_id": ["This student_id is already registered"],
    "email": ["This email is already in use"],
    "error_code": "VAL_008"
}
```

---

## 前端处理建议

```javascript
fetch('/api/admin/login/', { method: 'POST', body: JSON.stringify(data) })
  .then(res => res.json())
  .then(data => {
    if (data.error_code) {
      switch (data.error_code) {
        case 'AUTH_001':  // 凭据错误，提示用户重输
        case 'AUTH_003':  // 未登录，跳转登录页
        case 'AUTH_004':  // 权限不足，提示无权限
        case 'VAL_008':   // 表单校验失败，展示字段错误
      }
    }
  });
```

---

## 错误码分类

### 1. 认证类（AUTH）

| 错误码 | HTTP | 含义 | 错误消息 | 触发场景 |
|--------|------|------|----------|----------|
| `AUTH_001` | 400 | 凭据无效 | Invalid student_id or password | 登录时用户名或密码错误 |
| `AUTH_002` | 403 | 非管理员 | Insufficient permissions: admin role required | 普通用户调用 `/api/admin/login/` |
| `AUTH_003` | 401 | 未登录 | Authentication credentials were not provided | 访问需认证接口但未携带 session cookie |
| `AUTH_004` | 403 | 权限不足 | You do not have permission to perform this action | 已登录但角色权限不满足接口要求 |

---

### 2. 用户管理类（USER）

| 错误码 | HTTP | 含义 | 错误消息 | 触发场景 |
|--------|------|------|----------|----------|
| `USER_001` | 400 | 禁止改自己角色 | Cannot change your own role | `PUT /api/admin/users/{id}/update/` 修改自己的 role |
| `USER_002` | 400 | 禁止删自己 | Cannot delete your own account | `DELETE /api/admin/users/{id}/delete/` 删除自己 |

---

### 3. 项目类（EVENT）

| 错误码 | HTTP | 含义 | 错误消息 | 触发场景 |
|--------|------|------|----------|----------|
| `EVENT_001` | 400 | 仅草稿可发布 | Only draft events can be published | 发布非草稿状态的项目 |
| `EVENT_002` | 400 | 仅草稿可删除 | Only draft events can be deleted | 删除非草稿项目 |
| `EVENT_003` | 400 | 已关闭不可编辑 | Closed events cannot be edited | 编辑已关闭项目 |
| `EVENT_004` | 400 | 已关闭 | Event is already closed | 重复关闭项目 |
| `EVENT_005` | 400 | 不可关闭 | Only published events that have not started can be closed | 关闭不满足条件的项目 |
| `EVENT_006` | 404 | 项目不存在 | Event not found | 请求不存在的项目（由异常处理器自动生成） |
| `EVENT_007` | 400 | 没有名额 | This event has no available slots | 无剩余名额 |

---

### 4. 申请类（APP）

| 错误码 | HTTP | 含义 | 错误消息 | 触发场景 |
|--------|------|------|----------|----------|
| `APP_001` | 400 | 不接受申请 | This event is not accepting applications | 项目不在接受申请的阶段 |
| `APP_002` | 400 | 项目已满 | This event is already full | 名额已满时申请 |
| `APP_003` | 400 | 重复申请 | You have already applied to this event | 已有待审核/已通过的申请时再次申请 |
| `APP_004` | 400 | 仅待审核可操作 | Only pending applications can perform this action | 审核非 pending 状态的申请 |
| `APP_005` | 400 | 不可变更决策 | This application decision cannot be changed | 项目已不再接受申请时操作 |
| `APP_006` | 400 | 已撤回 | Cancelled applications cannot be modified | 操作已撤回的申请 |
| `APP_007` | 400 | 项目名额不足 | This event has no available slots | 审核时项目已满 |

---

### 5. 文件类（FILE）

| 错误码 | HTTP | 含义 | 错误消息 | 触发场景 |
|--------|------|------|----------|----------|
| `FILE_001` | 400 | 文件使用中 | File is in use and cannot be deleted | 删除被项目/申请引用的文件 |

---

### 6. 校验类（VAL）

| 错误码 | HTTP | 含义 | 错误消息 | 触发场景 |
|--------|------|------|----------|----------|
| `VAL_001` | 400 | 密码不匹配 | Passwords do not match | 注册/修改密码时两次密码不一致 |
| `VAL_002` | 400 | 旧密码错误 | Old password is incorrect | 修改密码时旧密码校验失败 |
| `VAL_003` | 400 | 验证码无效 | Invalid or non-existent verification code | 邮箱验证码不存在/错误 |
| `VAL_004` | 400 | 验证码过期 | Verification code has expired | 邮箱验证码超过5分钟 |
| `VAL_005` | 400 | 值已存在 | This value is already registered | 用户名/学号/邮箱重复 |
| `VAL_006` | 400 | 不支持的筛选值 | Unsupported filter value | 查询参数值不被支持 |
| `VAL_007` | 400 | 布尔参数无效 | Boolean query parameter must be true or false | 布尔型查询参数格式错误 |
| `VAL_008` | 400 | 表单数据无效 | Invalid form data | 序列化器校验失败（由异常处理器自动生成） |

---

## 错误码生成机制

有两层错误码注入方式：

| 机制 | 覆盖范围 | 说明 |
|------|----------|------|
| 视图层手动调用 `error_response()` | 特定场景的错误码（如 `AUTH_001`、`AUTH_002`、`USER_001` 等） | 业务逻辑中显式返回细分错误码 |
| DRF 异常处理器 `custom_exception_handler` | 框架级异常自动注入通用错误码 | `ValidationError` → `VAL_008`、`NotAuthenticated` → `AUTH_003`、`PermissionDenied` → `AUTH_004`、`NotFound` → `EVENT_006` |
