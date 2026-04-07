"""
Pytest 全局夹具配置
"""
import pytest
import time
from common.requests_client import client
from common.auth import auth_manager
from utils.logger import logger


@pytest.fixture(scope="session")
def api_client():
    """API 客户端夹具（会话级别）"""
    logger.info("初始化 API 客户端")
    return client


@pytest.fixture(scope="session")
def auth():
    """认证夹具"""
    return auth_manager


@pytest.fixture(scope="session")
def token(auth, api_client):
    """获取 token"""
    logger.info("获取 Token")
    return auth.login(api_client.session)


# @pytest.fixture(scope="function")
# def test_data():
#     """测试数据夹具"""
#     timestamp = int(time.time())
#     return {
#         "timestamp": timestamp,
#         "member": {
#             "name": f"测试会员_{timestamp}",
#             "phone": f"138{timestamp % 100000000:08d}",
#             "points": 100
#         },
#         "goods": {
#             "name": f"测试商品_{timestamp}",
#             "price": 99.99,
#             "stock": 100
#         },
#         "role": {
#             "name": f"测试角色_{timestamp}",
#             "code": f"TEST_{timestamp}"
#         },
#         "employee": {
#             "username": f"testuser_{timestamp}",
#             "name": f"测试用户_{timestamp}",
#             "phone": f"138{timestamp % 100000000:08d}"
#         }
#     }


@pytest.fixture(scope="function")
def cleanup():
    """清理数据夹具"""
    cleanup_list = []

    def register_cleanup(func, *args, **kwargs):
        cleanup_list.append((func, args, kwargs))

    yield register_cleanup

    # 执行清理（逆序）
    logger.info(f"开始清理 {len(cleanup_list)} 项资源")
    for func, args, kwargs in reversed(cleanup_list):
        try:
            func(*args, **kwargs)
            logger.debug(f"清理成功: {func.__name__}")
        except Exception as e:
            logger.warning(f"清理失败: {func.__name__} - {e}")


@pytest.fixture(scope="function")
def login_as(api_client):
    """使用指定账号登录的夹具"""

    def _login(username, password):
        response = api_client.post(
            "/login",
            need_auth=False,
            json={"username": username, "password": password}
        )
        data = response.json()
        if data.get("code") == 200:
            token = data["data"]["token"]
            return token
        else:
            raise Exception(f"登录失败: {data.get('msg')}")

    return _login


def pytest_runtest_setup(item):
    """每个测试开始前的钩子"""
    logger.info(f"\n{'=' * 50}\n开始测试: {item.nodeid}\n{'=' * 50}")


def pytest_runtest_teardown(item, nextitem):
    """每个测试结束后的钩子"""
    logger.info(f"\n{'=' * 50}\n结束测试: {item.nodeid}\n{'=' * 50}")