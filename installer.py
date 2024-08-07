import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import os

# Define the URLs for the files
AUTO_PINGER_URL = 'https://github.com/suiyang12/Workout-Helper-V1.0/raw/main/AutoPinger.py'
REPACKER_URL = 'https://raw.githubusercontent.com/suiyang12/e8372383993/main/repacker.py'
ROGUI_URL = 'https://raw.githubusercontent.com/suiyang12/e8372383993/main/roguiv2.0.py'

def download_file(url, local_path):
    """Download file from a URL and save it locally."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        with open(local_path, 'wb') as file:
            file.write(response.content)
        messagebox.showinfo("Success", f"Downloaded {os.path.basename(local_path)} successfully!\nSaved to: {local_path}")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to download file: {e}")

def on_download_click(url, file_name):
    """Handle the download button click event."""
    folder_selected = filedialog.askdirectory(title="Select Folder")
    if folder_selected:
        local_path = os.path.join(folder_selected, file_name)
        download_file(url, local_path)

def show_info(info_text):
    """Display an information message box."""
    messagebox.showinfo("Information", info_text)

def create_gui():
    """Create and display the GUI."""
    root = tk.Tk()
    root.title("Program Installer")

    # Create a label
    label = tk.Label(root, text="Choose a program to download:", font=("Arial", 16))
    label.pack(pady=20)

    # Create a button to download AutoPinger
    download_autopinger_button = tk.Button(root, text="Download AutoPinger.py", font=("Arial", 14),
                                           command=lambda: on_download_click(AUTO_PINGER_URL, 'AutoPinger.py'))
    download_autopinger_button.pack(pady=10, side=tk.LEFT, padx=20)

    # Add a question mark icon next to AutoPinger button using text
    autopinger_info_button = tk.Button(root, text="❓", font=("Arial", 14), command=lambda: show_info(
        "AutoPinger.py: A script for ping automation. It allows you to manage pings efficiently."))
    autopinger_info_button.pack(pady=10, side=tk.LEFT)

    # Create a button to download repacker.py
    download_repacker_button = tk.Button(root, text="Download repacker.py", font=("Arial", 14),
                                         command=lambda: on_download_click(REPACKER_URL, 'repacker.py'))
    download_repacker_button.pack(pady=10, side=tk.LEFT, padx=20)

    # Add a question mark icon next to repacker.py button using text
    repacker_info_button = tk.Button(root, text="❓", font=("Arial", 14), command=lambda: show_info(
        "repacker.py: A script for packing and unpacking files. It helps in managing file storage and distribution."))
    repacker_info_button.pack(pady=10, side=tk.LEFT)

    # Create a button to download roguiv2.0.py
    download_ro_gui_button = tk.Button(root, text="Download roguiv2.0.py", font=("Arial", 14),
                                       command=lambda: on_download_click(ROGUI_URL, 'roguiv2.0.py'))
    download_ro_gui_button.pack(pady=10, side=tk.LEFT, padx=20)

    # Add a question mark icon next to roguiv2.0.py button using text
    ro_gui_info_button = tk.Button(root, text="❓", font=("Arial", 14), command=lambda: show_info(
        "roguiv2.0.py: Contains an autoclicker and an AFK mode for Roblox. Useful for automating tasks in Roblox."))
    ro_gui_info_button.pack(pady=10, side=tk.LEFT)

    # Run the GUI loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
