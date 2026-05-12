# CSRF问题
当前配置中 CSRF_COOKIE_HTTPONLY=True，见 [core/settings.py](core/settings.py#L188)。

这意味着浏览器 JavaScript 不能直接通过 document.cookie 读取 csrftoken。对于纯前后端分离页面，如果没有额外的 token 下发机制，将无法自行拼出合法的 X-CSRFToken，请求会持续 403。

当前项目已提供 CSRF token 获取接口：`GET /api/user/csrf/`。

该接口会返回：

```json
{
  "csrfToken": "<token>"
}
```
# 项目状态问题

项目自动进行ongoing，导致不能报名
修复：published和ongoing都可以报名，只要人不满