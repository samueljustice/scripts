# Plugin Installer Script
# 
# Description:
# This script provides a GUI-based utility for managing plugin installations for audio software.
# The utility uses Tkinter to create a user interface that allows users to select a source folder
# containing plugin files, create a folder structure, and execute the installation.
#
# Features:
# 1. "Create Folder Structure" creates a default directory structure where plugins will be placed. Place .VST files in the VST folder, .VST3 files in the VST3 folder, .component files in the AU folder and .aax files in the AAX folder
# 2. "Select Folder" allows users to specify the source directory containing the plugins.
# 3. "Execute Install" initiates the copying of plugin files from source to destination and runs package installers.
# 
# Author: Samuel Justice
# Created On: 2023-10-05
# Last Modified: 2023-10-05
#
# Dependencies:
# - Tkinter for GUI
# - shutil for file operations
# - glob for file pattern matching
# - subprocess for executing shell commands
# - os for file and directory operations
#
# Functions:
# - select_folder(): Opens a dialog box to allow folder selection.
# - create_folder_structure(): Creates a default folder structure in the specified location.
# - execute_install(): Initiates the installation process.
# - copy_files(src, dest): Copies files from 'src' directory to 'dest' directory.
#
# Usage:
# Execute this script to open the GUI. Use the buttons provided to perform actions.


import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import shutil
import glob
import subprocess
import os

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

def create_folder_structure():
    base_folder = filedialog.askdirectory()
    target_folder = os.path.join(base_folder, "SJsPluginInstaller")
    subfolders = ["AAX", "AU", "DOCUMENTS", "INSTALLERS", "VST", "VST3"]

    os.makedirs(target_folder, exist_ok=True)
    for subfolder in subfolders:
        os.makedirs(os.path.join(target_folder, subfolder), exist_ok=True)

def execute_install():
    FOLDER_PATH = folder_path.get()
    output.delete(1.0, tk.END)

    message = ""
    message += copy_files(f"{FOLDER_PATH}/VST", "/Library/Audio/Plug-Ins/VST")
    message += copy_files(f"{FOLDER_PATH}/VST3", "/Library/Audio/Plug-Ins/VST3")
    message += copy_files(f"{FOLDER_PATH}/AU", "/Library/Audio/Plug-Ins/Components")
    message += copy_files(f"{FOLDER_PATH}/AAX", "/Library/Application Support/Avid/Audio/Plug-Ins")
    message += copy_files(f"{FOLDER_PATH}/DOCUMENTS", "~/Documents")

    installer_folder = f"{FOLDER_PATH}/INSTALLERS"

    for pkg_file in glob.glob(f"{installer_folder}/*.pkg"):
        try:
            subprocess.run(["sudo", "installer", "-pkg", pkg_file, "-target", "/"], check=True)
            message += f"Installed {pkg_file}\n"
        except subprocess.CalledProcessError as e:
            print(e)
            message += f"Failed to install {pkg_file}\n"

    for mpkg_file in glob.glob(f"{installer_folder}/*.mpkg"):
        try:
            subprocess.run(["sudo", "installer", "-pkg", mpkg_file, "-target", "/"], check=True)
            message += f"Installed {mpkg_file}\n"
        except subprocess.CalledProcessError as e:
            print(e)
            message += f"Failed to install {mpkg_file}\n"

    output.insert(tk.INSERT, message)

def copy_files(src, dest):
    try:
        username = os.getlogin()
        absolute_dest = os.path.abspath(os.path.expanduser(dest))

        if not os.path.exists(src):
            return f"Source folder {src} does not exist. Skipping.\n"

        print(f"Copying from {src} to {absolute_dest}")

        print(f"Source folder permissions: {os.access(src, os.R_OK)}")

        print("Contents of source folder before copy:", os.listdir(src))
        if os.path.exists(absolute_dest):
            print("Contents of destination folder before copy:", os.listdir(absolute_dest))

        mkdir_cmd = ["sudo", "mkdir", "-p", absolute_dest]
        cp_cmd = ["sudo", "cp", "-Rv", f"{src}/.", absolute_dest]
        chown_cmd = ["sudo", "chown", "-R", username, absolute_dest]

        if dest == os.path.expanduser("~/Documents"):
            subprocess.run(mkdir_cmd, check=True)
            result = subprocess.run(cp_cmd, check=True, capture_output=True, text=True)
        else:
            if not os.path.exists(dest):
                subprocess.run(mkdir_cmd, check=True)
            result = subprocess.run(cp_cmd, check=True, capture_output=True, text=True)
            subprocess.run(chown_cmd, check=True)

        print("Copy command output:", result.stdout)
        print("Copy command errors:", result.stderr)

        if os.path.exists(absolute_dest):
            print("Contents of destination folder after copy:", os.listdir(absolute_dest))

        return f"Copied files from {src} to {absolute_dest}\n"
    except subprocess.CalledProcessError as e:
        return str(e) + "\n"
    
    message = ""
    message += copy_files(f"{FOLDER_PATH}/VST", "/Library/Audio/Plug-Ins/VST")
    message += copy_files(f"{FOLDER_PATH}/VST3", "/Library/Audio/Plug-Ins/VST3")
    message += copy_files(f"{FOLDER_PATH}/AU", "/Library/Audio/Plug-Ins/Components")
    message += copy_files(f"{FOLDER_PATH}/AAX", "/Library/Application Support/Avid/Audio/Plug-Ins")
    message += copy_files(f"{FOLDER_PATH}/DOCUMENTS", os.path.expanduser("~/Documents"))

    print(f"FOLDER_PATH is set to {FOLDER_PATH}")

    installer_folder = f"{FOLDER_PATH}/installers"

    for pkg_file in glob.glob(f"{installer_folder}/*.pkg"):
        try:
            subprocess.run(["sudo", "installer", "-pkg", pkg_file, "-target", "/"], check=True)
            message += f"Installed {pkg_file}\n"
        except subprocess.CalledProcessError as e:
            message += str(e) + "\n"

    for mpkg_file in glob.glob(f"{installer_folder}/*.mpkg"):
        try:
            subprocess.run(["sudo", "installer", "-pkg", mpkg_file, "-target", "/"], check=True)
            message += f"Installed {mpkg_file}\n"
        except subprocess.CalledProcessError as e:
            message += str(e) + "\n"

    output.insert(tk.INSERT, message)

# Initialize Tkinter
root = tk.Tk()
root.title('Plugin Installer')

# Folder Path TextBox
folder_path = tk.StringVar()
entry = tk.Entry(root, textvariable=folder_path, width=50)
entry.grid(row=0, column=1)

# Buttons
select_button = tk.Button(root, text='Select Folder', command=select_folder)
select_button.grid(row=0, column=0)

create_structure_button = tk.Button(root, text='Create Folder Structure', command=create_folder_structure)
create_structure_button.grid(row=1, column=0)

execute_button = tk.Button(root, text='Execute Install', command=execute_install)
execute_button.grid(row=1, column=1)

# Output TextBox
output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
output.grid(row=2, columnspan=2)

# Run Tkinter event loop
root.mainloop()
