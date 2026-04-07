"""
环境配置文件
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """基础配置"""
    # API 基础地址
    BASE_URL = os.getenv("BASE_URL", "http://localhost:9291/api")

    # 请求超时时间（秒）
    TIMEOUT = 30

    # 默认分页大小
    DEFAULT_PAGE_SIZE = 10

    # 测试账号
    TEST_USERNAME = os.getenv("TEST_USERNAME", "13333333333")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "123456")

    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = BASE_DIR / "logs"

    # 报告目录
    REPORT_DIR = BASE_DIR / "reports"

    # # 数据库配置（可选）
    # DB_HOST = os.getenv("DB_HOST", "localhost")
    # DB_PORT = int(os.getenv("DB_PORT", 3306))
    # DB_USER = os.getenv("DB_USER", "root")
    # DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    # DB_NAME = os.getenv("DB_NAME", "test_db")


class TestConfig(Config):
    """测试环境配置"""
    BASE_URL = "http://127.0.0.1:9291"
    # TEST_USERNAME = "13333333333"
    # TEST_PASSWORD = "123456"
    
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
    # TEST_USERNAME = "14788888888"
    # TEST_PASSWORD = "123456"
    
    # Cookie Token 配置（多用户）
    COOKIE_TOKENS = {
        "用户A": "LOGIN_USER:23333333333",
        "用户B": "LOGIN_USER:23333333334",
        "用户C": "LOGIN_USER:23333333335"
    }
    
    # 默认使用的用户
    DEFAULT_USER = "用户A"


# 根据环境变量选择配置
env = os.getenv("ENV", "test")
config_map = {
    "test": TestConfig,
    "prod": ProdConfig
}
config = config_map.get(env, TestConfig)
