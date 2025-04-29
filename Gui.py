import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import os
import shutil
import config

class LabelingToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Labeling & Annotation Tool (YOLOv11)")
        self.root.geometry("900x750")
        self.root.configure(bg="#ECEFF1")

        self.primary_color = "#1976D2"
        self.button_fg = "#FFFFFF"
        self.button_font = ("Segoe UI", 12, "bold")
        self.title_font = ("Segoe UI", 28, "bold")

        self.folder_path = ""

        self.setup_ui()

    def setup_ui(self):
        # Top frame (Logo + Title)
        top_frame = tk.Frame(self.root, bg="#ECEFF1")
        top_frame.pack(pady=10)

        self.load_logo(top_frame)

        title = tk.Label(top_frame, text="Welcome to TiHAN Labeling Tool", font=self.title_font, bg="#ECEFF1", fg="#0D47A1")
        title.pack(pady=10)

        # Middle Frame (Terminal)
        middle_frame = tk.Frame(self.root, bg="#ECEFF1")
        middle_frame.pack(pady=20, expand=True, fill="both")

        terminal_label = tk.Label(middle_frame, text="Terminal Output", font=("Segoe UI", 18, "bold"), bg="#ECEFF1", fg="#37474F")
        terminal_label.pack(pady=5)

        self.terminal = tk.Text(middle_frame, height=55, width=10, bg="#263238", fg="#ECEFF1", font=("Consolas", 8), bd=0)
        self.terminal.pack(padx=500, pady=10, fill="both", expand=False)
        self.terminal.configure(state='disabled')

        # Bottom Frame (Buttons)
        bottom_frame = tk.Frame(self.root, bg="#ECEFF1")
        bottom_frame.pack(side="bottom", pady=20)

        self.create_custom_button(bottom_frame, "Select Images Folder", self.select_folder)
        self.create_custom_button(bottom_frame, "Auto Generate Labels (YOLOv11)", self.generate_labels)
        self.create_custom_button(bottom_frame, "Add Classes File", self.add_classes_file)
        self.create_custom_button(bottom_frame, "Open LabelImg", self.open_labelimg)

    def load_logo(self, parent):
        try:
            logo = Image.open(config.LOGO_PATH).convert("RGBA")
            logo = logo.resize((320, 160))
            self.logo_img = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(parent, image=self.logo_img, bg="#ECEFF1")
            logo_label.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Logo could not be loaded: {e}")

    def create_custom_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=30,
            height=2,
            bg=self.primary_color,
            fg=self.button_fg,
            font=self.button_font,
            bd=0,
            activebackground="#1565C0",
            activeforeground=self.button_fg,
            cursor="hand2"
        )
        btn.pack(side="left", padx=10)

    def log_terminal(self, message):
        self.terminal.configure(state='normal')
        self.terminal.insert(tk.END, message + "\n")
        self.terminal.see(tk.END)  # Auto scroll down
        self.terminal.configure(state='disabled')

    def select_folder(self):
        self.folder_path = filedialog.askdirectory(
            title="Select Your Images Folder",
            initialdir=os.path.expanduser("~")
        )

        if self.folder_path:
            self.log_terminal(f"Folder selected: {self.folder_path}")
            messagebox.showinfo("Folder Selected", f"Selected folder:\n{self.folder_path}")

    def generate_labels(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Please select an images folder first.")
            return

        try:
            # Run YOLOv11 detection using CLI
            command = [
                "yolo",
                "task=detect",
                "mode=predict",
                f"model={config.MODEL_WEIGHTS}",
                f"source={self.folder_path}",
                "save_txt=True",
                f"project={self.folder_path}",
                "name=labels",
                "exist_ok=True"
            ]
            env = os.environ.copy()

            self.log_terminal(f"Running command: {' '.join(command)}")
            result = subprocess.run(command, env=env, capture_output=True, text=True)

            if result.returncode != 0:
                self.log_terminal(f"Error: {result.stderr}")
                messagebox.showerror("Error", f"Label generation failed!\n{result.stderr}")
                return

            # After generation, move label files into the images folder
            label_folder = os.path.join(self.folder_path, "labels", "labels")
            if not os.path.exists(label_folder):
                label_folder = os.path.join(self.folder_path, "labels")

            if os.path.exists(label_folder):
                txt_files = [f for f in os.listdir(label_folder) if f.endswith(".txt")]
                for txt_file in txt_files:
                    src = os.path.join(label_folder, txt_file)
                    dst = os.path.join(self.folder_path, txt_file)
                    shutil.move(src, dst)  # Move instead of copy
                shutil.rmtree(os.path.join(self.folder_path, "labels"))  # Clean up labels folder

            count = len(txt_files)
            self.log_terminal(f"Labels generated and moved successfully! Total labels: {count}")
            messagebox.showinfo("Success", f"Labels generated and moved successfully!\nTotal labels: {count}")

        except Exception as e:
            self.log_terminal(f"Exception: {e}")
            messagebox.showerror("Error", f"Label generation failed: {e}")

    def open_labelimg(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Please select an images folder first.")
            return

        try:
            self.log_terminal(f"Opening LabelImg for folder: {self.folder_path}")
            subprocess.Popen([config.LABELIMG_EXEC, self.folder_path])
        except Exception as e:
            self.log_terminal(f"Could not open LabelImg: {e}")
            messagebox.showerror("Error", f"Could not open LabelImg: {e}")

    def add_classes_file(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Please select an images folder first.")
            return

        try:
            classes_src = config.CLASSES_FILE_PATH  # path to your classes.txt

            if not os.path.exists(classes_src):
                self.log_terminal(f"Classes file not found at: {classes_src}")
                messagebox.showerror("Error", "Classes file not found!")
                return

            classes_dst = os.path.join(self.folder_path, "classes.txt")
            shutil.copy(classes_src, classes_dst)

            self.log_terminal(f"Classes file added successfully to {self.folder_path}")
            messagebox.showinfo("Success", f"Classes file added to:\n{self.folder_path}")

        except Exception as e:
            self.log_terminal(f"Exception while adding classes file: {e}")
            messagebox.showerror("Error", f"Could not add classes file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LabelingToolApp(root)
    root.mainloop()

