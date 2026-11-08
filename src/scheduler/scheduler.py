from .models import Employee, Requirement, Shift
from .rules import DAYS, check_rest_between_shifts


def _is_available(employee: Employee, req: Requirement) -> bool:
    window = employee.availability.get(req.day)
    return window is not None and window[0] <= req.start and req.end <= window[1]


def build_schedule(
    employees: list[Employee], requirements: list[Requirement]
) -> tuple[list[Shift], list[Requirement]]:
    """Greedily fill each requirement, giving shifts to whoever has the fewest hours.

    Returns the shifts it built and a list of requirements it couldn't fill.
    """
    shifts: list[Shift] = []
    unfilled: list[Requirement] = []
    hours = {e.name: 0.0 for e in employees}

    ordered = sorted(requirements, key=lambda r: (DAYS.index(r.day), r.start))
    for req in ordered:
        for _ in range(req.count):
            best = None
            for employee in employees:
                if employee.role != req.role or not _is_available(employee, req):
                    continue
                candidate = Shift(employee, req.day, req.start, req.end)
                if hours[employee.name] + candidate.hours > employee.max_hours:
                    continue
                if check_rest_between_shifts(shifts + [candidate]):
                    continue
                if best is None or hours[employee.name] < hours[best.employee.name]:
                    best = candidate

            if best is None:
                unfilled.append(req)
            else:
                shifts.append(best)
                hours[best.employee.name] += best.hours

    return shifts, unfilled