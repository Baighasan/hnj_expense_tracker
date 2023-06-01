import tkinter as tk
import thefuzz.fuzz as fuzz
import os
import csv
import re

#######################################################
#                      Functions                      #
#######################################################

def categorizeExpenses():
    '''
        Calls all the functions that opens the csv file and catagorizes the expenses
    '''
    # Loads the rules from rules.csv
    rules = loadRules()
    
    # Opens the reader for the transactions
    reader = openFile()
    
    # Reads the file and calls another function to catagorize each transaction
    catagorizedExpenses =  readFile(rules, reader)
    
    print(catagorizedExpenses)


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
    # Creates a dictionary for catagories
    expenseCatagories = {
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
        expenseCatagories = catagorize(rules, transaction, expenseCatagories)
    
    return expenseCatagories


def catagorize(rules, transaction, expenseCatagories):
    '''
        Reads the transaction and categorizes based on a set of rules
        
        @param transaction: the current row in the csv file that we are categorizing
    '''
    
    # Made lowercase so that we can map to rules.csv
    transactionDescriptor = transaction[1].lower()
    # Stores the transaction amount
    transactionAmount = float(transaction[2])
    
    # ?Maybe break into individual functions to help fix the issues?
    # TODO Add functionality so that it adds the transaction to miscellaneous if not able to map
    # Parsing through individual catagories
    for catagory in rules:
        # Parsing through descriptors in the rules.csv
        # !Needs to break out of the for loop after it finds a match within rules (maybe with a while loop? Might have to rethink some parts of this logic)
        for descriptor in rules[catagory]:
            if re.search(descriptor, transactionDescriptor):
                # Parsing through different expense catagories to match it to one and increase the money
                for i in expenseCatagories:
                    # Finds the catagory to increase the amount
                    if catagory == i:
                        expenseCatagories[i] += transactionAmount
                        break
                break
    
    return expenseCatagories


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