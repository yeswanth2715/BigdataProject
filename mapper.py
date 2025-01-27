#!/usr/bin/env python
import sys
import csv

for line in sys.stdin:
    try:
        reader = csv.reader([line])
        for row in reader:
            salary = row[2]  # Assuming column 2 contains the salary
            if salary:
                print(f"{salary}")
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line} - {str(e)}\n")
        continue


