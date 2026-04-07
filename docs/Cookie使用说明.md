# Cookie Token 使用说明

## 概述

本系统支持在 Cookie 中设置 Token，并且支持多用户、多环境配置。

## 配置 Cookie Token

### 1. 在配置文件中设置 Token

编辑 `config/settings.py`，在对应的环境配置类中添加 `COOKIE_TOKENS` 字典：

```python
class TestConfig(Config):
    """测试环境配置"""
    BASE_URL = "http://127.0.0.1:9291"
    TEST_USERNAME = "13333333333"
    TEST_PASSWORD = "123456"
    
    # Cookie Token 配置（多用户）
    COOKIE_TOKENS = {
        "用户A": "LOGIN_USER:13333333333",
        "用户B": "LOGIN_USER:13333333334",
        "用户C": "LOGIN_USER:13333333335"
    }
    
    # 默认使用的用户
    DEFAULT_USER = "用户A"


class ProdConfig(Config):
    """生产环境配置"""
    BASE_URL = "http://192.168.1.104:9291"
    TEST_USERNAME = "14788888888"
    TEST_PASSWORD = "123456"
    
    # Cookie Token 配置（多用户）
    COOKIE_TOKENS = {
        "用户A": "LOGIN_USER:23333333333",
        "用户B": "LOGIN_USER:23333333334",
        "用户C": "LOGIN_USER:23333333335"
    }
    
    # 默认使用的用户
    DEFAULT_USER = "用户A"
```

### 2. 环境切换

通过环境变量切换不同的配置：

```bash
# 使用测试环境（默认）
export ENV=test
python run.py

# 使用生产环境
export ENV=prod
python run.py
```

## 在代码中使用 Cookie Token

### 自动加载默认用户

当创建 `RequestsClient` 实例时，会自动从配置加载默认用户的 Token：

```python
from common.requests_client import client

# 自动加载默认用户的 Token
print(f"当前用户: {client.get_current_user()}")  # 用户A
print(f"当前 Cookie: {client.get_cookies()}")    # {'token': 'LOGIN_USER:13333333333'}
```

### 切换用户

```python
from common.requests_client import client

# 切换到用户B
client.set_user_token("用户B")
print(f"当前用户: {client.get_current_user()}")  # 用户B
print(f"当前 Cookie: {client.get_cookies()}")    # {'token': 'LOGIN_USER:13333333334'}

# 切换到用户C
client.set_user_token("用户C")
print(f"当前用户: {client.get_current_user()}")  # 用户C
print(f"当前 Cookie: {client.get_cookies()}")    # {'token': 'LOGIN_USER:13333333335'}
```

### 获取所有可用用户

```python
from common.requests_client import client

# 获取所有可用用户
users = client.get_available_users()
print(f"可用用户: {users}")  # ['用户A', '用户B', '用户C']
```

### 获取指定用户的 Token

```python
from common.requests_client import client

# 获取指定用户的 Token
token_a = client.get_token_by_user("用户A")
print(f"用户A Token: {token_a}")  # LOGIN_USER:13333333333

token_b = client.get_token_by_user("用户B")
print(f"用户B Token: {token_b}")  # LOGIN_USER:13333333334
```

## 在测试用例中使用

### 示例 1: 使用默认用户

```python
import pytest
from common.requests_client import client
from common.assert_utils import assert_utils
from config.api_paths import GoodsPaths


class TestGoods:
    """商品管理测试"""

    def test_query_goods(self, api_client):
        """测试查询商品"""
        # 默认用户会自动加载
        print(f"当前用户: {api_client.get_current_user()}")
        
        # Cookie 会自动携带
        response = api_client.post(
            GoodsPaths.QUERY_PAGE,
            json={"currentPage": 1, "pageSize": 10}
        )
        
        data = assert_utils.assert_success(response)
        print(f"✅ 查询成功，共 {data['data']['total']} 条")
```

### 示例 2: 使用指定用户

```python
def test_query_with_user_a(self, api_client):
    """测试使用用户A查询商品"""
    # 切换到用户A
    api_client.set_user_token("用户A")
    
    # 发送请求
    response = api_client.post(
        GoodsPaths.QUERY_PAGE,
        json={"currentPage": 1, "pageSize": 10}
    )
    
    data = assert_utils.assert_success(response)
    print(f"✅ 用户A查询成功，共 {data['data']['total']} 条")
```

