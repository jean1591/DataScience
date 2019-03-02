import pandas as pd
import numpy as np

# Imports csv file and stores it in df
df = pd.read_csv("datasets/Minimum Wage Data.csv", encoding="latin")
# Converts df to csv using utf-8 encoding
df.to_csv("datasets/minWage.csv", encoding="utf-8")
# Reads new utf-8 encoded csv file
df = pd.read_csv("datasets/minWage.csv")

# Create new dataframe
actMinWage = pd.DataFrame()

# Iterates over name state with group as dataframe of given state
for name, group in df.groupby("State"):
    # Create new dataframe if actMinWage is empty
    if actMinWage.empty:
        actMinWage = group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018": name})
    # Add column for new state to actMinWage if actMinWage not empty
    else:
        actMinWage = actMinWage.join(group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018": name}))

# Summary of values (count, mean, std, min, max, ...)
# print(actMinWage.describe())

# Display correlation between states
# print(actMinWage.corr().head())

# Display all states not containing data
issue_df = df[df["Low.2018"] == 0.0]
# print(issue_df["State"].unique())

# Replace all 0 with NaN value and drop column (axis=1) containing NaN
minWageCorr = actMinWage.replace(0, np.NaN).dropna(axis=1).corr()

