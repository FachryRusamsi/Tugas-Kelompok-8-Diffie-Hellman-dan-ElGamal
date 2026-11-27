# KriptoLab: Simulator Diffie-Hellman & ElGamal (From Scratch)

Aplikasi Desktop GUI modern untuk Tugas Besar Kriptografi:
**"Implementasi Algoritma Pertukaran Kunci Diffie-Hellman dan Kriptografi Asimetris ElGamal"**.

Seluruh algoritma matematika dan kriptografi diimplementasikan **100% DARI NOL (FROM SCRATCH)** tanpa pustaka kriptografi eksternal (hanya menggunakan pustaka bawaan standar Python: `tkinter`, `math`, `random`, `unittest`).

### 👥 Anggota Kelompok
- **Muhammad Fachry Shalahuddin Rusamsi** — `5027241031`
- **Prabaswara Febrian Winandika** — `5027241069`
- **Gemilang Ananda Lingua** — `5027241072`

**Departemen Teknologi Informasi** — **Institut Teknologi Sepuluh Nopember (ITS)**

---

## 🚀 Fitur Utama

1. **Modul 1: Diffie-Hellman Key Exchange (Step-by-Step)**:
   - Parameter Publik $p$ (Prima) dan $g$ (Akar Primitif).
   - Pembangkitan kunci privat Alice ($x$) dan Bob ($y$).
   - Kalkulasi kunci publik Alice $X = g^x \bmod p$ dan Bob $Y = g^y \bmod p$.
   - Kalkulasi kunci sesi bersama $K_A = Y^x \bmod p$ dan $K_B = X^y \bmod p$.
   - Bukti kesamaan sesi $K_A == K_B$.
   - **Tombol Preset**: *"Load Contoh Video (p=251, g=6, x=124, y=158)"*.
   - Generator acak parameter valid yang otomatis mencari akar primitif.

2. **Modul 2: Kriptografi Asimetris ElGamal (Keygen, Enkripsi, Dekripsi)**:
   - Pembangkitan kunci penerima (Alice): $y = g^x \bmod p$.
   - Pemetaan pesan ke blok numerik: $A=00, B=01, \dots, Z=25$ dengan syarat $m_i < p$.
   - Enkripsi pesan Bob: $a_i = g^k \bmod p$, $b_i = (y^k \cdot m_i) \bmod p$.
   - Dekripsi pesan Alice: $m_i = (b_i \cdot a_i^{p - 1 - x}) \bmod p$.
   - Rekonstruksi blok numerik kembali ke teks asli.
   - **Tombol Preset**: *"Load Contoh Video ElGamal (p=2273, g=3, x=243, M='HALO')"*.

3. **Modul 3: Playground Matematika (From Scratch Engine Test Bench)**:
   - `mod_pow(base, exp, mod)`: Square-and-Multiply.
   - `gcd(a, b)` & `ext_gcd(a, b)`: Algoritma Euclidean & Koefisien Bezout.
   - `mod_inverse(a, m)`: Balikan modular (Extended Euclidean & Teorema Fermat).
   - `is_prime(n)`: Pengujian bilangan prima deterministik.
   - `is_primitive_root(g, p)`: Verifikasi akar primitif & pencarian generator.

4. **Modul 4: Panduan Teori & Identitas Kelompok**:
   - Header identitas kelompok akademik lengkap.
   - Rangkuman teori DLP, Square-and-Multiply, dan mitigasi serangan MITM.

---

## 💻 Cara Menjalankan

### Persyaratan Sistem
- Python 3.10 atau versi lebih baru (teruji pada Python 3.13).
- Tidak memerlukan instalasi `pip` tambahan (bebas dependensi eksternal).

### 1. Menjalankan Desktop GUI
```bash
python main.py
```

### 2. Menjalankan Rangkaian Unit Testing Otomatis
```bash
python main.py --test
```
atau
```bash
python test_crypto.py
```

### 3. Menjalankan Demonstrasi Cepat di Terminal (Headless / CLI)
```bash
python main.py --cli
```

---

## 📁 Struktur Direktori
```
.
├── crypto_math.py       # Pustaka fungsi matematika dasar dari nol
├── diffie_hellman.py    # Logika protokol Diffie-Hellman & tracer
├── elgamal.py           # Logika kriptosistem ElGamal & tracer
├── gui.py               # Desain GUI Tkinter dark modern
├── main.py              # File utama (GUI, CLI, Test runner)
├── test_crypto.py       # Pengujian 10 unit test otomatis
├── LAPORAN_PROGRAM.md   # Draf laporan resmi akademik
└── README.md            # Dokumentasi panduan proyek
```
