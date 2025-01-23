import tkinter as tk
import darkdetect
import ttkbootstrap as ttk
import os
import subprocess
import ctypes
import sys
import shutil
from tqdm import tqdm
from tkinter import filedialog
from tkinter import messagebox
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

def link_ginko():

    file_path = filedialog.askopenfilename(
        initialdir=r"C:\Program Files (x86)\Steam\steamapps\common",
        filetypes=[("Executable Files", "*.exe")]
    )

    if file_path:
        response = messagebox.askokcancel("Warning!", "Linking GinkEngine to Puttler will clone Puttlerrs game files into the GinkEngine folder. It would be considered piracy if you shared that folder in any way without permission. For sharing mods, please us GinkEngines built in 'Create Mods' feature. Linking will also cause all potential already installed mods to be deleted from the game installation, but they will remain re-installable. Do you want to continue?")
        if response:
            log_("Linking Puttler(Ginko)...")

            parent_directory = os.path.dirname(file_path)
            print(f"Selected file path: {file_path}")
            log_(f"Set Puttler(Ginko) parent directory to {parent_directory}")
            log_(f"Set Standard Puttler(Ginko) exe to {file_path}")

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

            response = messagebox.askquestion("x64?", "Does the linked game requre the x64 version of BepInEx?")
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

            log_("Puttler(Ginko) has been linked successfully")

            messagebox.showinfo("Success!", "Puttler(Ginko) has been linked to GinkEngine successfully!")
        else:
            print("Puttler(Ginko) not linked")


    else:
        print("No file selected.")

def play_standard():

    with open("../../user.config", "r") as file:
        lines = file.readlines()

    with open("../../Scripts/boot.bat", "w") as file:
        message_ = f"Start-Process '{lines[2]}'"
        message2_ = f'powershell -Command "{message_}"'
        message2_ = message2_.replace("\n", " ")

        file.writelines(message2_)
    
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
        log_("Couldn't start Standard Game")

        messagebox.showwarning("Puttler(Ginko) not linked", "Go to Options -> Link Puttler, and select the .exe file named 'Puttler.exe' in your Steam Puttler folder")

def play_modded():

    log_("Building BepInEx mods...")
    build_mods()
    log_("Build function passed. If a mod doesn't run, check references in visual studio and ensure they all point to a path within the Puttler Data or BepInEx folder. Alternatively, you can provide your own dll's trough the dll folder in the games GinkEngine folder")

    with open("../../user.config", "r") as file:
        lines = file.readlines()
    
    exename = fr"{os.path.basename(lines[2])}"

    exe_path = os.path.abspath(f"../../../DONT_SHARE/Game Files/{exename}")

    with open("../../Scripts/boot.bat", "w") as file:
        message_ = f"Start-Process '{exe_path}'"
        message2_ = f'powershell -Command "{message_}"'
        message2_ = message2_.replace("\n", " ")

        file.write(message2_)

    with open("../../Scripts/boot.bat", "a") as file:
        file.write("\n")
        file.write("exit \n")

    print(exe_path)

    if lines[2] != "none":
        batch_file_relative = "../../Scripts/boot.bat"
        batch_file_absolute = os.path.abspath(batch_file_relative)

        subprocess.run(["start", "cmd", "/k", batch_file_absolute], shell=True)

        log_("Started Modded Game")
    else:
        log_("Couldn't start Modded Game")
        # Show a warning if the file doesn't exist
        messagebox.showwarning(
            "Puttler(Ginko) not linked",
            "Go to Options -> Link Puttler, and select the .exe file named 'Puttler.exe' in your Steam Puttler folder",
        )

def start_tool(tool_path):
    with open("../../Scripts/boot.bat", "w") as file:
        message_ = f"Start-Process '{tool_path}'"
        message2_ = f'powershell -Command "{message_}"'
        message2_ = message2_.replace("\n", " ")

        file.write(message2_)

    with open("../../Scripts/boot.bat", "a") as file:
        file.write("\n")
        file.write("exit \n")

    log_(f"Running {tool_path}")

    if os.path.exists(f"{tool_path}"):
        batch_file_relative = "../../Scripts/boot.bat"
        batch_file_absolute = os.path.abspath(batch_file_relative)

        subprocess.run(["start", "cmd", "/k", batch_file_absolute], shell=True)

        log_(f"Started Tool {tool_path}")
    else:
        log_(f"Couldnt run {tool_path}")
        # Show a warning if the file doesn't exist
        messagebox.showerror(
            "Error",
            f"Couldn't start tool: {tool_path}",
        )

