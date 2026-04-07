# Token 管理系统使用说明

## 概述

Token 管理系统支持多账号、多环境的 token 管理，可以在每个接口请求时选择使用哪个账号的 token。

## 配置文件

配置文件位置：`config/token_manager.py`

### 配置结构

```python
TOKEN_CONFIG = {
    "test": {  # 测试环境
        "description": "测试环境",
        "accounts": [
            {
                "name": "测试账号1",        # 账号名称
                "username": "13333333333",  # 用户名
                "password": "123456",       # 密码
                "token": "",                # token（登录后自动填充或手动填写）
                "enabled": True             # 是否启用
            },
            # 可以添加更多账号...
        ]
    },
    "prod": {  # 线上环境
        "description": "线上环境",
        "accounts": [
            {
                "name": "线上账号1",
                "username": "14788888888",
                "password": "123456",
                "token": "",
                "enabled": True
            },
            # 可以添加更多账号...
        ]
    }
}
```

## 使用方法

### 1. 在测试用例中使用

#### 方法一：使用默认账号（第一个启用的账号）

```python
from common.requests_client import client
from config.token_manager import set_current_env

# 设置环境
set_current_env("test")

# 发送请求，使用默认账号
response = client.post(
    "/member/queryPage",
    json={"currentPage": 1, "pageSize": 10}
)
```

#### 方法二：指定账号名称

```python
from common.requests_client import client

# 发送请求，指定使用 "测试账号1"
response = client.post(
    "/member/queryPage",
    account_name="测试账号1",  # 指定账号名称
    json={"currentPage": 1, "pageSize": 10}
)
```

#### 方法三：手动设置 token

```python
from common.requests_client import client

# 手动设置 token
client.set_token("LOGIN_USER:13333333333")

# 发送请求，使用手动设置的 token
response = client.post(
    "/member/queryPage",
    json={"currentPage": 1, "pageSize": 10}
)
```

### 2. 环境切换

```python
from config.token_manager import set_current_env, get_current_env

# 切换到测试环境
set_current_env("test")
print(f"当前环境: {get_current_env()}")  # 输出: test

# 切换到线上环境
set_current_env("prod")
print(f"当前环境: {get_current_env()}")  # 输出: prod
```

### 3. 账号管理

#### 获取所有账号

```python
from config.token_manager import get_accounts

accounts = get_accounts()
for account in accounts:
    print(f"账号: {account['name']}, 用户名: {account['username']}, 启用: {account['enabled']}")
```

#### 获取指定账号信息

```python
from config.token_manager import get_account_by_name

account = get_account_by_name("测试账号1")
if account:
    print(f"Token: {account['token']}")
```

#### 启用/禁用账号

```python
from config.token_manager import enable_account, disable_account

# 启用账号
enable_account("测试账号1")

# 禁用账号
disable_account("测试账号1")
```

#### 添加新账号

```python
from config.token_manager import add_account

# 添加新账号到测试环境
add_account(
    env="test",
    name="测试账号3",
    username="13900139000",
    password="123456",
    token="",  # 可选，可以留空
    enabled=True
)
```

#### 删除账号

```python
from config.token_manager import remove_account

# 删除账号
remove_account("测试账号3")
```

### 4. Token 操作

#### 获取 token

```python
from config.token_manager import get_token

# 获取默认账号的 token
token = get_token()

# 获取指定账号的 token
token = get_token(account_name="测试账号1")

# 获取指定环境的 token
token = get_token(env="prod")
```

#### 设置 token

```python
from config.token_manager import set_token

# 设置默认账号的 token
set_token("LOGIN_USER:13333333333")

# 设置指定账号的 token
set_token("LOGIN_USER:13333333333", account_name="测试账号1")

# 设置指定环境的 token
set_token("LOGIN_USER:14788888888", env="prod")
```

#### 清除 token

```python
from config.token_manager import clear_token

# 清除默认账号的 token
clear_token()

# 清除指定账号的 token
clear_token(account_name="测试账号1")

# 清除指定环境的 token
clear_token(env="prod")
```

## 完整示例

### 示例 1: 基本测试用例

