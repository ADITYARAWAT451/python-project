import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models import Expense
from file_operations import read_expenses_from_file, clear_all_expenses, add_expense_to_file
from utils.validators import validate_date, validate_amount
from utils.styles import BG_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, HEADER_FONT, LABEL_FONT, BUTTON_FONT, configure_styles

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)
        
        # Configure styles
        configure_styles()
        
        # Create UI components
        self.create_header()
        self.create_input_panel()
        self.create_buttons_panel()
        self.create_table_panel()
        
        # Load initial data
        self.refresh_table()
    
    def create_header(self):
        header_frame = tk.Frame(self.root, bg=PRIMARY_COLOR, pady=10)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, 
                text="EXPENSE TRACKER", 
                font=HEADER_FONT, 
                bg=PRIMARY_COLOR, 
                fg="white").pack()
    
    def create_input_panel(self):
        input_frame = tk.Frame(self.root, bg=BG_COLOR, padx=10, pady=10)
        input_frame.pack(fill=tk.X)
        
        # Date
        tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg=BG_COLOR, 
                font=LABEL_FONT).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_entry = tk.Entry(input_frame, font=LABEL_FONT, width=15)
        self.date_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Category
        tk.Label(input_frame, text="Category:", bg=BG_COLOR, 
                font=LABEL_FONT).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.categories = ["Food", "Transport", "Housing", "Entertainment", 
                          "Utilities", "Healthcare", "Education", "Other"]
        self.category_combobox = ttk.Combobox(input_frame, values=self.categories, 
                                            font=LABEL_FONT, width=15)
        self.category_combobox.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Amount
        tk.Label(input_frame, text="Amount:", bg=BG_COLOR, 
                font=LABEL_FONT).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.amount_entry = tk.Entry(input_frame, font=LABEL_FONT, width=15)
        self.amount_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Description
        tk.Label(input_frame, text="Description:", bg=BG_COLOR, 
                font=LABEL_FONT).grid(row=3, column=0, sticky=tk.NW, pady=5)
        self.desc_entry = tk.Text(input_frame, font=LABEL_FONT, width=30, height=3)
        self.desc_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
    
    def create_buttons_panel(self):
        button_frame = tk.Frame(self.root, bg=BG_COLOR, pady=10)
        button_frame.pack(fill=tk.X)
        
        self.add_btn = ttk.Button(button_frame, text="Add Expense", command=self.add_expense)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = ttk.Button(button_frame, text="Refresh", command=self.refresh_table)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Clear Fields", command=self.clear_inputs)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_all_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        self.clear_all_btn.pack(side=tk.LEFT, padx=5)
    
    def create_table_panel(self):
        tree_frame = tk.Frame(self.root, bg=BG_COLOR)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Treeview scrollbars
        self.tree_scroll_y = tk.Scrollbar(tree_frame)
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Date", "Category", "Amount", "Description"),
            show='headings',
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set,
            selectmode="browse"
        )
        
        # Configure headings
        self.tree.heading("Date", text="Date", anchor=tk.W)
        self.tree.heading("Category", text="Category", anchor=tk.W)
        self.tree.heading("Amount", text="Amount", anchor=tk.W)
        self.tree.heading("Description", text="Description", anchor=tk.W)
        
        # Configure columns
        self.tree.column("Date", width=100, minwidth=80, anchor=tk.W)
        self.tree.column("Category", width=100, minwidth=80, anchor=tk.W)
        self.tree.column("Amount", width=100, minwidth=80, anchor=tk.W)
        self.tree.column("Description", width=300, minwidth=150, anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        
        # Configure tags for alternating row colors
        self.tree.tag_configure('odd', background='#f9f9f9')
        self.tree.tag_configure('even', background='#ffffff')
        self.tree.tag_configure('total', background=PRIMARY_COLOR, 
                              foreground='white', font=('Helvetica', 10, 'bold'))
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_table_select)
    
    def get_inputs(self):
        """Return all input values as a dictionary"""
        return {
            "date": self.date_entry.get().strip(),
            "category": self.category_combobox.get().strip(),
            "amount": self.amount_entry.get().strip(),
            "description": self.desc_entry.get("1.0", tk.END).strip()
        }
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.category_combobox.set('')
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete("1.0", tk.END)
    
    def refresh_table(self):
        """Refresh the table with current data"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        expenses = read_expenses_from_file()
        if not expenses:
            return
        
        total = 0
        for index, exp in enumerate(expenses):
            total += exp.amount
            tag = 'odd' if index % 2 == 0 else 'even'
            self.tree.insert("", tk.END, values=exp.to_list(), tags=(tag,))
        
        # Add total row
        self.tree.insert("", tk.END, values=["", "TOTAL", f"₹{total:.2f}", ""], 
                       tags=('total',))
    
    def on_table_select(self, event):
        """Handle table selection event"""
        selected = self.tree.focus()
        if selected:  # Prevent error when clicking on empty space
            values = self.tree.item(selected, 'values')
            if values and values[1] != "TOTAL":  # Don't fill from total row
                self.clear_inputs()
                self.date_entry.insert(0, values[0])
                self.category_combobox.set(values[1])
                self.amount_entry.insert(0, values[2].replace('$', ''))
                self.desc_entry.insert("1.0", values[3])
    
    def add_expense(self):
        """Add a new expense"""
        inputs = self.get_inputs()
        
        try:
            # Validate inputs
            if not all(inputs.values()):
                raise ValueError("All fields are required!")
            
            if not validate_date(inputs["date"]):
                raise ValueError("Invalid date format. Use YYYY-MM-DD")
            
            if not validate_amount(inputs["amount"]):
                raise ValueError("Invalid amount. Must be a positive number")
            
            # Create and add expense
            expense = Expense(
                inputs["date"],
                inputs["category"],
                float(inputs["amount"]),
                inputs["description"]
            )
            
            add_expense_to_file(expense)
            self.clear_inputs()
            self.refresh_table()
            messagebox.showinfo("Success", "Expense added successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self.root)
    
    def delete_selected(self):
        """Delete the selected expense"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "No expense selected")
            return
        
        values = self.tree.item(selected, 'values')
        if values and values[1] == "TOTAL":  # Don't allow deleting the total row
            return
        
        if messagebox.askyesno("Confirm", "Delete selected expense?", icon='warning'):
            # Read all expenses, exclude the selected one, and rewrite the file
            expenses = read_expenses_from_file()
            updated_expenses = [
                exp for exp in expenses 
                if not (
                    exp.date == values[0] and 
                    exp.category == values[1] and 
                    f"₹{exp.amount:.2f}" == values[2] and 
                    exp.description == values[3]
                )
            ]
            
            # Clear and rewrite file
            clear_all_expenses()
            for exp in updated_expenses:
                add_expense_to_file(exp)
            
            self.refresh_table()
    
    def clear_all(self):
        """Clear all expenses"""
        if messagebox.askyesno("Confirm", "Delete ALL expenses? This cannot be undone!", icon='warning'):
            clear_all_expenses()
            self.refresh_table()