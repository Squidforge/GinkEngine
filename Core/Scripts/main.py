import tkinter as tk
import os
from tkinter import ttk

style_path = '../../../Assets/tkinter_themes/'

def on_new():
    print("New file created!")

def on_open():
    print("File opened!")

def on_exit():
    root.quit()

def switch_style(style_):
    if style_ not in style.theme_names():
        root.tk.call('source', f'../../../Assets/tkinter_themes/{style_}/{style_}.tcl')
    
    style.theme_use(style_)
    print(f"Using theme {style_}")

def add_style(style_):
    root.tk.call('source', '../../../Assets/tkinter_themes/{style_}/{style_}.tcl')
    print(f"Configured theme {style_}")

root = tk.Tk()
root.title("GinkEngine V0.1")
root.geometry("600x800")

style = ttk.Style()
switch_style("clearlooks")
print(style.theme_names())

# Create a Menu widget
menu_bar = tk.Menu(root)

# Create the "Options" menu
file_menu = tk.Menu(menu_bar, tearoff=0)  # tearoff=0 removes the dashed line

theme_menu = tk.Menu(file_menu, tearoff=0)
theme_menu.add_command(label="default", command=lambda: switch_style("default"))
theme_menu.add_command(label="clam", command=lambda: switch_style("clam"))
theme_menu.add_command(label="winnative", command=lambda: switch_style("winnative"))
theme_menu.add_command(label="classic", command=lambda: switch_style("classic"))
theme_menu.add_command(label="vista", command=lambda: switch_style("vista"))
theme_menu.add_command(label="xpnative", command=lambda: switch_style("xpnative"))


for folder_name in os.listdir(style_path):
            folder_path = os.path.join(style_path, folder_name)
            # Ensure only folders are added
            if os.path.isdir(folder_path):
                theme_menu.add_command(
                    label=folder_name, 
                    command=lambda name=folder_name: switch_style(f"{name}")
                )

file_menu.add_cascade(label="Themes", menu=theme_menu)
file_menu.add_separator()  # Add a separator line
file_menu.add_command(label="Exit", command=on_exit)

menu_bar.add_cascade(label="Options", menu=file_menu)  # Add "File" menu to the menu bar

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
