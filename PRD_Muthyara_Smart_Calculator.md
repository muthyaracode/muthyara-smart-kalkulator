# PRD — Muthyara Smart Calculator

| Item | Keterangan |
|---|---|
| **Nama Produk** | Muthyara Smart Calculator |
| **Platform** | Windows 10/11 (64-bit), aplikasi desktop |
| **Bahasa Pemrograman** | Python 3.11+ |
| **Distribusi** | Satu file `.exe` portabel (tanpa instalasi) |
| **Versi Dokumen** | 1.0 |
| **Status** | Draft |

---

## 1. Ringkasan Produk

**Muthyara Smart Calculator** adalah kalkulator desktop yang minimalis, cepat, dan cerdas. Berbeda dari kalkulator biasa, aplikasi ini menampilkan **hasil langsung (live preview)** saat pengguna mengetik, memahami ekspresi matematika lengkap (misalnya `2 + 3 × (4 − 1)`), menyimpan riwayat perhitungan, dan menyediakan mode ilmiah serta konverter satuan dalam satu antarmuka yang bersih.

Aplikasi dibuat dengan Python dan dikemas menjadi satu file `.exe` yang dapat dijalankan langsung dari flashdisk atau folder mana pun tanpa instalasi dan tanpa membutuhkan Python di komputer pengguna.

### 1.1 Latar Belakang
Kalkulator bawaan sering terasa kaku, sementara aplikasi pihak ketiga sering penuh iklan atau fitur yang tidak perlu. Proyek ini juga berfungsi sebagai **proyek belajar pengembangan aplikasi desktop dengan Python**, sehingga arsitekturnya dibuat sederhana, rapi, dan mudah dipahami.

### 1.2 Tujuan
1. Menyediakan kalkulator yang nyaman dipakai dengan tampilan minimalis dan modern.
2. Memberikan pengalaman "pintar": live preview, input keyboard penuh, riwayat, dan penanganan kesalahan yang ramah.
3. Dapat dijalankan **portabel** sebagai file `.exe` tunggal di Windows.
4. Menjadi basis belajar yang bersih (struktur kode modular dan mudah dikembangkan).

### 1.3 Bukan Tujuan (Out of Scope v1.0)
- Tidak ada fitur online (kurs mata uang real-time, akun, sinkronisasi cloud).
- Tidak ada grafik fungsi (graphing).
- Tidak ada versi macOS/Linux/mobile (bisa dipertimbangkan di versi berikutnya).

---

## 2. Target Pengguna

| Persona | Kebutuhan | Fitur Kunci |
|---|---|---|
| **Pelajar / Mahasiswa** | Hitung cepat, fungsi ilmiah | Mode ilmiah, riwayat |
| **Pekerja Kantoran / UMKM** | Hitung harga, persen, diskon | Mode standar, persen pintar, salin hasil |
| **Pengguna Umum** | Konversi satuan sehari-hari | Konverter satuan |
| **Pengguna Mobile-PC (flashdisk)** | Tanpa instalasi | Portabel `.exe` |

---

## 3. Fitur dan Kebutuhan Fungsional

### 3.1 Prioritas (MoSCoW)

| ID | Fitur | Prioritas |
|---|---|---|
| F-01 | Operasi dasar: `+ − × ÷`, desimal, tanda negatif | **Must** |
| F-02 | Tombol `C`, `⌫` (hapus satu karakter), `±` | **Must** |
| F-03 | Parser ekspresi penuh dengan urutan operasi dan tanda kurung | **Must** |
| F-04 | **Live preview** hasil saat mengetik | **Must** |
| F-05 | Dukungan keyboard penuh (angka, operator, Enter, Backspace, Esc) | **Must** |
| F-06 | Riwayat perhitungan (klik untuk memakai ulang) | **Must** |
| F-07 | Tema Terang / Gelap + ikut tema sistem | **Must** |
| F-08 | Penanganan error ramah (bagi nol, ekspresi tidak valid) | **Must** |
| F-09 | Layout responsif (ukuran jendela berubah, tata letak menyesuaikan) | **Must** |
| F-10 | Mode Ilmiah: `sin cos tan log ln √ x² xʸ π e n!` | **Should** |
| F-11 | Persen pintar (`200 + 10%` = `220`) | **Should** |
| F-12 | Salin hasil ke clipboard (klik hasil atau `Ctrl+C`) | **Should** |
| F-13 | Memori: `MC MR M+ M−` | **Should** |
| F-14 | Konverter satuan (panjang, berat, suhu, luas, volume, data) | **Should** |
| F-15 | Pemisah ribuan otomatis (`1.234.567,89` sesuai format Indonesia) | **Should** |
| F-16 | Simpan pengaturan (tema, mode, ukuran jendela) di file di samping `.exe` | **Should** |
| F-17 | Mode derajat / radian | **Could** |
| F-18 | Selalu di atas (always on top) | **Could** |
| F-19 | Ekspor riwayat ke `.txt` / `.csv` | **Could** |

