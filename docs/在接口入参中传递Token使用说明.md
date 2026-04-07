# 在接口入参中传递 Token 使用说明

## 快速开始

### 方法一：直接传递 Token 值（推荐）

```python
from common.requests_client import client
from config.api_paths import MemberPaths

# 直接在参数中传递 token
response = client.post(
    MemberPaths.QUERY_PAGE,
    token="LOGIN_USER:13333333333",  # 直接传递 token
    json={"currentPage": 1, "pageSize": 10}
)
```

### 方法二：从配置文件获取 Token 并传递

```python
from common.requests_client import client
from config.token_manager import get_token
from config.api_paths import MemberPaths

# 从配置文件获取 token
token = get_token()

# 在参数中传递
response = client.post(
    MemberPaths.QUERY_PAGE,
    token=token,  # 传递从配置文件获取的 token
    json={"currentPage": 1, "pageSize": 10}
)
```

### 方法三：指定账号名称

```python
from common.requests_client import client
from config.api_paths import MemberPaths

# 指定使用哪个账号的 token
response = client.post(
    MemberPaths.QUERY_PAGE,
    account_name="测试账号1",  # 指定账号名称
    json={"currentPage": 1, "pageSize": 10}
)
```

## 完整示例

### 示例 1: 在测试用例中使用

```python
import pytest
from common.requests_client import client
from common.assert_utils import assert_utils
from config.api_paths import MemberPaths


class TestMember:
    """会员管理测试"""
    
    def test_query_member_with_token(self, api_client):
        """测试查询会员 - 直接传递 token"""
        # 直接传递 token
        response = api_client.post(
            MemberPaths.QUERY_PAGE,
            token="LOGIN_USER:13333333333",  # 在参数中传递 token
            json={"currentPage": 1, "pageSize": 10}
        )
        data = assert_utils.assert_success(response)
        print(f"查询成功，共 {data['data']['total']} 条")
    
    def test_query_member_with_account(self, api_client):
        """测试查询会员 - 指定账号"""
        # 指定账号名称
        response = api_client.post(
            MemberPaths.QUERY_PAGE,
            account_name="测试账号1",  # 指定账号名称
            json={"currentPage": 1, "pageSize": 10}
        )
        data = assert_utils.assert_success(response)
        print(f"查询成功，共 {data['data']['total']} 条")
```

### 示例 2: 参数化测试使用不同 Token

```python
import pytest
from common.requests_client import client
from common.assert_utils import assert_utils
from config.api_paths import MemberPaths


class TestMemberMultiToken:
    """多 Token 会员管理测试"""
    
    @pytest.mark.parametrize("token", [
        "LOGIN_USER:13333333333",
        "LOGIN_USER:13800138000",
        "LOGIN_USER:14788888888"
    ])
    def test_query_member_with_different_tokens(self, api_client, token):
        """使用不同 token 查询会员"""
        response = api_client.post(
            MemberPaths.QUERY_PAGE,
            token=token,  # 在参数中传递不同的 token
            json={"currentPage": 1, "pageSize": 10}
        )
        data = assert_utils.assert_success(response)
        print(f"使用 token {token[:20]}... 查询成功，共 {data['data']['total']} 条")
```

### 示例 3: 动态获取 Token

```python
import pytest
from common.requests_client import client
from common.assert_utils import assert_utils
from config.api_paths import MemberPaths
from config.token_manager import get_token, get_account_by_name


class TestMemberDynamic:
    """动态 Token 会员管理测试"""
    
    def test_query_member_dynamic_token(self, api_client):
        """动态获取 token 并使用"""
        # 方式 1: 获取默认账号的 token
        token = get_token()
        response = api_client.post(
            MemberPaths.QUERY_PAGE,
            token=token,
            json={"currentPage": 1, "pageSize": 10}
        )
        
        # 方式 2: 获取指定账号的 token
        account = get_account_by_name("测试账号1")
        if account and account.get("token"):
            response = api_client.post(
                MemberPaths.QUERY_PAGE,
                token=account["token"],
                json={"currentPage": 1, "pageSize": 10}
            )
```

## Token 优先级

当同时使用多种方式传递 token 时，优先级如下：

1. **直接传递的 token**（最高优先级）
   ```python
   client.post(path, token="YOUR_TOKEN", ...)
   ```

2. **手动设置的 token**
   ```python
   client.set_token("YOUR_TOKEN")
   client.post(path, ...)
   ```

3. **指定账号的 token**
   ```python
   client.post(path, account_name="账号名称", ...)
   ```

4. **auth_manager 的 token**（最低优先级）
   ```python
   client.post(path, ...)  # 使用默认认证
   ```

## 使用场景

### 场景 1: 快速测试

直接传递 token，适合快速测试：

```python
response = client.post(
    MemberPaths.QUERY_PAGE,
    token="LOGIN_USER:13333333333",
    json={"currentPage": 1, "pageSize": 10}
)
```

### 场景 2: 多账号测试

使用不同的 token 进行测试：

```python
tokens = {
    "账号1": "LOGIN_USER:13333333333",
    "账号2": "LOGIN_USER:13800138000"
}

for name, token in tokens.items():
    response = client.post(
        MemberPaths.QUERY_PAGE,
        token=token,
        json={"currentPage": 1, "pageSize": 10}
    )
    print(f"{name}: {response.status_code}")
```

### 场景 3: 环境切换

在不同环境中使用不同的 token：

```python
from config.token_manager import set_current_env, get_token

# 测试环境
set_current_env("test")
test_token = get_token()
response = client.post(MemberPaths.QUERY_PAGE, token=test_token, json={...})

# 线上环境
set_current_env("prod")
prod_token = get_token()
response = client.post(MemberPaths.QUERY_PAGE, token=prod_token, json={...})
```

## 执行方式

### 执行测试

```bash
# 执行单个测试文件
venv/bin/pytest testcases/test_member.py -v

# 执行指定测试方法
venv/bin/pytest testcases/test_member.py::TestMember::test_query_member_with_token -v

# 生成 HTML 报告
venv/bin/pytest testcases/test_member.py -v --html=reports/report.html --self-contained-html
```

### 运行示例代码

```bash
# 运行 token 使用示例
python examples/token_in_params_example.py
```

## 总结

现在您可以在接口请求参数中直接传递 token：

```python
# 最简单的方式
response = client.post(
    "/api/path",
    token="YOUR_TOKEN",  # 直接传递 token
    json={...}
)

# 从配置文件获取 token
from config.token_manager import get_token
token = get_token()
response = client.post("/api/path", token=token, json={...})

# 指定账号名称
response = client.post("/api/path", account_name="账号名称", json={...})
```

选择最适合您的方式，灵活使用 token！