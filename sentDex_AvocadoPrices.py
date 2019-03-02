import pandas as pd
import matplotlib.pyplot as plt

# Imports csv file and stores it in df
df = pd.read_csv("datasets/avocado.csv")

# Converts df["Date"] in datetime object
df["Date"] = pd.to_datetime(df["Date"])

# Creates new Dataframe from df
albany_df = df.copy()[df["region"]=="Albany"]

# Set albany_df's index to Date column
# set_index() returns an new Dataframe,
# inplace=True returns it as initial variable
albany_df.set_index("Date", inplace=True)

# Orders the index (Dates)
albany_df.sort_index(inplace=True)

# Add a new calculated column (moving average of 25)
albany_df["price25ma"] = albany_df["AveragePrice"].rolling(25).mean()

# print(albany_df.tail())

"""
plt.plot(albany_df["AveragePrice"].rolling(25).mean())
plt.show()
"""


def plotMA25AllRegions(string):
    # Imports csv file and stores it in df variable
    # df = pd.read_csv("datasets/avocado.csv")
    df = pd.read_csv(string)

    # Drop all non-organic avocado data
    df = df.copy()[df["type"]=="organic"]

    # Converts df["Date"] in datetime object
    df["Date"] = pd.to_datetime(df["Date"])

    df.sort_values(by="Date", ascending=True, inplace=True)

    # Create new dataframe
    grapf_df = pd.DataFrame()

    # Loop through region
    for region in df["region"].unique():
        # Creates a new dataframe containing only current region
        region_df = df.copy()[df["region"] == region]
        # Set the index to Date colun and sort it
        region_df.set_index("Date", inplace=True)
        region_df.sort_index(inplace=True)
        # Add 25 periods moving average to region_df dataframe
        region_df[f"{region}price25ma"] = region_df["AveragePrice"].rolling(25).mean()

        # Create new dataframe if graph_df is empty
        if grapf_df.empty:
            grapf_df = region_df[[f"{region}price25ma"]]
        # Add column for new region's 25ma to graph_df 
        else:
            grapf_df = grapf_df.join(region_df[f"{region}price25ma"])
    
    # Plot 25MA from all regions
    plt.plot(grapf_df.dropna())
    plt.show()







plotMA25AllRegions("datasets/avocado.csv")

#print(df["region"].unique())