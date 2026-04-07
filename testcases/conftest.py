"""
Pytest 全局夹具配置
"""
import pytest
import time
import re
from common.requests_client import client
from utils.logger import logger


# 存储测试数据和断言信息
test_data_store = {}

# 存储当前测试项
current_test_item = None


@pytest.fixture(scope="session")
def api_client():
    """API 客户端夹具（会话级别）"""
    logger.info("初始化 API 客户端")
    return client


@pytest.fixture(scope="function")
def test_data():
    """测试数据夹具"""
    timestamp = int(time.time())
    return {
        "timestamp": timestamp,
        "member": {
            "name": f"测试会员_{timestamp}",
            "phone": f"138{timestamp % 100000000:08d}",
            "points": 100
        },
        "goods": {
            "name": f"测试商品_{timestamp}",
            "price": 99.99,
            "stock": 100
        },
        "role": {
            "name": f"测试角色_{timestamp}",
            "code": f"TEST_{timestamp}"
        },
        "employee": {
            "username": f"testuser_{timestamp}",
            "name": f"测试用户_{timestamp}",
            "phone": f"138{timestamp % 100000000:08d}"
        }
    }


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item):
    """测试开始前的钩子"""
    global current_test_item
    current_test_item = item
    nodeid = item.nodeid
    logger.info(f"pytest_runtest_setup: 初始化 test_data_store for {nodeid}")
    test_data_store[nodeid] = {
        "assertions": [],
        "response_info": []
    }
    logger.info(f"test_data_store 现在有 {len(test_data_store)} 个条目")
    yield


@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_header(cells):
    """修改测试报告表格头部"""
    # 在 duration 列之前添加断言内容、接口和响应摘要列
    cells.insert(2, '<th>断言内容</th>')
    cells.insert(3, '<th>接口</th>')
    cells.insert(4, '<th>响应内容</th>')


# 解码 Unicode 转义序列为中文
def decode_unicode_escape(s):
    """将 Unicode 转义序列解码为中文字符"""
    def replace_unicode(match):
        return chr(int(match.group(1), 16))
    return re.sub(r'\\u([0-9a-fA-F]{4})', replace_unicode, s)