### 3.2 Perilaku "Smart"

1. **Live preview**: saat pengguna mengetik `12*(3+4`, aplikasi menampilkan pratinjau hasil abu-abu di bawah input, serta menutup kurung otomatis pada pratinjau jika memungkinkan.
2. **Persen pintar**: `100 + 10%` → `110`; `100 − 10%` → `90`; `50 × 10%` → `5`.
3. **Auto-koreksi ringan**: operator ganda `5++3` diperbaiki menjadi `5+3`; `×` dan `*` dianggap sama; `,` dan `.` mengikuti pengaturan desimal.
4. **Riwayat interaktif**: klik item riwayat untuk memasukkan ekspresi atau hasilnya ke input.
5. **Error ramah**: pesan seperti "Tidak bisa dibagi nol" tampil di area hasil, bukan dialog yang mengganggu.

### 3.3 Konverter Satuan
- Kategori: Panjang, Berat/Massa, Suhu, Luas, Volume, Kecepatan, Data.
- Dua kolom (Dari → Ke) dengan tombol tukar (⇄), hasil berubah langsung saat mengetik.
- Seluruhnya offline.

---

## 4. Kebutuhan Non-Fungsional

| Aspek | Target |
|---|---|
| **Performa** | Startup `.exe` ≤ 3 detik; respons input ≤ 50 ms |
| **Ukuran file** | `.exe` ≤ 60 MB (idealnya ≤ 40 MB) |
| **Portabilitas** | Berjalan tanpa instalasi, tanpa hak admin, tanpa Python |
| **Keamanan** | Ekspresi **tidak boleh** dievaluasi dengan `eval()`; gunakan parser AST aman |
| **Akurasi** | Gunakan `decimal.Decimal` untuk operasi dasar agar `0.1 + 0.2 = 0.3` |
| **Aksesibilitas** | Kontras warna ≥ 4.5:1, ukuran font min. 14 px, navigasi keyboard penuh |
| **Kompatibilitas** | Windows 10 / 11 (64-bit), skala DPI 100%–200% |
| **Privasi** | Tidak ada koneksi internet, tidak ada telemetri |
| **Reliabilitas** | Tidak crash saat input tidak valid; error dicatat ke `log` lokal opsional |

---

## 5. Desain UI/UX

### 5.1 Prinsip Desain
1. **Minimalis**: hanya elemen yang dibutuhkan; ruang kosong yang lega.
2. **Fokus pada angka**: layar hasil besar dan terbaca jelas.
3. **Konsisten**: sudut membulat seragam, jarak berbasis kelipatan 8 px.
4. **Responsif**: tata letak beradaptasi dengan lebar jendela.
5. **Umpan balik halus**: efek hover dan tekan yang lembut pada tombol.

### 5.2 Palet Warna

**Tema Gelap (default)**

| Peran | Hex |
|---|---|
| Latar belakang | `#14161B` |
| Panel / layar | `#1C1F26` |
| Tombol angka | `#262A33` |
| Tombol operator | `#2F3440` |
| Aksen utama (tombol `=`) | `#7C5CFF` (ungu Muthyara) |
| Aksen sekunder (hover) | `#9B82FF` |
| Teks utama | `#F2F3F7` |
| Teks sekunder (preview/riwayat) | `#8A90A2` |
| Error | `#FF6B6B` |

**Tema Terang**

