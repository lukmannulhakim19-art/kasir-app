# 🛒 Kasir App — Aplikasi Kasir Web Modern untuk UMKM


> Aplikasi kasir berbasis web yang ringan, cepat, dan mudah digunakan — cocok untuk warung, toko kelontong, dan UMKM kecil menengah. Dibangun dengan Flask \& SQLite, dapat diakses dari HP maupun laptop tanpa install apapun.

🔗 **Live Demo:** [lukmannulhakim19.pythonanywhere.com](https://lukmannulhakim19.pythonanywhere.com)  
👤 **Demo Login:** username `kasir` / password `kasir123`

\---

## ✨ Fitur Utama

|Fitur|Keterangan|
|-|-|
|🔐 Multi-role login|Owner \& Kasir dengan akses berbeda|
|🛍️ Kasir real-time|Tambah produk ke keranjang, hitung otomatis|
|💸 Diskon \& kembalian|Input diskon %, hitung kembalian otomatis|
|🧾 Cetak struk|Struk digital langsung dari browser|
|📦 Manajemen produk|Tambah, edit, hapus produk \& stok|
|📊 Laporan penjualan|Ringkasan harian, grafik 7 hari, produk terlaris|
|📥 Export CSV|Download laporan transaksi ke Excel|
|⚙️ Pengaturan toko|Nama toko, alamat, password bisa diubah|
|📱 Responsive|Tampilan optimal di HP \& laptop|

\---

## 🖥️ Screenshot

> ## 🖥️screenshot1.jpeg

![Screenshot 1](WhatsApp%20Image%202026-05-09%20at%201.48.20%20PM.jpeg)
![Screenshot 2](WhatsApp%20Image%202026-05-09%20at%201.48.20%20PM%20(1).jpeg)
![Screenshot 3](WhatsApp%20Image%202026-05-09%20at%201.48.20%20PM%20(2).jpeg)
![Screenshot 4](WhatsApp%20Image%202026-05-09%20at%201.48.21%20PM.jpeg)
![Screenshot 5](WhatsApp%20Image%202026-05-09%20at%201.48.21%20PM%20(1).jpeg)
![Screenshot 6](WhatsApp%20Image%202026-05-09%20at%201.48.22%20PM.jpeg)

\---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript (Vanilla)
* **Deploy:** PythonAnywhere (cloud hosting)
* **Version Control:** Git \& GitHub

\---

## 🚀 Cara Install Lokal

```bash
# 1. Clone repo
git clone https://github.com/lukmannulhakim19-art/kasir-app.git
cd kasir-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan aplikasi
python app.py
```

Buka browser → `http://localhost:5000`

**Login:**

* Owner: `owner` / `owner123`
* Kasir: `kasir` / `kasir123`

\---

## 📁 Struktur Project

```
kasir-app/
├── app.py              # Main Flask app \& routing
├── database.py         # Database queries \& logic
├── kasir.db            # SQLite database
├── requirements.txt    # Python dependencies
├── Procfile            # Deploy config
└── templates/
    ├── index.html      # Halaman kasir utama
    ├── produk.html     # Manajemen produk
    ├── laporan.html    # Laporan \& grafik
    ├── settings.html   # Pengaturan toko
    └── login.html      # Halaman login
```

\---

## 💼 Tersedia untuk Kustomisasi

Aplikasi ini tersedia untuk dibeli atau dikustomisasi sesuai kebutuhan bisnis Anda:

* ✅ Tambah fitur (multi-cabang, barcode scanner, dll)
* ✅ Kustomisasi tampilan \& nama toko
* ✅ Integrasi printer struk
* ✅ Deploy ke domain sendiri
* ✅ Training penggunaan aplikasi

📩 **Hubungi saya:** 6281212487305 | lukmannulhakim19@gmail.com

\---

## 👨‍💻 Developer

**Lukmannul Hakim**  
Full-stack Developer | Python \& Flask Enthusiast

[!\[GitHub](https://img.shields.io/badge/GitHub-lukmannulhakim19--art-black?logo=github)](https://github.com/lukmannulhakim19-art)

\---

## 📄 License

MIT License — bebas digunakan untuk keperluan belajar dan pengembangan.

