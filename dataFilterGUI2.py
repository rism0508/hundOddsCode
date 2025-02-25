# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 16:07:21 2025

@author: rism0
"""

import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QCheckBox, QHeaderView, QMessageBox
)

# Function to load hunt data
def loadHuntDataFrame(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        QMessageBox.critical(None, "Error", f"File '{filename}' not found.")
        return pd.DataFrame()

class HuntFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hunt Data Filter")
        self.setGeometry(100, 100, 800, 500)  # Window size

        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        # Dropdown for species selection
        speciesLayout = QHBoxLayout()
        speciesLayout.addWidget(QLabel("Select Species:"))
        self.speciesCombo = QComboBox()
        self.speciesCombo.addItems(["ANT", "DER", "ELK", "IBX", "BBY", "ORX", "JAV", "BHS"])
        speciesLayout.addWidget(self.speciesCombo)
        mainLayout.addLayout(speciesLayout)

        # Dropdown for weapon type
        weaponLayout = QHBoxLayout()
        weaponLayout.addWidget(QLabel("Weapon Type:"))
        self.weaponCombo = QComboBox()
        self.weaponCombo.addItems(["Any Legal", "Bow", "Muzzle Loader"])
        self.weaponCombo.setCurrentIndex(0)
        weaponLayout.addWidget(self.weaponCombo)
        mainLayout.addLayout(weaponLayout)

        # Checkboxes for filters
        self.privateCheck = QCheckBox("Remove Private Land Only")
        self.youthCheck = QCheckBox("Remove Youth Only")
        self.mobilityCheck = QCheckBox("Remove Mobility Impaired Only")
        self.militaryCheck = QCheckBox("Remove Military Only")
        self.sortCheck = QCheckBox("Sort by Hunt Odds (Highest First)")
        self.sortCheck.setChecked(True)

        mainLayout.addWidget(self.privateCheck)
        mainLayout.addWidget(self.youthCheck)
        mainLayout.addWidget(self.mobilityCheck)
        mainLayout.addWidget(self.militaryCheck)
        mainLayout.addWidget(self.sortCheck)

        # Apply filter button
        self.filterButton = QPushButton("Apply Filter")
        self.filterButton.clicked.connect(self.displayFilteredHunts)
        mainLayout.addWidget(self.filterButton)

        # Table for displaying results
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Hunt Code", "Description", "Hunt Odds %"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        mainLayout.addWidget(self.tableWidget)

        # Set main widget
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

    def displayFilteredHunts(self):
        species = self.speciesCombo.currentText()
        weaponIndex = self.weaponCombo.currentIndex() + 1  # Mapping: 1 -> Any Legal, 2 -> Bow, 3 -> Muzzle
        removePrivateLand = self.privateCheck.isChecked()
        removeYouthOnly = self.youthCheck.isChecked()
        removeMobilityImpaired = self.mobilityCheck.isChecked()
        removeMilitaryOnly = self.militaryCheck.isChecked()
        sort = self.sortCheck.isChecked()

        df = loadHuntDataFrame("huntData.csv")

        if df.empty:
            return

        # Ensure required columns exist
        if "huntCode" not in df.columns or "unitDescription" not in df.columns:
            QMessageBox.critical(self, "Error", "Missing required columns in DataFrame.")
            return

        # Filter by species
        filteredDf = df[df["huntCode"].str.startswith(species, na=False)]

        # Filter by weapon type (2nd digit of huntCode)
        weaponMap = {1: "1", 2: "2", 3: "3"}
        filteredDf = filteredDf[filteredDf["huntCode"].str[4] == weaponMap[weaponIndex]]

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

        # Update Table
        self.tableWidget.setRowCount(len(filteredDf))

        for rowIdx, (_, row) in enumerate(filteredDf.iterrows()):
            self.tableWidget.setItem(rowIdx, 0, QTableWidgetItem(str(row["huntCode"])))
            self.tableWidget.setItem(rowIdx, 1, QTableWidgetItem(str(row["unitDescription"])))
            self.tableWidget.setItem(rowIdx, 2, QTableWidgetItem(str(row.get("huntOdds", "N/A"))))

# Run the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HuntFilterApp()
    window.show()
    sys.exit(app.exec_())
