"""债券路由模块 /api/bond/*。

提供债券（不含可转债）的列表查询和详情查询等端点。
底层调用 xtquant.xtdata 的相关接口：
- xtdata.get_stock_list_in_sector()  — 通过板块获取债券列表
- xtdata.get_instrument_detail()     — 获取债券合约详情
"""

from fastapi import APIRouter, Query
from xtquant import xtdata

from ..helpers import _numpy_to_python

router = APIRouter(prefix="/api/bond", tags=["bond"])

# 债券板块名称（按优先级尝试）
BOND_SECTORS = ["沪深债券", "沪市债券", "深市债券"]


@router.get("/list")
def get_bond_list():
    """获取沪深债券代码列表（不含可转债）。

    依次尝试多个板块名称，合并去重后返回。

    Returns:
        count: 债券数量。
        stocks: 债券代码列表。

    底层调用: xtdata.get_stock_list_in_sector()
    """
    stock_set = set()
    for sector in BOND_SECTORS:
        try:
            result = xtdata.get_stock_list_in_sector(sector)
            if result:
                stock_set.update(result)
        except Exception:
            continue

    stock_list = sorted(stock_set)
    return {"count": len(stock_list), "stocks": stock_list}


@router.get("/detail")
def get_bond_detail(
    stock: str = Query(..., description="债券代码，如 019733.SH"),
):
    """获取债券合约详情。

    Args:
        stock: 债券代码。

    Returns:
        stock: 债券代码。
        data: 债券合约详情（含名称、上市日期、到期日等）。

    底层调用: xtdata.get_instrument_detail(stock)
    """
    raw = xtdata.get_instrument_detail(stock)
    return {"stock": stock, "data": _numpy_to_python(raw)}
