# Imports necessary packages
# If packages are not installed, run "$ pip install -r requirements.txt"
import thefuzz.fuzz as fuzz
from fuzzysearch import find_near_matches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import filedialog
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# #######################################################
# #                      Functions                      #
# #######################################################

def categorizeExpenses():
    '''
        Calls all the functions that opens the csv file and categorizes the expenses
        
        @return categorizedExpenses: The dictionary containing the amount spent in each expense category
    '''
    
    # Opens the reader for the transactions
    reader = openFile()
    
    # Loads the rules from rules.csv
    rules = loadRules()
    
    # If the reader or rules returns none, that means the user selected nothing or rules.csv was deleted, which means that we should not continue
    if (reader == None) or (rules == None):
        return None
    
    # Reads the file and calls another function to categorize each transaction
    categorizedExpenses = readFile(rules, reader)
    
    return categorizedExpenses


def openFile():
    '''
        Uses dialog box to get the file
        
        @return None: Returns this if the user does not select anything
        @return file, reader: File is the file reader, reader is the csv reader
    '''
    filePath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filePath:
        if not filePath.endswith('.csv'):
            label = tk.Label(home_frame, text="Invalid file format. Please select a CSV file.", font=('Arial', 18), fg="red")
            label.pack(padx=20, pady=20)
            home_frame.after(1500, label.pack_forget)
            return None
        show_load_screen()
    # Try and except is used to catch error if the user does not input any file in the dialogue box
    try:
        file = open(filePath, "r")
    except FileNotFoundError:
        return None
    
    reader = csv.reader(file)
    return file, reader


def loadRules():
    '''
        Loads the rules from rules.csv into a dictionary for usage
        
        @return rules: A dictionary containing everything in rules.csv, used for the matching algorithm
    '''
    rulesFile = "rules.csv"

    try:
        file = open(rulesFile, "r")
    except FileNotFoundError:
        label = tk.Label(home_frame, text="Rules.csv does not exist. Visit the hnj_expense_tracker github repository to redownload it.", font=('Arial', 18), fg="red")
        label.pack(padx=20, pady=20)
        home_frame.after(1500, label.pack_forget)
        return None
        
    rulesReader = csv.reader(file)
    rules = {}
    
    # Row of keywords
    for row in rulesReader:
        rules[row[0]] = []
        
        # Parsing through the row of keywords
        for i in range(1, len(row)):
            rules[row[0]].append(row[i])

    file.close()
    return rules


def readFile(rules, transactionReader):
    '''
        Reads through the csv file of transactions and calls another function to sort it
        
        @param reader: csv file reader used to parse through the transactions
        @param transactionReader: Index 0 is the file reader, Index 1 is the csv file reader
        
        @return expenseCategories: The dictionary containing every transaction amount sorted into a expense category
    '''
    # Creates a dictionary for categories
    expenseCategories = {
                    "Housing": 0,
                    "Transportation": 0,
                    "Food": 0,
                    "Utilities": 0,
                    "Clothing": 0,
                    "Insurance": 0,
                    "Medical": 0,
                    "Entertainment": 0,
                    "Miscellaneous": 0,
                    "Gains": 0
                }
    
    for transaction in transactionReader[1]:
        # If index 2 of the transaction is blank, and the dollar amount is in index 3, that means that money was gained, then the loop is rerun and a new transaction is analyzed
        if transaction[2] == "":
            expenseCategories = calculateGains(transaction, expenseCategories)
            continue
        # Otherwise, it will run the catagorizing algorithm and match the descriptor
        expenseCategories = categorize(rules, transaction, expenseCategories)
    
    transactionReader[0].close()
    return expenseCategories


def categorize(rules, transaction, expenseCategories):
    '''
        Reads through the transaction csv file and uses a catagorizing algorithm that takes one transaction, and attempts to match a keyword substring to the transaction
        descriptor substring
        
        @param rules: a dictionary that holds the rules/mapping keywords that was loaded from rules.csv
        @param transaction: the current row in the csv file that we are categorizing
        @param expenseCategories: a dictionary with the key being the categories, and the value being the amount spent in that expense category

        @return expenseCategories: Everytime the function runs, it returns the dictionary with the updated numbers after it just sorted the transaction
    '''
    
    # Made lowercase so that we can map to rules.csv
    transactionDescriptor = transaction[1].lower()
    # Stores the transaction amount
    transactionAmount = float(transaction[2])
    bestFuzz = ["category","0"]
    
    # Parsing through the keys of the dictionary with the category expense amounts
    for category in rules:
        # Parsing through the keywords in the current category above
        for descriptor in rules[category]:

            # Uses fuzzy searching to find a potential matching descriptor in the transaction
            match = find_near_matches(descriptor, transactionDescriptor, max_l_dist=1)
            # If the fuzzy searching algorithm fails to find a match, it will return an empty list
            if match != []:
                # Iterates through the objects in the match list
                for object in match:
                    fuzzyratio = fuzz.ratio(descriptor, object.matched)
                    if fuzzyratio >= int(bestFuzz[1]):
                        # Sets the highest scoring category
                        bestFuzz[0] = category
                        # Calculates the highest ratio in a variable
                        highestRatio = fuzzyratio
                        # Assigns that variable to the 1st index of the bestFuzz list
                        bestFuzz[1] = str(highestRatio)
    
    # As long as the highest ratio is above a satisfactory number, it will continue
    if int(bestFuzz[1]) > 80:
        expenseCategories[bestFuzz[0]] += transactionAmount
        return expenseCategories
    
    # If the matching algorithm is not able to find a match, then the expense is set to miscellaneous
    expenseCategories["Miscellaneous"] += transactionAmount
    return expenseCategories


