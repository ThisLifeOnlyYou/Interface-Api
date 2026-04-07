"""
出入库数据模型
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class DetailStoreGoods:
    """出入库商品详情"""
    cn: Optional[str] = None
    goodsId: Optional[int] = None
    goodsName: Optional[str] = None
    storeId: Optional[int] = None
    storeName: Optional[str] = None
    supplierId: Optional[int] = None
    supplierName: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    totalAmount: Optional[float] = None
    remark: Optional[str] = None
    status: Optional[int] = 1


@dataclass
class QueryStoreIn:
    """入库查询参数"""
    currentPage: int = 1
    pageSize: int = 10
    cn: Optional[str] = None
    goodsName: Optional[str] = None
    storeName: Optional[str] = None
    supplierName: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None