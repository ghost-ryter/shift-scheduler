from pathlib import Path

from scheduler.cli import main

DATA = Path(__file__).parent.parent / "data"


def run_cli(capsys, *extra_args):
    main(
        [
            "--employees", str(DATA / "employees.sample.json"),
            "--demand", str(DATA / "demand.sample.csv"),
            *extra_args,
        ]
    )
    return capsys.readouterr().out


def test_cli_prints_all_sections(capsys):
    out = run_cli(capsys)
    for section in ("WEEKLY SCHEDULE", "LABOR REPORT", "UNFILLED SLOTS", "RULE VIOLATIONS"):
        assert section in out


def test_cli_reports_labor_percent(capsys):
    out = run_cli(capsys, "--sales", "20000")
    assert "Labor % of projected sales ($20,000)" in out