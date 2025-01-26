import tkinter as tk
import os
import subprocess
import ctypes
import sys
import shutil
import zipfile
from tqdm import tqdm
from tkinter import ttk, StringVar, Toplevel
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
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

def files_are_identical(file1, file2):
    """Compares two files byte-by-byte."""

    # Check if the file sizes match
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

    print(f"Exported modded file: {file2}")
    return False

def build_final_mod(mod_name, author_name, description_info):

    build_mods()

    with open("../../user.config", "r") as file:
        lines = file.readlines()

    if lines[1] == "none":
        log_("Couldn't build final mod because Puttler isn't linked")
        messagebox.showerror(
            "Error",
            f"Please link Puttler(Ginko) before building final mod",
        )
    
    folder1 = lines[1].strip().replace("/", "\\")

    folder2 = "../../../DONT_SHARE/Game Files/"

    folder3 = f"../../../Mods/{mod_name}"
    
    filecount = 0
    
    """
    Compare files in folder2 to folder1 and save the differing files into output_folder, keeping the same path structure.
    """
    for root, dirs, files in os.walk(folder2):
        for file in files:
            # Skip .exe files and Assembly-CSharp.dll
            if file.endswith(".exe") or file == "Assembly-CSharp.dll":
                continue
            
            # Skip files in the GinkEngine/raw directory
            relative_path = os.path.relpath(os.path.join(root, file), folder2)

            # Define corresponding file paths in folder1 and folder3
            file_in_folder1 = os.path.join(folder1, relative_path)
            file_in_folder2 = os.path.join(folder2, relative_path)
            file_in_folder3 = os.path.join(folder3, relative_path)

            if "GinkEngine\\raw" in (file_in_folder2):
                continue

            if os.path.exists(file_in_folder1):
                if files_are_identical(file_in_folder1, file_in_folder2):
                    continue  # Files are identical, skip copying

            # Ensure the folder structure exists in folder3
            os.makedirs(os.path.dirname(file_in_folder3), exist_ok=True)
            
            # Copy the file from folder2 to folder3
            print(f"Compared {file_in_folder1} to {file_in_folder2} and found differences")
            shutil.copy2(file_in_folder2, file_in_folder3)

            filecount = filecount + 1

    os.makedirs(f"{folder3}/GinkEngine", exist_ok=True)

    with open(f"{folder3}/GinkEngine/about_mod.ginko", 'w') as file:
        file.write(f"{mod_name}\n{author_name}\n{description_info}")

    messagebox.showinfo("Success!", f"{mod_name} has been exported successfully!")

    log_(f"Successfully exported {filecount} file(s) to mod {mod_name}")

def install_mod(source_folder):
    mod_name = source_folder

    with open("../../user.config", "r") as file:
        lines = file.readlines()

    if lines[1] == "none":
        log_("Couldn't install mod because Puttler isn't linked")
        messagebox.showerror(
            "Error",
            f"Please link Puttler(Ginko) before installing any mods",
        )

    with open(f"../../../Mods/{mod_name}/GinkEngine/about_mod.ginko", 'r') as file:
        lines = file.readlines()
    
    author_name = lines[1]

    response = messagebox.askquestion("Install?", f"Are you sure you want to install '{mod_name}' by {author_name}?")
    if response == 'no':
        return

    source_folder = f"../../../Mods/{mod_name}"
    destination_folder = "../../../DONT_SHARE/Game Files/"

    if not os.path.exists(source_folder):
        messagebox.showerror(
            "Error",
            f"Could not find mod, please try another mod",
        )
        log_("Could not find mod")
        return

    if not os.path.exists(destination_folder):
        messagebox.showerror(
            "Error",
            f"Please link Puttler first",
        )
        log_("Could not install mod because Puttler wasn't linked")
        return
    
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(root, source_folder)
            dest_dir = os.path.join(destination_folder, relative_path)
            os.makedirs(dest_dir, exist_ok=True)  # Create subdirectories as needed
            
            dest_file = os.path.join(dest_dir, file)
            shutil.copy2(source_file, dest_file)  # Copy the file, preserving metadata
            print(f"Copied: {source_file} -> {dest_file}")

    refresh_mod_dropdown()

    log_(f"{mod_name} was installed successfully")

    messagebox.showinfo("Success!", f"{mod_name} was installed successfully!")

