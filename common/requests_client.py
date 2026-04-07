"""
请求客户端
"""
import json
import time
from typing import Dict, Optional, Any
import requests
from utils.logger import logger
from config.settings import config


class RequestsClient:
    """请求客户端"""

    def __init__(self, base_url: str = None):
        """初始化客户端"""
        self.base_url = base_url or config.BASE_URL
        self.session = requests.Session()
        self.timeout = 30

    def _get_headers(self, user: Optional[str] = None) -> Dict[str, str]:
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if user:
            token_value = self._get_token_by_user(user)
            if token_value:
                logger.debug(f"使用用户 '{user}' 的 Token: {token_value[:20]}...")
                headers["token"] = token_value
        return headers

    def _get_token_by_user(self, user: str) -> Optional[str]:
        """根据用户获取 token"""
        if hasattr(config, "COOKIE_TOKENS"):
            return config.COOKIE_TOKENS.get(user)
        return None

    def get_available_users(self) -> list:
        """获取所有可用用户"""
        if hasattr(config, "COOKIE_TOKENS"):
            return list(config.COOKIE_TOKENS.keys())
        return []

    def get_token_by_user(self, user: str) -> Optional[str]:
        """根据用户获取 token"""
        return self._get_token_by_user(user)

    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求信息"""
        logger.info(f"📤 {method} {url}")
        if "json" in kwargs:
            logger.debug(f"    Body (JSON): {json.dumps(kwargs['json'], ensure_ascii=False)}")
        elif "data" in kwargs:
            logger.debug(f"    Body (Form): {kwargs['data']}")
        elif "params" in kwargs:
            logger.debug(f"    Params: {kwargs['params']}")

    def _log_response(self, response: requests.Response):
        """记录响应信息"""
        logger.info(f"📥 Response: {response.status_code}")
        if response.content:
            try:
                data = response.json()
                logger.debug(f"    Body: {json.dumps(data, ensure_ascii=False)}")
            except:
                logger.debug(f"    Body: {response.text}")

    def _record_response_info(self, method: str, url: str, response: requests.Response, **kwargs):
        """记录响应信息到测试报告"""
        try:
            logger.info("开始记录响应信息到测试报告")
            # 导入 conftest 中的 test_data_store 和 current_test_item
            logger.info("尝试导入 test_data_store 和 current_test_item")
            from testcases.conftest import test_data_store, current_test_item
            logger.info("导入成功")
            
            logger.info(f"获取到 current_test_item: {current_test_item}")
            
            if current_test_item:
                nodeid = current_test_item.nodeid
                logger.info(f"获取到 nodeid: {nodeid}")
                
                if nodeid in test_data_store:
                    logger.info(f"nodeid {nodeid} 在 test_data_store 中")
                    # 构建请求体信息
                    request_body = None
                    if "json" in kwargs:
                        request_body = json.dumps(kwargs['json'], ensure_ascii=False, indent=2)
                        logger.info(f"构建请求体 (JSON): {request_body[:50]}...")
                    elif "data" in kwargs:
                        request_body = str(kwargs['data'])
                        logger.info(f"构建请求体 (Form): {request_body}")
                    
                    # 构建响应体信息
                    response_body = None
                    if response.content:
                        try:
                            data = response.json()
                            response_body = json.dumps(data, ensure_ascii=False, indent=2)
                            logger.info(f"构建响应体 (JSON): {response_body[:50]}...")
                        except Exception as e:
                            response_body = response.text
                            logger.info(f"构建响应体 (Text): {response_body[:50]}...")
                    
                    # 记录响应信息
                    response_info = {
                        "url": url,
                        "method": method,
                        "status_code": response.status_code,
                        "request_body": request_body,
                        "response_body": response_body
                    }
                    test_data_store[nodeid]["response_info"].append(response_info)
                    logger.info(f"成功记录响应信息，现在响应信息数量: {len(test_data_store[nodeid]['response_info'])}")
                else:
                    logger.info(f"nodeid {nodeid} 不在 test_data_store 中")
            else:
                logger.info("current_test_item 为 None")
        except Exception as e:
            logger.error(f"记录响应信息失败: {e}")
            import traceback
            logger.error(f"错误堆栈: {traceback.format_exc()}")

    def request(self, method: str, path: str, user: Optional[str] = None, **kwargs) -> requests.Response:
        """通用请求方法
        
        Args:
            method: HTTP 方法
            path: 请求路径
            user: 指定使用哪个用户的 Cookie（如 '用户A', '用户B'）
            **kwargs: 其他请求参数
        """
        url = f"{self.base_url}{path}"
        
        headers = self._get_headers(user)

        # 如果使用 data 参数，修改 Content-Type 为表单数据
        if "data" in kwargs:
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        # 合并 headers
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))
        kwargs["headers"] = headers

        # 设置超时
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        self._log_request(method, url, **kwargs)

        try:
            response = self.session.request(method, url, **kwargs)
            self._log_response(response)
            self._record_response_info(method, url, response, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {e}")
            raise

    def get(self, path: str, user: Optional[str] = None, **kwargs) -> requests.Response:
        """GET 请求
        
        Args:
            path: 请求路径
            user: 指定使用哪个用户的 Cookie（如 '用户A', '用户B'）
            **kwargs: 其他请求参数
        """
        return self.request("GET", path, user, **kwargs)

    def post(self, path: str, user: Optional[str] = None, **kwargs) -> requests.Response:
        """POST 请求
        
        Args:
            path: 请求路径
            user: 指定使用哪个用户的 Cookie（如 '用户A', '用户B'）
            **kwargs: 其他请求参数
        """
        return self.request("POST", path, user, **kwargs)

    def put(self, path: str, user: Optional[str] = None, **kwargs) -> requests.Response:
        """PUT 请求
        
        Args:
            path: 请求路径
            user: 指定使用哪个用户的 Cookie（如 '用户A', '用户B'）
            **kwargs: 其他请求参数
        """
        return self.request("PUT", path, user, **kwargs)

    def delete(self, path: str, user: Optional[str] = None, **kwargs) -> requests.Response:
        """DELETE 请求
        
        Args:
            path: 请求路径
            user: 指定使用哪个用户的 Cookie（如 '用户A', '用户B'）
            **kwargs: 其他请求参数
        """
        return self.request("DELETE", path, user, **kwargs)


# 创建全局客户端实例
client = RequestsClient()
