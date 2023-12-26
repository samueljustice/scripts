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
    target_folder = os.path.join(base_folder, "SweejHelperPluginInstaller")
    subfolders = ["AAX", "DOCUMENTS", "INSTALLERS", "VST", "VST3"]

    os.makedirs(target_folder, exist_ok=True)
    for subfolder in subfolders:
        os.makedirs(os.path.join(target_folder, subfolder), exist_ok=True)

def execute_install():
    FOLDER_PATH = folder_path.get()
    output.delete(1.0, tk.END)

    message = ""
    # Update these paths according to the specific requirements of the plugins
    message += copy_files(f"{FOLDER_PATH}/VST", "C:/Program Files/VSTPlugins")
    message += copy_files(f"{FOLDER_PATH}/VST3", "C:/Program Files/Common Files/VST3")
    message += copy_files(f"{FOLDER_PATH}/AAX", "C:/Program Files/Common Files/Avid/Audio/Plug-Ins")
    message += copy_files(f"{FOLDER_PATH}/DOCUMENTS", os.path.expanduser("~/Documents"))  # Copying documents

    installer_folder = f"{FOLDER_PATH}/INSTALLERS"

    # Handling .exe files
    for exe_file in glob.glob(f"{installer_folder}/*.exe"):
        try:
            subprocess.run([exe_file], check=True)
            message += f"Installed {exe_file}\n"
        except subprocess.CalledProcessError as e:
            message += f"Failed to install {exe_file}\n"

    # Handling .msi files
    for msi_file in glob.glob(f"{installer_folder}/*.msi"):
        try:
            subprocess.run(["msiexec", "/i", msi_file], check=True)
            message += f"Installed {msi_file}\n"
        except subprocess.CalledProcessError as e:
            message += f"Failed to install {msi_file}\n"

    output.insert(tk.INSERT, message)

def copy_files(src, dest):
    try:
        if not os.path.exists(src):
            return f"Source folder {src} does not exist. Skipping.\n"

        print(f"Copying from {src} to {dest}")

        if not os.path.exists(dest):
            os.makedirs(dest, exist_ok=True)

        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dest_path = os.path.join(dest, item)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dest_path)

        return f"Copied files from {src} to {dest}\n"
    except Exception as e:
        return str(e) + "\n"

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