| Peran | Hex |
|---|---|
| Latar belakang | `#F5F6FA` |
| Panel / layar | `#FFFFFF` |
| Tombol angka | `#EDEFF5` |
| Tombol operator | `#E0E3EE` |
| Aksen utama | `#6C4BF0` |
| Teks utama | `#1B1D24` |
| Teks sekunder | `#6B7080` |
| Error | `#E04848` |

### 5.3 Tipografi
- **Font utama**: `Segoe UI` (tersedia di Windows, tanpa file tambahan). Alternatif: `Inter` jika ingin disertakan.
- Hasil besar: 40–48 px, *semibold*; ekspresi: 20 px; tombol: 18 px; label kecil: 12–13 px.
- Angka sebaiknya *tabular* agar rata dan stabil.

### 5.4 Bentuk dan Jarak
- Sudut membulat: tombol 12 px, panel 16 px.
- Jarak antar tombol: 8 px; padding jendela: 16 px.
- Tombol `=` lebih menonjol (warna aksen), tombol `C` memakai aksen error lembut.

### 5.5 Wireframe — Mode Standar (lebar ≈ 360–480 px)

```
┌──────────────────────────────────┐
│ ☰ Standar ▾           ◐  📜     │  ← bilah atas: mode, tema, riwayat
├──────────────────────────────────┤
│                                  │
│                 12 × (3 + 4)     │  ← ekspresi (kecil)
│                          = 84    │  ← hasil (besar)
│                                  │
├──────────────────────────────────┤
│  MC   MR   M+   M−               │  ← baris memori (kecil)
│ ┌────┬────┬────┬────┐            │
│ │ C  │ ( )│ %  │ ÷  │            │
│ ├────┼────┼────┼────┤            │
│ │ 7  │ 8  │ 9  │ ×  │            │
│ ├────┼────┼────┼────┤            │
│ │ 4  │ 5  │ 6  │ −  │            │
│ ├────┼────┼────┼────┤            │
│ │ 1  │ 2  │ 3  │ +  │            │
│ ├────┼────┼────┼────┤            │
│ │ ±  │ 0  │ ,  │ =  │            │
│ └────┴────┴────┴────┘            │
└──────────────────────────────────┘
```

### 5.6 Wireframe — Mode Lebar (≥ 720 px): Panel Riwayat Terbuka

```
┌───────────────────────────────┬──────────────────┐
│ ☰ Ilmiah ▾            ◐       │  Riwayat   🗑    │
├───────────────────────────────┤  ────────────    │
│                   2 × π × 5   │  12×(3+4)  = 84  │
│                    = 31,4159  │  100+10%   = 110 │
├───────────────────────────────┤  √144      = 12  │
│ sin cos tan │ 7 8 9 │ ÷       │  ...             │
│ log ln  √   │ 4 5 6 │ ×       │                  │
│ x²  xʸ  n!  │ 1 2 3 │ −       │                  │
│ π   e   ( ) │ ± 0 , │ + │ =   │                  │
└───────────────────────────────┴──────────────────┘
```

### 5.7 Perilaku Responsif

| Lebar Jendela | Perilaku |
|---|---|
| **< 420 px** (kompak) | Satu kolom; mode standar; riwayat dibuka sebagai panel geser (overlay) |
| **420–720 px** (sedang) | Tombol membesar proporsional; mode ilmiah menampilkan baris fungsi tambahan di atas |
| **≥ 720 px** (lebar) | Dua panel: kalkulator di kiri, riwayat/konverter di kanan |

- Ukuran minimum jendela: **340 × 520 px**; ukuran awal: **400 × 640 px**.
- Grid tombol memakai bobot baris/kolom yang sama sehingga tombol ikut melebar/menyempit.
- Ukuran font hasil mengecil otomatis jika angka sangat panjang (auto-fit).

### 5.8 Mode dan Navigasi
Menu mode (☰): **Standar · Ilmiah · Konverter Satuan · Riwayat · Pengaturan · Tentang**.

### 5.9 Interaksi dan Animasi
- Hover tombol: terang naik ±8%; tekan: gelap turun ±8% (durasi ~100 ms).
- Pergantian tema: transisi lembut (tanpa kedip).
- Hasil yang disalin: muncul toast kecil "Tersalin ✓" selama 1,2 detik.

