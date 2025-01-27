#!/usr/bin/env python
import sys

highest_salary = float('-inf')
lowest_salary = float('inf')

for line in sys.stdin:
    try:
        salary = float(line.strip())
        highest_salary = max(highest_salary, salary)
        lowest_salary = min(lowest_salary, salary)
    except ValueError:
        sys.stderr.write(f"Skipping invalid salary: {line}\n")
        continue

print(f"Highest Salary: {highest_salary}")
print(f"Lowest Salary: {lowest_salary}")
