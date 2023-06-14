import os
import re
import subprocess
import configparser
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog, simpledialog
from pdfreader import SimplePDFViewer
from shutil import rmtree
from tempfile import mkdtemp
from pdfminer.high_level import extract_text
from elevenlabs import set_api_key, voices, generate, Voice, is_voice_id

CONFIG_FILE = 'PDF2Speech_config.ini'
CHUNK_SIZE = 5000

config = configparser.ConfigParser()

if not os.path.exists(CONFIG_FILE):
    API_KEY = simpledialog.askstring('API Key', 'Enter your ElevenLabs API key:')
    config['DEFAULT'] = {'API_KEY': API_KEY}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
else:
    config.read(CONFIG_FILE)
    API_KEY = config.get('DEFAULT', 'API_KEY')

set_api_key(API_KEY)

# Initialization of the text variable
text = ''

def fetch_voices():
    return {voice.name: voice.id for voice in voices()}


def fetch_models():
    return [
        {
            "model_id": "eleven_monolingual_v1",
            "description": "This model supports English language."
        },
        {
            "model_id": "eleven_multilingual_v1",
            "description": "This model supports multiple languages including English, German, Polish, Spanish, Italian, French, Portuguese, and Hindi."
        }
    ]

def combine_audio_files(file_paths, output_path):
    input_files_str = "|".join(file_paths)
    command = f"ffmpeg -i 'concat:{input_files_str}' -c copy {output_path}"
    subprocess.call(command, shell=True)

def generate_audio():
    # Use the global text variable
    global text
    selected_voice_name = voice_var.get()
    selected_model = model_var.get()

    # Check if selected voice is voice_id or voice name
    voice = selected_voice_name if is_voice_id(selected_voice_name) else next((v for v in voices() if v.name == selected_voice_name), None)
    if not voice:
        raise ValueError(f"Voice '{selected_voice_name}' not found.")

    # Split the text into chunks.
    chunks = [text[i: i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
    
    # Create a temporary directory for storing chunks
    tmp_dir = mkdtemp()
    file_paths = []
    total_chunks = len(chunks)
    for i, chunk in enumerate(chunks):
        # Update the status text with the progress percentage.
        progress = round((i / total_chunks) * 100, 2)
        status_label.config(text=f"Processing voice for chunk {i+1} of {total_chunks} - {progress}% complete")

        # Generate the audio for this chunk of text.
        audio = generate(chunk, voice=voice, model=selected_model)

        # Save the audio to a temporary file.
        file_path = f"{tmp_dir}/chunk_{i+1}.mp3"
        with open(file_path, 'wb') as f:
            f.write(audio)
        file_paths.append(file_path)

    # Combine all audio files into one.
    combined_file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
    if combined_file_path: # If a file path is provided (i.e., the user didn't cancel the dialog)
        combine_audio_files(file_paths, combined_file_path)

    # Delete the temporary directory and its contents.
    rmtree(tmp_dir)

    # Update the status text.
    status_label.config(text=f"Finished generating voice")


def load_pdf():
    global text
    pdf_path = filedialog.askopenfilename()
    text = extract_text(pdf_path)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Replace any occurrence of more than one space with a single space.
    text = re.sub(r" +", " ", text)

    # Replace any occurrence of more than one newline with a single newline.
    text = re.sub(r"\n+", "\n", text)

    # Save the extracted text to a .txt file on the desktop.
    with open(os.path.expanduser("~/Desktop/extracted_text.txt"), "w") as f:
        f.write(text)
    
    # Set a status message instead of changing the button text.
    status_text.set("Finished loading PDF")


def save(audio):
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
    if file_path:  # If a file path is provided (i.e., the user didn't cancel the dialog)
        with open(file_path, 'wb') as f:
            f.write(audio)


root = tk.Tk()
root.geometry('250x625')
root.configure(bg='#da3467')

open_file_btn = tk.Button(root, text="Open PDF", command=load_pdf, bg='#ffa49a', fg='#35333f')
open_file_btn.pack(pady=10)

tk.Label(root, text='Select Voice', bg='#ffa49a', fg='black').pack()
voice_var = tk.StringVar(root)
voice_options = [voice.name for voice in voices()]
voice_dropdown = tk.OptionMenu(root, voice_var, *voice_options)
voice_dropdown.pack(pady=10)

tk.Label(root, text='Select Model', bg='#ffa49a', fg='black').pack()
model_var = tk.StringVar(root)
model_options = [model["model_id"] for model in fetch_models()]
model_dropdown = tk.OptionMenu(root, model_var, *model_options)
model_dropdown.pack(pady=10)

tk.Label(root, text='Stability', bg='#ffa49a', fg='black').pack()
stability_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", bg='#ffa49a', troughcolor='#35333f')  
stability_scale.pack(pady=10)

tk.Label(root, text='Similarity Boost', bg='#ffa49a', fg='black').pack()
similarity_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", bg='#ffa49a', troughcolor='#35333f')  
similarity_scale.pack(pady=10)

generate_btn = tk.Button(root, text="Generate Audio", command=generate_audio, bg='#ffa49a', fg='#35333f')
generate_btn.pack(pady=10)

status_text = tk.StringVar(root, value="Ready")
status_label = tk.Label(root, textvariable=status_text, bg='#ffa49a', fg='black')
status_label.pack(pady=10)

root.mainloop()
