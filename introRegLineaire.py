#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 23:09:05 2018

@author: jean

Plot linear regression based on price per rented area
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Fetch data from house.csv
house_data_raw = pd.read_csv("house.csv")
# Exclude abherant entries: rent over 7000
house_data = house_data_raw[house_data_raw["loyer"] < 7000]

x = np.matrix([np.ones(house_data.shape[0]), house_data["surface"]]).T
y = np.matrix(house_data["loyer"]).T
theta = np.linalg.inv(x.T.dot(x)).dot(x.T).dot(y)

# Plot rents per surface as red dots
plt.plot([0, 250], [theta.item(0), theta.item(0) + 250 * theta.item(1)])
plt.plot(house_data["surface"], house_data["loyer"], "ro", markersize=4)
plt.show()
