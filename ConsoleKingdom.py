import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import os
import json

class RentalPS:
    def __init__(self, kategori, harga):
        self.kategori = kategori
        self.harga_per_jam = harga
        self.ruangan = {
            f"{kategori[:2].upper()}{i:02}": {"status": "Kosong", "waktu": None, "durasi": 0}
            for i in range(1, 7)
        }

    def reservasi(self, kode_ruangan, durasi):
        now = datetime.now()
        if kode_ruangan in self.ruangan:
            if self.ruangan[kode_ruangan]["status"] == "Kosong":
                self.ruangan[kode_ruangan]["status"] = "Terisi"
                self.ruangan[kode_ruangan]["waktu"] = now.strftime("%Y-%m-%d %H:%M:%S")
                self.ruangan[kode_ruangan]["durasi"] = durasi
                save_data()
                save_riwayat(self.kategori, kode_ruangan, durasi, self.harga_per_jam, now)
                return True
            else:
                return False
        return False

    def cek_waktu_habis(self):
        now = datetime.now()
        for kode, info in self.ruangan.items():
            if info["status"] == "Terisi":
                waktu_mulai = datetime.strptime(info["waktu"], "%Y-%m-%d %H:%M:%S")
                if now >= waktu_mulai + timedelta(hours=info["durasi"]):
                    self.ruangan[kode] = {"status": "Kosong", "waktu": None, "durasi": 0}
                    messagebox.showinfo("Selesai", f"Waktu sewa untuk {kode} telah habis.")
        save_data()