@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_row(report, cells):
    """修改测试报告表格行"""
    # 获取测试数据
    nodeid = report.nodeid
    logger.info(f"pytest_html_results_table_row: 处理 {nodeid}")
    logger.info(f"test_data_store 中的键: {list(test_data_store.keys())}")
    
    # 解码测试用例名称中的 Unicode 转义序列
    for i, cell in enumerate(cells):
        if 'test_' in cell and '[' in cell:
            cells[i] = decode_unicode_escape(cell)
    
    assertions = []
    response_info = []
    
    if nodeid in test_data_store:
        logger.info(f"找到 nodeid {nodeid} 在 test_data_store 中")
        assertions = test_data_store[nodeid].get("assertions", [])
        response_info = test_data_store[nodeid].get("response_info", [])
        logger.info(f"断言数量: {len(assertions)}")
        logger.info(f"响应信息数量: {len(response_info)}")
    else:
        logger.info(f"未找到 nodeid {nodeid} 在 test_data_store 中")
    
    # 生成断言内容摘要
    assertion_content = []
    for assertion in assertions:
        status_icon = "✅" if assertion["status"] == "passed" else "❌"
        # 提取实际值（如果有）
        actual_value = assertion.get("actual", "")
        if actual_value:
            assertion_content.append(f"{status_icon} {assertion['message']}: {actual_value}")
        else:
            assertion_content.append(f"{status_icon} {assertion['message']}")
    assertion_content_html = '<br>'.join(assertion_content) if assertion_content else "无"
    
    # 计算接口统计
    interface_html = f"{len(response_info)}个"
    
    # 生成响应内容摘要，过滤掉 GET checkedToken 接口
    response_content = []
    for resp_info in response_info:
        status_code = resp_info['status_code']
        method = resp_info['method']
        url = resp_info['url']
        # 提取 URL 路径部分
        url_path = url.split('://')[1].split('/')[1:]
        url_summary = '/'.join(url_path)
        
        # 过滤掉 GET checkedToken 接口
        if method == 'GET' and 'checkedToken' in url_summary:
            continue
        
        # 尝试提取响应体中的关键信息
        response_body = resp_info.get('response_body', '')
        if response_body:
            # 简单处理，显示响应体的前 200 个字符
            if len(response_body) > 200:
                body_summary = response_body[:200] + '...'
            else:
                body_summary = response_body
        else:
            body_summary = "无"
        
        response_content.append(f"{method} {url_summary} ({status_code})\n{body_summary}")
    response_html = '<br>'.join(response_content) if response_content else "无"
    
    # 在 duration 列之前插入断言内容、接口和响应内容信息
    cells.insert(2, f'<td style="font-size: 12px; max-width: 200px; overflow: auto; white-space: pre-wrap;">{assertion_content_html}</td>')
    cells.insert(3, f'<td>{interface_html}</td>')
    cells.insert(4, f'<td style="font-size: 12px; max-width: 300px; overflow: auto; white-space: pre-wrap;">{response_html}</td>')


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """测试报告生成钩子"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        nodeid = item.nodeid
        logger.info(f"pytest_runtest_makereport: 处理 {nodeid}")
        if nodeid in test_data_store:
            # 获取断言信息和响应信息
            assertions = test_data_store[nodeid].get("assertions", [])
            response_info = test_data_store[nodeid].get("response_info", [])
            logger.info(f"断言数量: {len(assertions)}")
            logger.info(f"响应信息数量: {len(response_info)}")
            
            # 添加到报告的 extra 信息中
            if not hasattr(report, "extra"):
                report.extra = []
            
            # 单独添加断言信息部分
            if assertions:
                assertion_html = "<h3 style='color: #333; border-bottom: 1px solid #ddd; padding-bottom: 5px;'>断言详情</h3>"
                assertion_html += "<table style='width: 100%; border-collapse: collapse; margin: 10px 0;'>"
                assertion_html += "<tr style='background-color: #f5f5f5;'><th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>描述</th><th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>期望值</th><th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>实际值</th><th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>状态</th></tr>"
                for assertion in assertions:
                    status_style = "background-color: #d4edda; color: #155724;" if assertion["status"] == "passed" else "background-color: #f8d7da; color: #721c24;"
                    assertion_html += f"<tr style='{status_style}'><td style='border: 1px solid #ddd; padding: 8px;'>{assertion['message']}</td><td style='border: 1px solid #ddd; padding: 8px;'>{assertion['expected']}</td><td style='border: 1px solid #ddd; padding: 8px;'>{assertion['actual']}</td><td style='border: 1px solid #ddd; padding: 8px; font-weight: bold;'>{assertion['status']}</td></tr>"
                assertion_html += "</table>"
                # 使用正确的方式添加 HTML 内容
                report.extra.append({"name": "断言详情", "value": assertion_html, "format": "html"})
            
            # 单独添加接口响应信息部分
            if response_info:
                response_html = "<h3 style='color: #333; border-bottom: 1px solid #ddd; padding-bottom: 5px;'>接口响应信息</h3>"
                for i, resp_info in enumerate(response_info, 1):
                    # 过滤掉 GET checkedToken 接口
                    method = resp_info['method']
                    url = resp_info['url']
                    url_path = url.split('://')[1].split('/')[1:]
                    url_summary = '/'.join(url_path)
                    if method == 'GET' and 'checkedToken' in url_summary:
                        continue
                    
                    response_html += f"<div style='margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'>"
                    response_html += f"<h4 style='margin-top: 0; color: #007bff;'>请求 {i}: {resp_info['method']} {resp_info['url']}</h4>"
                    response_html += f"<p><strong>状态码:</strong> {resp_info['status_code']}</p>"
                    if resp_info.get('request_body'):
                        response_html += f"<p><strong>请求体:</strong></p><pre style='background-color: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto;'>{resp_info['request_body']}</pre>"
                    if resp_info.get('response_body'):
                        response_html += f"<p><strong>响应体:</strong></p><pre style='background-color: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto;'>{resp_info['response_body']}</pre>"
                    response_html += "</div>"
                # 使用正确的方式添加 HTML 内容
                report.extra.append({"name": "接口响应信息", "value": response_html, "format": "html"})
