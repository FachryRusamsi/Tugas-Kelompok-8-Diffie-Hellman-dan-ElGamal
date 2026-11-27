"""
================================================================================
MODUL MATEMATIKA KRIPTOGRAFI DARI NOL (FROM SCRATCH)
Mata Kuliah: Kriptografi
Implementasi: Diffie-Hellman Key Exchange & Kriptografi Asimetris ElGamal

Muhammad Fachry Shalahuddin Rusamsi - 5027241031
Prabaswara Febrian Winandika - 5027241069
Gemilang Ananda Lingua - 5027241072
================================================================================
"""

import math
import random


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Menghitung pemangkatan modular (base^exp) % mod secara efisien
    menggunakan Algoritma Square-and-Multiply (Binary Exponentiation).
    
    Kompleksitas Waktu: O(log exp)
    Kompleksitas Ruang: O(1)
    
    Langkah:
    1. Nyatakan exp dalam representasi biner.
    2. Iterasi bit dari yang paling tidak signifikan (LSB) ke paling signifikan (MSB),
       atau dari MSB ke LSB.
    3. Jika bit bernilai 1, kalikan hasil dengan base saat ini (Multiply).
    4. Kuadratkan base untuk bit berikutnya (Square).
    """
    if mod <= 0:
        raise ValueError("Modulus harus berupa bilangan bulat positif (> 0).")
    if mod == 1:
        return 0
    if exp < 0:
        # Jika eksponen negatif: base^exp mod m = (base^(-1))^(-exp) mod m
        inv_base = mod_inverse(base % mod, mod)
        return mod_pow(inv_base, -exp, mod)
    
    result = 1
    base = base % mod
    current_exp = exp

    while current_exp > 0:
        # Jika bit paling kanan adalah 1 (Multiply step)
        if current_exp & 1:
            result = (result * base) % mod
        # Kuadratkan base untuk iterasi berikutnya (Square step)
        base = (base * base) % mod
        # Geser bit ke kanan (current_exp //= 2)
        current_exp >>= 1

    return result


def mod_pow_trace(base: int, exp: int, mod: int) -> tuple[int, list[dict]]:
    """
    Versi mod_pow yang mengembalikan jejak (trace) eksekusi
    langkah-demi-langkah dari Algoritma Square-and-Multiply untuk edukasi.
    """
    if mod <= 0:
        raise ValueError("Modulus harus berupa bilangan bulat positif.")
    if mod == 1:
        return 0, []

    steps = []
    result = 1
    current_base = base % mod
    temp_exp = exp
    step_num = 1

    binary_str = bin(exp)[2:]

    while temp_exp > 0:
        bit = temp_exp & 1
        mul_action = "Tidak (bit=0)"
        old_res = result
        if bit == 1:
            result = (result * current_base) % mod
            mul_action = f"Ya: ({old_res} × {current_base}) mod {mod} = {result}"
        
        old_base = current_base
        new_base = (current_base * current_base) % mod
        
        steps.append({
            "step": step_num,
            "bit": bit,
            "exp_remaining": temp_exp,
            "multiply_action": mul_action,
            "result_after": result,
            "square_action": f"({old_base}² ) mod {mod} = {new_base}",
            "base_next": new_base
        })
        
        current_base = new_base
        temp_exp >>= 1
        step_num += 1

    return result, steps


def gcd(a: int, b: int) -> int:
    """
    Algoritma Euclidean standar untuk mencari Faktor Persekutuan Terbesar (FPB/GCD).
    gcd(a, b) = gcd(b, a % b) sampai b = 0.
    
    Kompleksitas Waktu: O(log(min(a, b)))
    """
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def ext_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Algoritma Euclidean Diperluas (Extended Euclidean Algorithm).
    Mencari gcd(a, b) beserta koefisien Bezout x dan y sedemikian rupa sehingga:
        a*x + b*y = gcd(a, b)
        
    Kompleksitas Waktu: O(log(min(a, b)))
    Return:
        (g, x, y) di mana g = gcd(a, b)
    """
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    orig_a, orig_b = a, b
    
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        
    return a, x0, y0


def mod_inverse(a: int, m: int) -> int:
    """
    Menghitung balikan modular a^(-1) mod m menggunakan
    Extended Euclidean Algorithm.
    
    Syarat: gcd(a, m) == 1. Jika tidak koprima, balikan modular tidak ada.
    """
    a = (a % m + m) % m
    g, x, _ = ext_gcd(a, m)
    if g != 1:
        raise ValueError(
            f"Balikan modular tidak ditemukan karena FPB({a}, {m}) = {g} != 1 (bukan koprima)."
        )
    return (x % m + m) % m


