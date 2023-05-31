import tkinter as tk
import os
import csv

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


def loadRules():
    '''
        Loads the rules from rules.csv into a dictionary for usage
    '''
    rulesFile = "rules.csv"
    if (os.path.exists(rulesFile) == False):
        print("Path does not exist")
        return False
    
    rules = {}
    with open("rules.csv", "r") as file:
        rulesReader = csv.reader(file)
        
        # Row of keywords
        for row in rulesReader:
            rules[row[0]] = []
            
            # Parsing through the row of keywords
            for i in range(1, len(row)):
                rules[row[0]].append(row[i])

    return rules 


def openFile():
    '''
        Checks if the file exists and returns it if it does
    '''
    validInput = False
    while validInput != True:
        fileInput = input("Name of file without .csv at the end\n") 
        fileName = fileInput + ".csv"
        if os.path.exists(fileName):
            validInput = True
            print("File exists")
        else:
            validInput = False
            print("File does not exists")
    with open(fileName, "r") as file:
        fileReader = csv.reader(file)
    return fileReader

def readFile(rules, reader):
    '''
        Reads through the csv file of transactions and calls another function to sort it
        
        @param reader: csv file reader used to parse through the transactions
    '''
    pass


def sortTransaction(transaction):
    '''
        Reads the transaction and categorizes based on a set of rules
        
        @param transaction: the current row in the csv file that we are categorizing
    '''
    pass


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