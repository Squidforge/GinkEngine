import tkinter as tk
from tkinter import ttk

def on_new():
    print("New file created!")

def on_open():
    print("File opened!")

def on_exit():
    root.quit()

root = tk.Tk()
root.title("Menu Bar Example")
root.geometry("600x400")

root.tk.call('source', '../../../Assets/tkinter_themes/aquablue/aquablue8.5.tcl')
style = ttk.Style()
style.theme_use('aquablue')  # You can try other themes like 'default', 'alt', 'clam', etc.
print(style.theme_names())

# Create a Menu widget
menu_bar = tk.Menu(root)

# Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)  # tearoff=0 removes the dashed line
file_menu.add_command(label="New", command=on_new)
file_menu.add_command(label="Open", command=on_open)
file_menu.add_separator()  # Add a separator line
file_menu.add_command(label="Exit", command=on_exit)

menu_bar.add_cascade(label="File", menu=file_menu)  # Add "File" menu to the menu bar

# Create the "Edit" menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Create the "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About")
menu_bar.add_cascade(label="Help", menu=help_menu)

# Attach the menu bar to the root window
root.config(menu=menu_bar)

#Interface

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create Frames for each tab
tab1 = ttk.Frame(notebook, padding=10)
tab2 = ttk.Frame(notebook, padding=10)
tab3 = ttk.Frame(notebook, padding=10)

# Add tabs to the Notebook
notebook.add(tab1, text="Browse Mods")
notebook.add(tab2, text="Create Mods")
notebook.add(tab3, text="Tab 3")

# Content for Tab 1
label1 = ttk.Label(tab1, text="This is Tab 1", font=("Arial", 14))
label1.pack(pady=10)
button1 = ttk.Button(tab1, text="Button in Tab 1")
button1.pack()

# Content for Tab 2
label2 = ttk.Label(tab2, text="This is Tab 2", font=("Arial", 14))
label2.pack(pady=10)
button2 = ttk.Button(tab2, text="+")
button2.pack()
entry2 = ttk.Entry(tab2)
entry2.pack()

# Content for Tab 3
label3 = ttk.Label(tab3, text="This is Tab 3", font=("Arial", 14))
label3.pack(pady=10)
combo3 = ttk.Combobox(tab3, values=["Option 1", "Option 2", "Option 3"])
combo3.pack()

root.mainloop()
