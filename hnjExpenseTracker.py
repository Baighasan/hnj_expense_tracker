import tkinter as tk
import csv

#######################################################
#                      Functions                      #
#######################################################

def categorizeExpenses():
    '''
        Calls all the functions that opens the csv file and catagorizes the expenses
    '''
    pass


def openFile():
    '''
        Checks if the file exists and returns it if it does
    '''
    pass


def readFile():
    '''
        Reads through the csv file of transactions and calls another function to sort it
    '''
    pass


def sortTransaction():
    '''
        Reads the transaction and categorizes based on a set of rules
    '''
    pass


def generateCSVfile():
    '''
        Generates the csv file and appends the data to it
    '''
    pass


def generateGraph():
    '''
        Creates a pie chart that visualizes the distribution of expenses
    '''
    pass

#######################################################
#               Graphic User Interface                #
#######################################################

def displayGUI():
    '''
        Displays the home frame, and switches the frame based on button pressed and if validation is passed
    '''
    # GUI
    win = tk.Tk()
    win.title("HNJ Expense Tracker")
    win.state("zoomed")

    win.rowconfigure(0, weight=1)
    win.columnconfigure(0, weight=1)

    win.mainloop()