### 5.10 Pintasan Keyboard

| Tombol | Aksi |
|---|---|
| `0–9`, `.`, `,` | Input angka |
| `+ − * /` | Operator |
| `( )` | Kurung |
| `Enter` atau `=` | Hitung |
| `Backspace` | Hapus karakter terakhir |
| `Esc` | Bersihkan (C) |
| `Ctrl+C` | Salin hasil |
| `Ctrl+H` | Buka/tutup riwayat |
| `Ctrl+T` | Ganti tema |
| `Ctrl+1 / 2 / 3` | Standar / Ilmiah / Konverter |

---

## 6. Arsitektur dan Teknologi

### 6.1 Tumpukan Teknologi

| Kebutuhan | Pilihan | Alasan |
|---|---|---|
| Bahasa | Python 3.11+ | Sesuai permintaan, mudah dipelajari |
| GUI | **CustomTkinter** | Tampilan modern, mendukung tema gelap/terang, sudut membulat, ringan, mudah untuk pemula |
| Evaluasi ekspresi | Modul `ast` + `decimal` (buatan sendiri) | Aman, tanpa `eval()` |
| Penyimpanan | `json` (berkas pengaturan & riwayat) | Sederhana dan portabel |
| Pengemasan | **PyInstaller** (`--onefile --windowed`) | Menghasilkan satu `.exe` |
| Pengujian | `pytest` | Menguji mesin kalkulasi tanpa GUI |

> **Alternatif**: PySide6 (Qt) untuk UI yang lebih canggih dan responsif, tetapi ukuran `.exe` lebih besar dan kurva belajar lebih tinggi. Untuk tahap belajar, CustomTkinter direkomendasikan.

### 6.2 Struktur Proyek

```
muthyara-smart-calculator/
├── main.py                    # titik masuk aplikasi
├── requirements.txt
├── build.bat                  # skrip build exe
├── assets/
│   ├── icon.ico               # ikon aplikasi
│   └── (font opsional)
├── app/
│   ├── __init__.py
│   ├── config.py              # konstanta, versi, path
│   ├── core/
│   │   ├── evaluator.py       # parser ekspresi aman (AST)
│   │   ├── formatter.py       # format angka (ribuan, desimal)
│   │   ├── units.py           # data & logika konversi satuan
│   │   └── history.py         # kelola riwayat
│   ├── ui/
│   │   ├── theme.py           # palet warna & font
│   │   ├── main_window.py     # jendela utama + layout responsif
│   │   ├── display.py         # layar ekspresi & hasil
│   │   ├── keypad.py          # grid tombol
│   │   ├── history_panel.py
│   │   └── converter_view.py
│   └── utils/
│       ├── paths.py           # resource_path() & lokasi file portabel
│       └── settings.py        # baca/tulis settings.json
└── tests/
    ├── test_evaluator.py
    └── test_units.py
```

### 6.3 Pemisahan Tanggung Jawab
- **`core/`** tidak mengimpor GUI sama sekali → mudah diuji dan dipakai ulang.
- **`ui/`** hanya menampilkan dan meneruskan input ke `core/`.
- **`utils/paths.py`** menangani perbedaan lokasi file saat dijalankan sebagai skrip vs sebagai `.exe`.

### 6.4 Rancangan Mesin Kalkulasi (Evaluator)
1. Normalisasi input: `×`→`*`, `÷`→`/`, `,`→`.`, `^`→`**`, `%` diproses khusus.
2. Parse ke pohon sintaks dengan `ast.parse(expr, mode="eval")`.
3. Telusuri pohon dan hanya izinkan node: `BinOp`, `UnaryOp`, `Constant` (angka), `Call` ke fungsi daftar-putih (`sin`, `cos`, `sqrt`, ...), dan nama konstanta (`pi`, `e`).
4. Tolak segala node lain (atribut, impor, string, dll.) → lempar `ExpressionError`.
5. Hitung menggunakan `Decimal` untuk operasi dasar; `math` untuk fungsi ilmiah.
6. Batasi pangkat dan faktorial agar tidak membekukan aplikasi (mis. eksponen ≤ 10.000, `n!` ≤ 1.000).

