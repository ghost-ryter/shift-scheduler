from datetime import time
from pathlib import Path

from scheduler.loader import load_employees

SAMPLE_FILE = Path(__file__).parent.parent / "data" / "employees.sample.json"


def test_loads_all_employees():
    employees = load_employees(SAMPLE_FILE)
    assert len(employees) == 6


def test_employee_fields():
    employees = load_employees(SAMPLE_FILE)
    alex = employees[0]
    assert alex.name == "Alex Rivera"
    assert alex.role == "server"
    assert alex.hourly_rate == 15.0
    assert alex.max_hours == 40.0  # default applied


def test_custom_max_hours():
    employees = load_employees(SAMPLE_FILE)
    jordan = employees[1]
    assert jordan.max_hours == 30


def test_availability_parsed_to_times():
    employees = load_employees(SAMPLE_FILE)
    alex = employees[0]
    assert alex.availability["Mon"] == (time(11, 0), time(22, 0))
    