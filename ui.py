import tkinter as tk
from tkinter import ttk

from tkinterdnd2 import DND_FILES, TkinterDnD



def init_window(on_file_dropped):
    root = TkinterDnD.Tk()
    window_design(root, on_file_dropped)
    # create_drop_area(root, on_file_dropped)
    return root


def create_drop_area(root, on_file_dropped):
    drop_area = tk.Frame(
        root,
        height=250,
        width=500,
        bg="#ffffff",
        relief="flat",
        bd=0,
        padx=3,
        pady=3,highlightbackground="DarkBlue", highlightthickness=1
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

    return label_status,drop_area


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
    progress = ttk.Progressbar(win, orient="horizontal", length=500, mode="indeterminate")
    progress.pack(pady=150)
    progress.start()
    return win


def center_window(window, width, height):
    window.update_idletasks()

    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

def original_window(root, on_file_dropped):
    label = tk.Label(root, text="Kill Bill", bg="gray97", fg="DarkBlue", font=("Georgia", 72, "bold"), width=20)
    label.pack(pady=5)

    subtext = tk.Label(root,
                       text="If you think a mistake has been made with your bill,\nor even if you want to understand your bill better"
                            "\nall you need is to upload the PDF bill and we will do the rest :)", bg="gray97", fg="DarkBlue", font=("Ariel", 14))
    subtext.pack()

    drop_area = create_drop_area(root, on_file_dropped)


def window_design(root, on_file_dropped):
    root.title("Kill Bill")
    root.geometry("700x700")
    root.configure(bg="gray97")
    root.resizable(False, False)  # שינוי גודל החלון לא אפשרי
    center_window(root,700,500)

    original_window(root, on_file_dropped)