### 6.5 Portabilitas `.exe`
- **Satu file**: `PyInstaller --onefile --windowed`.
- Seluruh aset (ikon, font) dirujuk lewat `resource_path()` yang memeriksa `sys._MEIPASS`.
- **Pengaturan dan riwayat** disimpan di folder `data/` **di samping file `.exe`** (bukan di `AppData`), sehingga benar-benar portabel. Jika folder tidak dapat ditulis (mis. drive baca-saja), fallback ke `%LOCALAPPDATA%\MuthyaraSmartCalculator`.
- Tidak menulis ke registry.

Contoh perintah build:

```bat
pip install -r requirements.txt
pyinstaller --noconfirm --onefile --windowed ^
  --name "Muthyara Smart Calculator" ^
  --icon assets\icon.ico ^
  --collect-all customtkinter ^
  --add-data "assets;assets" ^
  main.py
```

Hasil: `dist\Muthyara Smart Calculator.exe`

`requirements.txt`:

```
customtkinter>=5.2
pyinstaller>=6.0
pytest>=8.0
```

---

## 7. Model Data

**`data/settings.json`**
```json
{
  "version": 1,
  "theme": "dark",
  "mode": "standard",
  "angle_unit": "deg",
  "decimal_separator": ",",
  "always_on_top": false,
  "window": { "width": 400, "height": 640 }
}
```

**`data/history.json`**
```json
[
  { "expr": "12*(3+4)", "result": "84", "time": "2026-10-13T09:30:00" }
]
```
- Riwayat dibatasi **100 entri** terakhir.

---

## 8. Alur Pengguna (User Flow)

1. Pengguna membuka `.exe` → aplikasi tampil dengan tema terakhir dipakai.
2. Mengetik atau menekan tombol → ekspresi muncul, pratinjau hasil tampil langsung.
3. Menekan `=` / `Enter` → hasil final tampil, entri masuk riwayat.
4. Opsional: salin hasil, buka riwayat, ganti mode, ganti tema.
5. Menutup aplikasi → pengaturan dan riwayat tersimpan otomatis.

---

## 9. Kriteria Penerimaan (Acceptance Criteria)

- [ ] `0.1 + 0.2` menghasilkan `0,3` (bukan `0,30000000000000004`).
- [ ] `2 + 3 × 4` menghasilkan `14`; `(2 + 3) × 4` menghasilkan `20`.
- [ ] `100 + 10%` menghasilkan `110`.
- [ ] `5 ÷ 0` menampilkan pesan "Tidak bisa dibagi nol" tanpa crash.
- [ ] Input `__import__('os')` ditolak dengan pesan ekspresi tidak valid.
- [ ] Mengubah ukuran jendela dari 340 px sampai 1200 px tidak merusak tata letak.
- [ ] Tema gelap/terang berganti tanpa restart; pilihan tersimpan.
- [ ] Semua pintasan keyboard di bagian 5.10 berfungsi.
- [ ] `.exe` berjalan di Windows 10/11 bersih (tanpa Python) dan dari flashdisk.
- [ ] Waktu startup ≤ 3 detik pada PC standar.
- [ ] Teks tidak buram pada skala DPI 125%, 150%, dan 200%.

---

## 10. Rencana Pengujian

| Jenis | Cakupan |
|---|---|
| **Unit test** (`pytest`) | Evaluator (operasi, persen, error, keamanan), formatter, konversi satuan |
| **Uji manual UI** | Semua tombol, keyboard, tema, ukuran jendela, DPI |
| **Uji portabilitas** | Jalankan `.exe` di komputer lain tanpa Python; dari folder baca-saja; dari flashdisk |
| **Uji keamanan** | Coba input berbahaya (`__import__`, `open(...)`, string, atribut) |
| **Uji antivirus** | Periksa false positive (lihat risiko) |

---

## 11. Rencana Pengembangan (Roadmap)

