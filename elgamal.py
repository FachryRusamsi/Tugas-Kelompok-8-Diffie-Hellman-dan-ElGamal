"""
================================================================================
MODUL 2: KRIPTOGRAFI ASIMETRIS ELGAMAL (FROM SCRATCH)
Mata Kuliah: Kriptografi
Implementasi: Key Generation, Blok Numerik, Enkripsi, Dekripsi & Tracer
================================================================================
"""

import random
from crypto_math import (
    mod_pow,
    mod_inverse,
    mod_inverse_fermat,
    gcd,
    is_prime,
    is_primitive_root,
    get_prime_factors,
    find_primitive_roots,
    generate_prime,
)


class ElGamalCryptosystem:
    """
    Implementasi sistem kriptografi kunci publik ElGamal dari nol.
    
    Tiga tahap utama:
    1. Key Generation (Pembangkitan Kunci oleh Penerima - Alice):
       - Parameter Publik: Prima p dan Akar Primitif g.
       - Kunci Privat Alice: x (1 < x < p - 1).
       - Kunci Publik Alice: y = (g^x) mod p.
       - Kunci Publik = (y, g, p), Kunci Privat = x.
       
    2. Enkripsi (oleh Pengirim - Bob):
       - Memetakan teks ke blok numerik m_i < p.
       - Untuk tiap blok m_i, pilih k_i acak dengan gcd(k_i, p-1) == 1.
       - Hitung pasangan cipher (a_i, b_i):
         a_i = (g^k_i) mod p
         b_i = (y^k_i * m_i) mod p
         
    3. Dekripsi (oleh Penerima - Alice):
       - Menggunakan kunci privat x untuk menghitung:
         m_i = (b_i * (a_i^x)^(-1)) mod p = (b_i * a_i^(p - 1 - x)) mod p
       - Rekonstruksi m_i kembali ke karakter teks.
    """

    PRESET_VIDEO = {
        "p": 2273,
        "g": 3,
        "x": 243,
        "plaintext": "HALO",
        "preset_k": 1463,  # Nilai k acak dari contoh slide/video perkuliahan
    }

    def __init__(self, p: int = 2273, g: int = 3, x: int = 243):
        self.p = p
        self.g = g
        self.x = x  # Kunci privat
        self.y = None  # Kunci publik y = g^x mod p
        if self.p and self.g and self.x:
            self.compute_public_key()

    def validate_keys(self) -> tuple[bool, list[str]]:
        """
        Memvalidasi kelayakan parameter kunci ElGamal.
        """
        errors = []
        if not is_prime(self.p):
            errors.append(f"p = {self.p} bukan bilangan prima!")

        is_root, _ = is_primitive_root(self.g, self.p)
        if not is_root:
            errors.append(f"g = {self.g} bukan akar primitif modulo {self.p}!")

        if not (1 < self.x < self.p - 1):
            errors.append(f"Kunci privat x = {self.x} harus memenuhi 1 < x < {self.p - 1}!")

        return len(errors) == 0, errors

    def compute_public_key(self) -> int:
        """
        Menghitung kunci publik y = (g^x) mod p.
        """
        is_ok, errs = self.validate_keys()
        if not is_ok:
            raise ValueError("Kunci tidak valid: " + "; ".join(errs))
        self.y = mod_pow(self.g, self.x, self.p)
        return self.y

    # =========================================================================
    # KONVERSI TEKS KE BLOK NUMERIK DAN SEBALIKNYA
    # =========================================================================

    @staticmethod
    def text_to_blocks_2char(
        text: str, p: int, pad_char: str = "X"
    ) -> tuple[str, list[dict]]:
        """
        Memetakan teks ke blok 2-karakter alfabet:
        A=00, B=01, ..., Z=25.
        Contoh:
        'HA' -> H=07, A=00 -> "0700" -> integer 700.
        'LO' -> L=11, O=14 -> "1114" -> integer 1114.
        
        Return:
            (sanitized_text, list_of_block_info)
        """
        # Bersihkan hanya huruf A-Z kapital
        clean = "".join([c.upper() for c in text if c.isalpha()])
        if not clean:
            raise ValueError("Plainteks tidak mengandung huruf alfabet valid!")

        # Padding jika panjang ganjil
        padded_text = clean
        if len(padded_text) % 2 != 0:
            padded_text += pad_char

        blocks = []
        for i in range(0, len(padded_text), 2):
            chunk = padded_text[i : i + 2]
            c1 = ord(chunk[0]) - ord("A")
            c2 = ord(chunk[1]) - ord("A")
            num_str = f"{c1:02d}{c2:02d}"
            val = int(num_str)
            if val >= p:
                raise ValueError(
                    f"Blok '{chunk}' bernilai {val} >= p ({p})! "
                    f"Nilai blok harus m_i < p. Gunakan prima p yang lebih besar "
                    f"(p > 2525) atau gunakan mode 1 karakter per blok."
                )
            blocks.append(
                {
                    "index": i // 2 + 1,
                    "text": chunk,
                    "c1_char": chunk[0],
                    "c1_val": c1,
                    "c2_char": chunk[1],
                    "c2_val": c2,
                    "num_str": num_str,
                    "m": val,
                }
            )

        return padded_text, blocks

    @staticmethod
    def blocks_to_text_2char(m_list: list[int]) -> str:
        """
        Rekonstruksi kembali blok integer menjadi teks:
        m = 700 -> "0700" -> 07 ('H') + 00 ('A') -> 'HA'
        m = 1114 -> "1114" -> 11 ('L') + 14 ('O') -> 'LO'
        """
        chars = []
        for val in m_list:
            s = f"{val:04d}"
            c1 = int(s[:2])
            c2 = int(s[2:])
            chars.append(chr(ord("A") + c1))
            chars.append(chr(ord("A") + c2))
        return "".join(chars)

    @staticmethod
    def text_to_blocks_1char(text: str, p: int) -> tuple[str, list[dict]]:
        """
        Mode 1 Karakter per blok (A=00 .. Z=25).
        Aman untuk sembarang prima p > 25.
        """
        clean = "".join([c.upper() for c in text if c.isalpha()])
        if not clean:
            raise ValueError("Plainteks tidak mengandung huruf alfabet valid!")

        blocks = []
        for i, ch in enumerate(clean):
            val = ord(ch) - ord("A")
            if val >= p:
                raise ValueError(f"Karakter '{ch}' bernilai {val} >= p ({p})!")
            blocks.append(
                {
                    "index": i + 1,
                    "text": ch,
                    "c1_char": ch,
                    "c1_val": val,
                    "c2_char": "",
                    "c2_val": 0,
                    "num_str": f"{val:02d}",
                    "m": val,
                }
            )
        return clean, blocks

    @staticmethod
    def blocks_to_text_1char(m_list: list[int]) -> str:
        """
        Rekonstruksi mode 1 karakter per blok.
        """
        return "".join([chr(ord("A") + val) for val in m_list])

    # =========================================================================
    # ENKRIPSI DAN DEKRIPSI
    # =========================================================================

    def pick_random_k(self) -> int:
        """
        Memilih bilangan acak k pada interval [2, p - 2]
        yang memenuhi syarat gcd(k, p - 1) == 1.
        """
        phi = self.p - 1
        for _ in range(10000):
            k = random.randint(2, phi - 1)
            if gcd(k, phi) == 1:
                return k
        # Fallback deterministik jika range sempit
        for k in range(2, phi):
            if gcd(k, phi) == 1:
                return k
        raise ValueError("Gagal menemukan nilai k yang relatif prima dengan p-1.")

    def encrypt(
        self,
        text: str,
        mode: str = "2char",
        custom_k_list: list[int] | int | None = None,
    ) -> dict:
        """
        Mengenkrpsi teks plainteks menjadi pasangan ciphertext (a_i, b_i).
        
        Parameter:
            text: Plainteks (misal 'HALO')
            mode: '2char' (2 karakter per blok) atau '1char' (1 karakter per blok)
            custom_k_list: Nilai k tertentu (misal 1463 untuk preset video)
        """
        self.compute_public_key()

        if mode == "2char":
            processed_text, blocks = self.text_to_blocks_2char(text, self.p)
        else:
            processed_text, blocks = self.text_to_blocks_1char(text, self.p)

        cipher_pairs = []
        block_logs = []

        for idx, blk in enumerate(blocks):
            m_i = blk["m"]
            # Tentukan nilai k_i
            if custom_k_list is not None:
                if isinstance(custom_k_list, list):
                    k_i = custom_k_list[idx % len(custom_k_list)]
                else:
                    k_i = int(custom_k_list)
            else:
                k_i = self.pick_random_k()

            # Verifikasi k_i
            if not (1 < k_i < self.p - 1):
                raise ValueError(f"Nilai k={k_i} harus memenuhi 1 < k < {self.p - 1}!")
            if gcd(k_i, self.p - 1) != 1:
                # Catatan edukasi: secara teori dasar ElGamal standar, gcd(k, p-1)=1
                # disarankan agar pemetaan bijektif jika k dipakai sebagai eksponen.
                pass

            # Hitung pasangan ciphertext (a, b)
            # a_i = (g^k_i) mod p
            a_i = mod_pow(self.g, k_i, self.p)

            # b_i = (y^k_i * m_i) mod p
            y_pow_k = mod_pow(self.y, k_i, self.p)
            b_i = (y_pow_k * m_i) % self.p

            cipher_pairs.append((a_i, b_i))
            block_logs.append(
                {
                    "index": blk["index"],
                    "chunk": blk["text"],
                    "m_i": m_i,
                    "k_i": k_i,
                    "g^k_mod_p": a_i,
                    "y^k_mod_p": y_pow_k,
                    "a_i": a_i,
                    "b_i": b_i,
                }
            )

        return {
            "mode": mode,
            "original_text": text,
            "processed_text": processed_text,
            "blocks": blocks,
            "cipher_pairs": cipher_pairs,
            "block_logs": block_logs,
            "p": self.p,
            "g": self.g,
            "y": self.y,
        }

    def decrypt(
        self,
        cipher_pairs: list[tuple[int, int]],
        mode: str = "2char",
    ) -> dict:
        """
        Mendekripsi pasangan ciphertext (a_i, b_i) menggunakan kunci privat x:
        m_i = (b_i * (a_i^x)^(-1)) mod p = (b_i * a_i^(p - 1 - x)) mod p
        """
        if self.x is None or not (1 < self.x < self.p - 1):
            raise ValueError(f"Kunci privat x = {self.x} tidak valid!")

        decrypted_m = []
        block_logs = []

        for idx, (a_i, b_i) in enumerate(cipher_pairs):
            # Cara 1: Menggunakan Teorema Fermat (a_i^(p - 1 - x) mod p)
            fermat_exp = self.p - 1 - self.x
            inv_ax_fermat = mod_pow(a_i, fermat_exp, self.p)
            m_fermat = (b_i * inv_ax_fermat) % self.p

            # Cara 2: Menggunakan Extended Euclidean Algorithm
            ax = mod_pow(a_i, self.x, self.p)
            inv_ax_euclid = mod_inverse(ax, self.p)
            m_euclid = (b_i * inv_ax_euclid) % self.p

            decrypted_m.append(m_fermat)
            block_logs.append(
                {
                    "index": idx + 1,
                    "a_i": a_i,
                    "b_i": b_i,
                    "a_pow_x": ax,
                    "fermat_exp": fermat_exp,
                    "inv_ax": inv_ax_fermat,
                    "m_i": m_fermat,
                    "check_match": (m_fermat == m_euclid),
                }
            )

        if mode == "2char":
            restored_text = self.blocks_to_text_2char(decrypted_m)
        else:
            restored_text = self.blocks_to_text_1char(decrypted_m)

        return {
            "mode": mode,
            "cipher_pairs": cipher_pairs,
            "decrypted_m": decrypted_m,
            "restored_text": restored_text,
            "block_logs": block_logs,
        }

    # =========================================================================
    # GENERATOR LOG TRANSPARAN LENGKAP
    # =========================================================================

    def generate_detailed_log(
        self, enc_res: dict, dec_res: dict
    ) -> str:
        """
        Menghasilkan catatan teks komprehensif dari setiap rumus,
        perhitungan modular per blok, hingga pemulihan pesan teks.
        """
        lines = []
        lines.append("=" * 80)
        lines.append("           SIMULASI LENGKAP KRIPTOSISTEM ASIMETRIS ELGAMAL")
        lines.append("=" * 80)
        lines.append("")
        lines.append("1. PEMBANGKITAN KUNCI (KEY GENERATION - ALICE)")
        lines.append(f"   • Bilangan Prima Modulus (p) : {self.p}")
        lines.append(f"   • Akar Primitif / Generator (g) : {self.g}")
        lines.append(f"   • Kunci Privat Alice (x)      : {self.x}  (1 < x < {self.p - 1})")
        lines.append(f"   • Kalkulasi Kunci Publik Alice:")
        lines.append(f"     Rumus : y = (g^x) mod p")
        lines.append(f"     Hitung: y = ({self.g}^{self.x}) mod {self.p}")
        lines.append(f"     Hasil : y = {self.y}")
        lines.append(f"   • Pasangan Kunci Terbentuk:")
        lines.append(f"     -> Kunci Publik Alice : (y = {self.y}, g = {self.g}, p = {self.p})")
        lines.append(f"     -> Kunci Privat Alice : x = {self.x}")
        lines.append("")
        lines.append("2. PERSIAPAN PESAN & PEMBAGIAN BLOK (MESSAGE ENCODING)")
        lines.append(f"   • Teks Asli        : '{enc_res['original_text']}'")
        lines.append(f"   • Teks Terproses   : '{enc_res['processed_text']}'")
        lines.append(f"   • Skema Pemetaan   : Alfabet A=00, B=01, ..., Z=25")
        lines.append(f"   • Mode Pembagian   : {enc_res['mode']} (2 karakter per blok)")
        for blk in enc_res["blocks"]:
            if enc_res["mode"] == "2char":
                lines.append(
                    f"     Blok #{blk['index']} : '{blk['text']}' "
                    f"-> '{blk['c1_char']}'({blk['c1_val']:02d}) + '{blk['c2_char']}'({blk['c2_val']:02d}) "
                    f"-> \"{blk['num_str']}\" -> Integer m_{blk['index']} = {blk['m']} (< {self.p} : OK)"
                )
            else:
                lines.append(
                    f"     Blok #{blk['index']} : '{blk['text']}' "
                    f"-> '{blk['c1_char']}'({blk['c1_val']:02d}) "
                    f"-> Integer m_{blk['index']} = {blk['m']} (< {self.p} : OK)"
                )
        lines.append("")
        lines.append("3. ENKRIPSI PESAN PER BLOK (ENCRYPTION - BOB)")
        lines.append("   Rumus per blok m_i dengan bilangan acak k_i:")
        lines.append("     a_i = (g^k_i) mod p")
        lines.append("     b_i = (y^k_i * m_i) mod p")
        lines.append("-" * 80)
        for log in enc_res["block_logs"]:
            idx = log["index"]
            lines.append(f"   [BLOK #{idx} : '{log['chunk']}' -> m_{idx} = {log['m_i']}]")
            lines.append(f"   • Pilih Bilangan Acak (k_{idx}) : {log['k_i']}")
            lines.append(f"   • Hitung a_{idx} = (g^k_{idx}) mod p")
            lines.append(f"     a_{idx} = ({self.g}^{log['k_i']}) mod {self.p} = {log['a_i']}")
            lines.append(f"   • Hitung y^k_{idx} mod p = ({self.y}^{log['k_i']}) mod {self.p} = {log['y^k_mod_p']}")
            lines.append(f"   • Hitung b_{idx} = (y^k_{idx} * m_{idx}) mod p")
            lines.append(
                f"     b_{idx} = ({log['y^k_mod_p']} * {log['m_i']}) mod {self.p} = {log['b_i']}"
            )
            lines.append(f"   -> Pasangan Ciphertext #{idx} : c_{idx} = ({log['a_i']}, {log['b_i']})")
            lines.append("")

        lines.append("4. HASIL KESELURUHAN CIPHERTEXT:")
        cipher_str = ", ".join([f"({a}, {b})" for a, b in enc_res["cipher_pairs"]])
        lines.append(f"   C = [ {cipher_str} ]")
        lines.append("")
        lines.append("5. DEKRIPSI PESAN PER BLOK (DECRYPTION - ALICE)")
        lines.append("   Alice menggunakan Kunci Privat x = " + str(self.x) + ":")
        lines.append("   Rumus: m_i = (b_i * (a_i^x)^(-1)) mod p")
        lines.append(f"   Dengan Teorema Fermat: a_i^(-x) mod p ≡ a_i^(p - 1 - x) mod p")
        lines.append(f"   Eksponen Fermat: p - 1 - x = {self.p} - 1 - {self.x} = {self.p - 1 - self.x}")
        lines.append("-" * 80)
        for dlog in dec_res["block_logs"]:
            idx = dlog["index"]
            lines.append(f"   [DEKRIPSI BLOK #{idx} : Cipher (a_{idx}={dlog['a_i']}, b_{idx}={dlog['b_i']})]")
            lines.append(f"   • Hitung a_{idx}^x mod p = ({dlog['a_i']}^{self.x}) mod {self.p} = {dlog['a_pow_x']}")
            lines.append(
                f"   • Hitung Balikan Modular (a_{idx}^x)^(-1) mod p = "
                f"({dlog['a_i']}^{dlog['fermat_exp']}) mod {self.p} = {dlog['inv_ax']}"
            )
            lines.append(
                f"   • Hitung m_{idx} = (b_{idx} * {dlog['inv_ax']}) mod {self.p} "
                f"= ({dlog['b_i']} * {dlog['inv_ax']}) mod {self.p} = {dlog['m_i']}"
            )
            lines.append(f"   -> Nilai Terpulihkan : m_{idx} = {dlog['m_i']}")
            lines.append("")

        lines.append("6. REKONSTRUKSI PLAINTEKS DARI BLOK NUMERIK:")
        lines.append(f"   • Himpunan Blok Terdekripsi : {dec_res['decrypted_m']}")
        lines.append(f"   • Rekonstruksi Karakter    : '{dec_res['restored_text']}'")
        match = (enc_res["processed_text"] == dec_res["restored_text"])
        lines.append(f"   • Status Kesesuaian Pesan  : {'SUKSES PERSIS (MATCH)' if match else 'GAGAL'}")
        lines.append("=" * 80)
        return "\n".join(lines)

    @classmethod
    def generate_random_valid(cls) -> "ElGamalCryptosystem":
        """
        Membangkitkan pasangan parameter ElGamal acak yang valid.
        """
        p = generate_prime(2000, 5000)
        roots = find_primitive_roots(p, max_count=5)
        if not roots:
            p = 2273
            roots = [3]
        g = random.choice(roots)
        x = random.randint(2, p - 2)
        return cls(p=p, g=g, x=x)
