"""
================================================================================
MODUL 1: DIFFIE-HELLMAN KEY EXCHANGE (STEP-BY-STEP SIMULATION)
Mata Kuliah: Kriptografi
Implementasi: From Scratch murni tanpa library eksternal
================================================================================
"""

from crypto_math import (
    mod_pow,
    is_prime,
    is_primitive_root,
    get_prime_factors,
    find_primitive_roots,
    generate_prime,
)
import random


class DiffieHellmanSimulator:
    """
    Kelas simulasi protokol pertukaran kunci Diffie-Hellman antara Alice dan Bob.
    Mendukung input manual, generator acak parameter valid, preset soal/video,
    serta pembangkitan log perhitungan langkah demi langkah.
    """

    PRESET_VIDEO = {
        "p": 251,
        "g": 6,
        "x": 124,
        "y": 158,
    }

    def __init__(self, p: int = 251, g: int = 6, x: int = 124, y: int = 158):
        self.p = p
        self.g = g
        self.x = x  # Kunci privat Alice
        self.y = y  # Kunci privat Bob
        self.X = None  # Kunci publik Alice
        self.Y = None  # Kunci publik Bob
        self.Ka = None  # Kunci sesi yang dihitung Alice
        self.Kb = None  # Kunci sesi yang dihitung Bob
        self.is_valid = False
        self.validation_errors = []

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validasi parameter Diffie-Hellman:
        1. p harus bilangan prima.
        2. g harus akar primitif dari p (1 < g < p).
        3. x dan y harus berada pada interval [1, p-1] atau [2, p-2].
        """
        errors = []
        if not is_prime(self.p):
            errors.append(f"Parameter p = {self.p} bukan merupakan bilangan prima.")

        is_root, explanation = is_primitive_root(self.g, self.p)
        if not is_root:
            errors.append(f"Parameter g = {self.g} bukan akar primitif dari p = {self.p}.")

        if not (1 <= self.x < self.p):
            errors.append(f"Kunci privat Alice x = {self.x} harus memenuhi 1 <= x < p ({self.p}).")

        if not (1 <= self.y < self.p):
            errors.append(f"Kunci privat Bob y = {self.y} harus memenuhi 1 <= y < p ({self.p}).")

        self.is_valid = len(errors) == 0
        self.validation_errors = errors
        return self.is_valid, errors

    def execute(self) -> dict:
        """
        Menjalankan simulasi pertukaran kunci Diffie-Hellman:
        1. Alice: X = (g^x) mod p
        2. Bob:   Y = (g^y) mod p
        3. Alice: Ka = (Y^x) mod p
        4. Bob:   Kb = (X^y) mod p
        5. Verifikasi Ka == Kb
        """
        is_ok, errs = self.validate()
        if not is_ok:
            raise ValueError("Parameter tidak valid:\n" + "\n".join(errs))

        # 1. Kunci publik Alice
        self.X = mod_pow(self.g, self.x, self.p)

        # 2. Kunci publik Bob
        self.Y = mod_pow(self.g, self.y, self.p)

        # 3. Kunci bersama Alice
        self.Ka = mod_pow(self.Y, self.x, self.p)

        # 4. Kunci bersama Bob
        self.Kb = mod_pow(self.X, self.y, self.p)

        is_match = (self.Ka == self.Kb)

        return {
            "p": self.p,
            "g": self.g,
            "x": self.x,
            "y": self.y,
            "X": self.X,
            "Y": self.Y,
            "Ka": self.Ka,
            "Kb": self.Kb,
            "match": is_match,
        }

    def generate_detailed_log(self) -> str:
        """
        Menghasilkan catatan eksekusi terstruktur, transparan, dan detail
        untuk ditampilkan pada GUI dan draf laporan.
        """
        res = self.execute()
        lines = []
        lines.append("=" * 78)
        lines.append("       SIMULASI PROTOKOL PERTUKARAN KUNCI DIFFIE-HELLMAN")
        lines.append("=" * 78)
        lines.append("")
        lines.append("1. PARAMETER PUBLIK (PUBLIC DOMAIN PARAMETERS)")
        lines.append(f"   • Bilangan Prima Modulus (p) : {self.p}")
        lines.append(f"   • Akar Primitif / Generator (g) : {self.g}")
        lines.append(f"   • Status Uji Prima p         : {'VALID (Prima)' if is_prime(self.p) else 'TIDAK VALID'}")
        
        is_root, _ = is_primitive_root(self.g, self.p)
        factors_phi = get_prime_factors(self.p - 1)
        lines.append(f"   • Faktorisasi (p - 1 = {self.p - 1}) : {factors_phi}")
        lines.append(f"   • Status Akar Primitif g      : {'VALID (Generator)' if is_root else 'TIDAK VALID'}")
        lines.append("")
        lines.append("2. PEMILIHAN KUNCI PRIVAT (PRIVATE KEYS - DIRAHASIAKAN)")
        lines.append(f"   • Kunci Privat Alice (x) : {self.x}  (1 <= x < {self.p})")
        lines.append(f"   • Kunci Privat Bob   (y) : {self.y}  (1 <= y < {self.p})")
        lines.append("")
        lines.append("3. KALKULASI KUNCI PUBLIK (PUBLIC KEY CALCULATION)")
        lines.append("   Setiap pihak menghitung kunci publik menggunakan Square-and-Multiply:")
        lines.append(f"   a. Kunci Publik Alice (X):")
        lines.append(f"      Rumus : X = (g^x) mod p")
        lines.append(f"      Hitung: X = ({self.g}^{self.x}) mod {self.p}")
        lines.append(f"      Hasil : X = {self.X}")
        lines.append("")
        lines.append(f"   b. Kunci Publik Bob (Y):")
        lines.append(f"      Rumus : Y = (g^y) mod p")
        lines.append(f"      Hitung: Y = ({self.g}^{self.y}) mod {self.p}")
        lines.append(f"      Hasil : Y = {self.Y}")
        lines.append("")
        lines.append("4. PERTUKARAN KUNCI MELALUI SALURAN PUBLIK (INSECURE CHANNEL)")
        lines.append(f"   • Alice mengirim kunci publik X = {self.X} kepada Bob.")
        lines.append(f"   • Bob mengirim kunci publik Y = {self.Y} kepada Alice.")
        lines.append(f"   • Parameter yang terlihat oleh pihak ketiga (Eve/Adversary):")
        lines.append(f"     [ p = {self.p}, g = {self.g}, X = {self.X}, Y = {self.Y} ]")
        lines.append("     (Kunci privat x dan y TETAP RAHASIA).")
        lines.append("")
        lines.append("5. KALKULASI KUNCI SESI BERSAMA (SHARED SESSION KEY CALCULATION)")
        lines.append(f"   a. Alice menghitung Kunci Sesi (Ka) menggunakan kunci publik Bob (Y):")
        lines.append(f"      Rumus : Ka = (Y^x) mod p")
        lines.append(f"      Hitung: Ka = ({self.Y}^{self.x}) mod {self.p}")
        lines.append(f"      Hasil : Ka = {self.Ka}")
        lines.append("")
        lines.append(f"   b. Bob menghitung Kunci Sesi (Kb) menggunakan kunci publik Alice (X):")
        lines.append(f"      Rumus : Kb = (X^y) mod p")
        lines.append(f"      Hitung: Kb = ({self.X}^{self.y}) mod {self.p}")
        lines.append(f"      Hasil : Kb = {self.Kb}")
        lines.append("")
        lines.append("6. VERIFIKASI KONSISTENSI KRIPTOGRAFIS")
        lines.append(f"   • Ka = {self.Ka}")
        lines.append(f"   • Kb = {self.Kb}")
        lines.append(f"   • Ka == Kb : {res['match']} (BERHASIL)")
        lines.append("")
        lines.append("7. PEMBUKTIAN MATEMATIS KESETARAAN:")
        lines.append(f"   Ka = (Y^x) mod p = ((g^y)^x) mod p = g^(x*y) mod p")
        lines.append(f"   Kb = (X^y) mod p = ((g^x)^y) mod p = g^(x*y) mod p")
        lines.append(f"   Oleh karena perkalian skalar komutatif (x*y = y*x = {self.x * self.y}),")
        lines.append(f"   maka Ka = Kb = {self.Ka}.")
        lines.append("")
        lines.append("8. ANALISIS KEAMANAN (DISCRETE LOGARITHM PROBLEM):")
        lines.append(f"   Penyerang (Eve) mengetahui p={self.p}, g={self.g}, X={self.X}, Y={self.Y}.")
        lines.append(f"   Untuk mendapatkan kunci bersama K={self.Ka}, Eve harus memecahkan")
        lines.append(f"   x = log_{self.g}({self.X}) mod {self.p} atau y = log_{self.g}({self.Y}) mod {self.p}.")
        lines.append("   Pada bilangan prima p berskala besar (misal 2048-bit), pencarian logaritma")
        lines.append("   diskrit secara komputasi tidak fisibel (intractable).")
        lines.append("=" * 78)
        
        return "\n".join(lines)

    @classmethod
    def generate_random_valid(cls) -> "DiffieHellmanSimulator":
        """
        Membangkitkan satu set parameter Diffie-Hellman acak yang dijamin valid.
        """
        p = generate_prime(100, 1000)
        roots = find_primitive_roots(p, max_count=5)
        if not roots:
            p = 251
            roots = [6]
        g = random.choice(roots)
        x = random.randint(2, p - 2)
        y = random.randint(2, p - 2)
        return cls(p=p, g=g, x=x, y=y)
