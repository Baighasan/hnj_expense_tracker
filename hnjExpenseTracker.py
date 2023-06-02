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


def readFile(reader):
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

import tkinter as tk

import tkinter as tk

def create_home_screen():
    def show_statistics_screen():
        clear_window()
        label = tk.Label(win, text="Statistics Screen", font=('Arial', 18))
        label.pack(padx=20, pady=20)

        back_btn = tk.Button(win, text="Back", font=('Arial', 18), command=create_home_screen)
        back_btn.pack(pady=20)

    def show_load_screen():
        clear_window()
        label = tk.Label(win, text="Loaded successfully!", font=('Arial', 18))
        label.pack(padx=20, pady=20)

        back_btn = tk.Button(win, text="Back", font=('Arial', 18), command=create_home_screen)
        back_btn.pack(pady=20)

    def clear_window():
        for widget in win.winfo_children():
            widget.destroy()

    win = tk.Tk()
    win.title("Home Screen")
    win.state("zoomed")

    label = tk.Label(win, text="Welcome to the Home Screen!", font=('Arial', 18))
    label.pack(padx=20, pady=20)

    file_label = tk.Label(win, text="Enter transaction file name", font=('Arial', 14))
    file_label.pack()

    entry = tk.Entry(win, font=('Arial', 12))
    entry.pack()

    buttonframe = tk.Frame(win)
    buttonframe.columnconfigure(0, weight=1)
    buttonframe.columnconfigure(1, weight=1)

    btn1 = tk.Button(buttonframe, text="Statistics", font=('Arial', 18), command=show_statistics_screen)
    btn1.grid(row=0, column=0, sticky=tk.W + tk.E)

    btn2 = tk.Button(buttonframe, text="Load", font=('Arial', 18), command=show_load_screen)
    btn2.grid(row=0, column=1, sticky=tk.W + tk.E)

    buttonframe.pack(fill='x')
    win.rowconfigure(0, weight=1)

    win.mainloop()

# Main Program
if __name__ == '__main__':
    create_home_screen()