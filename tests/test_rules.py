from datetime import time

from scheduler.models import Employee, Shift
from scheduler.rules import (
    check_all,
    check_availability,
    check_max_hours,
    check_rest_between_shifts,
)


def make_shift(employee, day, start_hour, end_hour):
    return Shift(employee, day, time(start_hour), time(end_hour))


def make_employee(max_hours=40.0):
    return Employee(
        "Alex",
        "server",
        15.0,
        max_hours=max_hours,
        availability={
            "Mon": (time(11), time(22)),
            "Tue": (time(7), time(22)),
        },
    )


def test_shift_inside_availability_is_ok():
    alex = make_employee()
    assert check_availability([make_shift(alex, "Mon", 12, 20)]) == []


def test_flags_unavailable_day():
    alex = make_employee()
    violations = check_availability([make_shift(alex, "Wed", 12, 20)])
    assert len(violations) == 1
    assert "unavailable" in violations[0].message


def test_flags_shift_outside_window():
    alex = make_employee()
    violations = check_availability([make_shift(alex, "Mon", 9, 17)])
    assert len(violations) == 1
    assert "outside" in violations[0].message


def test_flags_over_max_hours():
    alex = make_employee(max_hours=10)
    shifts = [make_shift(alex, "Mon", 11, 19), make_shift(alex, "Tue", 11, 15)]
    violations = check_max_hours(shifts)
    assert len(violations) == 1
    assert violations[0].employee == "Alex"


def test_flags_clopen():
    alex = make_employee()
    shifts = [make_shift(alex, "Mon", 15, 23), make_shift(alex, "Tue", 7, 15)]
    violations = check_rest_between_shifts(shifts)
    assert len(violations) == 1
    assert "8.0 hours of rest" in violations[0].message


def test_enough_rest_is_ok():
    alex = make_employee()
    shifts = [make_shift(alex, "Mon", 11, 19), make_shift(alex, "Tue", 11, 19)]
    assert check_rest_between_shifts(shifts) == []


def test_check_all_combines_rules():
    alex = make_employee(max_hours=5)
    shifts = [make_shift(alex, "Wed", 11, 19)]  # unavailable AND over max hours
    assert len(check_all(shifts)) == 2