from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for, session
from database import (
    init_db, init_settings, get_semua_produk, tambah_produk, update_produk,
    hapus_produk, simpan_transaksi, get_laporan_hari_ini,
    get_riwayat_transaksi, get_detail_transaksi, get_laporan_7hari,
    get_produk_terlaris, get_setting, set_setting
)
import io, csv, functools

app = Flask(__name__)
app.secret_key = "kasir-rahasia-123"
init_db()
init_settings()
@app.context_processor
def inject_globals():
    return dict(get_setting=get_setting, session=session)

# ─── Helper login ─────────────────────────────────────────────────────
def login_required(role=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if "user" not in session:
                return redirect(url_for("login"))
            if role and session.get("role") != role and session.get("role") != "owner":
                return redirect(url_for("index"))
            return f(*args, **kwargs)
        return wrapped
    return decorator

# ─── Auth ─────────────────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        owner_pass = get_setting("owner_password", "owner123")
        kasir_pass = get_setting("kasir_password", "kasir123")
        if username == "owner" and password == owner_pass:
            session["user"] = "owner"
            session["role"] = "owner"
            return redirect(url_for("index"))
        elif username == "kasir" and password == kasir_pass:
            session["user"] = "kasir"
            session["role"] = "kasir"
            return redirect(url_for("index"))
        else:
            error = "Username atau password salah!"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ─── Kasir ────────────────────────────────────────────────────────────
@app.route("/")
@login_required()
def index():
    produk = get_semua_produk()
    nama_toko = get_setting("nama_toko", "Toko Saya")
    return render_template("index.html", produk=produk, nama_toko=nama_toko)

@app.route("/api/produk")
@login_required()
def api_produk():
    return jsonify([dict(p) for p in get_semua_produk()])

@app.route("/api/transaksi", methods=["POST"])
@login_required()
def api_transaksi():
    data = request.get_json()
    items = data.get("items", [])
    diskon_persen = data.get("diskon", 0)
    bayar = data.get("bayar", 0)
    subtotal = sum(i["subtotal"] for i in items)
    diskon_rp = int(subtotal * diskon_persen / 100)
    total = subtotal - diskon_rp
    kembalian = bayar - total
    if not items:
        return jsonify({"error": "Keranjang kosong!"}), 400
    if bayar < total:
        return jsonify({"error": "Uang bayar kurang!"}), 400
    transaksi_id = simpan_transaksi(items, total, bayar, kembalian, diskon_rp)
    return jsonify({"sukses": True, "transaksi_id": transaksi_id,
        "subtotal": subtotal, "diskon_rp": diskon_rp,
        "total": total, "bayar": bayar, "kembalian": kembalian})

# ─── Produk ───────────────────────────────────────────────────────────
@app.route("/produk")
@login_required()
def halaman_produk():
    return render_template("produk.html", produk=get_semua_produk())

@app.route("/produk/tambah", methods=["POST"])
@login_required()
def tambah():
    tambah_produk(request.form.get("nama","").strip().lower(),
                  int(request.form.get("harga",0)), int(request.form.get("stok",0)))
    return ("", 204)

@app.route("/produk/update/<int:id>", methods=["POST"])
@login_required()
def update(id):
    update_produk(id, request.form.get("nama","").strip().lower(),
                  int(request.form.get("harga",0)), int(request.form.get("stok",0)))
    return ("", 204)

@app.route("/produk/hapus/<int:id>", methods=["POST"])
@login_required()
def hapus(id):
    hapus_produk(id)
    return ("", 204)

# ─── Laporan (owner only) ─────────────────────────────────────────────
@app.route("/laporan")
@login_required(role="owner")
def halaman_laporan():
    return render_template("laporan.html",
        ringkasan=get_laporan_hari_ini(),
        riwayat=get_riwayat_transaksi(),
        grafik=get_laporan_7hari(),
        terlaris=get_produk_terlaris())

@app.route("/api/detail-transaksi/<int:id>")
@login_required()
def detail_transaksi(id):
    return jsonify([dict(i) for i in get_detail_transaksi(id)])

@app.route("/laporan/export-csv")
@login_required(role="owner")
def export_csv():
    riwayat = get_riwayat_transaksi(limit=500)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["No","Waktu","Total","Bayar","Kembalian","Diskon"])
    for i, t in enumerate(riwayat, 1):
        writer.writerow([i, t["tanggal"], t["total"], t["bayar"], t["kembalian"], t.get("diskon_rp",0)])
    output.seek(0)
    resp = make_response(output.getvalue())
    resp.headers["Content-Disposition"] = "attachment; filename=laporan-penjualan.csv"
    resp.headers["Content-type"] = "text/csv; charset=utf-8"
    return resp

# ─── Settings (owner only) ────────────────────────────────────────────
@app.route("/settings", methods=["GET", "POST"])
@login_required(role="owner")
def settings():
    pesan = None
    if request.method == "POST":
        for key in ["nama_toko","alamat_toko","telp_toko","footer_struk","owner_password","kasir_password"]:
            val = request.form.get(key, "").strip()
            if val:
                set_setting(key, val)
        pesan = "Pengaturan berhasil disimpan!"
    data = {
        "nama_toko": get_setting("nama_toko","Toko Saya"),
        "alamat_toko": get_setting("alamat_toko",""),
        "telp_toko": get_setting("telp_toko",""),
        "footer_struk": get_setting("footer_struk","Terima kasih telah berbelanja!"),
    }
    return render_template("settings.html", data=data, pesan=pesan, role=session.get("role"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
