"""
================================================================================
APLIKASI UTAMA TUGAS BESAR KRIPTOGRAFI
Judul: Implementasi Algoritma Pertukaran Kunci Diffie-Hellman dan Kriptografi Asimetris ElGamal
Implementasi: FROM SCRATCH (Murni tanpa library kriptografi eksternal)
Teknologi: Python 3 Standard Library (tkinter, math, random, unittest)

Kelompok Mahasiswa:
1. Muhammad Fachry Shalahuddin Rusamsi - 5027241031
2. Prabaswara Febrian Winandika - 5027241069
3. Gemilang Ananda Lingua - 5027241072
Departemen Teknologi Informasi - Institut Teknologi Sepuluh Nopember (ITS)
================================================================================
Cara Menjalankan:
1. Mode GUI Desktop (Default):
   python main.py

2. Mode Pengujian Otomatis (Unit Testing):
   python main.py --test

3. Mode Demonstrasi Terminal (CLI Quick Run):
   python main.py --cli
================================================================================
"""

import sys
import argparse


def run_gui():
    """Meluncurkan antarmuka grafis (GUI) KriptoLab."""
    try:
        from gui import ModernCryptoGUI
        app = ModernCryptoGUI()
        app.mainloop()
    except Exception as e:
        print(f"Error saat meluncurkan GUI: {e}")
        print("Menjalankan mode demonstrasi CLI sebagai alternatif...\n")
        run_cli_demo()


def run_unit_tests():
    """Menjalankan seluruh pengujian matematika dan kriptografi otomatis."""
    import unittest
    from test_crypto import TestCryptoMath, TestDiffieHellman, TestElGamal

    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCryptoMath))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDiffieHellman))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestElGamal))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


def run_cli_demo():
    """Menjalankan demonstrasi langsung di terminal console."""
    from diffie_hellman import DiffieHellmanSimulator
    from elgamal import ElGamalCryptosystem

    print("=" * 80)
    print("      DEMONSTRASI TERMINAL: DIFFIE-HELLMAN & ELGAMAL (FROM SCRATCH)")
    print("=" * 80)

    # 1. Diffie-Hellman Preset
    print("\n--- [1] MODUL 1: DIFFIE-HELLMAN KEY EXCHANGE ---")
    dh = DiffieHellmanSimulator(p=251, g=6, x=124, y=158)
    dh_res = dh.execute()
    print(f"Parameter Publik : Prima p = {dh.p}, Akar Primitif g = {dh.g}")
    print(f"Kunci Privat     : Alice x = {dh.x}, Bob y = {dh.y}")
    print(f"Kunci Publik     : Alice X = {dh_res['X']}, Bob Y = {dh_res['Y']}")
    print(f"Kunci Sesi Ka    : {dh_res['Ka']} (Dihitung Alice: Y^x mod p)")
    print(f"Kunci Sesi Kb    : {dh_res['Kb']} (Dihitung Bob:   X^y mod p)")
    print(f"Status Match     : {dh_res['match']} (Ka == Kb)")

    # 2. ElGamal Preset
    print("\n--- [2] MODUL 2: KRIPTOSISTEM ASIMETRIS ELGAMAL ---")
    eg = ElGamalCryptosystem(p=2273, g=3, x=243)
    print(f"Keygen Alice     : Prima p = {eg.p}, Akar Primitif g = {eg.g}, Kunci Privat x = {eg.x}")
    print(f"Kunci Publik     : y = (g^x) mod p = (3^243) mod 2273 = {eg.y}")

    plaintext = "HALO"
    print(f"\nPlainteks        : '{plaintext}'")
    enc_res = eg.encrypt(plaintext, mode="2char", custom_k_list=1463)
    for blk in enc_res["blocks"]:
        print(f"  Blok #{blk['index']} '{blk['text']}' -> Integer m_{blk['index']} = {blk['m']}")

    print(f"Ciphertext Pasangan (a, b) : {enc_res['cipher_pairs']}")

    dec_res = eg.decrypt(enc_res["cipher_pairs"], mode="2char")
    print(f"Blok Terdekripsi m_i       : {dec_res['decrypted_m']}")
    print(f"Plainteks Terpulihkan      : '{dec_res['restored_text']}'")
    print(f"Status Kesesuaian          : {'COCOK (SUCCESS)' if plaintext == dec_res['restored_text'] else 'GAGAL'}")
    print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Aplikasi Simulator Diffie-Hellman & ElGamal (From Scratch)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Jalankan rangkaian unit testing otomatis",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Jalankan demonstrasi terminal CLI",
    )

    args = parser.parse_args()

    if args.test:
        run_unit_tests()
    elif args.cli:
        run_cli_demo()
    else:
        run_gui()


if __name__ == "__main__":
    main()
