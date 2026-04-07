"""
员工数据模型
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    """员工模型"""
    id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    deptId: Optional[int] = None
    deptName: Optional[str] = None
    status: Optional[int] = 1  # 1-在职, 0-离职
    avatar: Optional[str] = None
    remark: Optional[str] = None


@dataclass
class EmployeeQuery:
    """员工查询参数"""
    currentPage: int = 1
    pageSize: int = 10
    username: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    deptId: Optional[int] = None
    status: Optional[int] = None