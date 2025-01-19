import tkinter as tk
import os
import subprocess
import ctypes
import sys
import shutil
from tqdm import tqdm
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from datetime import date
from datetime import datetime


today = datetime.now()

date_ = today.strftime("%B-%d-%Y")

time_ = today.strftime("%Y-%m-%d : %H-%M-%S")

style_path = '../../../Assets/tkinter_themes/'

def log_(message):
    today = datetime.now()
    date_ = today.strftime("%B-%d-%Y")
    time_ = today.strftime("%Y-%m-%d : %H-%M-%S")

    print(f"{message}")

    with open(f"../../../Logs/{date_}.log", "a") as file:
        file.write(f"\n{message} - {time_}")

def on_new():
    print("New file created!")

def on_open():
    print("File opened!")

def on_exit():
    log_("In-app exit triggered")
    root.quit()

def switch_style(style_):
    if style_ not in style.theme_names():
        root.tk.call('source', f'../../../Assets/tkinter_themes/{style_}/{style_}.tcl')
    
    style.theme_use(style_)
    log_(f"Using theme {style_}")

    # Save style to config file

    with open("../../user.config", "r") as file:
        lines = file.readlines()
    
    lines[0] = f"{style_}\n"

    with open("../../user.config", "w") as file:
        file.writelines(lines)

def link_ginko():

    file_path = filedialog.askopenfilename(
        initialdir=r"C:\Program Files (x86)\Steam\steamapps\common",
        filetypes=[("Executable Files", "*.exe")]
    )

    if file_path:
        response = messagebox.askokcancel("Warning!", "Linking GinkEngine to Puttle will clone Puttles game files into the GinkEngine folder. It would be considered piracy if you shared that folder in any way without permission. For sharing mods, please us GinkEngines built in 'Create Mods' feature. Linking will also cause all potential already installed mods to be deleted from the game installation, but they will remain re-installable. Do you want to continue?")
        if response:
            log_("Linking Puttle(Ginko)...")

            parent_directory = os.path.dirname(file_path)
            print(f"Selected file path: {file_path}")
            log_(f"Set Puttle(Ginko) parent directory to {parent_directory}")
            log_(f"Set Standard Puttle(Ginko) exe to {file_path}")

            with open("../../user.config", "r") as file:
                lines = file.readlines()

            lines[1] = f"{parent_directory}\n"
            lines[2] = f"{file_path}\n"

            with open("../../user.config", "w") as file:
                file.writelines(lines)

            destination_folder = "../../../DONT_SHARE/Game Files"

            if os.path.exists(destination_folder):
                try:
                    shutil.rmtree(destination_folder)
                    log_(f"Successfully deleted: {destination_folder}")
                except Exception as e:
                    log_(f"Error deleting folder: {e}")
            else:
                log_(f"The folder does not exist: {destination_folder}")

            # Create the destination folder if it doesn't exist
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            print(f"Source folder: {parent_directory}")
            print(f"Destination folder: {destination_folder}")

            # Get the list of all files and directories in the source folder
            total_files = sum([len(files) for _, _, files in os.walk(parent_directory)])
            if total_files == 0:
                log_("No files found in the game source directory.")
                return

            progress_bar = tqdm(total=total_files, desc="Copying files", unit="file")

            for root, dirs, files in os.walk(parent_directory):
                # Determine the relative path from the source folder
                relative_path = os.path.relpath(root, parent_directory)
                destination_root = os.path.join(destination_folder, relative_path)

                # Create directories in the destination
                for dir_name in dirs:
                    destination_dir = os.path.join(destination_root, dir_name)
                    os.makedirs(destination_dir, exist_ok=True)
                    print(f"Created directory: {destination_dir}")

                # Copy files and update the progress bar
                for file_name in files:
                    source_file = os.path.join(root, file_name)
                    destination_file = os.path.join(destination_root, file_name)
                    print(f"Copying file: {source_file} -> {destination_file}")
                    shutil.copy2(source_file, destination_file)
                    progress_bar.update(1)

            log_("Installing BepInEx...")

            bepinex = "../../BepInEx"

            response = messagebox.askquestion("Question", "Does the linked game requre the x64 version of BepInEx?")
            if response == 'yes':
                bepinex = "../../BepInExx64"

            # Install BepInEx
            total_files = sum([len(files) for _, _, files in os.walk(bepinex)])
            if total_files == 0:
                log_("No files found in the BepInEx directory.")
                return

            progress_bar = tqdm(total=total_files, desc="Copying files", unit="file")

            for root, dirs, files in os.walk(bepinex):
                # Determine the relative path from the source folder
                relative_path = os.path.relpath(root, bepinex)
                destination_root = os.path.join(destination_folder, relative_path)

                # Create directories in the destination
                for dir_name in dirs:
                    destination_dir = os.path.join(destination_root, dir_name)
                    os.makedirs(destination_dir, exist_ok=True)
                    print(f"Created directory: {destination_dir}")

                # Copy files and update the progress bar
                for file_name in files:
                    source_file = os.path.join(root, file_name)
                    destination_file = os.path.join(destination_root, file_name)
                    print(f"Copying file: {source_file} -> {destination_file}")
                    shutil.copy2(source_file, destination_file)
                    progress_bar.update(1)

            log_("Puttle(Ginko) has been linked successfully")

            messagebox.showinfo("Success!", "Puttle(Ginko) has been linked to GinkEngine successfully!")
        else:
            print("Puttle(Ginko) not linked")


    else:
        print("No file selected.")

