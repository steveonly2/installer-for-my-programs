import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import requests
import os
import json
import subprocess
import platform

# URLs
GITHUB_REPO_URL = "https://raw.githubusercontent.com/suiyang12/installer-for-my-programs/main/versions.json"
SPEC_READER_URL = "https://raw.githubusercontent.com/suiyang12/e8372383993/main/SpecReader.py"
LATEST_INSTALLER_URL = "https://raw.githubusercontent.com/suiyang12/installer-for-my-programs/main/installer.py"

# Fallback script for basic system specs
FALLBACK_SPECS_SCRIPT = '''
import platform
import psutil

def get_basic_specs():
    try:
        cpu = platform.processor()
        ram = psutil.virtual_memory().total / (1024 ** 3)  # Convert bytes to GB
        gpu = "N/A"  # GPU detection requires additional libraries or tools
        return f"CPU: {cpu}\\nRAM: {ram:.2f} GB\\nGPU: {gpu}"
    except Exception as e:
        return f"Error retrieving specs: {e}"

if __name__ == "__main__":
    print(get_basic_specs())
'''

def is_internet_available():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def get_system_specs():
    try:
        response = requests.get(SPEC_READER_URL)
        spec_reader_script = response.text
        with open("SpecReader.py", "w") as file:
            file.write(spec_reader_script)
        
        # Execute the script and capture its output
        result = subprocess.run(['python', 'SpecReader.py'], capture_output=True, text=True)
        os.remove("SpecReader.py")  # Clean up
        return result.stdout
    except requests.RequestException:
        return get_fallback_specs()

def get_fallback_specs():
    with open("fallback_specs.py", "w") as file:
        file.write(FALLBACK_SPECS_SCRIPT)
    
    # Execute the fallback script and capture its output
    result = subprocess.run(['python', 'fallback_specs.py'], capture_output=True, text=True)
    os.remove("fallback_specs.py")  # Clean up
    return result.stdout

def get_latest_version_info():
    try:
        response = requests.get(GITHUB_REPO_URL)
        response.raise_for_status()
        version_info = response.json()
        return version_info
    except requests.RequestException as e:
        print(f"Error fetching version info: {e}")
        return {}

def download_file(url, dest_folder, progress_callback=None):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    response = requests.get(url, stream=True)
    file_name = url.split('/')[-1]
    file_path = os.path.join(dest_folder, file_name)
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0
    
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            downloaded_size += len(chunk)
            if progress_callback:
                progress_callback(downloaded_size, total_size)
    
    return file_path

def show_info(title, message):
    messagebox.showinfo(title, message)

def on_download_complete(file_name):
    specs = get_system_specs()
    show_info("Download Complete", f"{file_name} downloaded successfully!\n\nSystem Specifications:\n{specs}")

def download_program(url, dest_folder):
    def update_progress(downloaded_size, total_size):
        progress = (downloaded_size / total_size) * 100
        progress_var.set(progress)
        progress_label.config(text=f"Downloading... {int(progress)}%")
        root.update_idletasks()

    download_window = Toplevel(root)
    download_window.title("Downloading")
    download_window.geometry("300x150")
    
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(download_window, variable=progress_var, maximum=100, length=250)
    progress_bar.pack(pady=20)
    
    progress_label = tk.Label(download_window, text="Downloading... 0%")
    progress_label.pack()
    
    file_path = download_file(url, os.getcwd(), update_progress)
    download_window.destroy()
    
    file_name = os.path.basename(file_path)
    on_download_complete(file_name)

def update_installer_if_needed(current_version):
    version_info = get_latest_version_info()
    if version_info:
        latest_version = version_info.get("latest_version", "")
        if latest_version != current_version:
            show_info("Update Available", "A new version of the installer is available. Downloading now...")
            download_file(LATEST_INSTALLER_URL, os.getcwd())
            show_info("Update Complete", "The installer has been updated. Please restart the application.")
            exit()

def show_credits():
    credits_window = Toplevel(root)
    credits_window.title("Credits")
    credits_window.geometry("300x150")
    
    tk.Label(credits_window, text="Credits", font=("Arial", 16)).pack(pady=10)
    tk.Label(credits_window, text="Steveonly", font=("Arial", 12)).pack(pady=10)
    tk.Button(credits_window, text="Close", command=credits_window.destroy).pack(pady=10)

def create_gui():
    global root
    root = tk.Tk()
    root.title("Steve's Installer")
    root.geometry("600x400")
    root.resizable(False, False)

    # Check for internet
    if not is_internet_available():
        show_info("Internet Not Found", "Internet Not Found - Switching to Manual.")
        return

    # Check for updates
    current_version = "1.0.0"  # Replace with your current version
    update_installer_if_needed(current_version)

    # Layout
    tk.Label(root, text="Steve's Installer", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Download Repacker", command=lambda: download_program("https://raw.githubusercontent.com/suiyang12/e8372383993/main/repacker.py", os.getcwd())).pack(side=tk.LEFT, padx=10)
    tk.Button(root, text="Download RoGui", command=lambda: download_program("https://raw.githubusercontent.com/suiyang12/e8372383993/main/roguiv2.0.py", os.getcwd())).pack(side=tk.LEFT, padx=10)
    tk.Button(root, text="Download AutoPinger", command=lambda: download_program("https://raw.githubusercontent.com/suiyang12/e8372383993/main/AutoPinger.py", os.getcwd())).pack(side=tk.LEFT, padx=10)
    
    tk.Button(root, text="Show Credits", command=show_credits).pack(pady=10)
    tk.Button(root, text="Go to GitHub", command=lambda: os.startfile("https://github.com/suiyang12")).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
