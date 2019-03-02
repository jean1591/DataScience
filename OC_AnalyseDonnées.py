#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 22:54:18 2019

@author: jean
"""

import pandas as pd
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 500)
pd.set_option('display.width', 1000)
from collections import Counter
import matplotlib as plt

# Import data from operations.csv, get the date with parse_dates
data = pd.read_csv("operations.csv", parse_dates=[1,2])
# print(data)


def mostCommonWords(labels):
    """
    Find the most common words of a given Dataframe
    """
    words = []
    
    # Retreive line per line
    for lab in labels:
        # Add each word from lab to list
        words +=lab.split(" ")
    
    # Return a dict of words and there occurences
    counter = Counter(words)
    for word in counter.most_common(100):
        print(word)

CATEGS = {
    'LOYER': 'LOYER',
    'FORFAIT COMPTE SUPERBANK': 'COTISATION BANCAIRE',
    'LES ANCIENS ROBINSON': 'COURSES',
    "L'EPICERIE DENBAS": 'COURSES',
    'TELEPHONE': 'FACTURE TELEPHONE',
    'LA CCNCF': 'TRANSPORT',
    'CHEZ LUC': 'RESTAURANT',
    'RAPT': 'TRANSPORT',
    'TOUPTIPRI': 'COURSES',
    'LA LOUVE': 'COURSES',
    'VELOC': 'TRANSPORT'
}

TYPES = {
    'CARTE': 'CARTE',
    'VIR': 'VIREMENT',
    'VIREMENT': 'VIREMENT',
    'RETRAIT': 'RETRAIT',
    'PRLV': 'PRELEVEMENT',
    'DON': 'DON',
}

# Petite depenses < €80 < Moyenne depense < €200 < Grosse depense
EXPENSES = [80,200]
# Solde du compte apres la derniere operation en date
LAST_BALANCE = 2400
WEEKEND = ["Saturday","Sunday"]


# Nettoyage de la Dataframe
for column in data.columns:
    if column not in ["date_operation", "libelle", "debit", "credit", "montant"]:
        del data[column]


def addTwoColumns(col1, col2, col):
    """
    Add two columns together to create a new one
    @param: string, col1: name of the first column to add
    @param: string, col2: name of the second column to add
    @param: string col: name of the new column
    """
    if col not in data.columns:
        data[col1] = data[col1].fillna(0)
        data[col2] = data[col2].fillna(0)
        data[col] = data[col1]+ data[col2]


def addBalanceColumn():
    data.sort_values("date_operation")
    amount = data["montant"]
    balance = amount.cumsum()
    balance = list(balance.values)
    last_val = balance[-1]
    balance = [0] + balance[:-1]
    balance = balance - last_val + LAST_BALANCE
    data["solde_avt_ope"] = balance

def detectWords(values, dictionary):
    result = []
    for lib in values:
        operation_type = "AUTRE"
        for word, val in dictionary.items():
            if word in lib:
                operation_type = val
        result.append(operation_type)
    return result

def expenseSlice(value):
    # Expenses are inferior to 0
    value = -value
    
    if value < 0:
        return "(pas une depense)"
    elif value < EXPENSES[0]:
        return ("petite")
    elif value < EXPENSES[1]:
        return "moyenne"
    else:
        return "grosse"

data["annee"] = data["date_operation"].map(lambda d: d.year)
data["mois"] = data["date_operation"].map(lambda d: d.month)
data["jour"] = data["date_operation"].map(lambda d: d.day)
data["jour_sem"] = data["date_operation"].map(lambda d: d.day_name)
data["jour_sem_num"] = data["date_operation"].map(lambda d: d.weekday()+1)
data["weekend"] = data["jour_sem"].isin(WEEKEND)
data["quart_mois"] = [int((jour-1)*4/31)+1 for jour in data["jour"]]


            
            
# mostCommonWords(data["libelle"].values)
# Create "montant" column
addTwoColumns("debit", "credit", "montant")
# Solde avant operation
addBalanceColumn()
# Create cated and type columns
data["categ"] = detectWords(data["libelle"], CATEGS)
data["type"] = detectWords(data["libelle"], TYPES)
# Create "tranche_depense" column
data["tranche_depense"] = data["montant"].map(expenseSlice)
# Save as CSV
# data.to_csv("operationEnrichies.csv", index=False)


effectifs = data["quart_mois"].value_counts()
modalites = effectifs.index

tab = pd.DataFrame(modalites, columns = ["quart_mois"])
tab["n"] = effectifs.values
tab["f"] = tab["n"] / len(data)
tab = tab.sort_values("quart_mois")
tab["F"] = tab["f"].cumsum()

print(tab)




# GRAPHS
# data["montant"].hist(normed=True)
# plt.show



# PRINTS
# print(data)
# mostCommonWords(data["type"])



