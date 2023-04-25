import tkinter as tk
from tkinter import ttk
import sys
import pprint
import time

sys.path.append("../Boolean")

from booleanMathematica import solveGUI

pp = pprint.PrettyPrinter(indent=1)


class MyApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("500x600")
        self.master.title("Matrix Solver")

        self.tabControl = ttk.Notebook(self.master)

        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text="4x4 Matrix")

        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text="9x9 Matrix")

        self.tabControl.pack(expand=1, fill="both")

        self.grid_4x4()
        self.grid_9x9()

        # Create a label to show the time taken to solve the matrix
        self.time_label = tk.Label(self.master, text="Time taken: ")
        self.time_label.pack(side="bottom")

    def grid_4x4(self):
        for i in range(4):
            self.tab1.columnconfigure(i, weight=1, uniform='c')
            self.tab1.rowconfigure(i, weight=1, uniform='r')
            for j in range(4):
                cell = tk.Entry(self.tab1, width=10, justify='center', font=("Arial", 20))
                cell.grid(row=i, column=j, padx=5, pady=5, ipady=10, sticky="nsew")

        submit_button = tk.Button(self.tab1, text="Submit", command=self.solve_4x4)
        submit_button.grid(row=5, column=1, columnspan=2, pady=10)

    def grid_9x9(self):
        for i in range(9):
            self.tab2.columnconfigure(i, weight=1, uniform='c')
            self.tab2.rowconfigure(i, weight=1, uniform='r')
            for j in range(9):
                cell = tk.Entry(self.tab2, width=6, justify='center')
                cell.grid(row=i, column=j, padx=5, pady=5, ipady=10, sticky="nsew")

        submit_button = tk.Button(self.tab2, text="Submit", command=self.solve_9x9)
        submit_button.grid(row=10, column=4, columnspan=2, pady=10)

    def solve_4x4(self):
        values = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_value = self.tab1.grid_slaves(row=i, column=j)[0].get()
                if cell_value != "":
                    row.append(cell_value)
                else:
                    row.append("0")
            values.append(row)

        print("Solving 4x4 Matrix:")
        pp.pprint(values)
        # Call the solve function with the matrix as an argument
        start_time = time.time()
        sol = solveGUI(values)
        elapsed_time = time.time() - start_time
        pp.pprint(sol)
        for i in range(4):
            for j in range(4):
                self.tab1.grid_slaves(row=i, column=j)[0].delete(0, tk.END)
                self.tab1.grid_slaves(row=i, column=j)[0].insert(0, sol[i][j])
        
        # Update the time label to show the time taken to solve the matrix
        self.time_label.config(text="Time taken: {:.3f} seconds".format(elapsed_time))

    def solve_9x9(self):
        values = []
        for i in range(9):
            row = []
            for j in range(9):
                cell_value = self.tab2.grid_slaves(row=i, column=j)[0].get()
                if cell_value != "":
                    row.append(cell_value)
                else:
                    row.append("0")
            values.append(row)

        print("Solving 9x9 Matrix:")
        pp.pprint(values)
        # Call the solve function with the matrix as an argument
        start_time = time.time()
        sol = solveGUI(values)
        elapsed_time = time.time() - start_time
        pp.pprint(sol)
        for i in range(9):
            for j in range(9):
                self.tab2.grid_slaves(row=i, column=j)[0].delete(0, tk.END)
                self.tab2.grid_slaves(row=i, column=j)[0].insert(0, sol[i][j])


root = tk.Tk()
app = MyApp(root)
app.mainloop()
