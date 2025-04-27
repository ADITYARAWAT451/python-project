# Color scheme
BG_COLOR = "#f5f5f5"
PRIMARY_COLOR = "#4a6fa5"
SECONDARY_COLOR = "#166088"
ACCENT_COLOR = "#4fc3f7"
ERROR_COLOR = "#ff5252"
SUCCESS_COLOR = "#4caf50"

# Fonts
HEADER_FONT = ("Helvetica", 14, "bold")
LABEL_FONT = ("Helvetica", 10)
BUTTON_FONT = ("Helvetica", 10, "bold")

def configure_styles():
    """Configure ttk styles for the application"""
    from tkinter import ttk
    
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure("Treeview", 
                   background="#ffffff",
                   foreground="black",
                   rowheight=25,
                   fieldbackground="#ffffff",
                   font=('Helvetica', 10))
    style.map('Treeview', background=[('selected', SECONDARY_COLOR)])
    
    style.configure("Treeview.Heading", 
                   background=PRIMARY_COLOR,
                   foreground="white",
                   padding=5,
                   font=('Helvetica', 10, 'bold'))
    
    style.configure("TButton", 
                   font=BUTTON_FONT,
                   padding=6,
                   background=PRIMARY_COLOR,
                   foreground="white")
    style.map("TButton",
             background=[('active', SECONDARY_COLOR), ('disabled', '#cccccc')])
    
    style.configure("TCombobox", fieldbackground="white", background="white")
    
    return style