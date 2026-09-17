# auto_rapi

> Perkakas analisis, perbaikan, dan pengenal skema otomatis untuk berkas JSON dan CSV berkinerja tinggi.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-SPECTRA--FIXER--v5.0-magenta.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)](#)

---

## Deskripsi

**auto_rapi** (SPECTRA JSON REPAIR - Ultimate Edition) adalah sebuah solusi berbasis Python yang dirancang untuk memuat, menganalisis, serta memulihkan struktur data JSON dan CSV yang tidak valid atau tidak terstruktur. Perkakas ini secara otomatis mendeteksi pola data (*data patterns*) dari skema khusus maupun generik untuk memudahkan pengolahan data berskala besar.

Sistem ini dilengkapi dengan modul *auto-detection* cerdas yang memanfaatkan algoritma pembobotan skor penanda (*signature scoring algorithm*). Modul ini secara otomatis mengidentifikasi apakah struktur data yang dianalisis merupakan format profil pengguna CSV, atau JSON generik tanpa memerlukan konfigurasi manual dari pengguna.

Dikembangkan dengan prinsip ketiadaan dependensi pihak ketiga (*zero-dependency*), **auto_rapi** dapat dijalankan dengan cepat di berbagai lingkungan sistem operasi. Aplikasi ini sangat cocok digunakan oleh administrator sistem, *data engineer*, dan pengembang aplikasi yang sering berurusan dengan pembersihan data (*data cleansing*) dan restrukturisasi berkas JSON.

---

## Fitur

* **Deteksi Skema Otomatis (*Auto-Detect Schema*)**: Mengidentifikasi tipe data secara otomatis berdasarkan sidik kunci (*key signatures*) untuk skema CSV User, dan Generik.
* **Penanganan Toleransi Enkoding (*Encoding Fault-Tolerance*)**: Memuat berkas JSON dengan mekanisme penanganan kesalahan karakter (*error handling*) guna mencegah kegagalan pemrosesan akibat *corrupted encoding*.
* **Pembersihan dan Normalisasi Kunci**: Mengubah kunci skema data menjadi bentuk terstandarisasi untuk mempermudah *parsing* data lanjutan.
* **Tampilan Terminal Berwarna (ANSI Colorized CLI)**: Menyediakan antarmuka baris perintah yang rapi, komunikatif, dan informatif menggunakan visualisasi warna ANSI.
* **Portabel dan Tanpa Dependensi Eksternal**: Dibangun sepenuhnya menggunakan pustaka standar Python (*standard library*), sehingga tidak memerlukan instalasi *package* tambahan melalui `pip`.

---

## Instalasi

### Prasyarat

Pastikan perangkat Anda telah terpasang **Python 3.8** atau versi yang lebih baru.

### Langkah Instalasi

1. **Klon Repositori**
   ```bash
   git clone https://github.com/celisantinel/auto_rapi.git
   cd auto_rapi
   ```

2. **Verifikasi Lingkungan Python**
   ```bash
   python3 --version
   ```

3. **Beri Hak Akses Eksekusi (Opsional untuk Linux/macOS)**
   ```bash
   chmod +x main.py
   ```

---

## Cara Penggunaan

### Menjalankan Skrip

Untuk menjalankan perkakas perbaikan JSON, eksekusi perintah berikut pada terminal:

```bash
python3 main.py
```

### Metode Deteksi Skema Data

Sistem mendeteksi skema data berdasarkan daftar kata kunci unik (*signature keys*) berikut:

| Tipe Data | Kunci Penanda (*Signature Keys*) | Ambang Batas Skor |
| :--- | :--- | :--- |
| **Dapodik** | `nama`, `jenis_kelamin`, `nisn`, `rombel`, `tingkat` | Minimal 3 kecocokan |
| **BPJS** | `nik`, `name`, `gender`, `birthdate`, `phone`, `address`, `district` | Minimal 3 kecocokan |
| **CSV User** | `id`, `group`, `nickname`, `mobile`, `avatar`, `logintime` | Minimal 3 kecocokan |
| **Generic** | Tidak memenuhi kriteria di atas | Default (0) |

---

## Konfigurasi

Konfigurasi aplikasi dikelola langsung melalui variabel internal di dalam berkas `main.py`:

```python
# ============ KONFIGURASI ============
VERSION = "SPECTRA-FIXER-v5.0"
```

### Skema Pewarnaan ANSI

Pengaturan warna antarmuka dapat disesuaikan pada kelas `Colors` dalam skrip utama:

```python
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
```

---

## Struktur Proyek

Berikut adalah struktur direktori dari proyek `auto_rapi`:

```
auto_rapi/
├── main.py
├── README.md
└── LICENSE
```

### Penjelasan Berkas

* `main.py`: Skrip utama yang berisi logika perbaikan JSON, deteksi tipe data, dan antarmuka CLI.
* `README.md`: Dokumentasi resmi proyek.

---

## Kebutuhan Sistem

| Komponen | Spesifikasi Minimum |
| :--- | :--- |
| **Sistem Operasi** | Linux, macOS, atau Windows 10/11 |
| **Bahasa Pemrograman** | Python 3.8 atau lebih baru |
| **Modul Python** | `json`, `re`, `os`, `sys`, `csv`, `shutil`, `datetime` (Built-in) |
| **Memori (RAM)** | 512 MB (tergantung ukuran berkas JSON yang diproses) |

---

## Kontribusi

Kontribusi selalu terbuka untuk perbaikan fitur dan penambahan skema deteksi baru. Silakan ikuti langkah-langkah berikut:

1. Fork repositori ini.
2. Buat *feature branch* baru (`git checkout -b fitur/SkemaBaru`).
3. Lakukan *commit* perubahan Anda (`git commit -m 'Menambahkan skema deteksi X'`).
4. Push ke *branch* tersebut (`git push origin fitur/SkemaBaru`).
5. Buat *Pull Request* baru.

---

## Lisensi

Proyek ini didistribusikan di bawah lisensi **MIT License**. Lihat berkas `LICENSE` untuk informasi selengkapnya.

---

## Penulis

* **Celi Santinel** - *Pengembang Utama* - [@celisantinel](https://github.com/celisantinel)

---

> Made with love by SPECTRA ENGINE
