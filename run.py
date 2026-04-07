#!/usr/bin/env python
"""
测试执行入口脚本
"""
import sys
import os
import argparse
import pytest

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="接口自动化测试执行器")
    parser.add_argument(
        "-m", "--marker",
        help="执行指定标记的测试用例，如: smoke, p0, regression"
    )
    parser.add_argument(
        "-n", "--workers",
        type=int,
        default=1,
        help="并行执行的进程数"
    )
    parser.add_argument(
        "-k", "--keyword",
        help="执行名称包含关键字的测试用例"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="生成 HTML 报告"
    )
    parser.add_argument(
        "--allure",
        action="store_true",
        help="生成 Allure 报告"
    )
    parser.add_argument(
        "--env",
        default="test",
        choices=["dev", "test", "prod"],
        help="测试环境"
    )
    parser.add_argument(
        "--no-cov",
        action="store_true",
        help="不生成覆盖率报告"
    )

    args = parser.parse_args()

    # 设置环境变量
    os.environ["ENV"] = args.env

    # 构建 pytest 参数
    pytest_args = []

    # 添加测试路径
    pytest_args.append("testcases/")

    if args.marker:
        pytest_args.extend(["-m", args.marker])

    if args.keyword:
        pytest_args.extend(["-k", args.keyword])

    if args.workers > 1:
        pytest_args.extend(["-n", str(args.workers)])

    # 基本参数
    pytest_args.extend(["-v", "-s"])

    # 报告相关（如果指定）
    if args.html:
        pytest_args.extend(["--html=reports/report.html", "--self-contained-html"])

    if args.allure:
        pytest_args.extend(["--alluredir=allure-results"])

    # 执行测试
    print(f"执行参数: {pytest_args}")
    print(f"测试环境: {args.env}")
    print(f"当前目录: {os.getcwd()}")
    print("=" * 50)

    exit_code = pytest.main(pytest_args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()