### 示例 3: 遍历所有用户

```python
def test_query_all_users(self, api_client):
    """测试使用所有用户查询商品"""
    # 获取所有可用用户
    users = api_client.get_available_users()
    
    for user in users:
        # 切换用户
        api_client.set_user_token(user)
        
        # 发送请求
        response = api_client.post(
            GoodsPaths.QUERY_PAGE,
            json={"currentPage": 1, "pageSize": 5}
        )
        
        print(f"用户: {user}, Token: {api_client.get_token_by_user(user)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 查询成功，共 {data['data']['total']} 条")
```

## 执行测试

```bash
# 执行商品管理测试
venv/bin/pytest testcases/test_goods.py -v

# 执行特定测试方法
venv/bin/pytest testcases/test_goods.py::TestGoods::test_query_goods_with_user_a -v

# 生成 HTML 报告
venv/bin/pytest testcases/test_goods.py -v --html=reports/report.html --self-contained-html
```

## 运行示例代码

```bash
# 运行 Cookie Token 使用示例
python examples/cookie_token_example.py
```

## API 参考

### RequestsClient 方法

| 方法 | 说明 | 参数 | 返回值 |
|------|------|------|--------|
| `set_user_token(user_name)` | 设置指定用户的 Token | user_name: 用户名称 | None |
| `get_current_user()` | 获取当前使用的用户 | None | str |
| `get_available_users()` | 获取所有可用的用户 | None | List[str] |
| `get_token_by_user(user_name)` | 获取指定用户的 Token | user_name: 用户名称 | str |
| `get_cookies()` | 获取当前所有 Cookie | None | Dict[str, str] |

## 注意事项

1. **自动加载**：默认用户的 Token 会在客户端初始化时自动加载
2. **环境隔离**：不同环境的用户 Token 在配置文件中分开管理
3. **动态切换**：可以在运行时动态切换用户
4. **会话保持**：Token 在 `RequestsClient` 的 session 中保持
5. **日志记录**：用户的切换和 Token 的设置会在日志中记录

## 常见问题

### Q: 如何添加新用户？

A: 在 `config/settings.py` 的 `COOKIE_TOKENS` 字典中添加新的键值对：

```python
COOKIE_TOKENS = {
    "用户A": "LOGIN_USER:13333333333",
    "用户B": "LOGIN_USER:13333333334",
    "用户C": "LOGIN_USER:13333333335",
    "用户D": "LOGIN_USER:13333333336"  # 新增用户
}
```

### Q: 如何修改默认用户？

A: 修改 `DEFAULT_USER` 配置：

```python
DEFAULT_USER = "用户B"  # 修改默认用户为用户B
```

### Q: Token 没有生效？

A: 请检查：
1. 配置文件中的 `COOKIE_TOKENS` 字典是否正确设置
2. 环境变量 `ENV` 是否设置正确
3. 使用 `client.get_cookies()` 查看当前 Cookie

### Q: 生产环境和测试环境的 Token 如何区分？

A: 在 `config/settings.py` 中分别为 `TestConfig` 和 `ProdConfig` 设置不同的 `COOKIE_TOKENS` 字典，通过 `ENV` 环境变量切换。

## 配置示例

### 测试环境配置

```python
class TestConfig(Config):
    """测试环境配置"""
    BASE_URL = "http://127.0.0.1:9291"
    
    # 测试环境用户
    COOKIE_TOKENS = {
        "用户A": "LOGIN_USER:13333333333",
        "用户B": "LOGIN_USER:13333333334",
        "用户C": "LOGIN_USER:13333333335"
    }
    
    DEFAULT_USER = "用户A"
```

### 生产环境配置

```python
class ProdConfig(Config):
    """生产环境配置"""
    BASE_URL = "http://192.168.1.104:9291"
    
    # 生产环境用户
    COOKIE_TOKENS = {
        "用户A": "LOGIN_USER:23333333333",
        "用户B": "LOGIN_USER:23333333334",
        "用户C": "LOGIN_USER:23333333335"
    }
    
    DEFAULT_USER = "用户A"
```