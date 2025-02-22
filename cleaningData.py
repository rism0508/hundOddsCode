# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 18:09:02 2025

@author: chad.smith

"""
import pandas as pd


df = pd.read_excel('2024OddsSummary.xlsx')
 # Step 1: Set the correct column headers (row 5 in your screenshot)
df.columns = df.iloc[5]  # Use row 5 (index 4) as column names
df = df[6:].reset_index(drop=True)  # Drop previous header rows

df = df.rename(columns={
    "Hunt Code": "huntCode",
    "Unit/Description": "unitDescription",
    "Bag": "bag",
    "Licenses": "nLicenses"     
    })

df.columns.values[8] = "r1st"
df.columns.values[9] = "r2nd"
df.columns.values[10] = "r3rd"
df.columns.values[11] = "rTot"

df = df.iloc[:,:12]
df = df.dropna(subset=["huntCode"])
df = df.dropna(subset = ["unitDescription"])

df["huntCode"] = df["huntCode"].str.strip()  # Remove leading/trailing spaces
df = df[~df["huntCode"].str.contains("Hunt Code", na=False)]
'''
df = df[~df["huntCode"].str.contains("BIGHORN SHEEP", na=False)]
df = df[~df["huntCode"].str.contains("DEER", na=False)]
df = df[~df["huntCode"].str.contains("ELK", na=False)]
df = df[~df["huntCode"].str.contains("BARBARY SHEEP", na=False)]
'''
df["rTot"] = df["rTot"].replace(0, 1_000_000)
df["huntOdds"] = (df["nLicenses"] * 0.84) / df["rTot"]*100

#df.to_csv('huntData.csv',index=False)