def save_data():
    data = {
        "AC": rental_AC.ruangan,
        "NONAC": rental_NONAC.ruangan,
        "PRIVATE": rental_PRIVATE.ruangan
    }
    with open("data_rental.json", "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    if os.path.exists("data_rental.json"):
        with open("data_rental.json", "r") as f:
            data = json.load(f)
            rental_AC.ruangan = data.get("AC", rental_AC.ruangan)
            rental_NONAC.ruangan = data.get("NONAC", rental_NONAC.ruangan)
            rental_PRIVATE.ruangan = data.get("PRIVATE", rental_PRIVATE.ruangan)

def save_riwayat(kategori, kode, durasi, harga_per_jam, waktu):
    total = durasi * harga_per_jam
    riwayat = []
    if os.path.exists("riwayat_peminjaman.json"):
        with open("riwayat_peminjaman.json", "r") as f:
            try:
                riwayat = json.load(f)
            except json.JSONDecodeError:
                pass
    riwayat.append({
        "kategori": kategori,
        "kode_ruangan": kode,
        "durasi_jam": durasi,
        "harga_per_jam": harga_per_jam,
        "total_biaya": total,
        "waktu_mulai": waktu.strftime("%Y-%m-%d %H:%M:%S")
    })
    with open("riwayat_peminjaman.json", "w") as f:
        json.dump(riwayat, f, indent=4)

def hapus_riwayat(kode_ruangan):
    if os.path.exists("riwayat_peminjaman.json"):
        with open("riwayat_peminjaman.json", "r") as f:
            try:
                riwayat = json.load(f)
                # Cari entri yang akan dihapus
                for item in riwayat:
                    if item["kode_ruangan"] == kode_ruangan:
                        kategori = item["kategori"]
                        sistem = rental_map.get(kategori)
                        if sistem and kode_ruangan in sistem.ruangan:
                            sistem.ruangan[kode_ruangan] = {
                                "status": "Kosong",
                                "waktu": None,
                                "durasi": 0
                            }
                        break

                # Filter dan simpan ulang
                riwayat = [item for item in riwayat if item["kode_ruangan"] != kode_ruangan]
                with open("riwayat_peminjaman.json", "w") as f:
                    json.dump(riwayat, f, indent=4)
                
                save_data()  # Simpan perubahan ke file data_rental.json
                tampilkan_riwayat()
                update_grid()  # Perbarui tampilan tombol ruangan
            except json.JSONDecodeError:
                pass

def tampilkan_riwayat():
    beranda_frame.pack_forget()
    kategori_frame.pack_forget()
    ruangan_frame.pack_forget()
    waktu_frame.pack_forget()
    riwayat_frame.pack()

    for i in tree_riwayat.get_children():
        tree_riwayat.delete(i)

    if os.path.exists("riwayat_peminjaman.json"):
        with open("riwayat_peminjaman.json", "r") as f:
            try:
                data = json.load(f)
                if not data:
                    messagebox.showinfo("Info", "Belum ada data riwayat.")
                    tree_riwayat.insert("", tk.END, values=("Belum ada riwayat", "-", "-", "-", "-", "-", "-"))
                    return
                for item in data:
                    waktu_mulai = datetime.strptime(item["waktu_mulai"], "%Y-%m-%d %H:%M:%S")
                    waktu_habis = waktu_mulai + timedelta(hours=item["durasi_jam"])
                    tree_riwayat.insert("", tk.END, values=(
                        item["kategori"],
                        item["kode_ruangan"],
                        item["durasi_jam"],
                        f"{item['harga_per_jam']}k",
                        f"Rp{item['total_biaya']}k",
                        waktu_mulai.strftime("%Y-%m-%d %H:%M:%S"),
                        waktu_habis.strftime("%Y-%m-%d %H:%M:%S")
                    ), tags=("active",))
                    tree_riwayat.tag_bind("active", "<Button-3>", lambda event, kode=item["kode_ruangan"]: context_menu(event, kode))
            except json.JSONDecodeError:
                tree_riwayat.insert("", tk.END, values=("Error", "-", "-", "-", "-", "-", "-"))
    else:
        messagebox.showinfo("Info", "Belum ada data riwayat.")
        tree_riwayat.insert("", tk.END, values=("Belum ada riwayat", "-", "-", "-", "-", "-", "-"))

def context_menu(event, kode):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Hapus Riwayat", command=lambda: hapus_riwayat(kode))
    menu.post(event.x_root, event.y_root)

def mulai_pilih_kategori():
    beranda_frame.pack_forget()
    kategori_frame.pack()

def kembali_ke_beranda():
    kategori_frame.pack_forget()
    ruangan_frame.pack_forget()
    waktu_frame.pack_forget()
    riwayat_frame.pack_forget()
    beranda_frame.pack()
    update_grid()

def pilih_kategori(kat):
    global kategori_terpilih, sistem_terpilih
    kategori_terpilih = kat
    sistem_terpilih = rental_map[kat]
    kategori_frame.pack_forget()
    ruangan_frame.pack()
    update_grid()

def update_grid():
    for w in grid_frame.winfo_children():
        w.destroy()
    for kode, data in sistem_terpilih.ruangan.items():
        color = "green" if data["status"] == "Kosong" else "red"
        b = tk.Button(grid_frame, text=kode, bg=color, width=10, height=2,
                      state="normal" if data["status"] == "Kosong" else "disabled",
                      command=lambda k=kode: pilih_ruangan(k))
        b.pack(side="left", padx=5, pady=5)

def pilih_ruangan(kode):
    if not kode:
        messagebox.showerror("Kesalahan", "Kode ruangan tidak valid.")
        return
    global ruangan_dipilih
    ruangan_dipilih = kode
    ruangan_frame.pack_forget()
    waktu_frame.pack()

def konfirmasi_booking():
    try:
        durasi = int(entry_durasi.get())
        if durasi <= 0:
            messagebox.showerror("Durasi Tidak Valid", "Durasi harus lebih dari 0 jam.")
            return
    except ValueError:
        messagebox.showerror("Input Salah", "Masukkan durasi dalam angka.")
        return

    sukses = sistem_terpilih.reservasi(ruangan_dipilih, durasi)
    if sukses:
        total = sistem_terpilih.harga_per_jam * durasi
        messagebox.showinfo("Booking Berhasil", f"Ruang: {kategori_terpilih}\nKode: {ruangan_dipilih}\nDurasi: {durasi} jam\nTotal: Rp{total}K")
        kembali_ke_beranda()
    else:
        messagebox.showerror("Gagal", "Ruangan telah terisi.")

root = tk.Tk()
root.title("Rental PS")

kategori_terpilih = ""
ruangan_dipilih = ""
sistem_terpilih = None

rental_AC = RentalPS("AC", 15)
rental_NONAC = RentalPS("NON AC", 12)
rental_PRIVATE = RentalPS("PRIVATE", 25)
rental_map = {
    "AC": rental_AC,
    "NON AC": rental_NONAC,
    "PRIVATE": rental_PRIVATE
}

load_data()

beranda_frame = tk.Frame(root)
beranda_frame.pack(pady=20)
tk.Label(beranda_frame, text="Selamat Datang di Rental PS", font=("Arial", 20)).pack(pady=10)
tk.Button(beranda_frame, text="AC (15k/jam)", width=20, command=lambda: pilih_kategori("AC")).pack(pady=5)
tk.Button(beranda_frame, text="NON AC (12k/jam)", width=20, command=lambda: pilih_kategori("NON AC")).pack(pady=5)
tk.Button(beranda_frame, text="PRIVATE (25k/jam)", width=20, command=lambda: pilih_kategori("PRIVATE")).pack(pady=5)
tk.Button(beranda_frame, text="Lihat Riwayat Peminjaman", width=25, command=tampilkan_riwayat).pack(pady=5)
tk.Button(beranda_frame, text="Keluar", command=root.destroy, bg="black", fg="white").pack(pady=10)

kategori_frame = tk.Frame(root)
tk.Label(kategori_frame, text="Pilih Kategori Ruangan", font=("Arial", 16)).pack(pady=10)
tk.Button(kategori_frame, text="Kembali", command=kembali_ke_beranda).pack()

ruangan_frame = tk.Frame(root)
tk.Label(ruangan_frame, text="Pilih Ruangan", font=("Arial", 14)).pack(pady=10)
grid_frame = tk.Frame(ruangan_frame)
grid_frame.pack()
tk.Button(ruangan_frame, text="Kembali", command=kembali_ke_beranda).pack(pady=10)

waktu_frame = tk.Frame(root)
tk.Label(waktu_frame, text="Masukkan Durasi (jam)", font=("Arial", 14)).pack(pady=10)
entry_durasi = tk.Entry(waktu_frame)
entry_durasi.pack(pady=5)
tk.Button(waktu_frame, text="Konfirmasi Booking", command=konfirmasi_booking).pack(pady=5)
tk.Button(waktu_frame, text="Kembali", command=kembali_ke_beranda).pack(pady=5)

riwayat_frame = tk.Frame(root)
tk.Label(riwayat_frame, text="Riwayat Peminjaman", font=("Arial", 16)).pack(pady=10)
tree_riwayat = ttk.Treeview(riwayat_frame, columns=("kategori", "kode", "durasi", "harga", "total", "mulai", "habis"), show="headings")
tree_riwayat.heading("kategori", text="Kategori")
tree_riwayat.heading("kode", text="Kode Ruangan")
tree_riwayat.heading("durasi", text="Durasi (jam)")
tree_riwayat.heading("harga", text="Harga/jam")
tree_riwayat.heading("total", text="Total Biaya")
tree_riwayat.heading("mulai", text="Waktu Mulai")
tree_riwayat.heading("habis", text="Waktu Habis")
tree_riwayat.column("kategori", width=100, anchor="center")
tree_riwayat.column("kode", width=90, anchor="center")
tree_riwayat.column("durasi", width=80, anchor="center")
tree_riwayat.column("harga", width=100, anchor="center")
tree_riwayat.column("total", width=100, anchor="center")
tree_riwayat.column("mulai", width=160, anchor="center")
tree_riwayat.column("habis", width=160, anchor="center")
tree_riwayat.pack(pady=5, fill="x")
tk.Button(riwayat_frame, text="Kembali", command=kembali_ke_beranda).pack(pady=5)

def cek_booking():
    for rental in rental_map.values():
        rental.cek_waktu_habis()
    root.after(5000, cek_booking)

cek_booking()
root.mainloop() 