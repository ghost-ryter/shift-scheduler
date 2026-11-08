from collections import defaultdict
from dataclasses import dataclass
from datetime import time

from .labor import hours_by_employee
from .models import Shift

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MIN_REST_HOURS = 10.0


@dataclass
class Violation:
    employee: str
    day: str
    message: str


def _to_hours(t: time) -> float:
    return t.hour + t.minute / 60


def check_availability(shifts: list[Shift]) -> list[Violation]:
    """Flag shifts on unavailable days or outside the availability window."""
    violations = []
    for shift in shifts:
        window = shift.employee.availability.get(shift.day)
        if window is None:
            violations.append(
                Violation(shift.employee.name, shift.day, "scheduled on a day they are unavailable")
            )
        elif shift.start < window[0] or shift.end > window[1]:
            violations.append(
                Violation(shift.employee.name, shift.day, "scheduled outside their availability window")
            )
    return violations


def check_max_hours(shifts: list[Shift]) -> list[Violation]:
    """Flag employees scheduled for more than their max weekly hours."""
    violations = []
    totals = hours_by_employee(shifts)
    limits = {s.employee.name: s.employee.max_hours for s in shifts}
    for name, total in totals.items():
        if total > limits[name]:
            violations.append(
                Violation(name, "week", f"scheduled {total:.1f} hours, over their limit of {limits[name]:.1f}")
            )
    return violations


def check_rest_between_shifts(
    shifts: list[Shift], min_rest: float = MIN_REST_HOURS
) -> list[Violation]:
    """Flag back-to-back shifts with less than min_rest hours between them."""
    violations = []
    by_employee: dict[str, list[Shift]] = defaultdict(list)
    for shift in shifts:
        by_employee[shift.employee.name].append(shift)

    for name, employee_shifts in by_employee.items():
        employee_shifts.sort(key=lambda s: (DAYS.index(s.day), s.start))
        for earlier, later in zip(employee_shifts, employee_shifts[1:]):
            day_gap = DAYS.index(later.day) - DAYS.index(earlier.day)
            rest = day_gap * 24 - _to_hours(earlier.end) + _to_hours(later.start)
            if rest < min_rest:
                violations.append(
                    Violation(name, later.day, f"only {rest:.1f} hours of rest before this shift")
                )
    return violations


def check_all(shifts: list[Shift]) -> list[Violation]:
    """Run every rule check and return all violations."""
    return (
        check_availability(shifts)
        + check_max_hours(shifts)
        + check_rest_between_shifts(shifts)
    )