def refresh_mod_dropdown():
    log_("Mod dropdown refreshed")
    mod_folders = [folder for folder in os.listdir("../../../Mods/") if os.path.isdir(os.path.join("../../../Mods/", folder))]
    
    if mod_folders:
        mod_combobox['values'] = mod_folders  # Update dropdown options
        mod_combobox.set(mod_folders[0])  # Default to the first mod in the list
    else:
        mod_combobox['values'] = ["No mods downloaded"]
        mod_combobox.set("No mods downloaded")  # Set to placeholder if no mods found

def refresh_delete_mod_dropdown():
    log_("Mod dropdown refreshed")
    mod_folders = [folder for folder in os.listdir("../../../Mods/") if os.path.isdir(os.path.join("../../../Mods/", folder))]
    
    if mod_folders:
        delete_mod_combobox['values'] = mod_folders  # Update dropdown options
        delete_mod_combobox.set(mod_folders[0])  # Default to the first mod in the list
    else:
        delete_mod_combobox['values'] = ["No mods downloaded"]
        delete_mod_combobox.set("No mods downloaded")  # Set to placeholder if no mods found


def prevent_highlight(event):
    event.widget.selection_clear()

def add_mod_from_zip():
    # Open a file dialog to select a .zip file
    zip_file_path = filedialog.askopenfilename(title="Select Mod ZIP File", filetypes=[("ZIP files", "*.zip")])
    
    if not zip_file_path:
        messagebox.showinfo("No File Selected", "You did not select a .zip file.")
        log_("No mod added because no file was selected")
        return
    
    # Get the name of the folder that will be created from the ZIP file
    folder_name = os.path.splitext(os.path.basename(zip_file_path))[0]
    destination_folder = os.path.join("../../../Mods/", folder_name)
    log_(f"Adding mod {folder_name}...")

    try:
        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        # Extract the ZIP file to the destination folder
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
        
        messagebox.showinfo("Success", f"Mod added successfully! To install it, go to the Install Mods tab!")
        log_("Mod was added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract mod: {e}")
        log_(f"Failed to extract mod: {e}")

