from collections import defaultdict

from .models import Shift

OVERTIME_THRESHOLD = 40.0
OVERTIME_MULTIPLIER = 1.5


def hours_by_employee(shifts: list[Shift]) -> dict[str, float]:
    """Total scheduled hours for each employee."""
    totals: dict[str, float] = defaultdict(float)
    for shift in shifts:
        totals[shift.employee.name] += shift.hours
    return dict(totals)


def employee_cost(hourly_rate: float, hours: float) -> float:
    """Pay for one employee, with time-and-a-half past 40 hours."""
    regular_hours = min(hours, OVERTIME_THRESHOLD)
    overtime_hours = max(hours - OVERTIME_THRESHOLD, 0)
    return (
        regular_hours * hourly_rate
        + overtime_hours * hourly_rate * OVERTIME_MULTIPLIER
    )


def total_labor_cost(shifts: list[Shift]) -> float:
    """Total labor cost for a whole schedule."""
    hours = hours_by_employee(shifts)
    rates = {s.employee.name: s.employee.hourly_rate for s in shifts}
    return sum(employee_cost(rates[name], h) for name, h in hours.items())


def labor_percent(labor_cost: float, projected_sales: float) -> float:
    """Labor cost as a percentage of projected sales."""
    if projected_sales <= 0:
        raise ValueError("projected_sales must be greater than zero")
    return labor_cost / projected_sales * 100