| Fase | Isi | Estimasi |
|---|---|---|
| **0. Persiapan** | Instal Python, buat venv, struktur proyek, Git | 0,5 hari |
| **1. Core** | `evaluator.py` + `formatter.py` + unit test | 2–3 hari |
| **2. UI Dasar** | Jendela, display, keypad, tema gelap/terang | 3–4 hari |
| **3. Interaksi** | Keyboard, live preview, riwayat, salin hasil | 2–3 hari |
| **4. Responsif** | Layout adaptif, panel riwayat, auto-fit font | 2 hari |
| **5. Fitur Lanjutan** | Mode ilmiah, memori, konverter satuan | 3–4 hari |
| **6. Pengaturan & Polishing** | settings.json, animasi halus, ikon, toast | 2 hari |
| **7. Build & QA** | PyInstaller, uji portabel, perbaikan bug | 2 hari |
| **8. Rilis v1.0** | Dokumentasi singkat, tag rilis | 0,5 hari |

**Total ± 3–4 minggu** (paruh waktu, untuk pemula).

### Rencana Versi Berikutnya
- **v1.1**: ekspor riwayat, always-on-top, mode derajat/radian
- **v1.2**: kalkulator tanggal & selisih hari, kalkulator diskon/PPN
- **v2.0**: kalkulator programmer (biner/hex), grafik fungsi sederhana, multi-bahasa (ID/EN)

---

## 12. Risiko dan Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| `.exe` PyInstaller terdeteksi antivirus (false positive) | Pengguna ragu menjalankan | Hindari UPX, build dari venv bersih, sertakan hash SHA-256 saat rilis, pertimbangkan penandatanganan kode |
| Ukuran `.exe` membengkak | Lambat dibuka | Gunakan venv bersih, hindari pustaka yang tidak perlu |
| Startup `--onefile` lambat (ekstraksi ke temp) | UX kurang mulus | Optimalkan impor; sebagai alternatif sediakan mode `--onedir` yang di-zip |
| Tampilan buram di layar DPI tinggi | Tampilan kurang tajam | Aktifkan DPI awareness (CustomTkinter menanganinya) dan uji di 125–200% |
| Folder `.exe` baca-saja | Pengaturan tidak tersimpan | Fallback ke `%LOCALAPPDATA%` |
| Kesalahan presisi float | Hasil tidak akurat | Gunakan `Decimal` untuk operasi dasar |
| Evaluasi ekspresi tidak aman | Celah keamanan | Parser AST daftar-putih, tanpa `eval()` |

---

## 13. Metrik Keberhasilan

- Seluruh kriteria penerimaan (bagian 9) terpenuhi.
- Tidak ada crash pada 100+ kasus uji input.
- Waktu startup ≤ 3 detik.
- Umpan balik uji coba pengguna: minimal 4 dari 5 penguji menilai tampilan "rapi dan nyaman dipakai".

---

## 14. Lampiran

### A. Cuplikan Kerangka `main.py`

```python
import customtkinter as ctk
from app.ui.main_window import MainWindow
from app.utils.settings import load_settings

def main():
    settings = load_settings()
    ctk.set_appearance_mode(settings.get("theme", "dark"))
    app = MainWindow(settings)
    app.mainloop()

if __name__ == "__main__":
    main()
```

### B. Cuplikan `resource_path()` (untuk PyInstaller)

```python
import sys
from pathlib import Path

def resource_path(relative: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base / relative

def data_dir() -> Path:
    """Folder data di samping .exe (portabel)."""
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).resolve().parents[2]
    d = base / "data"
    try:
        d.mkdir(exist_ok=True)
        return d
    except OSError:
        import os
        fallback = Path(os.environ.get("LOCALAPPDATA", base)) / "MuthyaraSmartCalculator"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback
```

### C. Daftar Fungsi yang Diizinkan pada Evaluator

`sin, cos, tan, asin, acos, atan, log (basis 10), ln, sqrt, abs, factorial` dan konstanta `pi`, `e`.

### D. Glosarium
- **PRD**: Product Requirements Document, dokumen kebutuhan produk.
- **AST**: Abstract Syntax Tree, representasi struktur ekspresi yang aman diperiksa sebelum dihitung.
- **Portabel**: dapat dijalankan langsung tanpa instalasi.
- **Live preview**: hasil sementara yang tampil saat pengguna masih mengetik.

---

*© Muthyara Smart Calculator — Dokumen PRD v1.0*
