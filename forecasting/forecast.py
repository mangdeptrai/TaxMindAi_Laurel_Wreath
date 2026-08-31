from copy import deepcopy

from taxtwin.calculator import calculate_vat
from taxtwin.calculator import calculate_cit


def forecast_company(
    company,
    revenue_growth,
    cost_growth
):

    forecast = deepcopy(company)

    forecast.revenue *= (1 + revenue_growth)
    forecast.cost *= (1 + cost_growth)

    return forecast