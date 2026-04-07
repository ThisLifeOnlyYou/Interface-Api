"""
登录模块测试用例
"""
import pytest
from common.requests_client import client
from common.assert_utils import assert_utils
from config.api_paths import LoginPaths


class TestLogin:
    """登录模块测试"""

    @pytest.mark.smoke
    @pytest.mark.p0
    def test_login_success(self):
        """测试登录成功"""
        response = client.post(
            LoginPaths.LOGIN,
            data={
                "username": "13333333333",
                "password": "123456"
            }
        )
        # 断言响应成功
        data = assert_utils.assert_success(response)

        # 断言返回信息 不为空
        assert_utils.assert_not_empty(data["data"],"employee", "employee")
        # 断言 token 不为 null
        assert_utils.assert_not_null(data["data"], "token", "登录token")
        #断言返回信息精准断言
        assert_utils.assert_business_data(data["data"]["employee"], "nickName", "张三11", "用户昵称")
        # 断言 token 存在
        token_data = data.get("data", {})
        assert "token" in token_data or isinstance(data.get("data"), str), \
            "响应中未包含 token"
        
        print(f"✅ 登录成功,Token: {data.get('data', {}).get('token', '')[:20]}...")  

    @pytest.mark.regression
    def test_login_wrong_password(self):
        """测试密码错误"""
        response = client.post(
            LoginPaths.LOGIN,
            data={
                "username": "13333333333",
                "password": "wrong_password"
            }
        )
        #根据这个写断言{"code": 50000, "msg": "账号或密码错误,错误剩余5次", "data": null} 那个 5 次 是动态的，根据实际错误次数变化
        data = response.json()
        error_count = data.get("msg", "").split("错误剩余")[1].split("次")[0]
        #进行断言
        assert_utils.assert_business_data(data, "code", 50000, "错误码")
        assert_utils.assert_business_data(data, "msg", f"账号或密码错误,错误剩余{error_count}次", "错误提示")
        data = assert_utils.assert_fail(response, 50000, f"账号或密码错误,错误剩余{error_count}次")

    @pytest.mark.regression
    def test_login_missing_username(self):
        """测试缺少用户名"""
        response = client.post(
            LoginPaths.LOGIN,
            data={
                "password": "123456"
            }
        )

        data = response.json()
        #进行断言
        assert_utils.assert_business_data(data, "code", 50000, "错误码")
        assert_utils.assert_business_data(data, "msg", f"login.username: 账号不能为空", "错误提示")
       
        data = assert_utils.assert_fail(response, 50000, "账号不能为空")
        # 断言响应失败
        assert_utils.assert_fail(response, 50000, "账号不能为空")
        # 可能返回 400 或业务错误码
        if response.status_code == 200:
            try:
                data = response.json()
                assert data.get("code") != 200, "缺少用户名应失败"
            except:
                # 如果不是 JSON 格式，说明登录失败
                print("✅ 缺少用户名验证通过: 服务器返回非 JSON 响应")
        else:
            print("✅ 缺少用户名验证通过")

    @pytest.mark.parametrize("username,password,expected_keyword", [
        ("", "123456", "账号不能为空"),
        ("username", "", "密码不能为空"),
        ("", "", "账号不能为空"),
    ])
    def test_login_empty_params(self, username, password, expected_keyword):
        """测试空参数登录"""
        response = client.post(
            LoginPaths.LOGIN,
            data={"username": username, "password": password}
        )
        
        data = response.json()

        #进行断言
        assert_utils.assert_business_data(data, "code", 50000, "错误码")

        if username:
            assert_utils.assert_business_data(data, "msg", f"login.password: {expected_keyword}", "错误提示")
        if password:
            assert_utils.assert_business_data(data, "msg", f"login.username: {expected_keyword}", "错误提示")
        if not username and not password:
            # 两个都为空时，检查是否包含两个错误提示（顺序可能不同）
            msg = data.get("msg", "")
            assert "账号不能为空" in msg and "密码不能为空" in msg, \
                f"错误信息应包含两个提示: {msg}"        
        assert_utils.assert_fail(response, 50000, expected_keyword)
       
    @pytest.mark.p0
    def test_checked_token_valid(self):
        """测试验证有效 token"""
        # 先登录获取 token
        login_response = client.post(
            LoginPaths.LOGIN,
            data={
                "username": "13333333333",
                "password": "123456"
            }
        )
        login_data = assert_utils.assert_success(login_response)
        token = login_data["data"]["token"]
        
        # 验证 token
        response = client.get(
            LoginPaths.CHECKED_TOKEN,
            params={"token": token}
        )
        data = assert_utils.assert_success(response)

        # 根据实际返回验证
        result = data.get("data")
        assert result is True or result == "valid" or result is not None, \
            "Token 验证应返回有效"

        # 断言返回信息 不为空
        if data["data"] and data["data"].get("employee"):
            assert_utils.assert_not_empty(data["data"],"employee", "employee")
            # 断言 token 不为 null
            assert_utils.assert_not_null(data["data"], "token", "登录token")
            #断言返回信息精准断言
            assert_utils.assert_business_data(data["data"]["employee"], "nickName", "张三11", "用户昵称")

        print("✅ Token 验证通过")
