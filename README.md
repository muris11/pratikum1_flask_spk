# LAPORAN TUGAS SISTEM PENDUKUNG KEPUTUSAN

**Oleh :**

- **Nama** : Muhammad Rifqy Saputra
- **NIM** : 2307046
- **Kelas** : D4 SIKC 3B

**PROGRAM STUDI SISTEM INFORMASI KOTA CERDAS**  
**JURUSAN TEKNIK INFORMATIKA**  
**POLITEKNIK NEGERI INDRAMAYU**  
**2026**

---

## 📝 A. Deskripsi Tugas Mandiri

Aplikasi ini merupakan implementasi Sistem Pendukung Keputusan (SPK) berbasis **Flask** dan **Pandas**. Pada tugas mandiri ini, studi kasus praktikum awal yaitu **"Seleksi Penerima Bantuan Sosial / Beasiswa"** telah dimodifikasi menjadi **"Pemilihan Laptop Terbaik untuk Mahasiswa"**.

Aplikasi ini dapat mengubah data mentah dari file CSV menjadi informasi visual ke dalam bentuk tabel yang mudah dipahami pengguna pada browser, lengkap dengan rekapitulasi data.

### 🔄 Ringkasan Perubahan

| Aspek                | Sebelum (Praktikum)         | Sesudah (Tugas Mandiri)                 |
| -------------------- | --------------------------- | --------------------------------------- |
| **Studi Kasus**      | Pemilihan Penerima Beasiswa | Pemilihan Laptop Terbaik                |
| **Jumlah Kriteria**  | 5 kriteria (C1 – C5)        | 6 Kriteria (C1 – C6)                    |
| **Kriteria Baru**    | -                           | C6 - Berat (KG) (Cost)                  |
| **Alternatif**       | 5 Mahasiswa                 | 5 Laptop (ASUS, Lenovo, HP, Dell, Acer) |
| **Kriteria Cost**    | C2 (Penghasilan)            | C1 (Harga), C6 (Berat)                  |
| **Kriteria Benefit** | C1, C3, C4, C5              | C2, C3, C4, C5                          |

---

## 💻 B. Data Studi Kasus: Pemilihan Laptop Terbaik

Data format disimpan pada folder `data/` dalam bentuk `.csv`.

- **Alternatif:** Laptop ASUS, Laptop Lenovo, Laptop HP, Laptop Dell, Laptop Acer
- **Kriteria:**
  1. `C1` - Harga (Cost)
  2. `C2` - RAM (Benefit)
  3. `C3` - Storage (Benefit)
  4. `C4` - Processor Score (Benefit)
  5. `C5` - Ukuran Layar (Benefit)
  6. `C6` - Berat (KG) (Cost) -> _Kriteria Baru_

---

## 🧩 C. Penjelasan 5 Potongan Kode Utama

### 1. Import dan Inisialisasi Flask

```python
import pandas as pd
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
```

**Fungsi:**

- `pandas` → Library untuk membaca dan memproses file CSV.
- `pathlib` → Mengelola path file/folder secara cross-platform (Windows/Linux/Mac).
- `Flask` → Framework web Python untuk membuat aplikasi web.
- `Flask(__name__)` → Membuat instance aplikasi Flask.
- `render_template` → Menampilkan file HTML.
- `request` → Menangani data dari form upload.
- `redirect`, `url_for` → Mengarahkan user ke halaman lain setelah upload.

### 2. Fungsi `load_csv()`

```python
def load_csv(path):
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()
```

**Fungsi:**

- **Tujuan**: Membaca file CSV dan mengubahnya menjadi DataFrame Pandas.
- **Cara kerja**: Cek apakah file ada (`path.exists()`). Kalau ada, baca menggunakan `pd.read_csv()`. Kalau tidak ada, maka direturn DataFrame kosong.
- **Kenapa penting**: Menghindari error kalau file belum diunggah, aplikasi tetap jalan normal dengan menampilkan data kosong.

### 3. Route Index (Halaman Utama)

```python
@app.route("/")
def index():
    kriteria = load_csv(KRI_PATH)
    alternatif = load_csv(ALT_PATH)

    return render_template(
        "index.html",
        kriteria=kriteria.to_html(index=False) if not kriteria.empty else "<p>Belum ada data</p>",
        alternatif=alternatif.to_html(index=False) if not alternatif.empty else "<p>Belum ada data</p>",
        info_kriteria=info_data(kriteria),
        info_alternatif=info_data(alternatif),
    )
```

**Fungsi:**

- `@app.route("/")` → URL root (halaman awal).
- Memuat data CSV dari lokasi `KRI_PATH` dan `ALT_PATH`.
- Mengkonversi DataFrame Pandas ke markup tabel HTML secara langsung pakai `.to_html(index=False)`.
- Mengirim 4 variabel ke template HTML: tabel `kriteria`, tabel `alternatif`, objek `info_kriteria`, dan `info_alternatif`.
- Menangani kondisi bila data kosong dengan "_Belum ada data_".

### 4. Route Upload (Proses Form)

```python
@app.route("/upload", methods=["POST"])
def upload():
    if "kriteria" in request.files:
        request.files["kriteria"].save(KRI_PATH)
    if "alternatif" in request.files:
        request.files["alternatif"].save(ALT_PATH)
    return redirect(url_for("index"))
```

**Fungsi:**

- Menangani proses unggah dengan method `POST`.
- Menggunakan objek input `request.files` untuk mengambil file dari form browser.
- Pengecekan keamanan `if "kriteria" in request.files` agar program tidak error jika tidak ada file yang dikirim.
- Function `.save()` digunakan untuk menyimpan (dan menimpa) file CSV di folder terstruktur.
- Terakhir, `.redirect()` user agar UI Web langsung kembali ke halaman Index (merefresh tabel otomatis).

### 5. Fungsi `info_data()`

```python
def info_data(df):
    return {
        "baris": df.shape[0],
        "kolom": df.shape[1]
    }
```

**Fungsi:**

- **Tujuan**: Mendapatkan informasi statistik metadata dari DataFrame.
- **Parameter**: menerima argumen `df` (DataFrame pandas).
- Mengambil `.shape[0]` sebagai **Jumlah Baris** data (contoh: 5 alternatif / 6 kriteria).
- Mengambil `.shape[1]` sebagai **Jumlah Kolom**.
- Direturn sebagai dictionary sehingga bisa diakses di UI HTML lewat _Jinja2_, seperti kode: `{{ info_kriteria.baris }}`.

---

## 🚀 D. Cara Menjalankan Aplikasi

1. **Clone Project**:
   ```bash
   git clone https://github.com/muris11/pratikum1_flask_spk.git
   cd pratikum1_flask_spk
   ```
2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan Aplikasi Web**:
   ```bash
   python app.py
   ```
   Akses di tab web browser Anda pada alamat `http://localhost:5000`
