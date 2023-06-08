import tkinter as tk
import thefuzz.fuzz as fuzz
from fuzzysearch import find_near_matches
from tkinter import filedialog
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# #######################################################
# #                      Functions                      #
# #######################################################

def categorizeExpenses():
    '''
        Calls all the functions that opens the csv file and categorizes the expenses
    '''
    # Loads the rules from rules.csv
    rules = loadRules()
    
    # Opens the reader for the transactions
    reader = openFile()
    
    # Reads the file and calls another function to categorize each transaction
    categorizedExpenses = readFile(rules, reader)
    
    return categorizedExpenses



def loadRules():
    '''
        Loads the rules from rules.csv into a dictionary for usage
    '''
    rulesFile = "rules.csv"
    if (os.path.exists(rulesFile) == False):
        print("Path does not exist")
        return False
    
    rules = {}
    file = open("rules.csv", "r")
    rulesReader = csv.reader(file)
    
    # Row of keywords
    for row in rulesReader:
        rules[row[0]] = []
        
        # Parsing through the row of keywords
        for i in range(1, len(row)):
            rules[row[0]].append(row[i])

    file.close()
    return rules 

def openFile():
    '''
        Uses dialog box to get the file
    '''
    filePath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filePath:
        if not filePath.endswith('.csv'):
            label = tk.Label(home_frame, text="Invalid file format. Please select a CSV file.", font=('Arial', 18), fg="red")
            label.pack(padx=20, pady=20)
            home_frame.after(1500, label.pack_forget)
            return None
        show_load_screen()
    file = open(filePath, "r")
    reader = csv.reader(file)
    return file, reader


def readFile(rules, transactionReader):
    '''
        Reads through the csv file of transactions and calls another function to sort it
        
        @param reader: csv file reader used to parse through the transactions
        @param transactionReader: Index 0 is the file reader, Index 1 is the csv file reader
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
                    "gains": 0
                }
    
    for transaction in transactionReader[1]:
        # If index 2 of the transaction is blank, and the dollar amount is in index 3, that means that money was gained, then the loop is rerun and a new transaction is analyzed
        if transaction[2] == "":
            expenseCategories = calculateGains(transaction, expenseCategories)
            continue
        # Otherwise, it will run the catagorizing algorithm and match the descriptor
        expenseCategories = categorize(rules, transaction, expenseCategories)
    
    return expenseCategories


def categorize(rules, transaction, expenseCategories):
    '''
        Reads through the transaction csv file and uses a catagorizing algorithm that takes one transaction, and attempts to match a keyword substring to the transaction
        descriptor substring
        
        @param rules: a dictionary that holds the rules/mapping keywords that was loaded from rules.csv
        @param transaction: the current row in the csv file that we are categorizing
        @param expenseCategories: a dictionary with the key being the categories, and the value being the amount spent in that expense category
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
        @param expenseCategories: 
    '''
    gain = float(transaction[3])
    expenseCategories["gains"] += gain
    return expenseCategories


def generateCSVfile(categorizedExpenses):
    '''
        Generates the csv file and appends the data to it
        
        @param categorizedExpenses: A list/dictionary (not decided yet) that has all the sorted expense data
    '''
    pass


def generateGraph(expenseCategories):
    '''
        Creates a pie chart that visualizes the distribution of expenses
        
        @param categorizedExpenses: A list/dictionary (not decided yet) that has all the sorted expense data
    '''

    totalSpending = sum(expenseCategories.values())

    # Calculate percentage for each category
    percentages = {category: (amount / totalSpending) * 100 for category, amount in expenseCategories.items() if amount != 0}

    
    # Create lists for labels and values
    categories = list(percentages.keys())
    values = list(percentages.values())

    # Define custom colors for the pie slices
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#ffb3b3', '#c2d6d6', '#b3ffcc']

    # Create a pie chart with customizations
    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})
    ax.set_title('Expense Distribution')

    # Add a legend
    ax.legend(title="Categories", loc="center left", bbox_to_anchor=(1, 0.5))

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
    win.geometry(f"{screen_width}x{screen_height}")

def show_load_screen():
    home_frame.pack_forget()
    load_frame.pack()

def back_to_home_screen():
    load_frame.pack_forget()
    home_frame.pack()

def display_graph_and_save():
    categorizedExpenses = categorizeExpenses()
    generateGraph(categorizedExpenses)

win = tk.Tk()
win.title("HNJ Expense Tracker")

set_window_size()

home_frame = tk.Frame(win)
home_frame.pack(fill='both', expand=True)

label = tk.Label(home_frame, text="Welcome to the HNJ Expense Tracker!", font=('Arial', 18))
label.pack(padx=20, pady=20)

buttonframe = tk.Frame(home_frame)
buttonframe.pack(pady=(10, 0))

loadButton = tk.Button(buttonframe, text="Load Transaction File", font=('Arial', 24), command=display_graph_and_save)
loadButton.pack(fill='x')

load_frame = tk.Frame(win)
label = tk.Label(load_frame, text="Loaded successfully!", font=('Arial', 18)) 
label.pack(padx=20, pady=20)

back_btn = tk.Button(load_frame, text="Back", font=('Arial', 18), command=back_to_home_screen)
back_btn.pack(pady=20)

# Configure weights to make the frames expand with the window
win.rowconfigure(0, weight=1)
win.columnconfigure(0, weight=1)

win.mainloop()
