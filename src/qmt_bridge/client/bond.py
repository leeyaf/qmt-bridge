"""BondMixin — 债券数据客户端方法。

封装了债券（不含可转债）相关的查询接口。

底层对应 xtquant 的 ``xtdata.get_stock_list_in_sector()`` 和
``xtdata.get_instrument_detail()`` 等函数。
"""


class BondMixin:
    """债券数据客户端方法集合，对应 /api/bond/* 端点。"""

    def get_bond_list(self) -> list[str]:
        """获取全部债券代码列表（不含可转债）。

        Returns:
            债券代码列表，如 ``["019733.SH", "127045.SZ", ...]``
        """
        resp = self._get("/api/bond/list")
        return resp.get("stocks", [])

    def get_bond_detail(self, stock: str) -> dict:
        """获取债券合约详情。

        Args:
            stock: 债券代码，如 ``"019733.SH"``

        Returns:
            债券合约详情字典
        """
        resp = self._get("/api/bond/detail", {"stock": stock})
        return resp.get("data", {})