def mod_inverse_fermat(a: int, p: int) -> int:
    """
    Menghitung balikan modular a^(-1) mod p menggunakan
    Teorema Kecil Fermat (Fermat's Little Theorem):
        a^(p-1) ≡ 1 (mod p)   [jika p prima dan a bukan kelipatan p]
        a * a^(p-2) ≡ 1 (mod p)
        Maka: a^(-1) ≡ a^(p-2) (mod p)
    """
    if not is_prime(p):
        raise ValueError(f"Modulus p={p} harus merupakan bilangan prima untuk Teorema Fermat.")
    if a % p == 0:
        raise ValueError(f"a={a} tidak boleh merupakan kelipatan prima p={p}.")
    return mod_pow(a, p - 2, p)


def is_prime(n: int) -> bool:
    """
    Pengujian bilangan prima deterministik dari nol:
    - Eliminasi angka <= 1, genap selain 2, kelipatan 3 selain 3.
    - Pengujian pembagian bentuk 6k ± 1 hingga sqrt(n).
    
    Cepat dan akurat untuk bilangan integer yang umum dipakai dalam simulasi.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def get_prime_factors(n: int) -> list[int]:
    """
    Mencari daftar faktor-faktor prima unik dari sebuah bilangan n secara manual.
    Digunakan dalam pengujian akar primitif (primitive root).
    """
    factors = set()
    temp = abs(n)
    
    # Faktor 2
    if temp % 2 == 0:
        factors.add(2)
        while temp % 2 == 0:
            temp //= 2
            
    # Faktor bilangan ganjil 3, 5, 7, ...
    d = 3
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 2
        
    if temp > 1:
        factors.add(temp)
        
    return sorted(list(factors))


def is_primitive_root(g: int, p: int) -> tuple[bool, str]:
    """
    Memverifikasi apakah g adalah akar primitif (primitive root / generator)
    dari bilangan prima p.
    
    Definisi Matematis:
    Sebuah bilangan g adalah akar primitif modulo prima p jika dan hanya jika:
    1. 1 < g < p
    2. gcd(g, p) == 1
    3. Untuk setiap faktor prima q dari (p - 1):
       g^((p - 1) / q) % p != 1
       
    Return:
        (is_root, keterangan_detail)
    """
    if not is_prime(p):
        return False, f"Modulus p = {p} bukan bilangan prima!"
    if g <= 1 or g >= p:
        return False, f"Nilai g = {g} harus berada pada rentang 1 < g < {p}!"
    if gcd(g, p) != 1:
        return False, f"Nilai g = {g} tidak relatif prima dengan p = {p} (FPB != 1)!"

    phi = p - 1
    factors = get_prime_factors(phi)
    
    details = [f"ϕ(p) = p - 1 = {phi}", f"Faktor prima dari {phi}: {factors}"]
    
    for q in factors:
        exp = phi // q
        val = mod_pow(g, exp, p)
        details.append(f"Uji faktor q={q}: {g}^({phi}/{q}) mod {p} = {g}^{exp} mod {p} = {val}")
        if val == 1:
            details.append(
                f"-> GAGAL: {g}^{exp} ≡ 1 mod {p}. Ordo dari {g} membagi {exp} < {phi}."
            )
            return False, "\n".join(details)

    details.append(f"-> VALID: Seluruh uji g^((p-1)/q) ≢ 1 mod {p}. Maka g = {g} adalah AKAR PRIMITIF.")
    return True, "\n".join(details)


def find_primitive_roots(p: int, max_count: int = 10) -> list[int]:
    """
    Mencari daftar akar-akar primitif untuk bilangan prima p (hingga batas max_count).
    """
    if not is_prime(p):
        return []
    
    roots = []
    phi = p - 1
    factors = get_prime_factors(phi)
    
    for g in range(2, p):
        is_root = True
        for q in factors:
            if mod_pow(g, phi // q, p) == 1:
                is_root = False
                break
        if is_root:
            roots.append(g)
            if len(roots) >= max_count:
                break
                
    return roots


def generate_prime(min_val: int = 200, max_val: int = 5000) -> int:
    """
    Membangkitkan sebuah bilangan prima acak dari nol pada selang [min_val, max_val].
    """
    candidates = list(range(min_val if min_val % 2 == 1 else min_val + 1, max_val + 1, 2))
    random.shuffle(candidates)
    for c in candidates:
        if is_prime(c):
            return c
    # Fallback jika range sempit
    for c in range(min_val, max_val + 1):
        if is_prime(c):
            return c
    raise ValueError(f"Tidak ada bilangan prima pada rentang [{min_val}, {max_val}].")
