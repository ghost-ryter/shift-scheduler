from dataclasses import dataclass, field
from datetime import time


@dataclass
class Employee:
    name: str
    role: str
    hourly_rate: float
    max_hours: float = 40.0
    availability: dict[str, tuple[time, time]] = field(default_factory=dict)


@dataclass
class Shift:
    employee: Employee
    day: str
    start: time
    end: time

    @property
    def hours(self) -> float:
        start_hours = self.start.hour + self.start.minute / 60
        end_hours = self.end.hour + self.end.minute / 60
        return end_hours - start_hours