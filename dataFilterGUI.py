# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 08:43:31 2025

@author: rism0
"""

import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Function to load hunt data
def loadHuntDataFrame(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filename}' not found.")
        return pd.DataFrame()

# Function to filter and display results
def displayFilteredHunts():
    species = speciesVar.get()  # Get selected species from dropdown
    weapon = weaponVar.get()
    sort = sortVar.get()

    removePrivateLand = privateVar.get()
    removeYouthOnly = youthVar.get()
    removeMobilityImpaired = mobilityVar.get()
    removeMilitaryOnly = militaryVar.get()

    df = loadHuntDataFrame("huntData.csv")
    
    if df.empty:
        return

    # Ensure required columns exist
    if "huntCode" not in df.columns or "unitDescription" not in df.columns:
        messagebox.showerror("Error", "Missing required columns in DataFrame.")
        return

    # Filter by species
    filteredDf = df[df["huntCode"].str.startswith(species, na=False)]

    # Filter by weapon type (2nd digit of huntCode)
    weaponMap = {1: "1", 2: "2", 3: "3"}
    if weapon in weaponMap:
        filteredDf = filteredDf[filteredDf["huntCode"].str[4] == weaponMap[weapon]]

    # Apply individual filters
    if removePrivateLand:
        filteredDf = filteredDf[~filteredDf["unitDescription"].str.contains(r"private land only", case=False, na=False)]
    if removeYouthOnly:
        filteredDf = filteredDf[~filteredDf["unitDescription"].str.contains(r"youth only", case=False, na=False)]
    if removeMobilityImpaired:
        filteredDf = filteredDf[~filteredDf["unitDescription"].str.contains(r"mobility impaired only", case=False, na=False)]
    if removeMilitaryOnly:
        filteredDf = filteredDf[~filteredDf["unitDescription"].str.contains(r"military only", case=False, na=False)]

    # Sort the data
    sortColumn = "huntOdds" if sort else "huntCode"
    ascending = not sort  # Descending for huntOdds, ascending for huntCode
    filteredDf = filteredDf.sort_values(by=sortColumn, ascending=ascending)

    # Clear previous table data
    for row in tree.get_children():
        tree.delete(row)

    # Insert new data
    for _, row in filteredDf.iterrows():
        tree.insert("", tk.END, values=(row["huntCode"], row["unitDescription"], row["huntOdds"]))

# Create main application window
root = tk.Tk()
root.title("Hunt Data Filter")

# Species selection dropdown
tk.Label(root, text="Select Species:").grid(row=0, column=0, padx=5, pady=5)
speciesVar = tk.StringVar(value="ANT")
speciesMenu = ttk.Combobox(root, textvariable=speciesVar, values=["ANT", "DER", "ELK","IBX","BBY","ORX","JAV","BHS"], state="readonly")
speciesMenu.grid(row=0, column=1, padx=5, pady=5)

# Weapon selection dropdown
tk.Label(root, text="Weapon Type:").grid(row=1, column=0, padx=5, pady=5)
weaponVar = tk.IntVar(value=1)
weaponMenu = ttk.Combobox(root, textvariable=weaponVar, values=[1, 2, 3], state="readonly")
weaponMenu.grid(row=1, column=1, padx=5, pady=5)
weaponMenu.set(1)  # Default to Any Legal

# Checkboxes for different filters
privateVar = tk.BooleanVar(value=True)
privateCheck = tk.Checkbutton(root, text="Remove Private Land Only", variable=privateVar)
privateCheck.grid(row=2, column=0, columnspan=2, padx=5, pady=2)

youthVar = tk.BooleanVar(value=True)
youthCheck = tk.Checkbutton(root, text="Remove Youth Only", variable=youthVar)
youthCheck.grid(row=3, column=0, columnspan=2, padx=5, pady=2)

mobilityVar = tk.BooleanVar(value=True)
mobilityCheck = tk.Checkbutton(root, text="Remove Mobility Impaired Only", variable=mobilityVar)
mobilityCheck.grid(row=4, column=0, columnspan=2, padx=5, pady=2)

militaryVar = tk.BooleanVar(value=True)
militaryCheck = tk.Checkbutton(root, text="Remove Military Only", variable=militaryVar)
militaryCheck.grid(row=5, column=0, columnspan=2, padx=5, pady=2)

# Checkbox for sorting by huntOdds
sortVar = tk.BooleanVar(value=True)
sortCheck = tk.Checkbutton(root, text="Sort by Hunt Odds", variable=sortVar)
sortCheck.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Button to apply filter
filterButton = tk.Button(root, text="Apply Filter", command=displayFilteredHunts)
filterButton.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Treeview Table
columns = ("Hunt Code", "Description", "Hunt Odds")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# Scrollbar for table
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=8, column=2, sticky="ns")

# Run GUI
root.mainloop()
