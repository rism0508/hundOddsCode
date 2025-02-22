# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:41:10 2025

@author: chad.smith
"""

import pandas as pd




# Function to load the DataFrame
def loadHuntDataFrame(filename="huntData.csv"):
    """
    Loads the hunt DataFrame from a CSV file.
    
    Parameters:
    - filename: Name of the CSV file (default: "hunt_data.csv")
    
    Returns:
    - df: Loaded Pandas DataFrame
    """
    try:
        df = pd.read_csv(filename)
        print(f"DataFrame loaded from {filename}")
        return df
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please save the DataFrame first.")
        return None

# Function to compute the hunt chance
def computeHuntChance(filename="huntData.csv"):
    """
    Loads the hunt data, prompts the user for a hunt code, computes the chance, and outputs the result.
    
    Formula: round(nLicenses * 0.84) / rTot

    Parameters:
    - filename: Name of the CSV file to load data from (default: "hunt_data.csv")

    Returns:
    - Prints the computed value or an error message if the hunt code is not found
    """
    df = loadHuntDataFrame(filename)
    
    if df is None:
        return  # Stop if the DataFrame couldn't be loaded

    # Ask the user to enter a hunt code
    huntCode = input("Enter the Hunt Code (e.g., ANT-1-101): ").strip()

    # Check if hunt code exists in the DataFrame
    if huntCode not in df["huntCode"].values:
        print(f"Hunt Code {huntCode} not found. Please try again.")
        return

    # Select the first matching row (handle duplicates)
    huntRow = df[df["huntCode"] == huntCode].iloc[0]

    # Extract values
    nLicenses = int(huntRow["nLicenses"])
    rTot = int(huntRow["rTot"])

    if rTot == 0:
        print("Error: Cannot divide by zero (rTot value is 0).")
        return

    # Compute chance
    result = round(nLicenses * 0.84) / rTot

    # Output the result
    #print(f"Chance of getting {huntCode}: {result:.2%}")  # Displays as percentage


    return f"Chance of getting {huntCode}: {result:.2%}"  # Format as percentage



def displayFilteredHunts(species, filename="huntData.csv", sort=True, removePrivateYouth=True, weapon=1):
    """
    Filters the DataFrame based on huntCode prefix, weapon type, optionally removes private land and youth-only hunts,
    sorts the results, and prints them.

    Parameters:
        species (str): The prefix to filter the 'huntCode' column.
        filename (str): The CSV file containing hunting data.
        sort (bool): If True, sorts by 'huntOdds' (highest to lowest); otherwise, sorts by 'huntCode'.
        removePrivateYouth (bool): If True, removes private land and youth-only hunts.
        weapon (int): Weapon type filter. 1 = Any Legal, 2 = Bow, 3 = Muzzle Loader.

    Displays:
        A formatted table of filtered and sorted hunt results.
    """
    df = loadHuntDataFrame(filename)
    
    if df.empty:
        print("⚠️ Error: DataFrame is empty or could not be loaded.")
        return

    # Ensure required columns exist
    requiredColumns = ["huntCode", "unitDescription"]
    for col in requiredColumns:
        if col not in df.columns:
            print(f"⚠️ Error: Missing required column '{col}' in DataFrame.")
            return

    # Filter rows where 'huntCode' starts with the given prefix
    filteredDf = df[df["huntCode"].str.startswith(species, na=False)]

    # Apply weapon filter based on the second digit of huntCode
    weaponMap = {1: "1", 2: "2", 3: "3"}
    if weapon in weaponMap:
        filteredDf = filteredDf[filteredDf["huntCode"].str[4] == weaponMap[weapon]]

    # Optionally remove private land and youth-only hunts
    if removePrivateYouth:
        filteredDf = filteredDf[~filteredDf["unitDescription"].str.contains(r"private land only|youth only", case=False, na=False)]

    # Determine sorting column
    sortColumn = "huntOdds" if sort and "huntOdds" in df.columns else "huntCode"
    ascending = not sort  # Descending for huntOdds, ascending for huntCode

    # Ensure sorting column exists
    if sortColumn not in df.columns:
        print(f"⚠️ Error: Column '{sortColumn}' not found in DataFrame.")
        return

    # Sort the filtered DataFrame
    sortedDf = filteredDf.sort_values(by=sortColumn, ascending=ascending)

    # Display results in a clean format
    if sortedDf.empty:
        print(f"ℹ️ No results found for hunt codes starting with '{species}' and weapon type {weapon}.")
    else:
        print("\n🎯 Filtered Hunt Results\n" + "-"*40)
        print(sortedDf.to_string(index=False))  # Prints the table without the index

# Example Usage:
# displayFilteredHunts("ANT")  # Default sorting by huntOdds, removes private/youth hunts, any legal weapon
# displayFilteredHunts("ANT", sort=False)  # Sorts by huntCode instead
# displayFilteredHunts("ANT", removePrivateYouth=False)  # Includes private/youth hunts
# displayFilteredHunts("ANT", weapon=2)  # Filters for Bow hunts
# displayFilteredHunts("ELK", weapon=3)  # Filters for Muzzle Loader hunts


# Example Usage:
# displayFilteredHunts("ANT", df)  # Default sorting by huntOdds, removes private/youth hunts
# displayFilteredHunts("ANT", df, sort=False)  # Sorts by huntCode instead
# displayFilteredHunts("ANT", df, removePrivateYouth=False)  # Includes private/youth hunts



# Example Usage:
displayFilteredHunts("ANT",weapon=2)




