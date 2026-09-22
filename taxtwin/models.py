from dataclasses import dataclass


@dataclass
class Company:
    store_id: str
    month: str
    revenue: float
    cogs: float
    operating_cost: float
    profit_before_tax: float
    orders: int
    customers: int
    conversion_rate: float
    ending_inventory: int