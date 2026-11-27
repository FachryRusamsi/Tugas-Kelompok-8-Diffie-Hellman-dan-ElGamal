"""
================================================================================
UNIT TESTING SUITE: CRYPTO MATH, DIFFIE-HELLMAN, & ELGAMAL
Memastikan keakuratan matematis dari seluruh fungsi scratch.
================================================================================
"""

import unittest
from crypto_math import (
    mod_pow,
    mod_pow_trace,
    gcd,
    ext_gcd,
    mod_inverse,
    mod_inverse_fermat,
    is_prime,
    is_primitive_root,
    get_prime_factors,
    find_primitive_roots,
    generate_prime,
)
from diffie_hellman import DiffieHellmanSimulator
from elgamal import ElGamalCryptosystem


class TestCryptoMath(unittest.TestCase):
    def test_mod_pow(self):
        # Basis test terhadap built-in pow()
        test_cases = [
            (3, 1463, 2273),
            (6, 124, 251),
            (6, 158, 251),
            (197, 124, 251),
            (209, 158, 251),
            (2, 10, 1000),
            (7, 0, 13),
            (0, 5, 17),
        ]
        for b, e, m in test_cases:
            self.assertEqual(mod_pow(b, e, m), pow(b, e, m))

    def test_mod_pow_trace(self):
        res, steps = mod_pow_trace(3, 13, 17)
        self.assertEqual(res, pow(3, 13, 17))
        self.assertTrue(len(steps) > 0)

    def test_gcd(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(101, 103), 1)
        self.assertEqual(gcd(250, 6), 2)

    def test_ext_gcd_and_mod_inverse(self):
        g, x, y = ext_gcd(35, 15)
        self.assertEqual(35 * x + 15 * y, g)
        self.assertEqual(g, 5)

        # Invers modular: 3 * inv ≡ 1 mod 11 -> 3 * 4 = 12 ≡ 1 mod 11
        inv = mod_inverse(3, 11)
        self.assertEqual(inv, 4)
        self.assertEqual((3 * inv) % 11, 1)

        # Fermat inverse
        inv_f = mod_inverse_fermat(3, 11)
        self.assertEqual(inv_f, 4)

    def test_is_prime(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 251, 2273, 7919]
        composites = [0, 1, 4, 6, 9, 15, 25, 100, 252, 2274]
        for p in primes:
            self.assertTrue(is_prime(p), f"{p} harusnya prima")
        for c in composites:
            self.assertFalse(is_prime(c), f"{c} harusnya komposit")

    def test_primitive_root(self):
        # 6 adalah akar primitif mod 251
        is_root_251, _ = is_primitive_root(6, 251)
        self.assertTrue(is_root_251)

        # 3 adalah akar primitif mod 2273
        is_root_2273, _ = is_primitive_root(3, 2273)
        self.assertTrue(is_root_2273)

        # 2 bukan akar primitif mod 7? (2^1=2, 2^2=4, 2^3=1 -> bukan, ord=3 < 6)
        is_root_2_7, _ = is_primitive_root(2, 7)
        self.assertFalse(is_root_2_7)
        # 3 adalah akar primitif mod 7: 3^1=3, 3^2=2, 3^3=6, 3^4=4, 3^5=5, 3^6=1
        is_root_3_7, _ = is_primitive_root(3, 7)
        self.assertTrue(is_root_3_7)


class TestDiffieHellman(unittest.TestCase):
    def test_preset_video(self):
        # p=251, g=6, x=124, y=158
        dh = DiffieHellmanSimulator(p=251, g=6, x=124, y=158)
        res = dh.execute()
        self.assertEqual(res["X"], 209)
        self.assertEqual(res["Y"], 197)
        self.assertEqual(res["Ka"], 79)
        self.assertEqual(res["Kb"], 79)
        self.assertTrue(res["match"])

    def test_random_simulation(self):
        dh = DiffieHellmanSimulator.generate_random_valid()
        res = dh.execute()
        self.assertTrue(res["match"])
        self.assertEqual(res["Ka"], res["Kb"])


class TestElGamal(unittest.TestCase):
    def test_preset_video(self):
        # p=2273, g=3, x=243, M='HALO'
        eg = ElGamalCryptosystem(p=2273, g=3, x=243)
        self.assertEqual(eg.y, 461)

        # Enkripsi dengan k=1463 (contoh slide ITB)
        enc = eg.encrypt("HALO", mode="2char", custom_k_list=1463)
        # Blok: 'HA' -> 700, 'LO' -> 1114
        self.assertEqual(enc["blocks"][0]["m"], 700)
        self.assertEqual(enc["blocks"][1]["m"], 1114)

        # Ciphertext blok 1: (1439, 74)
        # Ciphertext blok 2: (1439, 988)
        self.assertEqual(enc["cipher_pairs"][0], (1439, 74))
        self.assertEqual(enc["cipher_pairs"][1], (1439, 988))

        # Dekripsi
        dec = eg.decrypt(enc["cipher_pairs"], mode="2char")
        self.assertEqual(dec["decrypted_m"], [700, 1114])
        self.assertEqual(dec["restored_text"], "HALO")

    def test_random_encryption(self):
        eg = ElGamalCryptosystem(p=2273, g=3, x=243)
        enc = eg.encrypt("KRIPTOGRAFI", mode="2char")  # panjang 11 -> padded 'KRIPTOGRAFIX'
        dec = eg.decrypt(enc["cipher_pairs"], mode="2char")
        self.assertEqual(dec["restored_text"], "KRIPTOGRAFIX")


if __name__ == "__main__":
    unittest.main()
