"""
商品管理测试用例
演示如何在接口中直接指定使用哪个 Cookie
"""
import pytest
from common.requests_client import client
from common.assert_utils import assert_utils
from config.api_paths import GoodsPaths
from config.settings import config


# 商品管理测试用例
def test_save_goods(test_data_store, user_name):
    """测试保存商品"""
    # 准备测试数据
    test_data = {
        "name": "测试商品",
        "price": 99.99,
        "stock": 100,
        "description": "这是一个测试商品"
    }
    
    # 发送请求
    response = client.post(GoodsPaths.SAVE, 
        user=user_name,
        data=test_data
    )
    
    # 断言响应状态码
    assert_utils.assert_status_code(response, 200, "保存商品应返回 200 成功")
    
    # 解析响应 JSON
    data = response.json()
    
    # 数据断言
    assert_utils.assert_business_data(data, "code", 200, "保存商品状态码")
    assert_utils.assert_business_data(data, "msg", f"保存商品成功", "保存商品提示")

    
