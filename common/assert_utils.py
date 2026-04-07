"""
断言工具类
"""
import json
from typing import Any, Optional
from utils.logger import logger


# 获取当前测试节点 ID
def get_current_nodeid():
    """获取当前测试的 nodeid"""
    try:
        # 从 conftest 导入 current_test_item
        from testcases.conftest import current_test_item
        if current_test_item:
            return current_test_item.nodeid
    except Exception as e:
        logger.debug(f"获取当前测试节点 ID 失败: {e}")
    return None


# 存储断言信息
def record_assertion(message, expected=None, actual=None, status="passed"):
    """记录断言信息到测试报告"""
    try:
        # 导入 conftest 中的 test_data_store
        from testcases.conftest import test_data_store
        nodeid = get_current_nodeid()
        if nodeid and nodeid in test_data_store:
            test_data_store[nodeid]["assertions"].append({
                "message": message,
                "expected": str(expected) if expected is not None else "",
                "actual": str(actual) if actual is not None else "",
                "status": status
            })
            logger.debug(f"成功记录断言信息: {message}, 状态: {status}")
        else:
            logger.debug(f"无法记录断言信息: nodeid={nodeid}, test_data_store 中是否存在: {nodeid in test_data_store}")
    except Exception as e:
        logger.debug(f"记录断言信息失败: {e}")


class AssertUtils:
    """断言工具类"""

    @staticmethod
    def assert_success(response, expected_code: int = 200):
        """
        断言接口成功
        :param response: 响应对象
        :param expected_code: 期望的业务码
        :return: 响应 JSON 数据
        """
        # 记录断言信息到日志
        logger.info(f"断言: HTTP状态码期望=200, 实际={response.status_code}")
        
        if response.status_code != 200:
            error_msg = f"HTTP状态码错误: 期望=200, 实际={response.status_code}"
            logger.error(error_msg)
            record_assertion("HTTP状态码检查", expected=200, actual=response.status_code, status="failed")
            assert False, error_msg

        try:
            data = response.json()
            logger.info(f"断言: 业务码期望={expected_code}, 实际={data.get('code')}, 消息={data.get('msg')}")
        except Exception as e:
            error_msg = f"响应不是 JSON 格式: {response.text}"
            logger.error(error_msg)
            record_assertion("响应格式检查", expected="JSON", actual="非JSON", status="failed")
            assert False, error_msg

        actual_code = data.get("code")
        if actual_code != expected_code:
            error_msg = f"业务码错误: 期望={expected_code}, 实际={actual_code}, 消息={data.get('msg')}"
            logger.error(error_msg)
            record_assertion("业务码检查", expected=expected_code, actual=actual_code, status="failed")
            assert False, error_msg
            
        logger.info(f"✅ 断言通过: 业务码={actual_code}")
        record_assertion("业务码检查", expected=expected_code, actual=actual_code, status="passed")
        return data

    @staticmethod
    def assert_fail(response, expected_code: int = 500, expected_msg: Optional[str] = None):
        """
        断言接口失败
        :param response: 响应对象
        :param expected_code: 期望的错误码
        :param expected_msg: 期望的错误信息（可选）
        """
        logger.info(f"断言: HTTP状态码期望=200, 实际={response.status_code}")
        
        if response.status_code != 200:
            error_msg = f"HTTP状态码错误: 期望=200, 实际={response.status_code}"
            logger.error(error_msg)
            record_assertion("HTTP状态码检查", expected=200, actual=response.status_code, status="failed")
            assert False, error_msg

        try:
            data = response.json()
        except Exception as e:
            error_msg = f"响应不是 JSON 格式: {response.text}"
            logger.error(error_msg)
            record_assertion("响应格式检查", expected="JSON", actual="非JSON", status="failed")
            assert False, error_msg

        actual_code = data.get("code")
        if actual_code != expected_code:
            error_msg = f"业务码错误: 期望={expected_code}, 实际={actual_code}, 消息={data.get('msg')}"
            logger.error(error_msg)
            record_assertion("业务码检查", expected=expected_code, actual=actual_code, status="failed")
            assert False, error_msg

        if expected_msg:
            actual_msg = data.get("msg")
            if expected_msg not in actual_msg:
                error_msg = f"错误信息不匹配: 期望包含'{expected_msg}', 实际='{actual_msg}'"
                logger.error(error_msg)
                record_assertion("错误信息检查", expected=expected_msg, actual=actual_msg, status="failed")
                assert False, error_msg
            
            logger.info(f"✅ 断言通过: 错误信息包含'{expected_msg}'")
            record_assertion("错误信息检查", expected=expected_msg, actual=actual_msg, status="passed")
        else:
            logger.info(f"✅ 断言通过: 业务码={actual_code}")
            record_assertion("业务码检查", expected=expected_code, actual=actual_code, status="passed")

        return data

    @staticmethod
    def assert_business_data(data, key, expected, message):
        """
        断言业务数据
        :param data: 业务数据对象
        :param key: 键
        :param expected: 期望值
        :param message: 断言描述
        """
        actual = data.get(key)
        logger.info(f"断言: {message} 期望={expected}, 实际={actual}")
        if actual != expected:
            error_msg = f"{message} 不匹配: 期望={expected}, 实际={actual}"
            logger.error(error_msg)
            record_assertion(message, expected=expected, actual=actual, status="failed")
            assert False, error_msg
        
        logger.info(f"✅ 断言通过: {message} 正确")
        record_assertion(message, expected=expected, actual=actual, status="passed")

    @staticmethod
    def assert_not_null(data, key, message):
        """
        断言值不为空
        :param data: 数据对象
        :param key: 键
        :param message: 断言描述
        """
        actual = data.get(key)
        logger.info(f"断言: {message} 不为 null, 实际={actual}")
        if actual is None:
            error_msg = f"{message} 为 null"
            logger.error(error_msg)
            record_assertion(message, expected="非null", actual="null", status="failed")
            assert False, error_msg
        
        logger.info(f"✅ 断言通过: {message} 不为 null, 值={actual}")
        record_assertion(message, expected="非null", actual=actual, status="passed")

    @staticmethod
    def assert_not_empty(data, key, message):
        """
        断言值不为空
        :param data: 数据对象
        :param key: 键
        :param message: 断言描述
        """
        actual = data.get(key)
        logger.info(f"断言: {message} 不为空, 实际={actual}")
        if not actual:
            error_msg = f"{message} 为空"
            logger.error(error_msg)
            record_assertion(message, expected="非空", actual=actual, status="failed")
            assert False, error_msg
        
        logger.info(f"✅ 断言通过: {message} 不为空, 值={actual}")
        record_assertion(message, expected="非空", actual=actual, status="passed")


# 导出断言工具实例
assert_utils = AssertUtils()
