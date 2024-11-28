import pandas as pd
df = pd.read_csv("../Data Files/reliability_age_data.csv")

correlation = df[['Reliability','Age']].corr()
print(correlation)