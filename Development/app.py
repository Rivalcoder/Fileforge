import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Notebook
import subprocess
import os
import shutil
import zipfile
import threading
import time

# Function Definitions

def browse_source():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder_selected)

def browse_destination():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        dest_entry.delete(0, tk.END)
        dest_entry.insert(0, folder_selected)

def update_log(text):
    log_text.insert(tk.END, text + "\n")
    log_text.yview(tk.END)

def stop_task():
    global stop_thread
    stop_thread = True
    status_text.set("Task stopped.")

def run_robocopy():
    notebook.select(log_tab)
    thread = threading.Thread(target=run_robocopy_in_background)
    thread.start()

def run_robocopy_in_background():
    global stop_thread
    stop_thread = False
    source = source_entry.get().strip()
    destination = dest_entry.get().strip()
    selected_excludes = [key for key, var in exclude_vars.items() if var.get()]
    custom_exclude = custom_exclude_entry.get().strip()
    if custom_exclude:
        selected_excludes.extend([x.strip() for x in custom_exclude.split(',') if x.strip()])

    if not os.path.exists(source) or not os.path.exists(destination):
        update_log("Error: Source or destination folder doesn't exist.")
        return

    command = ["robocopy", source, destination, "/E", "/MT:8"]
    if selected_excludes:
        command += ["/XD"] + selected_excludes

    update_log(f"🧳 Starting copy from {source} to {destination}...")

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        for line in process.stdout:
            update_log(line.strip())
            app.update_idletasks()
            if stop_thread:
                process.terminate()
                update_log("🛑 Copy stopped.")
                status_text.set("Copy stopped.")
                break
        process.wait()
        if not stop_thread:
            status_text.set("Copy complete.")
    except Exception as e:
        status_text.set("Error during copy.")
        messagebox.showerror("Error", str(e))

def extract_zip():
    file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
    extract_to = dest_entry.get().strip()
    if not file_path or not extract_to:
        messagebox.showerror("Error", "Select both a ZIP file and destination.")
        return
    thread = threading.Thread(target=extract_zip_in_background, args=(file_path, extract_to))
    thread.start()

def extract_zip_in_background(file_path, extract_to):
    global stop_thread
    stop_thread = False
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            files = zip_ref.infolist()
            total = len(files)
            start_time = time.time()

            update_log(f"📦 Extracting ZIP file: {file_path} to {extract_to}")

            for i, zf in enumerate(files):
                if stop_thread:
                    update_log("⛔ Extraction stopped.")
                    status_text.set("Extraction stopped.")
                    break
                zip_ref.extract(zf, extract_to)
                if (i + 1) % 10 == 0 or (time.time() - start_time) > 1:
                    elapsed = time.time() - start_time
                    update_log(f"Progress: {i + 1}/{total} files extracted in {elapsed:.2f} seconds")
            elapsed = time.time() - start_time
            update_log(f"✅ Finished extracting ZIP file in {elapsed:.2f} seconds.")
            status_text.set("ZIP extracted successfully.")
    except Exception as e:
        update_log(f"❌ Extraction failed: {e}")
        status_text.set("Extraction failed.")

def open_in_explorer():
    folder = source_entry.get().strip()
    if os.path.exists(folder):
        os.startfile(folder)
    else:
        messagebox.showerror("Error", "Source folder does not exist.")

def clean_node_modules():
    root = source_entry.get().strip()
    if not root:
        messagebox.showerror("Error", "No source folder selected.")
        return
    thread = threading.Thread(target=clean_node_modules_in_background, args=(root,))
    thread.start()

def clean_node_modules_in_background(root):
    global stop_thread
    stop_thread = False
    deleted = 0
    start_time = time.time()

    update_log(f"🧹 Cleaning node_modules folders in {root}...")

    try:
        for dirpath, dirnames, _ in os.walk(root):
            if stop_thread:
                update_log("⛔ Cleaning stopped.")
                status_text.set("Cleaning stopped.")
                break
            if "node_modules" in dirnames:
                full_path = os.path.join(dirpath, "node_modules")
                shutil.rmtree(full_path)
                deleted += 1
                if deleted % 10 == 0 or (time.time() - start_time) > 1:
                    elapsed = time.time() - start_time
                    update_log(f"Progress: {deleted} node_modules folders deleted in {elapsed:.2f} seconds")

        elapsed = time.time() - start_time
        update_log(f"✅ Cleaned {deleted} node_modules folders in {elapsed:.2f} seconds.")
        status_text.set(f"Deleted {deleted} node_modules folders.")
    except Exception as e:
        status_text.set("Clean failed.")
        update_log(f"❌ Clean failed: {e}")

def clear_log():
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "Log cleared.\n")

