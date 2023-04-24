import tkinter as tk
import sys
import pprint

sys.path.append("../Boolean")

from booleanMathematica import solveGUI

pp = pprint.PrettyPrinter(indent=1)

# Define the function to be called when the user clicks "Submit"
def solve(matrix):
    # Do something with the matrix (for example, print it)
    for row in matrix:
        print(row)

# Define the function to be called when the user clicks "Submit"
def submit():
    # Get the values from the Entry widgets and store them in a 2D array
    matrix = []
    for i in range(4):
        row = []
        for j in range(4):
            val = matrix_entries[i][j].get()
            if val == "":
                row.append("0")
            else:
                row.append(val)
        matrix.append(row)

    pp.pprint(matrix)
    # Call the solve function with the matrix as an argument
    sol = solveGUI(matrix)
    pp.pprint(sol)

    for i in range(4):
        for j in range(4):
            matrix_entries[i][j].delete(0, tk.END)
            matrix_entries[i][j].insert(0, sol[i][j])

# Create the main window
root = tk.Tk()
root.title("Matrix Input")

# Create a frame with a thicker margin on the left and right sides
frame = tk.Frame(root, padx=50, pady=10)
frame.pack()

# Create a 4x4 grid of Entry widgets for the user to input the matrix
matrix_entries = []
for i in range(4):
    matrix_row = []
    for j in range(4):
        entry = tk.Entry(frame, width=10, font=("Arial", 14))
        entry.grid(row=i, column=j, padx=5, pady=5, ipady=10, sticky="nsew")
        matrix_row.append(entry)
    matrix_entries.append(matrix_row)

# Configure the grid to center the Entry widgets horizontally
for i in range(4):
    frame.grid_columnconfigure(i, weight=1)

# Create a button to submit the matrix
submit_button = tk.Button(frame, text="Submit", font=("Arial", 16), bg="#4CAF50", fg="white", command=submit)
submit_button.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# Set the size of the window and center it on the screen
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Start the main event loop
root.mainloop()