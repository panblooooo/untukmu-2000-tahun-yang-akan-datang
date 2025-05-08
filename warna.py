import tkinter as tk

# Daftar nama warna dan kode hex
warna = {
    "Black": "#000000",
    "White": "#FFFFFF",
    "Red": "#FF0000",
    "Green": "#00FF00",
    "Blue": "#0000FF",
    "Yellow": "#FFFF00",
    "Cyan": "#00FFFF",
    "Magenta": "#FF00FF",
    "Gray": "#808080",
    "Dark Gray": "#A9A9A9",
    "Light Gray": "#D3D3D3",
    "Orange": "#FFA500",
    "Pink": "#EE82EE",
    "Purple": "#800080",
    "Brown": "#A52A2A",
    "Violet": "#EE82EE",
    "Lime": "#00FF00",
    "Teal": "#008080",
    "Navy": "#000080",
    "Olive": "#808000",
    "Silver": "#C0C0C0",
    "Gold": "#FFD700",
    "Indigo": "#4B0082",
    "Coral": "#FF7F50",
    "Light Blue": "#ADD8E6",
    "Sky Blue": "#87CEEB",
    "Dark Green": "#006400",
    "Light Green": "#90EE90",
    "Salmon": "#FA8072",
    "Peach": "#FFDAB9",
    "Tan": "#D2B48C",
    "Maroon": "#800000"
}

root = tk.Tk()
root.title("Contoh Warna di Tkinter")

# Menampilkan semua warna sebagai label
for warna_nama, kode_hex in warna.items():
    label = tk.Label(root, text=warna_nama, bg=kode_hex, fg="black", width=20)
    label.pack(pady=2)

root.mainloop()
