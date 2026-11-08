import csv
import json
from datetime import time
from pathlib import Path

from .models import Employee, Requirement


def _parse_time(text: str) -> time:
    """Turn '11:00' into a time object."""
    return time.fromisoformat(text)


def load_employees(path: str | Path) -> list[Employee]:
    """Read employees from a JSON file."""
    with open(path) as f:
        raw_employees = json.load(f)

    employees = []
    for item in raw_employees:
        availability = {
            day: (_parse_time(window[0]), _parse_time(window[1]))
            for day, window in item.get("availability", {}).items()
        }
        employees.append(
            Employee(
                name=item["name"],
                role=item["role"],
                hourly_rate=item["hourly_rate"],
                max_hours=item.get("max_hours", 40.0),
                availability=availability,
            )
        )
    return employees

def load_requirements(path: str | Path) -> list[Requirement]:
    """Read staffing requirements from a CSV file."""
    with open(path, newline="") as f:
        return [
            Requirement(
                day=row["day"],
                role=row["role"],
                start=_parse_time(row["start"]),
                end=_parse_time(row["end"]),
                count=int(row["count"]),
            )
            for row in csv.DictReader(f)
        ]