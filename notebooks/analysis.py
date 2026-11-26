#!/usr/bin/env python
# coding: utf-8

# # Week 1 Assessment – Data Analysis
# 
# ## Objective
# Analyze employee data using Python, NumPy, Pandas and Matplotlib.

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path.cwd().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

print("Project folder:", BASE_DIR)
print("Data folder:", DATA_DIR)
print("Libraries imported successfully")


# ## 1. NumPy Analysis

# In[2]:


marks = np.array([
    [80, 75, 90],
    [70, 85, 80],
    [90, 95, 85],
    [60, 70, 75]
])

print("Student averages:", marks.mean(axis=1))
print("Subject averages:", marks.mean(axis=0))

updated_marks = marks + 5
print("Updated marks:\n", updated_marks)

weights = np.array([0.3, 0.3, 0.4])
weighted_scores = np.dot(marks, weights)

print("Weighted scores:", weighted_scores)

get_ipython().run_line_magic('timeit', 'marks.mean(axis=1)')


# ## 2. Pandas Employee Analysis

# In[3]:


employees = pd.read_csv(DATA_DIR / "employees.csv")

print("Data Information:")
employees.info()

print("\nData Description:")
display(employees.describe())

print("\nEmployees earning above 50000:")
display(employees.loc[employees["salary"] > 50000])

print("\nFirst three employees:")
display(employees.iloc[:3])


# ## 3. Department Analysis

# In[4]:


departments = pd.read_csv(DATA_DIR / "departments.csv")

summary = employees.groupby("department").agg(
    headcount=("id", "count"),
    average_salary=("salary", "mean"),
    maximum_salary=("salary", "max")
).reset_index()

print("Department Summary:")
display(summary)

print("\nOuter Merge:")
outer_merge = pd.merge(
    employees,
    departments,
    on="department",
    how="outer"
)
display(outer_merge)

print("\nDepartments without employees:")
empty_departments = departments[
    ~departments["department"].isin(employees["department"])
]
display(empty_departments)


# ## 4. Findings and Conclusion
# 
# 1. IT has the highest employee headcount with 3 employees.
# 2. Finance has the highest maximum salary of 90000.
# 3. IT has the highest average salary of 67666.67.
# 4. Marketing department has no employees.
# 5. NumPy and Pandas help perform numerical and employee data analysis.
