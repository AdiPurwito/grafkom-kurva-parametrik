# Visualisasi Kurva Konik Parametrik

> Tugas Mata Kuliah Grafika Komputer — Semester 4
> Implementasi algoritma representasi parametrik pada Lingkaran, Elips, Parabola, dan Hiperbola

Program interaktif berbasis Python yang membangkitkan kurva konik menggunakan
**representasi parametrik**, dilengkapi panel slider real-time untuk mengubah
parameter kurva dan membandingkan hasil render *low-resolution* vs
*high-resolution* secara langsung.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Matplotlib](https://img.shields.io/badge/Matplotlib-interactive-orange)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Fitur

- **4 jenis kurva konik**: Lingkaran, Elips, Parabola, dan Hiperbola (dua cabang)
- **Slider interaktif** — ubah pusat, jari-jari/semi-axis, dan jumlah titik secara real-time
- **Perbandingan resolusi** — panel low-res vs high-res ditampilkan berdampingan
- **Hover tooltip** menampilkan koordinat tiap titik (via `mplcursors`)
- **Statistik terminal** — jumlah titik, delta parameter (Δt), jarak antar titik, dan waktu render
- **Tema dark mode** kustom yang konsisten di seluruh visualisasi

## 🧮 Dasar Matematis

Setiap kurva dibangkitkan dengan mengiterasi parameter `t` (atau `θ`) dari
rentang awal hingga akhir, lalu menghitung koordinat `(x, y)` di setiap langkah —
bukan dengan menyelesaikan persamaan implisit kartesian.

| Kurva | x(t) | y(t) | Domain t |
|---|---|---|---|
| Lingkaran | `xc + r·cos(t)` | `yc + r·sin(t)` | `[0, 2π]` |
| Elips | `xc + a·cos(t)` | `yc + b·sin(t)` | `[0, 2π]` |
| Parabola | `xp + a·t²` | `yp + 2a·t` | `[-3, 3]` |
| Hiperbola | `xc + a·sec(t)` | `yc + b·tan(t)` | `(-π/2, π/2) ∪ (π/2, 3π/2)` |

Hiperbola dibangkitkan dalam dua cabang terpisah (kanan & kiri) karena fungsi
`sec(t)` dan `tan(t)` memiliki asimtot di `t = ±π/2`; titik-titik di dekat
asimtot ini dihindari dengan offset kecil (`eps`) agar tidak menghasilkan
nilai tak hingga.

## 📂 Struktur Proyek

Kode dipisah menjadi tiga lapisan agar logic matematika, input pengguna, dan
GUI tidak saling bercampur:

```
.
├── Grafkom_logic.py    # Rumus matematika tiap kurva, warna tema, statistik
├── Grafkom_gui.py      # Render plot, slider, tombol, hover (matplotlib)
├── Grafkom_input.py    # Entry point: menu CLI & input parameter awal
├── requirements.txt
└── README.md
```

| File | Tanggung jawab |
|---|---|
| `Grafkom_logic.py` | Perhitungan koordinat tiap kurva (`hitung_lingkaran`, `hitung_elips`, `hitung_parabola`, `hitung_hiperbola`), helper validasi input, dan pencetak statistik. **Tidak ada kode matplotlib di sini.** |
| `Grafkom_gui.py` | Semua komponen visual: render dua panel (low/high-res), slider, tombol "Terapkan Perubahan", dan tooltip hover. **Tidak mengandung rumus kurva apa pun** — menerima fungsi perhitungan dari luar sebagai parameter. |
| `Grafkom_input.py` | Titik masuk program (`python3 Grafkom_input.py`). Menampilkan menu, menerima input awal dari pengguna, lalu merangkai parameter slider dan memanggil GUI. |

## 🚀 Cara Menjalankan

```bash
git clone https://github.com/AdiPurwito/grafkom-kurva-parametrik.git
cd grafkom-kurva-parametrik
pip install -r requirements.txt
python3 Grafkom_input.py
```

Setelah dijalankan, pilih jenis kurva dari menu, masukkan parameter awal
(pusat, radius/semi-axis, jumlah titik), lalu jendela visualisasi interaktif
akan terbuka. Geser slider untuk mengubah parameter, klik **"✓ Terapkan
Perubahan"** untuk me-render ulang.

## 📦 Dependensi

```
numpy
matplotlib
mplcursors   # opsional, untuk fitur hover tooltip
```

## 🎓 Latar Belakang

Proyek ini dibuat sebagai implementasi praktik dari konsep **irisan kerucut
(conic sections)** dalam Grafika Komputer — bagaimana keempat kurva ini
(lingkaran, elips, parabola, hiperbola) sebenarnya berasal dari satu keluarga
geometris yang sama: perpotongan bidang datar dengan kerucut ganda pada sudut
kemiringan yang berbeda-beda.

Representasi parametrik dipilih dibanding representasi implisit kartesian
karena lebih efisien untuk iterasi (loop), bebas dari masalah pembagian
dengan nol/nilai imajiner, dan memberi kontrol mulus atas kerapatan titik
melalui delta parameter.

## 📄 Lisensi

MIT — bebas digunakan dan dimodifikasi untuk keperluan pembelajaran.
