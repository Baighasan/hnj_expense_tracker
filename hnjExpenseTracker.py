import tkinter as tk
import thefuzz as fuzz
import os
import csv
import re

#######################################################
#                      Functions                      #
#######################################################

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
    
    print(categorizedExpenses)


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


def openFile(fileInput):
    '''
        Checks if the file exists and returns it if it does exist
    '''
    fileName = fileInput + ".csv"
    if (os.path.exists(fileName) == False):
        print("Path does not exist")
        return False
    
    # opens file and sets reader to a variable that is returned
    file =  open(fileName, "r")
    fileReader = csv.reader(file)
    return file, fileReader


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
                    "Investements": 0,
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
    
    # ?Maybe break into individual functions
    # Parsing through the keys of the dictionary with the category expense amounts
    for category in rules:
        # Parsing through the keywords in the current category above
        for  descriptor in rules[category]:
            if re.search(descriptor, transactionDescriptor):
                # Parsing through different expense categories to match it to one and increase the money
                for i in expenseCategories:
                    # Finds the category to increase the amount
                    if category == i:
                        expenseCategories[i] += transactionAmount
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


def generateGraph(categorizedExpenses):
    '''
        Creates a pie chart that visualizes the distribution of expenses
        
        @param categorizedExpenses: A list/dictionary (not decided yet) that has all the sorted expense data
    '''
    pass


#######################################################
#               Graphic User Interface                #
#######################################################

def validate_file():
    fileName = entry.get()
    if openFile(fileName):
        show_load_screen()
    else:
        label = tk.Label(home_frame, text="Invalid file, cannot load", font=('Arial', 18))
        label.pack(padx=20, pady=20)
        home_frame.after(1000, label.pack_forget)

def show_statistics_screen():
    home_frame.pack_forget()
    statistics_frame.pack()

def show_load_screen():
    home_frame.pack_forget()
    load_frame.pack()

def back_to_home_screen():
    statistics_frame.pack_forget()
    load_frame.pack_forget()
    home_frame.pack()

win = tk.Tk()
win.title("HNJ Expense Tracker")

home_frame = tk.Frame(win)
home_frame.pack(fill='both', expand=True)

label = tk.Label(home_frame, text="Welcome to the HNJ Expense Tracker!", font=('Arial', 18))
label.pack(padx=20, pady=20)

file_label = tk.Label(home_frame, text="Enter transaction file name", font=('Arial', 18))
file_label.pack(padx=20, pady=(0, 10))

entry = tk.Entry(home_frame, font=('Arial', 16))
entry.pack(padx=20, pady=(0, 10))

buttonframe = tk.Frame(home_frame)
buttonframe.pack(pady=(10, 0))

btn2 = tk.Button(buttonframe, text="Load Transaction File", font=('Arial', 24), command=validate_file)
btn2.pack(fill='x')

statistics_frame = tk.Frame(win)
label = tk.Label(statistics_frame, text="Statistics Screen", font=('Arial', 18))
label.pack(padx=20, pady=20)

back_btn = tk.Button(statistics_frame, text="Back", font=('Arial', 18), command=back_to_home_screen)
back_btn.pack(pady=20)

load_frame = tk.Frame(win)
label = tk.Label(load_frame, text="Loaded successfully!", font=('Arial', 18))
label.pack(padx=20, pady=20)

back_btn = tk.Button(load_frame, text="Back", font=('Arial', 18), command=back_to_home_screen)
back_btn.pack(pady=20)

# Configure weights to make the frames expand with the window
win.rowconfigure(0, weight=1)
win.columnconfigure(0, weight=1)

win.mainloop()
