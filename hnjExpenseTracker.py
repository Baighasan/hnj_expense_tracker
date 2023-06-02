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


def openFile():
    '''
        Checks if the file exists and returns it if it does exist
    '''
    fileInput = input("Name of file without .csv at the end: ")
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
                    "Medical": 0,
                    "Entertainment": 0,
                    "Miscellaneous": 0
                }
    
    for transaction in transactionReader[1]:
        expenseCategories = categorize(rules, transaction, expenseCategories)
    
    return expenseCategories


def categorize(rules, transaction, expenseCategories):
    '''
        Reads the transaction and categorizes based on a set of rules
        
        @param transaction: the current row in the csv file that we are categorizing
    '''
    
    # Made lowercase so that we can map to rules.csv
    transactionDescriptor = transaction[1].lower()
    # Stores the transaction amount
    transactionAmount = float(transaction[2])
    
    # ?Maybe break into individual functions to help fix the issues?
    # Parsing through individual categories
    for category in rules:
        # Parsing through descriptors in the rules.csv
        for  descriptor in rules[category]:
            if re.search(descriptor, transactionDescriptor):
                # Parsing through different expense categories to match it to one and increase the money
                for i in expenseCategories:
                    # Finds the category to increase the amount
                    if category == i:
                        expenseCategories[i] += transactionAmount
                        return expenseCategories
                
        
    expenseCategories["Miscellaneous"] += transactionAmount
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


def displayGUI():
    '''
        Displays the home frame, and switches the frame based on button pressed and if validation is passed
    '''
    '''
    # GUI
    win = tk.Tk()
    win.title("HNJ Expense Tracker")
    win.state("zoomed")

    win.rowconfigure(0, weight=1)
    win.columnconfigure(0, weight=1)

    win.mainloop()
'''

# Main Program
categorizeExpenses()