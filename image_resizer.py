import os
import glob
from pathlib import Path
from PIL import Image
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD  # Fixed: DND_FILES (uppercase)

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Image Batch Resizer")
        self.root.geometry("500x350")
        
        # Root window handles drag-drop (reliable on Windows)
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
        
        self.folder_path = ""
        self.max_sizes = [1920, 1200, 800]

        # Drop zone label (click to browse)
        self.drop_label = tk.Label(root, text="Drag & drop FOLDER anywhere on window\nor CLICK HERE to browse", 
                                   bg="lightblue", relief="solid", bd=2, height=5, font=("Arial", 10))
        self.drop_label.pack(pady=20, padx=20, fill="x")
        self.drop_label.bind('<Button-1>', lambda e: self.browse_folder())

        self.path_var = tk.StringVar()
        self.path_entry = tk.Entry(root, textvariable=self.path_var, state="readonly")
        self.path_entry.pack(pady=5, padx=20, fill="x")

        # Size selection
        tk.Label(root, text="Max side length (px):").pack(pady=5)
        self.size_var = tk.StringVar(value="1920")
        sizes = ttk.Combobox(root, textvariable=self.size_var, values=self.max_sizes, state="readonly", width=10)
        sizes.pack(pady=5)

        # Progress bar
        # Checkbox for copying small images
        self.copy_small = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Copy small images too", variable=self.copy_small).pack(pady=5)

        self.progress = ttk.Progressbar(root, mode='determinate')
        self.progress.pack(pady=10, padx=20, fill="x")

        # Button
        tk.Button(root, text="Resize Images", command=self.resize_images, bg="#4CAF50", fg="white").pack(pady=10)


    def on_drop(self, event):
        print("RAW DROP DATA:", repr(event.data))  # Debug - remove later if wanted
        paths = self.parse_drop(event.data)
        print("PARSED:", paths)
        folders = [p for p in paths if os.path.isdir(p)]
        if folders:
            self.folder_path = folders[0]
            self.path_var.set(self.folder_path)
            print("Loaded folder:", self.folder_path)
        elif paths:
            messagebox.showerror("Error", f"Got files: {len(paths)}. Drag a FOLDER from File Explorer.")
        else:
            messagebox.showerror("Error", "No valid drop.")

    def parse_drop(self, data):
        if not data:
            return []
        try:
            # Tcl splitlist handles {} perfectly
            paths = self.root.tk.splitlist(data)
        except:
            # Fallback for braces/multi
            clean = data.strip().strip("{}").replace("}", "").replace("{", "")
            paths = [p.strip() for p in clean.split(chr(0))]  # Null-separated on Win
            paths = [p for p in paths if p]  # Filter empty
        return [os.path.normpath(p) for p in paths]

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            self.path_var.set(folder)

    def resize_images(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Select folder first.")
            return
        max_side = int(self.size_var.get())
        output_dir = Path(self.folder_path) / "resized"
        output_dir.mkdir(exist_ok=True)
        image_exts = ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.bmp', '*.tiff', '*.tif']
        images = []
        for ext in image_exts:
            images.extend(glob.glob(os.path.join(self.folder_path, '**', ext), recursive=True))
        if not images:
            messagebox.showinfo("No images", "No images found.")
            return

        self.progress['maximum'] = len(images)
        self.progress['value'] = 0
        processed = skipped = errors = 0
        for i, img_path in enumerate(images):
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    if max(width, height) <= max_side:
                        skipped += 1
                        if self.copy_small.get():
                            import shutil
                            base, ext = os.path.splitext(os.path.basename(img_path))
                            out_path = output_dir / f"{base}_small{ext}"
                            shutil.copy2(img_path, out_path)
                        else:
                            continue

                    ratio = max_side / max(width, height)
                    new_w = int(width * ratio)
                    new_h = int(height * ratio)
                    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    base, _ = os.path.splitext(os.path.basename(img_path))
                    out_path = output_dir / f"{base}.jpg"
                    resized.convert('RGB').save(out_path, 'JPEG', quality=92, optimize=True)
                    processed += 1
            except Exception as e:
                errors += 1
                print(f"Error {img_path}: {e}")
            self.progress['value'] = i + 1
            self.root.update()
        messagebox.showinfo("Complete", f"Processed: {processed}\nSkipped: {skipped}\nErrors: {errors}\n→ {output_dir}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
