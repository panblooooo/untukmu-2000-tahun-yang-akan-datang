import tkinter as tk
from tkinter import font

# Membuat jendela utama
root = tk.Tk()
root.title("Contoh Menampilkan Font di Tkinter")

# Daftar font dan ukurannya
fonts = [
    ("Arial", 16),
    ("Helvetica", 16),
    ("Times New Roman", 16),
    ("Courier", 16),
    ("Georgia", 16),
    ("Comic Sans MS", 16)
]

# Menampilkan font pada label
for font_name, font_size in fonts:
    label = tk.Label(root, text=f"Font: {font_name}", font=(font_name, font_size))
    label.pack(pady=5)

# Menjalankan aplikasi
root.mainloop()
