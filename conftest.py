"""
项目根目录的 conftest.py - 全局配置
"""
import pytest


def pytest_html_report_title(report):
    """自定义报告标题"""
    report.title = "API 自动化测试报告"


def pytest_html_results_summary(prefix, summary, postfix):
    """自定义报告摘要"""
    prefix.extend([
        "<h2>测试环境信息</h2>",
        "<ul>",
        f"<li><strong>环境:</strong> {getattr(pytest, 'env', 'test')}</li>",
        "</ul>"
    ])


def pytest_configure(config):
    """配置 pytest"""
    # 设置环境变量
    import os
    pytest.env = os.getenv("ENV", "test")
    
    # 添加自定义 CSS
    config._metadata = {
        "项目名称": "SupermarketManagerAPI 自动化测试",
        "测试环境": pytest.env,
        "测试框架": "pytest",
        "报告工具": "pytest-html"
    }


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_html(report, data):
    """添加自定义 CSS 样式"""
    css_style = """
    <style>
        .requests-container, .responses-container, .assertions-container {
            max-height: 300px;
            overflow-y: auto;
            font-size: 12px;
        }
        
        .request-item, .response-item, .assertion-item {
            border: 1px solid #ddd;
            margin-bottom: 10px;
            border-radius: 4px;
            background: #f9f9f9;
        }
        
        .request-header, .response-header, .assertion-header {
            background: #e9e9e9;
            padding: 5px 10px;
            font-weight: bold;
            border-bottom: 1px solid #ddd;
        }
        
        .request-body, .response-body, .assertion-details {
            padding: 10px;
        }
        
        .method {
            background: #007bff;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            margin-right: 10px;
            font-size: 11px;
        }
        
        .url {
            color: #333;
        }
        
        .status-code {
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
        }
        
        .status-code.success {
            background: #28a745;
            color: white;
        }
        
        .status-code.error {
            background: #dc3545;
            color: white;
        }
        
        .assertion-item.success {
            border-left: 4px solid #28a745;
        }
        
        .assertion-item.error {
            border-left: 4px solid #dc3545;
        }
        
        .status-icon {
            font-weight: bold;
            margin-right: 5px;
        }
        
        .assertion-item.success .status-icon {
            color: #28a745;
        }
        
        .assertion-item.error .status-icon {
            color: #dc3545;
        }
        
        pre {
            background: #f4f4f4;
            padding: 8px;
            border-radius: 4px;
            overflow-x: auto;
            margin: 5px 0;
            font-family: monospace;
            font-size: 11px;
        }
        
        .no-data {
            color: #999;
            font-style: italic;
            padding: 10px;
        }
        
        .expected {
            color: #28a745;
            margin: 3px 0;
        }
        
        .actual {
            color: #dc3545;
            margin: 3px 0;
        }
        
        .params, .body {
            margin: 5px 0;
        }
        
        td.request_data, td.response_data, td.assertions {
            min-width: 300px;
            max-width: 400px;
        }
    </style>
    """
    data.append(css_style)
