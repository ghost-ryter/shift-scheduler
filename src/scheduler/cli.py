import argparse
from pathlib import Path

from .labor import employee_cost, hours_by_employee, labor_percent, total_labor_cost
from .loader import load_employees, load_requirements
from .models import Requirement, Shift
from .rules import DAYS, Violation, check_all
from .scheduler import build_schedule


def _fmt(t) -> str:
    return t.strftime("%H:%M")


def print_schedule(shifts: list[Shift]) -> None:
    print("WEEKLY SCHEDULE")
    print("-" * 50)
    for day in DAYS:
        day_shifts = sorted(
            (s for s in shifts if s.day == day),
            key=lambda s: (s.start, s.employee.role, s.employee.name),
        )
        print(day)
        if not day_shifts:
            print("  (no shifts)")
        for s in day_shifts:
            print(f"  {_fmt(s.start)}-{_fmt(s.end)}  {s.employee.role:<10} {s.employee.name}")
    print()


def print_labor_report(shifts: list[Shift], projected_sales: float | None) -> None:
    print("LABOR REPORT")
    print("-" * 50)
    hours = hours_by_employee(shifts)
    rates = {s.employee.name: s.employee.hourly_rate for s in shifts}
    for name, h in sorted(hours.items()):
        flag = "  OVERTIME" if h > 40 else ""
        print(f"  {name:<16}{h:>6.1f} hrs  ${employee_cost(rates[name], h):>9,.2f}{flag}")
    cost = total_labor_cost(shifts)
    print(f"  Total labor cost: ${cost:,.2f}")
    if projected_sales:
        pct = labor_percent(cost, projected_sales)
        print(f"  Labor % of projected sales (${projected_sales:,.0f}): {pct:.1f}%")
    print()


def print_unfilled(unfilled: list[Requirement]) -> None:
    print("UNFILLED SLOTS")
    print("-" * 50)
    if not unfilled:
        print("  None. Every requirement is covered.")
    for r in unfilled:
        print(f"  {r.day} {_fmt(r.start)}-{_fmt(r.end)}  {r.role}")
    print()


def print_violations(violations: list[Violation]) -> None:
    print("RULE VIOLATIONS")
    print("-" * 50)
    if not violations:
        print("  None.")
    for v in violations:
        print(f"  {v.employee} ({v.day}): {v.message}")
    print()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Build a weekly shift schedule and labor cost report."
    )
    parser.add_argument("--employees", type=Path, default=Path("data/employees.sample.json"))
    parser.add_argument("--demand", type=Path, default=Path("data/demand.sample.csv"))
    parser.add_argument(
        "--sales", type=float, default=15000.0, help="projected weekly sales in dollars"
    )
    args = parser.parse_args(argv)

    employees = load_employees(args.employees)
    requirements = load_requirements(args.demand)
    shifts, unfilled = build_schedule(employees, requirements)

    print_schedule(shifts)
    print_labor_report(shifts, args.sales)
    print_unfilled(unfilled)
    print_violations(check_all(shifts))


if __name__ == "__main__":
    main()