def select_all_excludes():
    for var in exclude_vars.values():
        var.set(True)
    update_log("All exclude options selected.")

def deselect_all_excludes():
    for var in exclude_vars.values():
        var.set(False)
    update_log("All exclude options deselected.")

# GUI Setup
app = tk.Tk()
app.title("File Utility Tool")
app.geometry("800x600")  # Reduced default window size
app.minsize(600, 400)  # Reduced minimum window size
app.configure(bg="#f0f2f5")

# Modern style configuration
style = {
    "background_color": "#f0f2f5",
    "button_color": "#4a90e2",
    "button_hover": "#357abd",
    "label_color": "#2c3e50",
    "text_color": "#34495e",
    "entry_bg_color": "#ffffff",
    "frame_bg": "#ffffff",
    "border_color": "#e1e4e8"
}

# Configure ttk styles
ttk_style = ttk.Style()
ttk_style.configure("Custom.TNotebook", background=style["background_color"])
ttk_style.configure("Custom.TNotebook.Tab", padding=[10, 5], background=style["frame_bg"])
ttk_style.map("Custom.TNotebook.Tab",
    background=[("selected", style["button_color"])],
    foreground=[("selected", "white")])

# Create main container with padding
main_container = tk.Frame(app, bg=style["background_color"])
main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Reduced padding

# Create main canvas with scrollbar
main_canvas = tk.Canvas(main_container, bg=style["background_color"], highlightthickness=0)
main_scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas, bg=style["background_color"])

def configure_scroll_region(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scroll_region)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=main_canvas.winfo_width())
main_canvas.configure(yscrollcommand=main_scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
main_scrollbar.pack(side="right", fill="y")

# Bind mouse wheel to scroll
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Create notebook with custom style
notebook = Notebook(scrollable_frame, style="Custom.TNotebook")
notebook.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

# Default exclude folders list
default_exclude_folders = [
    "node_modules", ".git", "dist", "__pycache__", "build", ".idea", ".vscode",
    "venv", "env", ".env", ".next", ".parcel-cache", ".turbo", "target", "out",
    "android", "ios", ".gradle", ".cxx", ".expo", ".angular", "Pods",
    "DerivedData", ".sass-cache"
]

exclude_vars = {}

# Tabs
file_operations_tab = tk.Frame(notebook, bg=style["frame_bg"])
notebook.add(file_operations_tab, text="File Operations")

log_tab = tk.Frame(notebook, bg=style["frame_bg"])
notebook.add(log_tab, text="Log")

# Create styled frames for better organization
def create_styled_frame(parent, title):
    frame = tk.Frame(parent, bg=style["frame_bg"], padx=15, pady=15)
    if title:
        tk.Label(frame, text=title, font=("Segoe UI", 12, "bold"), 
                bg=style["frame_bg"], fg=style["label_color"]).pack(anchor="w", pady=(0, 10))
    return frame

# Source and Destination Section
paths_frame = create_styled_frame(file_operations_tab, "Source and Destination")
paths_frame.pack(fill=tk.X, pady=(0, 10))  # Reduced padding

# Source
source_frame = tk.Frame(paths_frame, bg=style["frame_bg"])
source_frame.pack(fill=tk.X, pady=2)  # Reduced padding
tk.Label(source_frame, text="Source Folder:", bg=style["frame_bg"], 
         fg=style["label_color"]).pack(side=tk.LEFT, padx=(0, 5))  # Reduced padding
source_entry = tk.Entry(source_frame, width=50)  # Reduced width
source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))  # Reduced padding
tk.Button(source_frame, text="Browse", command=browse_source, 
          bg=style["button_color"], fg="white", relief=tk.FLAT).pack(side=tk.LEFT)

# Destination
dest_frame = tk.Frame(paths_frame, bg=style["frame_bg"])
dest_frame.pack(fill=tk.X, pady=2)  # Reduced padding
tk.Label(dest_frame, text="Destination Folder:", bg=style["frame_bg"], 
         fg=style["label_color"]).pack(side=tk.LEFT, padx=(0, 5))  # Reduced padding
dest_entry = tk.Entry(dest_frame, width=50)  # Reduced width
dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))  # Reduced padding
tk.Button(dest_frame, text="Browse", command=browse_destination, 
          bg=style["button_color"], fg="white", relief=tk.FLAT).pack(side=tk.LEFT)

# Exclude folders section
exclude_frame = create_styled_frame(file_operations_tab, "Exclude Folders")
exclude_frame.pack(fill=tk.X, pady=(0, 10))

# Custom exclude entry
custom_frame = tk.Frame(exclude_frame, bg=style["frame_bg"])
custom_frame.pack(fill=tk.X, pady=(0, 5))
tk.Label(custom_frame, text="Custom Exclude (comma-separated):", 
         bg=style["frame_bg"], fg=style["label_color"]).pack(side=tk.LEFT, padx=(0, 5))
