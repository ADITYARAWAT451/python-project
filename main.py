import tkinter as tk
from gui import ExpenseTrackerApp
# __name__ is a special variable 
# This line checks if the script is being run directly (not imported as a module).

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()