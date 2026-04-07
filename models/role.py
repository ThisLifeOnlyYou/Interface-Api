"""
角色数据模型
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Role:
    """角色模型"""
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[int] = 1  # 1-启用, 0-停用
    description: Optional[str] = None
    createTime: Optional[str] = None
    updateTime: Optional[str] = None


@dataclass
class RoleQuery:
    """角色查询参数"""
    currentPage: int = 1
    pageSize: int = 10
    name: Optional[str] = None
    status: Optional[int] = None


@dataclass
class RolePermission:
    """角色权限"""
    roleId: int
    menuIds: List[int]