def start_visual_studio():

    with open("../../user.config", "r") as file:
        lines = file.readlines()

    tool_path = lines[3]

    if tool_path == "none":
        response = messagebox.askquestion("Connect Visual Studio", "Visual studio does unfortunately not come pre-installed with GinkEngine. If you don't have Visual Studio installed, please install Visual Studio 2022 Community from https://visualstudio.microsoft.com/vs/. If you already have Visual Studio installed, would you like to connect the exe to GinkEngine?")
        if response == 'yes':
            tool_path = filedialog.askopenfilename(
                initialdir=r"C:\Program Files (x86)",
                filetypes=[("Executable Files", "*.exe")]
            )
            log_("Visual Studio connected")
    
    lines[3] = tool_path
    with open("../../user.config", "w") as file:
        file.writelines(lines)

    if tool_path == "none":
        log_("Visual Studio path not found")
        return
    
    with open("../../Scripts/boot.bat", "w") as file:
        message_ = f"Start-Process '{tool_path}'"
        message2_ = f'powershell -Command "{message_}"'
        message2_ = message2_.replace("\n", " ")

        file.write(message2_)

    with open("../../Scripts/boot.bat", "a") as file:
        file.write("\n")
        file.write("exit \n")

    log_(f"Running {tool_path}")

    if os.path.exists(f"{tool_path}"):
        batch_file_relative = "../../Scripts/boot.bat"
        batch_file_absolute = os.path.abspath(batch_file_relative)

        subprocess.run(["start", "cmd", "/k", batch_file_absolute], shell=True)

        log_(f"Started Tool {tool_path}")
    else:
        log_(f"Couldnt run {tool_path}")
        # Show a warning if the file doesn't exist
        messagebox.showerror(
            "Error",
            f"Couldn't start tool: {tool_path}",
        )

def show_bepinex_console():
    if os.path.exists("../../../DONT_SHARE/Game Files/BepInEx/config/BepInEx.cfg"):
        log_("Turning on BepInEx console window")
        with open("../../../DONT_SHARE/Game Files/BepInEx/config/BepInEx.cfg", "r") as file:
            lines = file.readlines()

        if len(lines) > 48:
            lines[47] = "Enabled = true\n"

            log_("BepInEx show console setting turned on")

            with open("../../../DONT_SHARE/Game Files/BepInEx/config/BepInEx.cfg", "w") as file:
                file.writelines(lines)
        else:
            log_("Could not turn BepInEx show console setting on, config file not long enough")
            messagebox.showerror(
                "Error",
                f"Could not find appropriate config file for this action. To solve this, please make sure you have BepInEx installed on your game in the DONT_SHARE folder, and also that you have booted the game as modded prior to trying to configure this setting.",
            )
    else:
        log_("Could not turn BepInEx show console setting on, BepInEx not found")
        messagebox.showerror(
            "Error",
            f"BepInEx config file not found, please link your game first. If you already have a linked game, please start that game by going to Play -> Modded before trying to change this setting",
        )

def hide_bepinex_console():
    if os.path.exists("../../../DONT_SHARE/Game Files/BepInEx/config/BepInEx.cfg"):
        log_("Turning on BepInEx console window")
        with open("../../../DONT_SHARE/Game Files/BepInEx/config/BepInEx.cfg", "r") as file:
            lines = file.readlines()

        if len(lines) > 48:
            lines[47] = "Enabled = false\n"

            log_("BepInEx show console setting turned off")

            with open("../../../DONT_SHARE/Game Files/BepInEx/config/BepInEx.cfg", "w") as file:
                file.writelines(lines)
        else:
            log_("Could not turn BepInEx show console setting off, config file not long enough")
            messagebox.showerror(
                "Error",
                f"Could not find appropriate config file for this action. To solve this, please make sure you have BepInEx installed on your game in the DONT_SHARE folder, and also that you have booted the game as modded prior to trying to configure this setting.",
            )
    else:
        log_("Could not turn BepInEx show console setting off, BepInEx not found")
        messagebox.showerror(
            "Error",
            f"BepInEx config file not found, please link your game first. If you already have a linked game, please start that game by going to Play -> Modded before trying to change this setting",
        )

