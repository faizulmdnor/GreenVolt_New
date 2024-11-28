import csv
import random

# Generate 200 rows of data
data = [{"Reliability": round(random.uniform(0.7, 1.0), 2), "Age": round(random.uniform(20, 60), 1)} for _ in range(200)]

# Write to CSV file
with open("../Data Files/reliability_age_data.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Reliability", "Age"])
    writer.writeheader()
    writer.writerows(data)

print("../Data Files/reliability_age_data.csv")
