import tkinter as tk
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
    readFile(rules, reader)


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
    for transaction in transactionReader[1]:
        catagorize(rules, transaction)


def catagorize(rules, transaction):
    '''
        Reads the transaction and categorizes based on a set of rules
        
        @param transaction: the current row in the csv file that we are categorizing
    '''
    print(transaction)


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

    label = tk.Label(win, text = "Welcome to HNJ Expense Tracker!", font = ('Arial', 18))
    label.pack(padx= 20, pady = 20)

    buttonframe = tk.Frame(win)
    buttonframe.columnconfigure(0, weight=1)
    buttonframe.columnconfigure(1, weight=1)
    buttonframe.columnconfigure(2, weight=1)
    
    btn1 = tk.Button(buttonframe, text = "Export Statistics/Pie Graph", font= ('Arial', 18))
    btn1.grid(row = 0, column = 0 , sticky= tk.W+tk.E)

    btn2 = tk.Button(buttonframe, text = "Load Transcations from CSV File", font= ('Arial', 18))
    btn2.grid(row = 0, column = 1 , sticky= tk.W+tk.E)

    buttonframe.pack(fill = 'x')
    win.rowconfigure(0, weight=1)

    win.mainloop()
'''

# Main Program
categorizeExpenses()