custom_exclude_entry = tk.Entry(custom_frame, width=50)
custom_exclude_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Add Select All/Deselect All buttons
select_buttons_frame = tk.Frame(exclude_frame, bg=style["frame_bg"])
select_buttons_frame.pack(fill=tk.X, pady=(0, 5))

select_all_btn = tk.Button(select_buttons_frame, text="Select All", 
                          command=select_all_excludes,
                          bg=style["button_color"], fg="white", 
                          relief=tk.FLAT, padx=10, pady=2)
select_all_btn.pack(side=tk.LEFT, padx=(0, 5))

deselect_all_btn = tk.Button(select_buttons_frame, text="Deselect All", 
                            command=deselect_all_excludes,
                            bg=style["button_color"], fg="white", 
                            relief=tk.FLAT, padx=10, pady=2)
deselect_all_btn.pack(side=tk.LEFT)

# Checkboxes frame
checkbox_frame = tk.Frame(exclude_frame, bg=style["frame_bg"])
checkbox_frame.pack(fill=tk.X)

# Calculate number of columns based on 5 rows
num_columns = (len(default_exclude_folders) + 4) // 5  # Ceiling division to ensure 5 rows

# Display checkboxes in a grid layout
for idx, folder in enumerate(default_exclude_folders):
    var = tk.BooleanVar(value=False)
    exclude_vars[folder] = var
    chk = tk.Checkbutton(checkbox_frame, text=folder, variable=var, 
                        bg=style["frame_bg"], fg=style["text_color"],
                        selectcolor=style["button_color"])
    row = idx % 5  # 5 rows
    col = idx // 5  # Calculate column
    chk.grid(row=row, column=col, sticky='w', padx=5, pady=2)

# Configure grid columns to be equal width
for i in range(num_columns):
    checkbox_frame.grid_columnconfigure(i, weight=1)

# Buttons section
buttons_frame = create_styled_frame(file_operations_tab, "Actions")
buttons_frame.pack(fill=tk.X, pady=(0, 10))  # Reduced padding

# Style for buttons
button_style = {
    "bg": style["button_color"],
    "fg": "white",
    "relief": tk.FLAT,
    "padx": 10,  # Reduced padding
    "pady": 5,   # Reduced padding
    "width": 15  # Reduced width
}

# Create buttons with consistent styling
tk.Button(buttons_frame, text="🔄 Copy Files", command=run_robocopy, **button_style).pack(pady=2)  # Reduced padding
tk.Button(buttons_frame, text="📦 Extract ZIP File", command=extract_zip, **button_style).pack(pady=2)  # Reduced padding
tk.Button(buttons_frame, text="🧹 Clean node_modules", command=clean_node_modules, **button_style).pack(pady=2)  # Reduced padding
tk.Button(buttons_frame, text="📁 Open in Explorer", command=open_in_explorer, **button_style).pack(pady=2)  # Reduced padding
tk.Button(buttons_frame, text="⛔ Stop Current Task", command=stop_task, **button_style).pack(pady=2)  # Reduced padding

# Status bar
status_frame = tk.Frame(file_operations_tab, bg=style["frame_bg"], height=25)  # Reduced height
status_frame.pack(fill=tk.X, pady=(5, 0))  # Reduced padding
status_text = tk.StringVar(value="Ready")
tk.Label(status_frame, textvariable=status_text, bg=style["frame_bg"], 
         fg=style["label_color"]).pack(side=tk.LEFT)

# Log Tab
log_frame = tk.Frame(log_tab, bg=style["frame_bg"])
log_frame.pack(expand=True, fill=tk.BOTH)

log_scrollbar = ttk.Scrollbar(log_frame)
log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

log_text = tk.Text(log_frame, wrap=tk.WORD, yscrollcommand=log_scrollbar.set,
                   bg=style["entry_bg_color"], fg=style["text_color"],
                   font=("Consolas", 9))  # Reduced font size
log_text.pack(expand=True, fill=tk.BOTH)
log_scrollbar.config(command=log_text.yview)

tk.Button(log_tab, text="🧼 Clear Log", command=clear_log, 
          bg=style["button_color"], fg="white", relief=tk.FLAT,
          padx=10, pady=5).pack(pady=5)  # Reduced padding

# Update the canvas width when the window is resized
def update_canvas_width(event):
    main_canvas.itemconfig(main_canvas.find_withtag("all")[0], width=event.width)
    main_canvas.configure(width=event.width)

main_canvas.bind("<Configure>", update_canvas_width)

# Start GUI
app.mainloop()
