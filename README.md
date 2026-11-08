# shift-scheduler

![Tests](https://github.com/ghost-ryter/shift-scheduler/actions/workflows/tests.yml/badge.svg)

A Python command-line tool that builds a weekly restaurant shift schedule from employee availability and staffing needs, then reports labor cost, labor percentage, rule violations, and coverage gaps.

## Why I built this

Scheduling is one of the biggest time sinks in a restaurant manager's week, and it's easy to miss something, especially with a team of 100+ people where every schedule passes through several levels of review and errors still slip through. I wanted a tool that catches those problems automatically: availability conflicts, overtime, short turnarounds between closing and opening shifts, and coverage gaps, while tracking labor cost against projected sales. The goal is a schedule that works for both the business and the team, so managers spend less time double-checking and more time running the floor.

## Features

- Loads employees (role, pay rate, availability, max hours) from JSON
- Loads staffing requirements by day, role, and time from CSV
- Builds a schedule with a greedy algorithm that spreads hours evenly
- Calculates labor cost with time-and-a-half overtime past 40 hours
- Reports labor as a percentage of projected sales
- Flags availability conflicts, max-hour overruns, and "clopens" (short rest between shifts)
- Reports requirements it couldn't fill so you can see coverage gaps

## Install

Requires Python 3.10 or newer.

```bash
git clone https://github.com/ghost-ryter/shift-scheduler.git
cd shift-scheduler
python3 -m venv .venv
source .venv/bin/activate
pip install -e . pytest
```

## Usage

```bash
shift-scheduler
shift-scheduler --sales 20000
shift-scheduler --employees my_staff.json --demand my_demand.csv
```

Run the commands from the project's top-level folder, since the default data paths are relative to it.

## Example output

```
WEEKLY SCHEDULE
--------------------------------------------------
Mon
  10:00-18:00  cook       Taylor Nguyen
  11:00-19:00  server     Alex Rivera
Tue
  10:00-18:00  cook       Taylor Nguyen
  11:00-19:00  server     Alex Rivera
Wed
  10:00-18:00  cook       Taylor Nguyen
  11:00-19:00  server     Jordan Lee
Thu
  10:00-18:00  cook       Riley Brooks
  11:00-19:00  server     Jordan Lee
  16:00-23:00  bartender  Sam Patel
Fri
  10:00-18:00  cook       Riley Brooks
  16:00-23:00  bartender  Sam Patel
  16:00-22:00  host       Casey Morgan
  16:00-23:00  server     Alex Rivera
Sat
  10:00-22:00  cook       Riley Brooks
  11:00-20:00  host       Casey Morgan
  11:00-22:00  server     Alex Rivera
  11:00-22:00  server     Jordan Lee
  16:00-23:00  bartender  Sam Patel
Sun
  10:00-18:00  cook       Riley Brooks
  11:00-19:00  host       Casey Morgan

LABOR REPORT
--------------------------------------------------
  Alex Rivera       34.0 hrs  $   510.00
  Casey Morgan      23.0 hrs  $   299.00
  Jordan Lee        27.0 hrs  $   391.50
  Riley Brooks      36.0 hrs  $   594.00
  Sam Patel         21.0 hrs  $   378.00
  Taylor Nguyen     24.0 hrs  $   408.00
  Total labor cost: $2,580.50
  Labor % of projected sales ($15,000): 17.2%

UNFILLED SLOTS
--------------------------------------------------
  Fri 16:00-23:00  server
  Sun 10:00-18:00  server

RULE VIOLATIONS
--------------------------------------------------
  None.

```

## Data formats

**Employees (JSON):**

```json
{
  "name": "Alex Rivera",
  "role": "server",
  "hourly_rate": 15.0,
  "max_hours": 40,
  "availability": { "Mon": ["11:00", "22:00"] }
}
```

**Staffing requirements (CSV):**

```
day,role,start,end,count
Fri,server,16:00,23:00,2
```

All sample data is fictional.

## How the scheduler works

Requirements are processed in day and time order. For each open slot, the scheduler considers every employee in the right role who is available, wouldn't exceed their max hours, and wouldn't be left with too little rest between shifts. It assigns the slot to whoever has the fewest scheduled hours so far. Slots with no eligible employee are reported as unfilled. This is a greedy approach: simple and explainable, but not guaranteed to find the optimal schedule.

## Project structure

```
src/scheduler/   models, loader, labor math, rules, scheduler, CLI
tests/           pytest suite
data/            sample employees and staffing requirements
```

## Run the tests

```bash
pytest
```

## Roadmap

- Labor budget cap (dollars and hours) so the scheduler stops before exceeding it
- Fairness and preferences: balance weekends and closing shifts across the team
- Handle overlapping shifts and split shifts
- CSV export of the finished schedule
- Streamlit page to view the schedule as a grid
- Smarter scheduling (backtracking) to fill more slots
- Staffing requirements driven by hourly sales forecasts