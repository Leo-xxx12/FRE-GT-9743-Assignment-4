from __future__ import annotations
from atexit import register
from typing import Any, Dict, List, Tuple
import pandas as pd
from functools import singledispatchmethod
from fixedincomelib.product.product_interfaces import Product, ProductVisitor
from fixedincomelib.product.product_portfolio import ProductPortfolio
from fixedincomelib.product.linear_products import (
    ProductBulletCashflow,
    ProductFixedAccrued,
    ProductOvernightIndexCashflow,
    ProductRFRSwap,
)


class ProductDisplayVisitor(ProductVisitor):

    def __init__(self) -> None:
        super().__init__()
        self.nvps_ = []

    @singledispatchmethod
    def visit(self, product: Product):
        raise NotImplementedError(f"No visitor for {Product._product_type}")

    def display(self) -> pd.DataFrame:
        return pd.DataFrame(self.nvps_, columns=["Name", "Value"])

    # TODO: ProductBulletCashflow

    # TODO: ProductFixedAccrued

    # TODO: ProductOvernightIndexCashflow

    # TODO: ProductRFRSwap
    # ----------------------------
    # I used str to convert some characters into str to output. But I met some errors about converting directly. So I wrote a helper to do it.
    def _safe_str(self, x):
        if x is None:
            return "N/A"

        if hasattr(x, "value_str"):
            try:
                return str(getattr(x, "value_str"))
            except Exception:
                pass

        if hasattr(x, "name"):
            try:
                return str(getattr(x, "name"))
            except Exception:
                pass
            
        if hasattr(x, "to_string"):
            try:
                return str(x.to_string())
            except Exception:
                pass

        if isinstance(x, (str, int, float, bool)):
            return str(x)

        try:
            return str(x)
        except Exception:
            return x.__class__.__name__
    
    def _add(self, name, value):
        self.nvps_.append([name, self._safe_str(value)])


    # -------------------------
    # ProductBulletCashflow
    # -------------------------
    @visit.register
    def _(self, product: ProductBulletCashflow):
        self._add("Type", "ProductBulletCashflow")
        self._add("Termination Date", product.termination_date)
        self._add("Payment Date", product.payment_date)
        currency = getattr(product, "currency_", None)
        currency_str = getattr(currency, "value_str", None)  or getattr(currency, "code", None)   or str(currency)
        self._add("Currency", currency_str)

        los = getattr(product, "long_or_short_", None)
        los_str = getattr(los, "name", None) or (los.to_string() if hasattr(los, "to_string") else str(los))
        self._add("Long/Short", los_str)
        self._add("Notional", getattr(product, "notional_", "N/A"))

    # -------------------------
    # ProductFixedAccrued
    # -------------------------
    @visit.register
    def _(self, product: ProductFixedAccrued):
        self._add("Type", "ProductFixedAccrued")
        self._add("Effective Date", product.effective_date)
        self._add("Termination Date", product.termination_date)
        self._add("Payment Date", product.payment_date)
        currency = getattr(product, "currency_", None)
        currency_str = getattr(currency, "value_str", None)  or getattr(currency, "code", None)   or  "Currency"
        self._add("Currency", currency_str)
        self._add("Notional", getattr(product, "notional_", "N/A"))
        self._add("Accrual Basis", product.accrual_basis)
        self._add("Business Day Convention", product.business_day_convention)
        self._add("Holiday Convention", product.holiday_convention)
        self._add("Accrued", product.accrued)

    # -------------------------
    # ProductOvernightIndexCashflow
    # -------------------------
    @visit.register
    def _(self, product: ProductOvernightIndexCashflow):
        self._add("Type", "ProductOvernightIndexCashflow")
        self._add("Effective Date", product.effective_date)
        self._add("Termination Date", product.termination_date)
        self._add("Payment Date", product.payment_date)
        currency = getattr(product, "currency_", None)
        currency_str = getattr(currency, "value_str", None)  or getattr(currency, "code", None)   or str(currency)
        self._add("Currency", currency_str)
        self._add("Notional", getattr(product, "notional_", "N/A"))
        self._add("ON Index", getattr(product, "on_index_str_", "N/A"))
        self._add("Compounding Method", product.compounding_method)
        self._add("Spread", product.spread)

    # -------------------------
    # ProductRFRSwap
    # -------------------------
    @visit.register
    def _(self, product: ProductRFRSwap):
        self._add("Type", "ProductRFRSwap")
        self._add("Effective Date", product.effective_date)
        self._add("Termination Date", product.termination_date)
        self._add("Currency", getattr(product, "currency_", "N/A"))
        self._add("Notional", getattr(product, "notional_", "N/A"))
        self._add("ON Index", getattr(product, "on_index_str_", "N/A"))
        self._add("Pay Offset", product.pay_offset)
        self._add("Fixed Rate", product.fixed_rate)
        self._add("Spread", product.spread)
        self._add("Pay/Receive", product.pay_or_rec)
        self._add("Accrual Period", product.accrual_period)
        self._add("Floating Accrual Period", product.floating_leg_accrual_period)
        self._add("Accrual Basis", product.accrual_basis)
        self._add("Compounding Method", product.compounding_method)
        self._add("Pay BDC", product.pay_business_day_convention)
        self._add("Pay Holiday", product.pay_holiday_convention)
