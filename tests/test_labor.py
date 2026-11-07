from datetime import time

import pytest

from scheduler.labor import (
    employee_cost,
    hours_by_employee,
    labor_percent,
    total_labor_cost,
)
from scheduler.models import Employee, Shift


def make_shift(employee, day, start_hour, end_hour):
    return Shift(employee, day, time(start_hour), time(end_hour))


def test_cost_without_overtime():
    assert employee_cost(15.0, 30) == 450.0


def test_cost_with_overtime():
    # 40 regular hours at $20 + 5 overtime hours at $30
    assert employee_cost(20.0, 45) == 950.0


def test_hours_by_employee():
    alex = Employee("Alex", "server", 15.0)
    shifts = [
        make_shift(alex, "Mon", 11, 19),
        make_shift(alex, "Tue", 11, 17),
    ]
    assert hours_by_employee(shifts) == {"Alex": 14.0}


def test_total_labor_cost_multiple_employees():
    alex = Employee("Alex", "server", 15.0)
    sam = Employee("Sam", "bartender", 18.0)
    shifts = [
        make_shift(alex, "Mon", 10, 18),  # 8 hrs x $15 = $120
        make_shift(sam, "Mon", 16, 22),   # 6 hrs x $18 = $108
    ]
    assert total_labor_cost(shifts) == 228.0


def test_labor_percent():
    assert labor_percent(300.0, 1000.0) == 30.0


def test_labor_percent_rejects_zero_sales():
    with pytest.raises(ValueError):
        labor_percent(300.0, 0)