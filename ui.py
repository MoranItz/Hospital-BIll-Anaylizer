import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

def center_window(window, width, height):
    window.update_idletasks()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def init_window(on_file_dropped):
    root = TkinterDnD.Tk()
    root.title("Hospital Bill Analyzer")
    center_window(root, 700, 500)
    root.configure(bg="#f4f7fb")

    tk.Label(
        root,
        text="Hospital Bill Analyzer",
        font=("Helvetica", 25, "bold"),
        fg="#17324d",
        bg="#f4f7fb"
    ).pack(pady=(28, 4))
    tk.Label(
        root,
        text="Upload a hospital bill to review its charges",
        font=("Helvetica", 11),
        fg="#607286",
        bg="#f4f7fb"
    ).pack()

    create_drop_area(root, on_file_dropped)
    return root


def create_drop_area(root, on_file_dropped):
    drop_area = tk.Frame(
        root,
        height=250,
        width=500,
        bg="#d7e6f2",
        relief="flat",
        bd=0,
        padx=3,
        pady=3
    )
    drop_area.pack(side="bottom", padx=20, pady=35)
    drop_area.pack_propagate(False)

    label_status = tk.Label(
        drop_area,
        text="Drag & Drop Your File Here\n\nPDF files only",
        font=("Helvetica", 16, "bold"),
        fg="#17324d",
        bg="#ffffff",
        relief="flat",
        bd=0
    )
    label_status.pack(fill="both", expand=True)
    label_status.drop_target_register(DND_FILES)

    label_status.dnd_bind(
        '<<Drop>>',
        lambda event: handle_drop(event, on_file_dropped)
    )
    return label_status


def handle_drop(event, on_file_dropped):
    file_path = event.data
    if file_path:
        file_path = file_path.strip('{}')  # Remove curly braces if present
        on_file_dropped(file_path)


def show_loading_dots(parent=None):
    win = tk.Toplevel(parent) if parent else tk.Tk()
    win.title("Receipt Review")
    center_window(win, 700, 500)
    win.resizable(False, False)
    if parent:
        win.transient(parent)
        win.lift()

    label = tk.Label(
        win,
        text="Wait for receipt review to load",
        font=("Helvetica", 16)
    )
    label.pack(expand=True)
    return win

