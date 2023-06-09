# hnj_expense_tracker

This program categorizes a list of transactions into categories. Credit card companies have the functionality to export your transaction data in a csv file,
which this program takes. It then uses a matching algorithm to categorize each expense into its own category. A GUI is generated using Tkinter which displays
all the results in a visual format, including a pie chart and table. All the data is exported to a csv file


# Packages Used

- thefuzz
              > These are used to optimize the matching algorithm. If the user does not have these installed, the script will automatically install it with pip
- fuzzysearch
- subprocess
- sys
- tkinter
- csv
- matplotlib
