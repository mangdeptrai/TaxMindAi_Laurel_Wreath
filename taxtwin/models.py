from dataclasses import dataclass


@dataclass
class Company:
    company_name: str
    revenue: float
    cost: float
    vat_input: float
    vat_output: float