def export_mod():
    def refresh_export_mod_dropdown():
        log_("Export mod dropdown refreshed")
        mod_folders = [folder for folder in os.listdir("../../../Mods/") if os.path.isdir(os.path.join("../../../Mods/", folder))]

        if mod_folders:
            export_mod_combobox['values'] = mod_folders
            export_mod_combobox.set(mod_folders[0]) 
        else:
            export_mod_combobox['values'] = ["No mods downloaded"]
            export_mod_combobox.set("No mods downloaded")
    
    # Get a list of installed mods (all folders in the mods directory)
    mod_folders = [folder for folder in os.listdir("../../../Mods/") if os.path.isdir(os.path.join("../../../Mods/", folder))]
    
    # If there are no mods installed, show an error message
    if not mod_folders:
        messagebox.showerror("No Mods Imported", "There are no mods to export. Please build your mod first")
        return

    # Create a new popup window
    export_window = Toplevel()
    export_window.title("Export Mod")
    export_window.geometry("300x200")

    icon = PhotoImage(file='../../../Assets/icon.png')
    export_window.iconphoto(True, icon)
    
    # Label for the dropdown menu
    label = ttk.Label(export_window, text="Select Mod to Export", font=("Arial", 12))
    label.pack(pady=10)

    export_mod_combobox = ttk.Combobox(export_window, state="readonly")  # Set to readonly to prevent typing
    export_mod_combobox.pack(pady=10)
    export_mod_combobox.bind("<FocusIn>", prevent_highlight)

    refresh_export_mod_dropdown()

    def handle_export():
        selected_mod_name = export_mod_combobox.get()
        
        # Open a file dialog to choose where to save the zip file
        save_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Zip files", "*.zip")], title="Save Mod As")
        
        # Check if a save path is selected (i.e., the user didn't cancel the dialog)
        if save_path:
            try:
                # Create the zip file and add the selected mod folder to it
                mod_folder_path = os.path.join("../../../Mods/", selected_mod_name)
                with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Walk through the selected mod folder and add all files
                    for root, dirs, files in os.walk(mod_folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Add the file to the zip, maintaining the folder structure
                            zipf.write(file_path, os.path.relpath(file_path, mod_folder_path))
                            print(f"Writing file {file_path} to {save_path}")
                
                log_(f"Mod '{selected_mod_name}' has been successfully exported!")
                messagebox.showinfo("Success", f"Mod '{selected_mod_name}' has been successfully exported.")
                export_window.destroy()  # Close the popup after successful export

            except Exception as e:
                log_(f"An error occured while exporting mod: {e}")
                messagebox.showerror("Error", f"An error occurred while exporting the mod: {e}")
    
    # Export button
    export_button = ttk.Button(export_window, text="Export Mod", command=handle_export)
    export_button.pack(pady=10)

    # Start the event loop for the popup window
    export_window.mainloop()

def delete_mods(folder_path):
    folder_path = os.path.join("../../../Mods/", folder_path)

    if os.path.exists(folder_path):
        # Ask for user confirmation before deleting
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the mod folder '{folder_path}' and all of its contents? This will not remove the mod from the game installation, to do that you have to re-link the game. This will simply remove the option of installing the mod, as well as remove it's files from your hard drive. This action can not be reversed")
        
        if confirm:
            try:
                # Delete the folder and all its contents
                shutil.rmtree(folder_path)
                log_(f"{folder_path} removed successfully")
                messagebox.showinfo("Success", f"The folder '{folder_path}' has been deleted successfully.")
            except Exception as e:
                # Handle errors (if any)
                messagebox.showerror("Error", f"An error occurred while deleting the folder: {e}")
        else:
            messagebox.showinfo("Cancelled", "Folder deletion has been cancelled.")
    else:
        messagebox.showerror("Error", f"The folder '{folder_path}' does not exist.")

def open_about_window():
    about_window = Toplevel()
    about_window.title("About GinkEngine")
    about_window.geometry("400x400")

    icon = PhotoImage(file='../../../Assets/icon.png')
    about_window.iconphoto(True, icon)

    label = tk.Label(about_window, wraplength=350, text="GinkEngine is a versatile and user-friendly modding tool designed for the game Puttler. Developed by Squidforge Productions, GinkEngine aims to streamline the modding process by providing a comprehensive set of tools that make mod creation, management, and sharing as easy as possible. \n \n Whether youre looking to add new content to the game or modify existing features, GinkEngine comes pre-packaged with a variety of utilities to handle common modding tasks. From extracting and exporting mod files to managing mod directories, GinkEngine simplifies the process, ensuring you can focus on creativity rather than technical details. \n \n The tool was developed with accessibility in mind, offering a clean, intuitive interface that allows both new and experienced modders to dive right in. RaixuStuffRaixuStuff (raysullyplays) also contributed to the project, adding valuable features and improvements to make GinkEngine even better. \n \n You are using the pre-release version of GinkEngine, otherwise known as version 0.9")
    label.pack(pady=20)  # Pack it into the window with some padding

    about_window.mainloop()

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
root.title("GinkEngine Pre-Release (v0.9)")
root.geometry("600x800")

icon = PhotoImage(file='../../../Assets/icon.png')
root.iconphoto(True, icon)

# Create a Menu widget
style = ttk.Style()
print(style.theme_names())

with open("../../user.config", "r") as file:
    style_ = file.readline().strip()  # Read the first line and remove leading/trailing whitespace
    switch_style(style_)

menu_bar = tk.Menu(root)


# Create the "Options" menu
file_menu = tk.Menu(menu_bar, tearoff=0)  # tearoff=0 removes the dashed line

# Link Ginko Option
file_menu.add_command(label="Link Puttler", command=lambda: link_ginko())
file_menu.add_separator()  # Add a separator line

#BepInEx console show/hide
file_menu.add_command(label="Turn on BepInEx console", command=lambda: show_bepinex_console())
file_menu.add_command(label="Turn off BepInEx console", command=lambda: hide_bepinex_console())
file_menu.add_separator()  # Add a separator line

#Add and export mods
file_menu.add_command(label="Import mod", command=lambda: add_mod_from_zip())
file_menu.add_command(label="Export mod", command=lambda: export_mod())
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
help_menu.add_command(label="About", command=lambda: open_about_window())
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
tools_menu.add_command(label="dnSpy", command=lambda: start_tool(os.path.abspath("../../dnSpy/dnSpy.exe")))

UABE_menu = tk.Menu(tools_menu, tearoff=0)
UABE_menu.add_command(label="UABEA(recommended)", command=lambda: start_tool(os.path.abspath("../../UABEA/UABEAvalonia.exe")))
UABE_menu.add_command(label="UABE", command=lambda: start_tool(os.path.abspath("../../UABE/AssetBundleExtractor.exe")))
tools_menu.add_cascade(label="UABE", menu=UABE_menu)

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
Remove = ttk.Frame(notebook, padding=10)
Create = ttk.Frame(notebook, padding=10)
Install = ttk.Frame(notebook, padding=10)

# Add tabs to the Notebook
notebook.add(Create, text="Create Mods")
notebook.add(Install, text="Install Mods")
notebook.add(Remove, text="Delete Mods")

# Content for Create tab
label2 = ttk.Label(Create, text="Create Mod", font=("Arial", 14))
label2.pack(pady=10)

name_label = ttk.Label(Create, text="Name:")
name_label.pack(anchor="w", padx=5)
name_entry = ttk.Entry(Create, width=30)
name_entry.pack(padx=5, pady=2)

author_label = ttk.Label(Create, text="Author:")
author_label.pack(anchor="w", padx=5)
author_entry = ttk.Entry(Create, width=30)
author_entry.pack(padx=5, pady=2)

description_label = ttk.Label(Create, text="Description:")
description_label.pack(anchor="w", padx=5)
description_entry = ttk.Entry(Create, width=30)
description_entry.pack(padx=5, pady=2)

build_button = ttk.Button(Create, text="Build Mod", command=lambda: build_final_mod(name_entry.get(), author_entry.get(), description_entry.get()))
build_button.pack(pady=5)

# Content for Install tab

mod_folders = [folder for folder in os.listdir("../../../Mods/") if os.path.isdir(os.path.join("../../../Mods/", folder))]

label3 = ttk.Label(Install, text="Install Mods", font=("Arial", 14))
label3.pack(pady=10)

refresh_button = ttk.Button(Install, text="Refresh", command=lambda: refresh_mod_dropdown())
refresh_button.pack(pady=10)

mod_combobox = ttk.Combobox(Install, state="readonly")  # Set to readonly to prevent typing
mod_combobox.pack(pady=10)
mod_combobox.bind("<FocusIn>", prevent_highlight)

refresh_mod_dropdown()

install_button = ttk.Button(Install, text="Install", command=lambda: install_mod(mod_combobox.get()))
install_button.pack(pady=10)

# Content for Delete tab
label1 = ttk.Label(Remove, text="Remove mods", font=("Arial", 14))
label1.pack(pady=10)
refresh_button2 = ttk.Button(Remove, text="Refresh", command=lambda: refresh_delete_mod_dropdown())
refresh_button2.pack(pady=10)

delete_mod_combobox = ttk.Combobox(Remove, state="readonly")  # Set to readonly to prevent typing
delete_mod_combobox.pack(pady=10)
delete_mod_combobox.bind("<FocusIn>", prevent_highlight)

refresh_delete_mod_dropdown()

button1 = ttk.Button(Remove, text="Remove selected mod", command=lambda: delete_mods(delete_mod_combobox.get()))
button1.pack()

root.mainloop()
