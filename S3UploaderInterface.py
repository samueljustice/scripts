"""
S3Uploader GUI

This Python script provides a graphical user interface (GUI) for the S3Uploader app.
The user interface is built using Tkinter, a standard Python interface to the Tk GUI toolkit.

The GUI provides input fields for selecting the location of the S3Uploader app and the input and output directories.
For each argument of the S3Uploader app, the GUI provides a dropdown menu to select between 'Yes' or 'No'.

The 'Browse...' buttons allow for file system navigation to select directories.

After selecting all necessary information, pressing the 'Run' button will run the S3Uploader app with the provided arguments.

Styling:
Background color is #494d7e
Text color is #f2d3ab
Text font is Courier, size 12
Button color is #8b6d9c
Button text color is #8b6d9c
Text field background color is #8b6d9c
Text field text color is #f2d3ab

Written by: Samuel Justice
Date: 16th July 2023
"""


import tkinter as tk
from tkinter import filedialog
import subprocess
from tkinter import font as tkfont

def select_app_directory():
    filename = filedialog.askdirectory()
    e0.delete(0, tk.END)
    e0.insert(0, filename)

def select_input_directory():
    filename = filedialog.askdirectory()
    e1.delete(0, tk.END)
    e1.insert(0, filename)

def select_output_directory():
    filename = filedialog.askdirectory()
    e2.delete(0, tk.END)
    e2.insert(0, filename)

def run_s3uploader():
    cmd = [
        f"{e0.get()}/Contents/MacOS/S3Uploader",
        "--in", e1.get(),
        "--out", e2.get(),
        "--hog", '1' if v_hog.get() == 'Yes' else '0',
        "--loudness", '1' if v_loudness.get() == 'Yes' else '0',
        "--analysis", '1' if v_analysis.get() == 'Yes' else '0',
        "--skip", '1' if v_skip.get() == 'Yes' else '0',
    ]
    subprocess.run(cmd)

root = tk.Tk()
root.title("S3Uploader Interface")

# Styling
root.configure(bg='#494d7e')
stylish_font = tkfont.Font(family="Courier", size=12)

# Variables for holding dropdown options
v_hog = tk.StringVar(root)
v_loudness = tk.StringVar(root)
v_analysis = tk.StringVar(root)
v_skip = tk.StringVar(root)

# Default values for the dropdowns
v_hog.set("Yes")
v_loudness.set("Yes")
v_analysis.set("Yes")
v_skip.set("No")

options = ["Yes", "No"]  # The options in the dropdown

labels = ['S3Uploader App Location:', 'Input Directory:', 'Output Directory:', 'Hog CPU:', 'Calculate Loudness:', 'Spectral Analysis:', 'Skip Existing:']
for i, label in enumerate(labels):
    lbl = tk.Label(root, text=label, bg='#494d7e', fg='#f2d3ab', font=stylish_font)
    lbl.grid(row=i, column=0, sticky='w')

e0 = tk.Entry(root, bg='#8b6d9c', fg='#f2d3ab', insertbackground='#f2d3ab')
e0.insert(0, '/Volumes/S3Uploader/S3Uploader.app')
e1 = tk.Entry(root, bg='#8b6d9c', fg='#f2d3ab', insertbackground='#f2d3ab')
e2 = tk.Entry(root, bg='#8b6d9c', fg='#f2d3ab', insertbackground='#f2d3ab')

e0.grid(row=0, column=1)
e1.grid(row=1, column=1)
e2.grid(row=2, column=1)

tk.OptionMenu(root, v_hog, *options).grid(row=3, column=1)
tk.OptionMenu(root, v_loudness, *options).grid(row=4, column=1)
tk.OptionMenu(root, v_analysis, *options).grid(row=5, column=1)
tk.OptionMenu(root, v_skip, *options).grid(row=6, column=1)

# Buttons for directory selection
browse_button0 = tk.Button(root, text="Browse...", command=select_app_directory, fg='#8b6d9c')
browse_button0.grid(row=0, column=2)

browse_button1 = tk.Button(root, text="Browse...", command=select_input_directory, fg='#8b6d9c')
browse_button1.grid(row=1, column=2)

browse_button2 = tk.Button(root, text="Browse...", command=select_output_directory, fg='#8b6d9c')
browse_button2.grid(row=2, column=2)

run_button = tk.Button(root, text='Run', command=run_s3uploader, fg='#8b6d9c')
run_button.grid(row=7, column=0, columnspan=2)

root.mainloop()
