import pytest
import pandas as pd
from src.metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)


@pytest.fixture
def sample_df():
    # 6 employees: 3 leavers (ids 1, 2, 5), 3 stayers (ids 3, 4, 6)
    # Sales: 2 leavers / 2 employees = 100%
    # HR:    0 leavers / 2 employees = 0%
    # IT:    1 leaver  / 2 employees = 50%
    # Overtime Yes: 3 leavers / 3 employees = 100%
    # Overtime No:  0 leavers / 3 employees = 0%
    # Satisfaction 1: 1/2 = 50%, Satisfaction 2: 2/2 = 100%, Satisfaction 3: 0/2 = 0%
    # Avg income leavers: (3000+4000+5000)/3 = 4000.0, stayers: (6000+7000+8000)/3 = 7000.0
    return pd.DataFrame({
        "employee_id":      [1,       2,       3,     4,     5,     6],
        "department":       ["Sales", "Sales", "HR",  "HR",  "IT",  "IT"],
        "overtime":         ["Yes",   "Yes",   "No",  "No",  "Yes", "No"],
        "monthly_income":   [3000,    4000,    6000,  7000,  5000,  8000],
        "job_satisfaction": [1,       2,       1,     3,     2,     3],
        "attrition":        ["Yes",   "Yes",   "No",  "No",  "Yes", "No"],
    })


# --- attrition_rate ---

def test_attrition_rate_returns_expected_percent():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "attrition": ["Yes", "No", "No", "Yes"],
    })
    assert attrition_rate(df) == 50.0


def test_attrition_rate_no_leavers(sample_df):
    df = sample_df.copy()
    df["attrition"] = "No"
    assert attrition_rate(df) == 0.0


def test_attrition_rate_all_leavers(sample_df):
    df = sample_df.copy()
    df["attrition"] = "Yes"
    assert attrition_rate(df) == 100.0


# --- attrition_by_department ---

def test_attrition_by_department_returns_expected_columns(sample_df):
    result = attrition_by_department(sample_df)
    assert list(result.columns) == ["department", "employees", "leavers", "attrition_rate"]


def test_attrition_by_department_correct_rates(sample_df):
    result = attrition_by_department(sample_df)
    rates = dict(zip(result["department"], result["attrition_rate"]))
    assert rates["Sales"] == 100.0
    assert rates["IT"] == 50.0
    assert rates["HR"] == 0.0


def test_attrition_by_department_sorted_descending(sample_df):
    result = attrition_by_department(sample_df)
    assert list(result["attrition_rate"]) == sorted(result["attrition_rate"], reverse=True)


# --- attrition_by_overtime ---

def test_attrition_by_overtime_returns_expected_columns(sample_df):
    result = attrition_by_overtime(sample_df)
    assert list(result.columns) == ["overtime", "employees", "leavers", "attrition_rate"]


def test_attrition_by_overtime_correct_rates(sample_df):
    result = attrition_by_overtime(sample_df)
    rates = dict(zip(result["overtime"], result["attrition_rate"]))
    assert rates["Yes"] == 100.0
    assert rates["No"] == 0.0


def test_attrition_by_overtime_correct_headcounts(sample_df):
    result = attrition_by_overtime(sample_df)
    counts = dict(zip(result["overtime"], result["employees"]))
    assert counts["Yes"] == 3
    assert counts["No"] == 3


# --- average_income_by_attrition ---

def test_average_income_by_attrition_returns_expected_columns(sample_df):
    result = average_income_by_attrition(sample_df)
    assert list(result.columns) == ["attrition", "avg_monthly_income"]


def test_average_income_by_attrition_correct_values(sample_df):
    result = average_income_by_attrition(sample_df)
    income = dict(zip(result["attrition"], result["avg_monthly_income"]))
    assert income["Yes"] == 4000.0   # (3000 + 4000 + 5000) / 3
    assert income["No"] == 7000.0    # (6000 + 7000 + 8000) / 3


# --- satisfaction_summary ---

def test_satisfaction_summary_returns_expected_columns(sample_df):
    result = satisfaction_summary(sample_df)
    assert list(result.columns) == ["job_satisfaction", "total_employees", "leavers", "attrition_rate"]


def test_satisfaction_summary_correct_rates(sample_df):
    result = satisfaction_summary(sample_df)
    rates = dict(zip(result["job_satisfaction"], result["attrition_rate"]))
    assert rates[1] == 50.0    # 1 leaver / 2 employees
    assert rates[2] == 100.0   # 2 leavers / 2 employees
    assert rates[3] == 0.0     # 0 leavers / 2 employees


def test_satisfaction_summary_sorted_by_satisfaction(sample_df):
    result = satisfaction_summary(sample_df)
    assert list(result["job_satisfaction"]) == sorted(result["job_satisfaction"])