def find_folders_with_csproj(root_dir):
    folders_with_csproj = []
    
    for foldername, subfolders, filenames in os.walk(root_dir):
        if any(file.endswith(".csproj") for file in filenames):
            folders_with_csproj.append(foldername)
    
    return folders_with_csproj

def build_mods():
    folders = find_folders_with_csproj("../../../DONT_SHARE/Game Files/GinkEngine/raw")

    with open("../../Scripts/build_mods.bat", "w") as file:
        file.write("")

    for folder in folders:

        log_(f"Setting up mod in folder {folder}")

        with open("../../Scripts/build_mods.bat", "a") as file:
            message_ = f'cd "{os.path.abspath(f"../../../Game Files/GinkEngine/raw/{folder}")}"\n dotnet msbuild  -p:OutputPath="{os.path.abspath("../../../DONT_SHARE/Game Files/BepInEx/plugins")}"\n'

            file.write(message_)

    with open("../../Scripts/build_mods.bat", "a") as file:
        file.write("exit")

    batch_file_relative = "../../Scripts/build_mods.bat"
    batch_file_absolute = os.path.abspath(batch_file_relative)

    subprocess.run(["start", "cmd", "/k", batch_file_absolute], shell=True)

    log_("Started building all mods")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    script = sys.argv[0]
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)

def dark_listener(theme):
    if theme == "Dark":
        s.theme_use('darkly')
    else:
        s.theme_use('flatly')

# if not is_admin():
#         run_as_admin()
#         sys.exit(0)

root = ttk.Window()
root.title("GinkEngine V0.1")
root.geometry("600x800")

s=ttk.Style()
if darkdetect.isDark():
    s.theme_use('darkly')
else:
    s.theme_use('flatly')

# Create a Menu widget
menu_bar = tk.Menu(root)


# Create the "Options" menu
file_menu = tk.Menu(menu_bar, tearoff=0)  # tearoff=0 removes the dashed line

# Link Ginko Option
file_menu.add_command(label="Link Puttler", command=lambda: link_ginko())
file_menu.add_separator()  # Add a separator line
file_menu.add_command(label="Turn on BepInEx console", command=lambda: show_bepinex_console())
file_menu.add_command(label="Turn off BepInEx console", command=lambda: hide_bepinex_console())
file_menu.add_separator()  # Add a separator line

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
tools_menu.add_command(label="Visual Studio", command= start_visual_studio)

tools_menu.add_separator()

tools_menu.add_command(label="Code Editors", state="disabled") # IDEs
tools_menu.add_command(label="VS Code", command=lambda: start_tool(os.path.abspath("../VS Code.exe")))

# Add Jupyter tools
jupyter_menu = tk.Menu(tools_menu, tearoff=0)
jupyter_menu.add_command(label="Jupyter Lab", command=lambda: start_tool(os.path.abspath("../Jupyter Lab.exe")))
jupyter_menu.add_command(label="Jupyter Notebook", command=lambda: start_tool(os.path.abspath("../Jupyter Notebook.exe")))
tools_menu.add_cascade(label="Jupyter", menu=jupyter_menu)

tools_menu.add_command(label="Spyder", command=lambda: start_tool(os.path.abspath("../Spyder.exe")))

tools_menu.add_separator()

tools_menu.add_command(label="Modding Tools", state="disabled") # Mod tools

tools_menu.add_command(label="AssetStudio", command=lambda: start_tool(os.path.abspath("../../AssetStudio/AssetStudioGUI.exe")))
tools_menu.add_command(label="UABE", command=lambda: start_tool(os.path.abspath("../../UABE/AssetBundleExtractor.exe")))
tools_menu.add_command(label="dnSpy", command=lambda: start_tool(os.path.abspath("../../dnSpy/dnSpy.exe")))

menu_bar.add_cascade(label="Tools", menu=tools_menu)

# Add option to play modded

play_menu = tk.Menu(menu_bar, tearoff=0)
play_menu.add_command(label="Play Modded", command=lambda:play_modded())
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
