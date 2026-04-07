"""
Cookie Token 使用示例
展示如何使用多用户 Cookie Token
"""

from common.requests_client import client
from config.api_paths import GoodsPaths
from config.settings import config


def example_1_check_current_user():
    """示例 1: 查看当前用户和 Token"""
    print("=== 示例 1: 查看当前用户和 Token ===")
    print(f"当前环境: {config.__class__.__name__}")
    print(f"当前用户: {client.get_current_user()}")
    print(f"当前 Cookie: {client.get_cookies()}")
    print(f"可用用户: {client.get_available_users()}")


def example_2_switch_user():
    """示例 2: 切换用户"""
    print("\n=== 示例 2: 切换用户 ===")
    
    # 查看所有可用用户
    users = client.get_available_users()
    print(f"可用用户: {users}")
    
    # 切换到用户B
    client.set_user_token("用户B")
    print(f"切换后当前用户: {client.get_current_user()}")
    print(f"切换后 Cookie: {client.get_cookies()}")
    
    # 切换到用户C
    client.set_user_token("用户C")
    print(f"切换后当前用户: {client.get_current_user()}")
    print(f"切换后 Cookie: {client.get_cookies()}")


def example_3_query_with_different_users():
    """示例 3: 使用不同用户查询商品"""
    print("\n=== 示例 3: 使用不同用户查询商品 ===")
    
    users = client.get_available_users()
    
    for user in users:
        # 切换用户
        client.set_user_token(user)
        
        # 发送请求
        response = client.post(
            GoodsPaths.QUERY_PAGE,
            json={"currentPage": 1, "pageSize": 5}
        )
        
        print(f"\n用户: {user}")
        print(f"Token: {client.get_token_by_user(user)}")
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                print(f"✅ 查询成功，共 {data['data']['total']} 条商品")
            else:
                print(f"❌ 查询失败: {data.get('msg')}")


def example_4_get_token_by_user():
    """示例 4: 获取指定用户的 Token"""
    print("\n=== 示例 4: 获取指定用户的 Token ===")
    
    users = client.get_available_users()
    
    for user in users:
        token = client.get_token_by_user(user)
        print(f"{user}: {token}")


def example_5_use_in_test():
    """示例 5: 在测试中使用"""
    print("\n=== 示例 5: 在测试中使用 ===")
    
    # 使用默认用户
    print(f"默认用户: {client.get_current_user()}")
    print(f"默认 Token: {client.get_cookies()}")
    
    # 切换到特定用户进行测试
    client.set_user_token("用户A")
    response = client.post(
        GoodsPaths.QUERY_PAGE,
        json={"currentPage": 1, "pageSize": 10}
    )
    print(f"使用 用户A 查询，响应状态码: {response.status_code}")
    
    # 切换到另一个用户
    client.set_user_token("用户B")
    response = client.post(
        GoodsPaths.QUERY_PAGE,
        json={"currentPage": 1, "pageSize": 10}
    )
    print(f"使用 用户B 查询，响应状态码: {response.status_code}")


if __name__ == "__main__":
    print("Cookie Token 使用示例")
    print("=" * 60)
    
    example_1_check_current_user()
    example_2_switch_user()
    example_3_query_with_different_users()
    example_4_get_token_by_user()
    example_5_use_in_test()
    
    print("\n" + "=" * 60)
    print("所有示例执行完成")
    print("\n使用说明:")
    print("1. Cookie Token 会自动从配置加载默认用户")
    print("2. 使用 client.set_user_token('用户名') 切换用户")
    print("3. 使用 client.get_current_user() 查看当前用户")
    print("4. 使用 client.get_available_users() 查看所有可用用户")
    print("5. 不同环境的用户 Token 在 config/settings.py 中配置")