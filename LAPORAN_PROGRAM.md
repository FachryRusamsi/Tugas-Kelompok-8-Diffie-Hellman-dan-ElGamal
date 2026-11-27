# LAPORAN PROGRAM KRIPTOGRAFI
## IMPLEMENTASI ALGORITMA PERTUKARAN KUNCI DIFFIE-HELLMAN DAN KRIPTOGRAFI ASIMETRIS ELGAMAL (FROM SCRATCH)

---

### **IDENTITAS KELOMPOK**
* **Mata Kuliah** : Kriptografi & Keamanan Informasi
* **Judul Tugas** : Tugas Besar Implementasi Algoritma Diffie-Hellman dan ElGamal dari Nol (From Scratch)
* **Kelompok** : Kelompok Mahasiswa
* **Anggota Kelompok** :
  1. Muhammad Fachry Shalahuddin Rusamsi — 5027241031
  2. Prabaswara Febrian Winandika — 5027241069
  3. Gemilang Ananda Lingua — 5027241072
* **Departemen / Program Studi** : Teknologi Informasi
* **Fakultas / Universitas** : Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC) / Institut Teknologi Sepuluh Nopember (ITS)
* **Tahun Akademik** : 2024 / 2025

---

## DAFTAR ISI
1. [Pendahuluan & Latar Belakang](#1-pendahuluan--latar-belakang)
2. [Dasar Teori Matematika Kriptografi](#2-dasar-teori-matematika-kriptografi)
   - 2.1 [Aritmatika Modular & Grup Multiplikatif](#21-aritmatika-modular--grup-multiplikatif)
   - 2.2 [Akar Primitif (Primitive Root / Generator)](#22-akar-primitif-primitive-root--generator)
   - 2.3 [Masalah Logaritma Diskrit (Discrete Logarithm Problem - DLP)](#23-masalah-logaritma-diskrit-discrete-logarithm-problem---dlp)
   - 2.4 [Protokol Pertukaran Kunci Diffie-Hellman](#24-protokol-pertukaran-kunci-diffie-hellman)
   - 2.5 [Kriptosistem Asimetris ElGamal](#25-kriptosistem-asimetris-elgamal)
3. [Arsitektur Sistem & Penjelasan Kode (From Scratch)](#3-arsitektur-sistem--penjelasan-kode-from-scratch)
   - 3.1 [Struktur Berkas Proyek](#31-struktur-berkas-proyek)
   - 3.2 [Fungsi Matematika Dasar (`crypto_math.py`)](#32-fungsi-matematika-dasar-crypto_mathpy)
   - 3.3 [Modul Diffie-Hellman (`diffie_hellman.py`)](#33-modul-diffie-hellman-diffie_hellmanpy)
   - 3.4 [Modul Kriptosistem ElGamal (`elgamal.py`)](#34-modul-kriptosistem-elgamal-elgamalpy)
   - 3.5 [Antarmuka Desktop GUI Tkinter (`gui.py`)](#35-antarmuka-desktop-gui-tkinter-guipy)
4. [Hasil Pengujian Program & Analisis](#4-hasil-pengujian-program--analisis)
   - 4.1 [Pengujian Kasus Uji Standar Diffie-Hellman ($p=251, g=6, x=124, y=158$)](#41-pengujian-kasus-uji-standar-diffie-hellman)
   - 4.2 [Pengujian Kasus Uji Standar ElGamal ($p=2273, g=3, x=243, M=\text{'HALO'}$)](#42-pengujian-kasus-uji-standar-elgamal)
   - 4.3 [Hasil Unit Testing Otomatis](#43-hasil-unit-testing-otomatis)
   - 4.4 [Tangkapan Layar GUI (Screenshot Placeholders)](#44-tangkapan-layar-gui-screenshot-placeholders)
5. [Analisis Kompleksitas & Evaluasi Keamanan](#5-analisis-kompleksitas--evaluasi-keamanan)
6. [Kesimpulan](#6-kesimpulan)
7. [Daftar Pustaka](#7-daftar-pustaka)

---

## 1. PENDAHULUAN & LATAR BELAKANG
Dalam komunikasi data modern melalui jaringan publik yang tidak aman (insecure channel), salah satu tantangan fundamental adalah **pertukaran kunci (Key Exchange)** dan **kerahasiaan data (Data Confidentiality)**. Sebelum ditemukannya kriptografi asimetris oleh Whitfield Diffie dan Martin Hellman pada tahun 1976, dua pihak yang ingin berkomunikasi secara rahasia harus terlebih dahulu menyepakati kunci simetris melalui jalur kurir fisik yang aman.

Penemuan algoritma **Diffie-Hellman Key Exchange (DHKE)** merevolusi paradigma keamanan informasi dengan memungkinkan dua entitas (misal: Alice dan Bob) membentuk sebuah kunci rahasia simetris bersama (shared secret session key) secara terbuka tanpa ada pihak penyadap (Eve) yang mampu memperoleh kunci tersebut. Mengembangkan gagasan pertukaran kunci tersebut, Taher ElGamal pada tahun 1985 memperkenalkan **Kriptosistem Asimetris ElGamal**, yang memanfaatkan prinsip yang sama untuk membangun skema enkripsi dan tanda tangan digital.

Tujuan utama dari proyek ini adalah:
1. Mengimplementasikan protokol pertukaran kunci Diffie-Hellman dan sistem kriptografi asimetris ElGamal secara utuh **dari nol (from scratch)** tanpa bantuan pustaka kriptografi pihak ketiga (seperti `cryptography`, `PyCryptodome`, dsb.).
2. Mengembangkan antarmuka grafis desktop (**Desktop GUI**) yang interaktif, elegan, dan informatif menggunakan Python standar (`tkinter`), lengkap dengan log perhitungan langkah-demi-langkah transparan.
3. Membuktikan kebenaran matematis dari algoritma menggunakan kasus uji standar akademik (*video / lecture test cases*).

---

## 2. DASAR TEORI MATEMATIKA KRIPTOGRAFI

### 2.1 Aritmatika Modular & Grup Multiplikatif
Aritmatika modular bekerja pada himpunan bilangan bulat berhingga $\mathbb{Z}_m = \{0, 1, 2, \dots, m - 1\}$. Untuk bilangan prima $p$, himpunan elemen yang memiliki invers perkalian membentuk grup abelian berhingga terhadap perkalian modular yang dilambangkan dengan $\mathbb{Z}_p^* = \{1, 2, \dots, p - 1\}$ dengan kardinalitas (ordo grup) sebesar:
$$\phi(p) = p - 1$$

### 2.2 Akar Primitif (Primitive Root / Generator)
Sebuah elemen $g \in \mathbb{Z}_p^*$ disebut sebagai **akar primitif** (atau *generator*) jika perpangkatan dari $g$ mampu membangkitkan seluruh elemen dalam $\mathbb{Z}_p^*$. Dengan kata lain, ordo dari $g$ sama dengan $\phi(p) = p - 1$:
$$\{g^1 \bmod p, g^2 \bmod p, \dots, g^{p-1} \bmod p\} = \{1, 2, \dots, p - 1\}$$

**Teorema Verifikasi Akar Primitif:**
Elemen $g$ adalah akar primitif modulo bilangan prima $p$ jika dan hanya jika untuk setiap faktor prima unik $q$ dari $(p - 1)$:
$$g^{\frac{p - 1}{q}} \not\equiv 1 \pmod p$$

Sebagai contoh:
* Untuk $p = 251$, $\phi(p) = 250 = 2 \times 5^3$. Faktor prima unik adalah $\{2, 5\}$.
  * Uji $q = 2$: $6^{\frac{250}{2}} = 6^{125} \equiv 250 \equiv -1 \not\equiv 1 \pmod{251}$.
  * Uji $q = 5$: $6^{\frac{250}{5}} = 6^{50} \equiv 111 \not\equiv 1 \pmod{251}$.
  * Karena kedua hasil $\not\equiv 1$, maka $g = 6$ terbukti adalah akar primitif dari $251$.

### 2.3 Masalah Logaritma Diskrit (Discrete Logarithm Problem - DLP)
Diberikan bilangan prima $p$, akar primitif $g$, dan nilai $y \in \mathbb{Z}_p^*$, pencarian nilai eksponen $x$ sedemikian rupa sehingga:
$$y \equiv g^x \pmod p$$
disebut sebagai **Discrete Logarithm Problem (DLP)**.
* Menghitung $y$ dari $g, x, p$ sangat mudah dan efisien menggunakan algoritma *Square-and-Multiply* dengan kompleksitas $O(\log x)$.
* Namun, menghitung $x$ dari $g, y, p$ secara komputasi sangat sulit (intractable) untuk bilangan prima $p$ berskala besar (misal 2048-bit atau lebih), karena tidak ada algoritma waktu polinomial klasik yang dapat menyelesaikannya secara instan.

### 2.4 Protokol Pertukaran Kunci Diffie-Hellman
Langkah kerja protokol pertukaran kunci Diffie-Hellman adalah sebagai berikut:
1. **Kesepakatan Parameter Publik**:
   Alice dan Bob menyepakati bilangan prima besar $p$ dan akar primitif $g$.
2. **Pembangkitan Kunci Privat**:
   - Alice memilih bilangan bulat rahasia $x$ ($1 \le x < p$).
   - Bob memilih bilangan bulat rahasia $y$ ($1 \le y < p$).
3. **Kalkulasi & Pertukaran Kunci Publik**:
   - Alice menghitung kunci publik $X = g^x \bmod p$ dan mengirimkannya ke Bob melalui saluran publik.
   - Bob menghitung kunci publik $Y = g^y \bmod p$ dan mengirimkannya ke Alice melalui saluran publik.
4. **Kalkulasi Kunci Sesi Bersama (Shared Session Key)**:
   - Alice menerima $Y$ dan menghitung:
     $$K_A = Y^x \bmod p$$
   - Bob menerima $X$ dan menghitung:
     $$K_B = X^y \bmod p$$
5. **Bukti Kesetaraan Matematis**:
   $$K_A \equiv (g^y)^x \equiv g^{yx} \equiv g^{xy} \equiv (g^x)^y \equiv K_B \pmod p$$
   Karena perkalian skalar bersifat komutatif ($xy = yx$), maka $K_A = K_B = K$.

### 2.5 Kriptosistem Asimetris ElGamal
Skema ElGamal terdiri atas tiga tahapan:

#### A. Pembangkitan Kunci (Key Generation - Alice):
1. Pilih bilangan prima $p$ dan akar primitif $g$.
2. Pilih kunci privat $x \in [2, p - 2]$.
3. Hitung kunci publik $y = g^x \bmod p$.
4. Pasangan kunci: Kunci Publik = $(y, g, p)$, Kunci Privat = $x$.

#### B. Enkripsi Pesan (Encryption - Bob):
1. Teks plainteks dipetakan ke dalam representasi numerik dan dibagi menjadi blok-blok $m_i$ sedemikian rupa sehingga $m_i < p$.
2. Untuk setiap blok $m_i$:
   - Bob memilih bilangan acak $k_i \in [2, p - 2]$ dengan $\gcd(k_i, p - 1) = 1$.
   - Hitung bagian ciphertext pertama:
     $$a_i = g^{k_i} \bmod p$$
   - Hitung bagian ciphertext kedua:
     $$b_i = (y^{k_i} \cdot m_i) \bmod p$$
3. Pasangan ciphertext yang dikirimkan adalah kumpulan $(a_i, b_i)$.

#### C. Dekripsi Pesan (Decryption - Alice):
Untuk setiap pasangan $(a_i, b_i)$, Alice memanfaatkan kunci privatnya $x$:
$$m_i \equiv b_i \cdot (a_i^x)^{-1} \pmod p$$
Berdasarkan Teorema Kecil Fermat ($a^{p-1} \equiv 1 \pmod p$), maka:
$$(a_i^x)^{-1} \equiv a_i^{p - 1 - x} \pmod p$$
Sehingga dekripsi dapat dihitung langsung melalui:
$$m_i = (b_i \cdot a_i^{p - 1 - x}) \bmod p$$
Setelah mendapatkan integer $m_i$, pesan direkonstruksi kembali menjadi karakter alfabet asli.

---

## 3. ARSITEKTUR SISTEM & PENJELASAN KODE (FROM SCRATCH)

### 3.1 Struktur Berkas Proyek
Sistem dibangun secara modular dengan pembagian tanggung jawab kode (*separation of concerns*) yang jelas:

```
Tugas Diffie Hellman dan ElGamal/
├── crypto_math.py       # Pustaka matematika kriptografi murni dari nol
├── diffie_hellman.py    # Simulator & verifikator Diffie-Hellman Key Exchange
├── elgamal.py           # Kriptosistem ElGamal (Keygen, Enkripsi Blok, Dekripsi)
├── gui.py               # Antarmuka desktop grafis Tkinter (Dark Slate Modern)
├── main.py              # Titik masuk utama aplikasi (GUI / CLI / Unit Tests)
├── test_crypto.py       # Rangkaian automated unit testing (10 kasus uji)
└── LAPORAN_PROGRAM.md   # Draf laporan program akademik
```

### 3.2 Fungsi Matematika Dasar (`crypto_math.py`)
Seluruh fungsi matematika dibangun tanpa menggunakan pustaka luar:

#### 1. Pemangkatan Modular Efisien (`mod_pow`):
Menggunakan algoritma *Square-and-Multiply* (Binary Exponentiation).
```python
def mod_pow(base: int, exp: int, mod: int) -> int:
    if mod == 1: return 0
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:  # Jika bit ganjil / 1 (Multiply step)
            result = (result * base) % mod
        base = (base * base) % mod  # Square step
        exp >>= 1  # Geser bit ke kanan
    return result
```

#### 2. Algoritma Euclidean & Extended Euclidean (`gcd` & `ext_gcd`):
Mencari FPB dan koefisien Bezout $(x, y)$ sedemikian rupa sehingga $a \cdot x + b \cdot y = \gcd(a, b)$:
```python
def ext_gcd(a: int, b: int) -> tuple[int, int, int]:
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0
```

#### 3. Balikan Modular (`mod_inverse`):
Memanfaatkan `ext_gcd` untuk mencari $a^{-1} \pmod m$. Mengembalikan eksepsi jika $\gcd(a, m) \ne 1$.
```python
def mod_inverse(a: int, m: int) -> int:
    g, x, _ = ext_gcd(a, m)
    if g != 1:
        raise ValueError(f"Invers modular tidak ada karena FPB({a}, {m}) != 1")
    return (x % m + m) % m
```

#### 4. Pengujian Keprimaan Deterministik (`is_prime`):
Melakukan eliminasi cepat angka genap dan pembagian bentuk $6k \pm 1$ hingga $\sqrt{n}$.
```python
def is_prime(n: int) -> bool:
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True
```

#### 5. Verifikasi Akar Primitif (`is_primitive_root`):
Memfaktorkan $p - 1$ menjadi faktor prima unik $\{q_1, q_2, \dots\}$, kemudian memastikan $g^{(p-1)/q_i} \not\equiv 1 \pmod p$.

---

## 4. HASIL PENGUJIAN PROGRAM & ANALISIS

### 4.1 Pengujian Kasus Uji Standar Diffie-Hellman
* **Parameter Masukan**:
  - Prima Modulus $p = 251$
  - Akar Primitif $g = 6$
  - Kunci Privat Alice $x = 124$
  - Kunci Privat Bob $y = 158$
* **Kalkulasi Kunci Publik**:
  - $X = 6^{124} \bmod 251 = 209$
  - $Y = 6^{158} \bmod 251 = 197$
* **Kalkulasi Kunci Sesi Bersama**:
  - Alice menghitung: $K_A = Y^x \bmod p = 197^{124} \bmod 251 = 79$
  - Bob menghitung: $K_B = X^y \bmod p = 209^{158} \bmod 251 = 79$
* **Verifikasi Kesamaan**:
  $K_A = K_B = 79$ $\implies$ **SESI SIMETRIS BERHASIL TERBENTUK (MATCH = TRUE)**.

---

### 4.2 Pengujian Kasus Uji Standar ElGamal
* **Pembangkitan Kunci (Alice)**:
  - Prima $p = 2273$
  - Generator $g = 3$
  - Kunci Privat $x = 243$
  - Kunci Publik: $y = 3^{243} \bmod 2273 = 461$
  - Pasangan Kunci: Publik = $(461, 3, 2273)$, Privat = $243$.
* **Pemetaan Plainteks**:
  - Plainteks: `"HALO"`
  - Pemetaan Huruf: $\text{H}=07, \text{A}=00, \text{L}=11, \text{O}=14$.
  - Blok 1: `"HA"` $\implies 0700 \implies m_1 = 700 < 2273$.
  - Blok 2: `"LO"` $\implies 1114 \implies m_2 = 1114 < 2273$.
* **Enkripsi (Bob dengan $k_1 = 1463, k_2 = 1463$)**:
  - Blok 1:
    - $a_1 = 3^{1463} \bmod 2273 = 1439$
    - $b_1 = (461^{1463} \cdot 700) \bmod 2273 = (1825 \cdot 700) \bmod 2273 = 74$
    - Pasangan Cipher: $(1439, 74)$
  - Blok 2:
    - $a_2 = 3^{1463} \bmod 2273 = 1439$
    - $b_2 = (461^{1463} \cdot 1114) \bmod 2273 = (1825 \cdot 1114) \bmod 2273 = 988$
    - Pasangan Cipher: $(1439, 988)$
  - Ciphertext Keseluruhan: $[(1439, 74), (1439, 988)]$.
* **Dekripsi (Alice dengan $x = 243$)**:
  - Eksponen Fermat: $p - 1 - x = 2273 - 1 - 243 = 2029$.
  - Blok 1:
    - Invers modular: $1439^{2029} \bmod 2273 = 1791$
    - $m_1 = (74 \cdot 1791) \bmod 2273 = 700$
    - $700 \implies \text{"0700"} \implies \text{"HA"}$
  - Blok 2:
    - Invers modular: $1439^{2029} \bmod 2273 = 1791$
    - $m_2 = (988 \cdot 1791) \bmod 2273 = 1114$
    - $1114 \implies \text{"1114"} \implies \text{"LO"}$
  - Plainteks Terpulihkan: `"HALO"` $\implies$ **COCOK 100% PERSIS (PERFECT MATCH)**.

---

### 4.3 Hasil Unit Testing Otomatis
Seluruh fungsi diuji melalui modul `test_crypto.py`:

```
test_ext_gcd_and_mod_inverse (test_crypto.TestCryptoMath) ... ok
test_gcd (test_crypto.TestCryptoMath) ... ok
test_is_prime (test_crypto.TestCryptoMath) ... ok
test_mod_pow (test_crypto.TestCryptoMath) ... ok
test_mod_pow_trace (test_crypto.TestCryptoMath) ... ok
test_primitive_root (test_crypto.TestCryptoMath) ... ok
test_preset_video (test_crypto.TestDiffieHellman) ... ok
test_random_simulation (test_crypto.TestDiffieHellman) ... ok
test_preset_video (test_crypto.TestElGamal) ... ok
test_random_encryption (test_crypto.TestElGamal) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.001s

OK
```

---

### 4.4 Tangkapan Layar GUI (Screenshot Placeholders)

> *(Catatan: Simpan berkas tangkapan layar pada folder proyek dan tautkan pada bagian di bawah ini saat pengumpulan laporan fisik / PDF).*

#### 1. Tampilan Tab 1: Diffie-Hellman Key Exchange
```
+-------------------------------------------------------------------------------+
|  [SCREENSHOT PLACEHOLDER 1: SIMULASI DIFFIE-HELLMAN KEY EXCHANGE]             |
|                                                                               |
|  Menampilkan:                                                                 |
|  - Card Input Parameter Publik p=251, g=6 dan Kunci Privat Alice=124, Bob=158 |
|  - Card Hasil Kunci Publik Alice X=209, Bob Y=197                             |
|  - Card Hasil Kunci Sesi Ka=79 dan Kb=79                                      |
|  - Banner Status Sesi: "SESI SIMETRIS BERHASIL TERBENTUK (Ka == Kb)"          |
|  - Panel Log Eksekusi Step-by-Step dengan rincian rumus Square-and-Multiply   |
+-------------------------------------------------------------------------------+
```

#### 2. Tampilan Tab 2: Kriptosistem Asimetris ElGamal
```
+-------------------------------------------------------------------------------+
|  [SCREENSHOT PLACEHOLDER 2: KRIPTOSISTEM ASIMETRIS ELGAMAL]                   |
|                                                                               |
|  Menampilkan:                                                                 |
|  - Kolom 1 (Keygen): p=2273, g=3, x=243 -> Kunci Publik y=461                 |
|  - Kolom 2 (Enkripsi): Pesan 'HALO' -> Blok m1=700, m2=1114 -> Ciphertext     |
|    Pasangan [(1439, 74), (1439, 988)] dengan k=1463                           |
|  - Kolom 3 (Dekripsi): Rekonstruksi m1=700, m2=1114 -> Teks Terpulihkan 'HALO'|
|  - Badge Hijau: "Status: Plainteks Selesai Didekripsi & Cocok 100%!"          |
|  - Panel Log Eksekusi Transparan rincian perkalian modular & Teorema Fermat   |
+-------------------------------------------------------------------------------+
```

#### 3. Tampilan Tab 3: Playground Matematika Dasar
```
+-------------------------------------------------------------------------------+
|  [SCREENSHOT PLACEHOLDER 3: TEST BENCH FUNGSI MATEMATIKA DARI NOL]            |
|                                                                               |
|  Menampilkan tester interaktif untuk:                                         |
|  1. mod_pow(base, exp, mod)                                                   |
|  2. gcd(a, b) & ext_gcd(a, b) Bezout Coefficients                             |
|  3. mod_inverse(a, m)                                                         |
|  4. is_prime(n) Primality Checker                                             |
|  5. is_primitive_root(g, p) Primitive Root Verifier & Generator Finder        |
+-------------------------------------------------------------------------------+
```

---

## 5. ANALISIS KOMPLEKSITAS & EVALUASI KEAMANAN

### 5.1 Perbandingan Efisiensi Waktu Komputasi
| Operasi / Algoritma | Metode Naif | Metode yang Diimplementasikan (From Scratch) | Keuntungan |
| :--- | :--- | :--- | :--- |
| **Pemangkatan Modular** | Perkalian berulang $a \times a \times \dots \times a$ sebanyak $b$ kali: $O(b)$ | **Square-and-Multiply (Binary Exponentiation)**: $O(\log b)$ | Mengurangi ribuan operasi perkalian menjadi belasan iterasi; mencegah *integer overflow*. |
| **FPB & Invers Modular** | Pencarian faktor bersama $O(\min(a, b))$ | **Algoritma Euclidean Diperluas**: $O(\log(\min(a, b)))$ | Sangat cepat bahkan untuk bilangan ribuan digit. |
| **Dekripsi ElGamal** | Pencarian invers modular naif | **Teorema Kecil Fermat**: $a^{p - 1 - x} \bmod p$ | Menggunakan `mod_pow` langsung tanpa pembagian. |

### 5.2 Analisis Keamanan & Kerentanan
1. **Discrete Logarithm Problem (DLP)**:
   Keamanan protokol DH dan ElGamal terjamin selama ukuran bilangan prima $p$ cukup besar ($\ge 2048$ bit dalam implementasi industri). Pada nilai $p$ kecil (seperti contoh kuliah $p = 251$ atau $p = 2273$), penyerang dapat melakukan brute-force atau algoritma Baby-step Giant-step untuk menemukan kunci privat $x$.
2. **Man-In-The-Middle Attack (MITM)**:
   Protokol Diffie-Hellman murni tidak memiliki mekanisme autentikasi identitas pihak yang bertransaksi. Pihak ketiga aktif (Darth/Eve) dapat menyadap pertukaran dan mengganti kunci publik dengan kuncinya sendiri. Solusi standar adalah menggabungkan DH dengan tanda tangan digital (Digital Signature) atau sertifikat digital (PKI).
3. **Pentingnya Kunci Acak Efemeral ($k$) pada ElGamal**:
   Nilai $k$ pada enkripsi ElGamal tidak boleh digunakan kembali untuk pesan yang berbeda. Jika pengirim menggunakan $k$ yang sama untuk mengenkripsi dua pesan berbeda $m_1$ dan $m_2$, maka rasio ciphertext:
   $$\frac{b_1}{b_2} \equiv \frac{y^k m_1}{y^k m_2} \equiv \frac{m_1}{m_2} \pmod p$$
   memungkinkan penyerang mencari hubungan antar pesan tanpa mengetahui kunci privat penerima.

---

## 6. KESIMPULAN
Berdasarkan perancangan, implementasi, dan pengujian program yang telah dilaksanakan, dapat ditarik beberapa kesimpulan penting:
1. **Keberhasilan Implementasi Mandiri (From Scratch)**:
   Seluruh fungsi matematika inti (`mod_pow`, `gcd`, `ext_gcd`, `mod_inverse`, `is_prime`, dan `is_primitive_root`) berhasil diimplementasikan dari nol hanya dengan pustaka standar bawaan Python. Tidak ada modul kriptografi eksternal yang digunakan, sesuai dengan instruksi tugas besar.
2. **Kebenaran Matematis Terbukti Akurat**:
   - Protokol Diffie-Hellman sukses menyelaraskan kunci sesi bersama $K_A = K_B = 79$ pada kasus uji $p=251, g=6, x=124, y=158$.
   - Kriptosistem ElGamal sukses mengenkripsi plainteks `"HALO"` menjadi pasangan cipher $[(1439, 74), (1439, 988)]$ dan merekonstruksinya kembali secara utuh tanpa kecacatan data pada kasus uji $p=2273, g=3, x=243$.
3. **Pengalaman Pengguna Interaktif**:
   Aplikasi Desktop GUI yang dibangun menyediakan tombol preset otomatis, validasi parameter instan, pembangkit angka acak terverifikasi, serta panel catatan eksekusi step-by-step yang sangat transparan dan edukatif bagi pengguna maupun penguji.

---

## 7. DAFTAR PUSTAKA
1. Diffie, W., & Hellman, M. (1976). *New Directions in Cryptography*. IEEE Transactions on Information Theory, 22(6), 644–654.
2. ElGamal, T. (1985). *A Public Key Cryptosystem and a Signature Scheme Based on Discrete Logarithms*. IEEE Transactions on Information Theory, 31(4), 469–472.
3. Munir, Rinaldi. (2019). *Diktat Kuliah IF4020 Kriptografi: Kriptografi Kunci-Publik (Diffie-Hellman & ElGamal)*. Program Studi Teknik Informatika, Sekolah Teknik Elektro dan Informatika, Institut Teknologi Bandung.
4. Stallings, W. (2017). *Cryptography and Network Security: Principles and Practice* (7th ed.). Pearson Education.
5. Menezes, A. J., van Oorschot, P. C., & Vanstone, S. A. (1996). *Handbook of Applied Cryptography*. CRC Press.