def play_standard():

    with open("../../user.config", "r") as file:
        lines = file.readlines()

    with open("../../Scripts/boot.bat", "w") as file:
        message_ = f"Start-Process '{lines[2]}'"
        message2_ = f'powershell -Command "{message_}"'
        message2_ = message2_.replace("\n", " ")

        file.write(message2_)
    
    with open("../../Scripts/boot.bat", "a") as file:
        file.write("\n")
        file.write("exit \n")

    if lines[2] != "none":
        print(f"Current working directory: {os.getcwd()}")

        batch_file_relative = "../../Scripts/boot.bat"
        batch_file_absolute = os.path.abspath(batch_file_relative)

        subprocess.run(["start", "cmd", "/k", batch_file_absolute], shell=True)

        log_("Started Standard Game")
    else:
        messagebox.showwarning("Puttle(Ginko) not linked", "Go to Options -> Link Puttle, and select the .exe file named 'Puttle.exe' in your Steam Puttle folder")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    script = sys.argv[0]
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)


# if not is_admin():
#         run_as_admin()
#         sys.exit(0)

root = tk.Tk()
root.title("GinkEngine V0.1")
root.geometry("600x800")

style = ttk.Style()
print(style.theme_names())

# Read style from config file

with open("../../user.config", "r") as file:
    style_ = file.readline().strip()  # Read the first line and remove leading/trailing whitespace
    switch_style(style_)

# Create a Menu widget
menu_bar = tk.Menu(root)

# Create the "Options" menu
file_menu = tk.Menu(menu_bar, tearoff=0)  # tearoff=0 removes the dashed line

# Link Ginko Option
file_menu.add_command(label="Link Puttle", command=lambda: link_ginko())
file_menu.add_separator()  # Add a separator line

# Add themes to Options
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

# More options
file_menu.add_separator()  # Add a separator line
file_menu.add_command(label="Exit", command=on_exit)

menu_bar.add_cascade(label="Options", menu=file_menu)  # Add "File" menu to the menu bar

# Create the "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About")
help_menu.add_command(label="Startup Guide")
menu_bar.add_cascade(label="Help", menu=help_menu)

# Create the "Tools" menu

tools_menu = tk.Menu(menu_bar, tearoff=0)
tools_menu.add_command(label="IDEs", state="disabled") # IDEs
tools_menu.add_command(label="VS Code")

# Add Jupyter tools
jupyter_menu = tk.Menu(tools_menu, tearoff=0)
jupyter_menu.add_command(label="Jupyter Lab")
jupyter_menu.add_command(label="Jupyter Notebook")
tools_menu.add_cascade(label="Jupyter", menu=jupyter_menu)

tools_menu.add_command(label="Spyder")

tools_menu.add_separator()

tools_menu.add_command(label="Modding Tools", state="disabled") # Mod tools

tools_menu.add_command(label="AssetStudio")
tools_menu.add_command(label="UABE")


menu_bar.add_cascade(label="Tools", menu=tools_menu)

# Add option to play modded

play_menu = tk.Menu(menu_bar, tearoff=0)
play_menu.add_command(label="Play Modded")
play_menu.add_command(label="Play Standard", command=lambda:play_standard())

menu_bar.add_cascade(label="Play", menu=play_menu)

# Attach the menu bar to the root window
root.config(menu=menu_bar)

#Interface

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create Frames for each tab
Browse = ttk.Frame(notebook, padding=10)
Create = ttk.Frame(notebook, padding=10)
Install = ttk.Frame(notebook, padding=10)

# Add tabs to the Notebook
notebook.add(Browse, text="Browse Mods")
notebook.add(Create, text="Create Mods")
notebook.add(Install, text="Install Mods")

# Content for Tab 1
label1 = ttk.Label(Browse, text="This is Tab 1", font=("Arial", 14))
label1.pack(pady=10)
button1 = ttk.Button(Browse, text="Button in Tab 1")
button1.pack()

# Content for Tab 2
label2 = ttk.Label(Create, text="This is Tab 2", font=("Arial", 14))
label2.pack(pady=10)
button2 = ttk.Button(Create, text="+")
button2.pack()
entry2 = ttk.Entry(Create)
entry2.pack()

# Content for Tab 3
label3 = ttk.Label(Install, text="This is Tab 3", font=("Arial", 14))
label3.pack(pady=10)
combo3 = ttk.Combobox(Install, values=["Option 1", "Option 2", "Option 3"])
combo3.pack()

root.mainloop()