def calculateGains(transaction, expenseCategories):
    '''
        Adds the value in the third index of the transaction to the gains key in the expenseCatagories dictionary
        
        @param transaction: the current transaction we are adding to the dictionary
        @param expenseCategories: the dictionary holding all the categorized expenses
        
        @return expenseCategories: returns the categorized expenses with the correct gains
    '''
    gain = float(transaction[3])
    expenseCategories["Gains"] += gain
    return expenseCategories


def generateCSVfile(categorizedExpenses):
    '''
        Generates the csv file and appends the data to it
        
        @param categorizedExpenses: A list/dictionary (not decided yet) that has all the sorted expense data
    '''
    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Categories", "Spending"])  # Write the header row
        
        for key, value in categorizedExpenses.items():
            value = round(value, 2)
            writer.writerow([key, "$" + str(value)])  # Write each key-value pair as a row with a "$" sign before the value


def generateGraph(categorizedExpenses):
    '''
        Creates a pie chart that visualizes the distribution of expenses
        
        @param categorizedExpenses: A list/dictionary (not decided yet) that has all the sorted expense data
    '''
    # Filter out categories with $0 spent
    categorizedExpenses = {category: amount for category, amount in categorizedExpenses.items() if amount != 0}

    totalSpending = sum(categorizedExpenses.values())

    # Create lists for labels and values
    categories = list(categorizedExpenses.keys())
    values = list(categorizedExpenses.values())

    # Calculate Percentages
    percentages = [(amount / totalSpending) * 100 for amount in values]
    percentages_formatted = [f'{p:.1f}%' for p in percentages]

    # Define custom colors for the pie slices
    colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45']
    # Create a figure and two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Create a pie chart on the left subplot
    wedges, textLabels = ax1.pie(
        values,
        colors=colors,
        startangle=90,
        wedgeprops={'edgecolor': 'black'},
        labels=None,
        textprops={'fontsize': 12}
    )
    ax1.set_title('Expense Distribution')

    # Create a legend on the left subplot
    legend_labels = [f'{category} ({percentage})' for category, percentage in zip(categories, percentages_formatted)]
    ax1.legend(wedges, legend_labels, title='Categories', loc='center left', bbox_to_anchor=(1, 0.5))


    # Create a table on the right subplot
    table_data = [[category, f'${amount:.2f}'] for category, amount in categorizedExpenses.items()]
    table = ax2.table(
        cellText=table_data,
        colLabels=['Category', 'Amount'],
        loc='center',
        cellLoc='center',
        colWidths=[0.4, 0.4],
        cellColours=[['#eaeaea'] * 2] * len(table_data),
        bbox=[0.4, 0, 0.6, 1]  # Adjust the bbox to position the table and increase its width
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)

    # Remove the borders from the table
    for key, cell in table.get_celld().items():
        cell.set_linewidth(0)

    # Remove the scale from the table
    ax2.axis('off')

    # Create a Tkinter canvas to embed the plot
    canvas = FigureCanvasTkAgg(fig, master=load_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create a navigation toolbar for the plot
    toolbar = NavigationToolbar2Tk(canvas, load_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Display the chart and toolbar
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar.pack(side=tk.BOTTOM)


#######################################################
#               Graphic User Interface                #   
#######################################################

def set_window_size():
    # Calculate the desired width and height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    win_width = screen_width // 3
    win_height = screen_height // 3
    win.geometry(f"{win_width}x{win_height}")

def show_load_screen():
    home_frame.pack_forget()
    load_frame.pack()   
    label = tk.Label(load_frame, text="Loaded successfully!", font=('Arial', 24), bg='royal blue', fg='white')
    label.pack(padx=20, pady=10)

    label = tk.Label(load_frame, text="View results in exported csv file (expenses.csv)", font=('Arial', 20), bg='royal blue', fg='white')
    label.pack(padx=20, pady=10)

    buttonframe2.pack()

    # Remove any existing back button
    for widget in buttonframe2.winfo_children():
        widget.destroy()
    
    back_btn = tk.Button(buttonframe2, text="Back", font=('Arial', 18), command=back_to_home_screen, bg='royal blue', fg='black')
    back_btn.pack(side=tk.LEFT)


def back_to_home_screen():
    load_frame.pack_forget()
    buttonframe2.pack_forget()
    home_frame.pack()
    # Remove the graph canvas and toolbar
    for widget in load_frame.winfo_children():
        widget.pack_forget()

def display_graph_and_export_data():
    categorizedExpenses = categorizeExpenses()
    # If none is returned that means that the user cancelled the operation, so we skip the next functions
    if categorizedExpenses != None:
        generateGraph(categorizedExpenses)
        generateCSVfile(categorizedExpenses)

def on_closing():
    win.quit()
    win.destroy()

win = tk.Tk()
win.title("HNJ Expense Tracker")
win.configure(bg='navy blue')

set_window_size()

home_frame = tk.Frame(win, bg='royal blue')
home_frame.pack(fill='both', expand=True)

label = tk.Label(home_frame, text="Welcome to the HNJ Expense Tracker!", font=('Arial', 18), bg='royal blue', fg='white')
label.pack(padx=20, pady=20)

buttonframe = tk.Frame(home_frame, bg='royal blue')
buttonframe.pack(pady=(10, 0))

loadButton = tk.Button(buttonframe, text="Load Transaction File", font=('Arial', 24), command=display_graph_and_export_data, bg='light blue', fg='navy blue')
loadButton.pack(fill='x')

load_frame = tk.Frame(win, bg='royal blue')

buttonframe2 = tk.Frame(load_frame, bg='royal blue')

# Configure weights to make the frames expand with the window
win.rowconfigure(0, weight=1)
win.columnconfigure(0, weight=1)

win.protocol("WM_DELETE_WINDOW", on_closing)

win.mainloop()