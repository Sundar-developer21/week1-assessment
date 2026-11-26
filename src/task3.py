
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# --------------------------------
# 1. NUMPY OPERATIONS
# --------------------------------

marks = np.array([
    [80, 75, 90],
    [70, 85, 80],
    [90, 95, 85],
    [60, 70, 75]
])

print("Student averages:", marks.mean(axis=1))
print("Subject averages:", marks.mean(axis=0))

updated_marks = marks + 5
print("Marks after adding 5:\n", updated_marks)

weights = np.array([0.3, 0.3, 0.4])
weighted_scores = np.dot(marks, weights)
print("Weighted scores:", weighted_scores)

# --------------------------------
# 2. PANDAS DATA INSPECTION
# --------------------------------

employees = pd.read_csv(DATA_DIR / "employees.csv")

print("\nData Information:")
employees.info()

print("\nData Description:")
print(employees.describe())

print("\nUsing loc:")
print(employees.loc[0:2, ["name", "salary"]])

print("\nUsing iloc:")
print(employees.iloc[0:3, 0:3])

print("\nSalary above 50000:")
print(employees[employees["salary"] > 50000])

# --------------------------------
# 3. DATA CLEANING
# --------------------------------

cleaned = employees.copy()

# Add two missing salaries
cleaned.loc[[1, 4], "salary"] = np.nan

# Add one duplicate row
cleaned = pd.concat(
    [cleaned, cleaned.iloc[[0]]],
    ignore_index=True
)

print("\nBefore cleaning:")
print("Rows:", len(cleaned))
print("Missing salaries:", cleaned["salary"].isna().sum())

# Remove duplicate rows
cleaned = cleaned.drop_duplicates()

# Correct data types
cleaned["salary"] = pd.to_numeric(
    cleaned["salary"], errors="coerce"
)

# Fill missing salaries with median
median_salary = cleaned["salary"].median()
cleaned["salary"] = cleaned["salary"].fillna(median_salary)

cleaned["id"] = cleaned["id"].astype(int)
cleaned["salary"] = cleaned["salary"].astype(float)

print("\nAfter cleaning:")
print("Rows:", len(cleaned))
print("Missing salaries:", cleaned["salary"].isna().sum())
print(cleaned)

# --------------------------------
# 4. GROUPBY AND AGGREGATION
# --------------------------------

summary = cleaned.groupby("department").agg(
    headcount=("id", "count"),
    average_salary=("salary", "mean"),
    maximum_salary=("salary", "max")
).reset_index()

print("\nDepartment Summary:")
print(summary)

# --------------------------------
# 5. DEPARTMENT MERGING
# --------------------------------

departments = pd.read_csv(DATA_DIR / "departments.csv")

inner_merge = pd.merge(
    cleaned, departments, on="department", how="inner"
)

left_merge = pd.merge(
    cleaned, departments, on="department", how="left"
)

outer_merge = pd.merge(
    cleaned, departments, on="department", how="outer"
)

print("\nInner Merge:")
print(inner_merge)

print("\nLeft Merge:")
print(left_merge)

print("\nOuter Merge:")
print(outer_merge)

# Find departments without employees
employee_departments = set(cleaned["department"])
all_departments = set(departments["department"])

empty_departments = sorted(all_departments - employee_departments)

print("\nDepartments with no employees:", empty_departments)

# --------------------------------
# 6. CREATE FOUR CHARTS
# --------------------------------

# Bar chart: Headcount by department
plt.figure()
plt.bar(summary["department"], summary["headcount"], label="Employees")
plt.title("Employee Headcount by Department")
plt.xlabel("Department")
plt.ylabel("Headcount")
plt.legend()
plt.tight_layout()
plt.savefig(REPORTS_DIR / "department_headcount.png")
plt.close()

# Histogram: Salary distribution
plt.figure()
plt.hist(cleaned["salary"], bins=5, label="Salary")
plt.title("Employee Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig(REPORTS_DIR / "salary_histogram.png")
plt.close()

# Scatter plot: Employee ID vs Salary
plt.figure()
plt.scatter(cleaned["id"], cleaned["salary"], label="Employees")
plt.title("Employee ID vs Salary")
plt.xlabel("Employee ID")
plt.ylabel("Salary")
plt.legend()
plt.tight_layout()
plt.savefig(REPORTS_DIR / "id_vs_salary_scatter.png")
plt.close()

# Line chart: Average salary by department
plt.figure()
plt.plot(
    summary["department"],
    summary["average_salary"],
    marker="o",
    label="Average Salary"
)
plt.title("Average Salary by Department")
plt.xlabel("Department")
plt.ylabel("Average Salary")
plt.legend()
plt.tight_layout()
plt.savefig(REPORTS_DIR / "average_salary_by_department.png")
plt.close()

print("\nChart Insights:")
print("1. IT has the highest headcount with 3 employees.")
print("2. Salaries range from 30000 to 75000 after cleaning.")
print("3. Employee ID 4 has the highest salary of 75000.")
print("4. IT has the highest average salary among departments.")