import sqlite3

DB_PATH = "kasir.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL UNIQUE,
            harga INTEGER NOT NULL,
            stok INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total INTEGER NOT NULL,
            bayar INTEGER NOT NULL,
            kembalian INTEGER NOT NULL,
            diskon_rp INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS item_transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaksi_id INTEGER,
            produk_nama TEXT NOT NULL,
            harga INTEGER NOT NULL,
            jumlah INTEGER NOT NULL,
            subtotal INTEGER NOT NULL,
            FOREIGN KEY (transaksi_id) REFERENCES transaksi(id)
        );
    """)
    # Tambah kolom diskon_rp jika belum ada (upgrade database lama)
    try:
        conn.execute("ALTER TABLE transaksi ADD COLUMN diskon_rp INTEGER DEFAULT 0")
        conn.commit()
    except:
        pass

    produk_awal = [
        ("susu uht 200 ml", 4500, 50),
        ("indomie goreng", 3500, 100),
        ("sabun lifeboy", 5000, 30),
        ("pasta enzim", 28000, 20),
    ]
    for nama, harga, stok in produk_awal:
        conn.execute("INSERT OR IGNORE INTO produk (nama, harga, stok) VALUES (?, ?, ?)", (nama, harga, stok))
    conn.commit()
    conn.close()

def get_semua_produk():
    conn = get_db()
    produk = conn.execute("SELECT * FROM produk ORDER BY nama").fetchall()
    conn.close()
    return produk

def tambah_produk(nama, harga, stok):
    conn = get_db()
    conn.execute("INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)", (nama, harga, stok))
    conn.commit()
    conn.close()

def update_produk(id, nama, harga, stok):
    conn = get_db()
    conn.execute("UPDATE produk SET nama=?, harga=?, stok=? WHERE id=?", (nama, harga, stok, id))
    conn.commit()
    conn.close()

def hapus_produk(id):
    conn = get_db()
    conn.execute("DELETE FROM produk WHERE id=?", (id,))
    conn.commit()
    conn.close()

def simpan_transaksi(items, total, bayar, kembalian, diskon_rp=0):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO transaksi (total, bayar, kembalian, diskon_rp) VALUES (?, ?, ?, ?)",
        (total, bayar, kembalian, diskon_rp)
    )
    transaksi_id = cur.lastrowid
    for item in items:
        conn.execute(
            "INSERT INTO item_transaksi (transaksi_id, produk_nama, harga, jumlah, subtotal) VALUES (?, ?, ?, ?, ?)",
            (transaksi_id, item['nama'], item['harga'], item['jumlah'], item['subtotal'])
        )
        conn.execute("UPDATE produk SET stok = stok - ? WHERE nama=?", (item['jumlah'], item['nama']))
    conn.commit()
    conn.close()
    return transaksi_id

def get_laporan_hari_ini():
    conn = get_db()
    hasil = conn.execute("""
        SELECT COUNT(*) as jumlah_transaksi,
               COALESCE(SUM(total), 0) as total_penjualan,
               COALESCE(SUM(diskon_rp), 0) as total_diskon
        FROM transaksi
        WHERE DATE(tanggal, 'localtime') = DATE('now', 'localtime')
    """).fetchone()
    conn.close()
    return hasil

def get_laporan_7hari():
    conn = get_db()
    data = conn.execute("""
        SELECT DATE(tanggal, 'localtime') as hari,
               COALESCE(SUM(total), 0) as total,
               COUNT(*) as jumlah
        FROM transaksi
        WHERE tanggal >= DATE('now', '-6 days', 'localtime')
        GROUP BY DATE(tanggal, 'localtime')
        ORDER BY hari ASC
    """).fetchall()
    conn.close()
    return [dict(d) for d in data]

def get_produk_terlaris(limit=5):
    conn = get_db()
    data = conn.execute("""
        SELECT produk_nama, SUM(jumlah) as total_terjual, SUM(subtotal) as total_omzet
        FROM item_transaksi
        GROUP BY produk_nama
        ORDER BY total_terjual DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(d) for d in data]

def get_riwayat_transaksi(limit=20):
    conn = get_db()
    data = conn.execute("""
        SELECT * FROM transaksi ORDER BY tanggal DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(d) for d in data]

def get_detail_transaksi(transaksi_id):
    conn = get_db()
    items = conn.execute("SELECT * FROM item_transaksi WHERE transaksi_id=?", (transaksi_id,)).fetchall()
    conn.close()
    return items

# ─── Settings toko ───────────────────────────────────────────────────
def get_setting(key, default=""):
    conn = get_db()
    try:
        row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        conn.close()
        return row["value"] if row else default
    except:
        conn.close()
        return default

def set_setting(key, value):
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def init_settings():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    # Default nilai
    defaults = [
        ("nama_toko", "Toko Saya"),
        ("alamat_toko", ""),
        ("telp_toko", ""),
        ("footer_struk", "Terima kasih telah berbelanja!"),
    ]
    for k, v in defaults:
        conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))
    conn.commit()
    conn.close()