```python
import pytest
from common.requests_client import client
from common.assert_utils import assert_utils
from config.api_paths import MemberPaths
from config.token_manager import set_current_env

class TestMember:
    """会员管理测试"""
    
    @pytest.fixture(autouse=True)
    def setup_env(self):
        """设置环境"""
        set_current_env("test")
    
    def test_query_member(self, api_client):
        """测试查询会员 - 使用默认账号"""
        response = api_client.post(
            MemberPaths.QUERY_PAGE,
            json={"currentPage": 1, "pageSize": 10}
        )
        data = assert_utils.assert_success(response)
        print(f"查询成功，共 {data['data']['total']} 条")
    
    def test_query_member_with_account(self, api_client):
        """测试查询会员 - 使用指定账号"""
        response = api_client.post(
            MemberPaths.QUERY_PAGE,
            account_name="测试账号1",  # 指定账号
            json={"currentPage": 1, "pageSize": 10}
        )
        data = assert_utils.assert_success(response)
        print(f"使用测试账号1查询成功，共 {data['data']['total']} 条")
```

### 示例 2: 多账号测试

```python
import pytest
from common.requests_client import client
from common.assert_utils import assert_utils
from config.api_paths import MemberPaths
from config.token_manager import get_accounts

class TestMemberMultiAccount:
    """多账号会员管理测试"""
    
    @pytest.mark.parametrize("account_name", ["测试账号1", "测试账号2"])
    def test_query_member_with_different_accounts(self, api_client, account_name):
        """使用不同账号查询会员"""
        # 检查账号是否启用
        account = get_account_by_name(account_name)
        if not account or not account.get("enabled"):
            pytest.skip(f"账号 {account_name} 未启用")
        
        response = api_client.post(
            MemberPaths.QUERY_PAGE,
            account_name=account_name,
            json={"currentPage": 1, "pageSize": 10}
        )
        data = assert_utils.assert_success(response)
        print(f"使用账号 {account_name} 查询成功，共 {data['data']['total']} 条")
```

### 示例 3: 环境切换测试

```python
import pytest
from common.requests_client import client
from common.assert_utils import assert_utils
from config.api_paths import MemberPaths
from config.token_manager import set_current_env, get_current_env

class TestMemberMultiEnv:
    """多环境会员管理测试"""
    
    @pytest.mark.parametrize("env", ["test", "prod"])
    def test_query_member_in_different_env(self, api_client, env):
        """在不同环境中查询会员"""
        # 切换环境
        set_current_env(env)
        print(f"当前环境: {get_current_env()}")
        
        response = api_client.post(
            MemberPaths.QUERY_PAGE,
            json={"currentPage": 1, "pageSize": 10}
        )
        data = assert_utils.assert_success(response)
        print(f"在 {env} 环境查询成功，共 {data['data']['total']} 条")
```

## 注意事项

1. **Token 优先级**：
   - 手动设置的 token (`client.set_token()`) > 指定账号的 token (`account_name`) > 默认账号的 token > auth_manager 的 token

2. **账号启用状态**：
   - 只有 `enabled=True` 的账号才会被使用
   - 可以通过 `enable_account()` 和 `disable_account()` 来控制账号的启用状态

3. **环境切换**：
   - 切换环境后，需要重新获取对应环境的 token
   - 建议在每个测试用例或测试类开始时设置环境

4. **Token 过期**：
   - 如果 token 过期，需要重新登录获取新的 token
   - 可以手动在配置文件中填写 token，或者通过登录接口自动获取

5. **安全性**：
   - 配置文件中包含敏感信息（用户名、密码、token），请注意保护
   - 不要将配置文件提交到公共代码仓库

## 常见问题

### Q1: 如何手动填写 token？

A: 直接在 `config/token_manager.py` 文件中修改对应账号的 `token` 字段：

```python
{
    "name": "测试账号1",
    "username": "13333333333",
    "password": "123456",
    "token": "LOGIN_USER:13333333333",  # 在这里填写 token
    "enabled": True
}
```

### Q2: 如何在登录后自动保存 token？

A: 在登录测试用例中，登录成功后调用 `set_token()` 保存 token：

```python
def test_login_success(self, api_client):
    response = api_client.post("/login", need_auth=False, data={
        "username": "13333333333",
        "password": "123456"
    })
    data = response.json()
    token = data["data"]["token"]
    
    # 保存 token 到配置文件
    from config.token_manager import set_token
    set_token(token, account_name="测试账号1")
```

### Q3: 如何区分线上和测试环境？

A: 使用 `set_current_env()` 切换环境：

```python
# 测试环境
set_current_env("test")

# 线上环境
set_current_env("prod")
```

### Q4: 如何在同一个测试中使用不同的账号？

A: 在每次请求时指定 `account_name` 参数：

```python
# 使用账号1
response1 = api_client.post("/api1", account_name="测试账号1", json={...})

# 使用账号2
response2 = api_client.post("/api2", account_name="测试账号2", json={...})
```

## 总结

Token 管理系统提供了灵活的多账号、多环境 token 管理功能，可以满足各种测试场景的需求。通过合理使用，可以提高测试的灵活性和可维护性。