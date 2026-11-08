from datetime import time
from pathlib import Path

from scheduler.loader import load_employees, load_requirements
from scheduler.models import Employee, Requirement
from scheduler.rules import check_all
from scheduler.scheduler import build_schedule

DATA = Path(__file__).parent.parent / "data"


def test_unfilled_when_nobody_qualified():
    server = Employee(
        "A", "server", 15.0, availability={"Mon": (time(9), time(22))}
    )
    req = Requirement("Mon", "bartender", time(16), time(22))
    shifts, unfilled = build_schedule([server], [req])
    assert shifts == []
    assert len(unfilled) == 1


def test_balances_hours_between_employees():
    availability = {"Mon": (time(9), time(22)), "Tue": (time(9), time(22))}
    a = Employee("A", "cook", 15.0, availability=availability)
    b = Employee("B", "cook", 15.0, availability=availability)
    reqs = [
        Requirement("Mon", "cook", time(10), time(18)),
        Requirement("Tue", "cook", time(10), time(18)),
    ]
    shifts, unfilled = build_schedule([a, b], reqs)
    assert unfilled == []
    assert {s.employee.name for s in shifts} == {"A", "B"}


def test_sample_schedule_has_no_rule_violations():
    employees = load_employees(DATA / "employees.sample.json")
    requirements = load_requirements(DATA / "demand.sample.csv")
    shifts, _ = build_schedule(employees, requirements)
    assert check_all(shifts) == []


def test_sample_data_leaves_friday_server_gap():
    employees = load_employees(DATA / "employees.sample.json")
    requirements = load_requirements(DATA / "demand.sample.csv")
    _, unfilled = build_schedule(employees, requirements)
    assert any(r.day == "Fri" and r.role == "server" for r in unfilled)