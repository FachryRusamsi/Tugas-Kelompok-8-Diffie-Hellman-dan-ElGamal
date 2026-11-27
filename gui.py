"""
================================================================================
APLIKASI DESKTOP GUI KRIPTOGRAFI: DIFFIE-HELLMAN & ELGAMAL
Implementasi: Python Standar Tkinter & TTK
Tema: Dark Slate Modern KriptoLab
100% Standard Library Python (Tanpa Library Kriptografi Eksternal)
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random

# Import modul matematika dan kriptografi mandiri
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


class ModernCryptoGUI(tk.Tk):
    """
    Jendela Utama Aplikasi Desktop GUI KriptoLab.
    """

    # Skema Warna Modern Dark Mode
    THEME = {
        "bg_app": "#0b0f19",       # Dark canvas background
        "bg_card": "#151e32",      # Card surface background
        "bg_card_inner": "#1c2842",# Nested card background
        "bg_entry": "#0f172a",     # Input entry background
        "bg_log": "#090d16",       # Terminal / log background
        "border": "#283859",       # Border stroke
        "border_focus": "#6366f1", # Focused border
        "text_primary": "#f8fafc", # High-contrast text
        "text_secondary": "#94a3b8",# Medium-contrast text
        "text_muted": "#64748b",   # Low-contrast helper text
        "accent_primary": "#4f46e5",# Primary indigo
        "accent_hover": "#4338ca", # Darker indigo on hover
        "accent_cyan": "#06b6d4",   # Cyan accent
        "accent_gold": "#f59e0b",   # Amber / gold preset button
        "accent_gold_hover": "#d97706",
        "accent_green": "#10b981",  # Emerald green success
        "accent_rose": "#f43f5e",   # Rose red alert
        "code_keyword": "#38bdf8",  # Log highlight cyan
        "code_number": "#fbbf24",   # Log highlight yellow
        "code_success": "#34d399",  # Log highlight green
    }

    def __init__(self):
        super().__init__()

        # Pengaturan Windows High-DPI agar font tajam
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        self.title("KriptoLab: Simulator Diffie-Hellman & ElGamal (From Scratch)")
        self.geometry("1160x860")
        self.minsize(980, 720)
        self.configure(bg=self.THEME["bg_app"])

        # Inisialisasi simulator backend
        self.dh_sim = DiffieHellmanSimulator(251, 6, 124, 158)
        self.elgamal_sys = ElGamalCryptosystem(2273, 3, 243)
        self.last_elgamal_enc = None

        # Konfigurasi TTK Style
        self._setup_styles()

        # Bangun Komponen Tampilan
        self._build_header()
        self._build_tabs()
        self._build_footer()

    # =========================================================================
    # STYLING & DESAIN
    # =========================================================================

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Custom Notebook Tabs
        self.style.configure(
            "TNotebook",
            background=self.THEME["bg_app"],
            borderwidth=0,
            tabmargins=[10, 5, 10, 0],
        )
        self.style.configure(
            "TNotebook.Tab",
            background=self.THEME["bg_card"],
            foreground=self.THEME["text_secondary"],
            padding=[16, 8],
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            relief="flat",
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", self.THEME["accent_primary"])],
            foreground=[("selected", "#ffffff")],
        )

        # Labels
        self.style.configure(
            "TLabel",
            background=self.THEME["bg_card"],
            foreground=self.THEME["text_primary"],
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "CardTitle.TLabel",
            background=self.THEME["bg_card"],
            foreground=self.THEME["accent_cyan"],
            font=("Segoe UI", 11, "bold"),
        )
        self.style.configure(
            "Muted.TLabel",
            background=self.THEME["bg_card"],
            foreground=self.THEME["text_muted"],
            font=("Segoe UI", 9),
        )

    # =========================================================================
    # HEADER & FOOTER
    # =========================================================================

    def _build_header(self):
        header_frame = tk.Frame(self, bg=self.THEME["bg_app"], padx=20, pady=12)
        header_frame.pack(fill="x")

        # Title & Subtitle Frame
        title_box = tk.Frame(header_frame, bg=self.THEME["bg_app"])
        title_box.pack(side="left")

        title_lbl = tk.Label(
            title_box,
            text="🔐 KriptoLab: Diffie-Hellman & ElGamal",
            font=("Segoe UI", 16, "bold"),
            fg=self.THEME["text_primary"],
            bg=self.THEME["bg_app"],
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            title_box,
            text="Tugas Besar Kriptografi • Implementasi Asli (From Scratch) Murni Tanpa Library Eksternal",
            font=("Segoe UI", 9),
            fg=self.THEME["text_secondary"],
            bg=self.THEME["bg_app"],
        )
        sub_lbl.pack(anchor="w")

        # Badges di sisi kanan
        badges_box = tk.Frame(header_frame, bg=self.THEME["bg_app"])
        badges_box.pack(side="right")

        badges = [
            ("100% From Scratch", "#3b82f6"),
            ("Square-and-Multiply", "#10b981"),
            ("Extended Euclidean", "#8b5cf6"),
        ]
        for text, color in badges:
            lbl = tk.Label(
                badges_box,
                text=text,
                font=("Segoe UI", 8, "bold"),
                fg="#ffffff",
                bg=color,
                padx=8,
                pady=3,
            )
            lbl.pack(side="left", padx=4)

        # Separator line
        sep = tk.Frame(self, bg=self.THEME["border"], height=1)
        sep.pack(fill="x")

    def _build_footer(self):
        footer_frame = tk.Frame(self, bg=self.THEME["bg_app"], padx=20, pady=6)
        footer_frame.pack(fill="x", side="bottom")

        left_lbl = tk.Label(
            footer_frame,
            text="Status Engine: Standar Python 3 • Bebas Dependensi Eksternal",
            font=("Segoe UI", 8),
            fg=self.THEME["text_muted"],
            bg=self.THEME["bg_app"],
        )
        left_lbl.pack(side="left")

        right_lbl = tk.Label(
            footer_frame,
            text="Diffie-Hellman Key Exchange & ElGamal Asymmetric Cryptosystem",
            font=("Segoe UI", 8),
            fg=self.THEME["text_muted"],
            bg=self.THEME["bg_app"],
        )
        right_lbl.pack(side="right")

    # =========================================================================
    # TAB NOTEBOOK
    # =========================================================================

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=8)

        # Tab 1: Diffie-Hellman
        self.tab_dh = tk.Frame(self.notebook, bg=self.THEME["bg_app"])
        self.notebook.add(self.tab_dh, text=" 🔑 Modul 1: Diffie-Hellman ")
        self._init_dh_tab(self.tab_dh)

        # Tab 2: ElGamal
        self.tab_eg = tk.Frame(self.notebook, bg=self.THEME["bg_app"])
        self.notebook.add(self.tab_eg, text=" 🛡️ Modul 2: Kriptografi ElGamal ")
        self._init_elgamal_tab(self.tab_eg)

        # Tab 3: Matematika Dasar (Playground)
        self.tab_math = tk.Frame(self.notebook, bg=self.THEME["bg_app"])
        self.notebook.add(self.tab_math, text=" 📐 Playground Matematika (Scratch) ")
        self._init_math_tab(self.tab_math)

        # Tab 4: Panduan & Identitas Kelompok
        self.tab_about = tk.Frame(self.notebook, bg=self.THEME["bg_app"])
        self.notebook.add(self.tab_about, text=" 📖 Panduan Teori & Kelompok ")
        self._init_about_tab(self.tab_about)

    # =========================================================================
    # TAB 1: DIFFIE-HELLMAN KEY EXCHANGE
    # =========================================================================

    def _init_dh_tab(self, parent):
        # Gunakan paned window vertikal: Bagian atas kontrol/hasil, bagian bawah log
        paned = tk.PanedWindow(
            parent,
            orient=tk.VERTICAL,
            bg=self.THEME["bg_app"],
            sashwidth=6,
            bd=0,
        )
        paned.pack(fill="both", expand=True, padx=4, pady=4)

        top_container = tk.Frame(paned, bg=self.THEME["bg_app"])
        paned.add(top_container, height=360)

        # Layout 2 Kolom untuk Top Container
        top_container.columnconfigure(0, weight=1)
        top_container.columnconfigure(1, weight=1)
        top_container.rowconfigure(0, weight=1)

        # Card Kiri: Parameter Publik & Kunci Privat
        left_card = self._create_card(top_container)
        left_card.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        self._build_dh_input_card(left_card)

        # Card Kanan: Hasil Perhitungan & Status Sesi
        right_card = self._create_card(top_container)
        right_card.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)

        self._build_dh_results_card(right_card)

        # Container Bawah: Log Eksekusi
        bot_container = tk.Frame(paned, bg=self.THEME["bg_app"])
        paned.add(bot_container)

        self.dh_log = self._build_log_panel(bot_container, title="Catatan Eksekusi Diffie-Hellman Step-by-Step")

        # Load preset awal
        self._load_dh_preset()

    def _build_dh_input_card(self, parent):
        tk.Label(
            parent,
            text="1. Parameter Publik & Kunci Privat",
            font=("Segoe UI", 11, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=12, pady=(10, 6))

        # Grid form
        form_frame = tk.Frame(parent, bg=self.THEME["bg_card"])
        form_frame.pack(fill="x", padx=12, pady=4)
        form_frame.columnconfigure(1, weight=1)

        # p
        tk.Label(form_frame, text="Prima Modulus (p):", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=0, column=0, sticky="w", pady=4
        )
        self.dh_entry_p = self._create_entry(form_frame)
        self.dh_entry_p.grid(row=0, column=1, sticky="ew", padx=6, pady=4)

        # g
        tk.Label(form_frame, text="Akar Primitif (g):", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=1, column=0, sticky="w", pady=4
        )
        self.dh_entry_g = self._create_entry(form_frame)
        self.dh_entry_g.grid(row=1, column=1, sticky="ew", padx=6, pady=4)

        # Kunci Privat x (Alice)
        tk.Label(form_frame, text="Kunci Privat Alice (x):", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=2, column=0, sticky="w", pady=4
        )
        self.dh_entry_x = self._create_entry(form_frame)
        self.dh_entry_x.grid(row=2, column=1, sticky="ew", padx=6, pady=4)

        # Kunci Privat y (Bob)
        tk.Label(form_frame, text="Kunci Privat Bob (y):", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=3, column=0, sticky="w", pady=4
        )
        self.dh_entry_y = self._create_entry(form_frame)
        self.dh_entry_y.grid(row=3, column=1, sticky="ew", padx=6, pady=4)

        # Status validasi inline
        self.dh_status_lbl = tk.Label(
            parent,
            text="Parameter belum divalidasi.",
            font=("Segoe UI", 9, "italic"),
            fg=self.THEME["text_muted"],
            bg=self.THEME["bg_card"],
        )
        self.dh_status_lbl.pack(anchor="w", padx=12, pady=4)

        # Tombol-tombol Aksi
        btn_box = tk.Frame(parent, bg=self.THEME["bg_card"])
        btn_box.pack(fill="x", padx=12, pady=(6, 10))

        # Tombol Jalankan Simulasi
        btn_run = self._create_button(
            btn_box,
            text="🚀 Jalankan Simulasi",
            command=self._on_dh_run,
            bg=self.THEME["accent_primary"],
            fg="#ffffff",
        )
        btn_run.pack(side="left", padx=(0, 6))

        # Tombol Preset Video
        btn_preset = self._create_button(
            btn_box,
            text="✨ Load Contoh Video (p=251, g=6, x=124, y=158)",
            command=self._load_dh_preset,
            bg=self.THEME["accent_gold"],
            fg="#000000",
        )
        btn_preset.pack(side="left", padx=4)

        # Tombol Acak Parameter Valid
        btn_rand = self._create_button(
            btn_box,
            text="🎲 Acak Valid",
            command=self._on_dh_randomize,
            bg=self.THEME["bg_card_inner"],
            fg=self.THEME["text_secondary"],
        )
        btn_rand.pack(side="left", padx=4)

    def _build_dh_results_card(self, parent):
        tk.Label(
            parent,
            text="2. Hasil Kalkulasi & Sesi Bersama",
            font=("Segoe UI", 11, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=12, pady=(10, 6))

        # Grid box indikator
        grid_frame = tk.Frame(parent, bg=self.THEME["bg_card"])
        grid_frame.pack(fill="x", padx=12, pady=4)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Kartu Alice
        alice_box = tk.Frame(grid_frame, bg=self.THEME["bg_card_inner"], padx=10, pady=8, bd=1, relief="solid")
        alice_box.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        tk.Label(alice_box, text="Pihak Alice", font=("Segoe UI", 10, "bold"), fg=self.THEME["accent_cyan"], bg=self.THEME["bg_card_inner"]).pack(anchor="w")
        self.dh_lbl_X = tk.Label(alice_box, text="Kunci Publik (X): -", font=("Consolas", 10), fg=self.THEME["text_primary"], bg=self.THEME["bg_card_inner"])
        self.dh_lbl_X.pack(anchor="w", pady=2)
        self.dh_lbl_Ka = tk.Label(alice_box, text="Kunci Sesi (Ka): -", font=("Consolas", 10, "bold"), fg=self.THEME["accent_green"], bg=self.THEME["bg_card_inner"])
        self.dh_lbl_Ka.pack(anchor="w", pady=2)

        # Kartu Bob
        bob_box = tk.Frame(grid_frame, bg=self.THEME["bg_card_inner"], padx=10, pady=8, bd=1, relief="solid")
        bob_box.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)

        tk.Label(bob_box, text="Pihak Bob", font=("Segoe UI", 10, "bold"), fg=self.THEME["accent_cyan"], bg=self.THEME["bg_card_inner"]).pack(anchor="w")
        self.dh_lbl_Y = tk.Label(bob_box, text="Kunci Publik (Y): -", font=("Consolas", 10), fg=self.THEME["text_primary"], bg=self.THEME["bg_card_inner"])
        self.dh_lbl_Y.pack(anchor="w", pady=2)
        self.dh_lbl_Kb = tk.Label(bob_box, text="Kunci Sesi (Kb): -", font=("Consolas", 10, "bold"), fg=self.THEME["accent_green"], bg=self.THEME["bg_card_inner"])
        self.dh_lbl_Kb.pack(anchor="w", pady=2)

        # Badge Status Sesi Besar
        self.dh_session_badge = tk.Label(
            parent,
            text="Silakan jalankan simulasi pertukaran kunci.",
            font=("Segoe UI", 10, "bold"),
            fg=self.THEME["text_muted"],
            bg=self.THEME["bg_card_inner"],
            padx=12,
            pady=8,
            bd=1,
            relief="solid",
        )
        self.dh_session_badge.pack(fill="x", padx=16, pady=8)

        # Keterangan Formula
        info_txt = (
            "Formula Kunci Bersama:\n"
            "Ka = (Y^x) mod p = (g^y)^x mod p = g^(xy) mod p\n"
            "Kb = (X^y) mod p = (g^x)^y mod p = g^(xy) mod p\n"
            "Oleh karena perkalian skalar bersifat komutatif, maka Ka == Kb."
        )
        tk.Label(
            parent,
            text=info_txt,
            font=("Consolas", 8),
            fg=self.THEME["text_secondary"],
            bg=self.THEME["bg_card"],
            justify="left",
        ).pack(anchor="w", padx=14, pady=4)

    def _load_dh_preset(self):
        """Memuat contoh video: p=251, g=6, x=124, y=158."""
        self.dh_entry_p.delete(0, tk.END)
        self.dh_entry_p.insert(0, str(DiffieHellmanSimulator.PRESET_VIDEO["p"]))

        self.dh_entry_g.delete(0, tk.END)
        self.dh_entry_g.insert(0, str(DiffieHellmanSimulator.PRESET_VIDEO["g"]))

        self.dh_entry_x.delete(0, tk.END)
        self.dh_entry_x.insert(0, str(DiffieHellmanSimulator.PRESET_VIDEO["x"]))

        self.dh_entry_y.delete(0, tk.END)
        self.dh_entry_y.insert(0, str(DiffieHellmanSimulator.PRESET_VIDEO["y"]))

        self._on_dh_run()

    def _on_dh_randomize(self):
        """Membangkitkan parameter acak yang dijamin prima dan akar primitif valid."""
        sim = DiffieHellmanSimulator.generate_random_valid()
        self.dh_entry_p.delete(0, tk.END)
        self.dh_entry_p.insert(0, str(sim.p))
        self.dh_entry_g.delete(0, tk.END)
        self.dh_entry_g.insert(0, str(sim.g))
        self.dh_entry_x.delete(0, tk.END)
        self.dh_entry_x.insert(0, str(sim.x))
        self.dh_entry_y.delete(0, tk.END)
        self.dh_entry_y.insert(0, str(sim.y))
        self._on_dh_run()

    def _on_dh_run(self):
        """Membaca input, memvalidasi parameter, dan menjalankan simulasi DH."""
        try:
            p = int(self.dh_entry_p.get().strip())
            g = int(self.dh_entry_g.get().strip())
            x = int(self.dh_entry_x.get().strip())
            y = int(self.dh_entry_y.get().strip())
        except ValueError:
            messagebox.showerror("Error Input", "Seluruh parameter p, g, x, dan y harus berupa bilangan bulat (integer)!")
            return

        sim = DiffieHellmanSimulator(p, g, x, y)
        is_ok, errs = sim.validate()
        if not is_ok:
            self.dh_status_lbl.configure(text="❌ " + "; ".join(errs), fg=self.THEME["accent_rose"])
            messagebox.showwarning("Parameter Tidak Valid", "\n".join(errs))
            return

        self.dh_status_lbl.configure(
            text=f"✅ Parameter Valid! p={p} prima, g={g} akar primitif terverifikasi.",
            fg=self.THEME["accent_green"],
        )

        res = sim.execute()
        self.dh_lbl_X.configure(text=f"Kunci Publik (X): {res['X']}")
        self.dh_lbl_Y.configure(text=f"Kunci Publik (Y): {res['Y']}")
        self.dh_lbl_Ka.configure(text=f"Kunci Sesi (Ka): {res['Ka']}")
        self.dh_lbl_Kb.configure(text=f"Kunci Sesi (Kb): {res['Kb']}")

        if res["match"]:
            self.dh_session_badge.configure(
                text=f"🎉 SESI SIMETRIS BERHASIL TERBENTUK!\nKunci Sesi Bersama K = {res['Ka']}  (Ka == Kb)",
                fg=self.THEME["accent_green"],
            )
        else:
            self.dh_session_badge.configure(
                text="❌ Kunci Sesi Tidak Cocok!",
                fg=self.THEME["accent_rose"],
            )

        # Perbarui Log Step-by-Step
        log_text = sim.generate_detailed_log()
        self._write_log(self.dh_log, log_text)

    # =========================================================================
    # TAB 2: KRIPTOGRAFI ASIMETRIS ELGAMAL
    # =========================================================================

    def _init_elgamal_tab(self, parent):
        paned = tk.PanedWindow(
            parent,
            orient=tk.VERTICAL,
            bg=self.THEME["bg_app"],
            sashwidth=6,
            bd=0,
        )
        paned.pack(fill="both", expand=True, padx=4, pady=4)

        top_container = tk.Frame(paned, bg=self.THEME["bg_app"])
        paned.add(top_container, height=410)

        # 3 Kolom Alur ElGamal: Keygen -> Enkripsi -> Dekripsi
        top_container.columnconfigure(0, weight=1)
        top_container.columnconfigure(1, weight=1)
        top_container.columnconfigure(2, weight=1)
        top_container.rowconfigure(0, weight=1)

        # Card 1: Keygen Alice
        c1 = self._create_card(top_container)
        c1.grid(row=0, column=0, sticky="nsew", padx=3, pady=4)
        self._build_eg_keygen_card(c1)

        # Card 2: Enkripsi Bob
        c2 = self._create_card(top_container)
        c2.grid(row=0, column=1, sticky="nsew", padx=3, pady=4)
        self._build_eg_encrypt_card(c2)

        # Card 3: Dekripsi Alice
        c3 = self._create_card(top_container)
        c3.grid(row=0, column=2, sticky="nsew", padx=3, pady=4)
        self._build_eg_decrypt_card(c3)

        # Container Bawah: Log Eksekusi ElGamal
        bot_container = tk.Frame(paned, bg=self.THEME["bg_app"])
        paned.add(bot_container)

        self.eg_log = self._build_log_panel(bot_container, title="Catatan Eksekusi ElGamal Per-Blok (Transparan)")

        # Load preset awal ElGamal
        self._load_eg_preset()

    def _build_eg_keygen_card(self, parent):
        tk.Label(
            parent,
            text="A. Key Generation (Alice)",
            font=("Segoe UI", 11, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=10, pady=(8, 4))

        form = tk.Frame(parent, bg=self.THEME["bg_card"])
        form.pack(fill="x", padx=10, pady=2)
        form.columnconfigure(1, weight=1)

        # p
        tk.Label(form, text="Prima (p):", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=0, column=0, sticky="w", pady=3
        )
        self.eg_entry_p = self._create_entry(form)
        self.eg_entry_p.grid(row=0, column=1, sticky="ew", padx=4, pady=3)

        # g
        tk.Label(form, text="Akar Primitif (g):", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=1, column=0, sticky="w", pady=3
        )
        self.eg_entry_g = self._create_entry(form)
        self.eg_entry_g.grid(row=1, column=1, sticky="ew", padx=4, pady=3)

        # x
        tk.Label(form, text="Kunci Privat (x):", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=2, column=0, sticky="w", pady=3
        )
        self.eg_entry_x = self._create_entry(form)
        self.eg_entry_x.grid(row=2, column=1, sticky="ew", padx=4, pady=3)

        # Hasil y
        tk.Label(form, text="Kunci Publik (y):", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=3, column=0, sticky="w", pady=3
        )
        self.eg_lbl_y = tk.Label(
            form,
            text="-",
            font=("Consolas", 10, "bold"),
            fg=self.THEME["accent_green"],
            bg=self.THEME["bg_entry"],
            anchor="w",
            padx=6,
            pady=3,
        )
        self.eg_lbl_y.grid(row=3, column=1, sticky="ew", padx=4, pady=3)

        # Info Box Pasangan Kunci
        self.eg_lbl_keypairs = tk.Label(
            parent,
            text="Kunci Publik: (y, g, p)\nKunci Privat: x",
            font=("Segoe UI", 8),
            fg=self.THEME["text_secondary"],
            bg=self.THEME["bg_card_inner"],
            padx=8,
            pady=4,
        )
        self.eg_lbl_keypairs.pack(fill="x", padx=10, pady=4)

        # Tombol Aksi Keygen
        btn_box = tk.Frame(parent, bg=self.THEME["bg_card"])
        btn_box.pack(fill="x", padx=10, pady=6)

        btn_keygen = self._create_button(
            btn_box,
            text="🔑 Hitung Kunci Publik",
            command=self._on_eg_keygen,
            bg=self.THEME["accent_primary"],
            fg="#ffffff",
        )
        btn_keygen.pack(side="left", padx=(0, 4))

        btn_preset = self._create_button(
            btn_box,
            text="✨ Preset HALO",
            command=self._load_eg_preset,
            bg=self.THEME["accent_gold"],
            fg="#000000",
        )
        btn_preset.pack(side="left", padx=2)

        btn_rand = self._create_button(
            btn_box,
            text="🎲 Acak",
            command=self._on_eg_randomize,
            bg=self.THEME["bg_card_inner"],
            fg=self.THEME["text_secondary"],
        )
        btn_rand.pack(side="left", padx=2)

    def _build_eg_encrypt_card(self, parent):
        tk.Label(
            parent,
            text="B. Enkripsi Pesan (Bob)",
            font=("Segoe UI", 11, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=10, pady=(8, 4))

        form = tk.Frame(parent, bg=self.THEME["bg_card"])
        form.pack(fill="x", padx=10, pady=2)
        form.columnconfigure(1, weight=1)

        # Plainteks
        tk.Label(form, text="Plainteks:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=0, column=0, sticky="w", pady=3
        )
        self.eg_entry_msg = self._create_entry(form)
        self.eg_entry_msg.grid(row=0, column=1, sticky="ew", padx=4, pady=3)
        self.eg_entry_msg.insert(0, "HALO")

        # Mode Blok
        tk.Label(form, text="Mode Blok:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=1, column=0, sticky="w", pady=3
        )
        self.eg_block_mode = tk.StringVar(value="2char")
        mode_box = tk.Frame(form, bg=self.THEME["bg_card"])
        mode_box.grid(row=1, column=1, sticky="w", padx=4, pady=3)
        tk.Radiobutton(
            mode_box,
            text="2 Karakter (A=00..Z=25)",
            variable=self.eg_block_mode,
            value="2char",
            bg=self.THEME["bg_card"],
            fg=self.THEME["text_primary"],
            selectcolor=self.THEME["bg_entry"],
            activebackground=self.THEME["bg_card"],
        ).pack(side="left")

        # Bilangan Acak k
        tk.Label(form, text="Nilai k Acak:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).grid(
            row=2, column=0, sticky="w", pady=3
        )
        self.eg_entry_k = self._create_entry(form)
        self.eg_entry_k.grid(row=2, column=1, sticky="ew", padx=4, pady=3)
        self.eg_entry_k.insert(0, "1463")

        # Tampilan Blok Numerik
        self.eg_lbl_blocks = tk.Label(
            parent,
            text="Blok Plainteks: -",
            font=("Consolas", 8),
            fg=self.THEME["text_secondary"],
            bg=self.THEME["bg_card_inner"],
            anchor="w",
            padx=8,
            pady=4,
        )
        self.eg_lbl_blocks.pack(fill="x", padx=10, pady=3)

        # Hasil Ciphertext
        self.eg_lbl_cipher = tk.Label(
            parent,
            text="Ciphertext (a_i, b_i):\n-",
            font=("Consolas", 8, "bold"),
            fg=self.THEME["code_number"],
            bg=self.THEME["bg_card_inner"],
            anchor="w",
            justify="left",
            padx=8,
            pady=4,
        )
        self.eg_lbl_cipher.pack(fill="x", padx=10, pady=3)

        # Tombol Enkripsi
        btn_enc = self._create_button(
            parent,
            text="🔒 Enkripsi Pesan",
            command=self._on_eg_encrypt,
            bg=self.THEME["accent_primary"],
            fg="#ffffff",
        )
        btn_enc.pack(anchor="w", padx=10, pady=6)

    def _build_eg_decrypt_card(self, parent):
        tk.Label(
            parent,
            text="C. Dekripsi Pesan (Alice)",
            font=("Segoe UI", 11, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=10, pady=(8, 4))

        tk.Label(
            parent,
            text="Input Pasangan Ciphertext (a, b):",
            font=("Segoe UI", 9),
            fg=self.THEME["text_secondary"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=10, pady=(2, 1))

        # Input Ciphertext Entry
        self.eg_entry_cipher_in = self._create_entry(parent)
        self.eg_entry_cipher_in.pack(fill="x", padx=10, pady=2)

        # Tombol Dekripsi
        btn_dec = self._create_button(
            parent,
            text="🔓 Dekripsi Pesan",
            command=self._on_eg_decrypt,
            bg=self.THEME["accent_green"],
            fg="#000000",
        )
        btn_dec.pack(anchor="w", padx=10, pady=6)

        # Blok Terdekripsi
        self.eg_lbl_dec_m = tk.Label(
            parent,
            text="Blok Terdekripsi (m_i): -",
            font=("Consolas", 8),
            fg=self.THEME["text_secondary"],
            bg=self.THEME["bg_card_inner"],
            anchor="w",
            padx=8,
            pady=4,
        )
        self.eg_lbl_dec_m.pack(fill="x", padx=10, pady=3)

        # Plainteks Terpulihkan
        self.eg_lbl_restored = tk.Label(
            parent,
            text="Plainteks Terpulihkan:\n-",
            font=("Segoe UI", 11, "bold"),
            fg=self.THEME["accent_green"],
            bg=self.THEME["bg_card_inner"],
            anchor="w",
            padx=8,
            pady=6,
        )
        self.eg_lbl_restored.pack(fill="x", padx=10, pady=3)

        # Status Kesesuaian
        self.eg_lbl_match_status = tk.Label(
            parent,
            text="Status: Siap.",
            font=("Segoe UI", 9, "italic"),
            fg=self.THEME["text_muted"],
            bg=self.THEME["bg_card"],
        )
        self.eg_lbl_match_status.pack(anchor="w", padx=10, pady=2)

    def _load_eg_preset(self):
        """Memuat contoh perkuliahan: p=2273, g=3, x=243, M='HALO', k=1463."""
        self.eg_entry_p.delete(0, tk.END)
        self.eg_entry_p.insert(0, str(ElGamalCryptosystem.PRESET_VIDEO["p"]))

        self.eg_entry_g.delete(0, tk.END)
        self.eg_entry_g.insert(0, str(ElGamalCryptosystem.PRESET_VIDEO["g"]))

        self.eg_entry_x.delete(0, tk.END)
        self.eg_entry_x.insert(0, str(ElGamalCryptosystem.PRESET_VIDEO["x"]))

        self.eg_entry_msg.delete(0, tk.END)
        self.eg_entry_msg.insert(0, ElGamalCryptosystem.PRESET_VIDEO["plaintext"])

        self.eg_entry_k.delete(0, tk.END)
        self.eg_entry_k.insert(0, str(ElGamalCryptosystem.PRESET_VIDEO["preset_k"]))

        self.eg_block_mode.set("2char")

        self._on_eg_keygen()
        self._on_eg_encrypt()
        self._on_eg_decrypt()

    def _on_eg_randomize(self):
        """Membangkitkan pasangan parameter acak valid untuk ElGamal."""
        eg = ElGamalCryptosystem.generate_random_valid()
        self.eg_entry_p.delete(0, tk.END)
        self.eg_entry_p.insert(0, str(eg.p))
        self.eg_entry_g.delete(0, tk.END)
        self.eg_entry_g.insert(0, str(eg.g))
        self.eg_entry_x.delete(0, tk.END)
        self.eg_entry_x.insert(0, str(eg.x))
        self.eg_entry_k.delete(0, tk.END)
        # Pilih k acak valid
        k_rand = eg.pick_random_k()
        self.eg_entry_k.insert(0, str(k_rand))
        self._on_eg_keygen()

    def _on_eg_keygen(self):
        try:
            p = int(self.eg_entry_p.get().strip())
            g = int(self.eg_entry_g.get().strip())
            x = int(self.eg_entry_x.get().strip())
        except ValueError:
            messagebox.showerror("Error Keygen", "Parameter p, g, dan x harus berupa bilangan bulat!")
            return

        eg = ElGamalCryptosystem(p, g, x)
        is_ok, errs = eg.validate_keys()
        if not is_ok:
            messagebox.showwarning("Kunci Tidak Valid", "\n".join(errs))
            return

        y = eg.compute_public_key()
        self.elgamal_sys = eg
        self.eg_lbl_y.configure(text=str(y))
        self.eg_lbl_keypairs.configure(
            text=f"Kunci Publik : (y = {y}, g = {g}, p = {p})\nKunci Privat : x = {x}"
        )

    def _on_eg_encrypt(self):
        self._on_eg_keygen()
        text = self.eg_entry_msg.get().strip()
        if not text:
            messagebox.showwarning("Peringatan", "Plainteks tidak boleh kosong!")
            return

        k_val_str = self.eg_entry_k.get().strip()
        custom_k = int(k_val_str) if k_val_str else None
        mode = self.eg_block_mode.get()

        try:
            enc = self.elgamal_sys.encrypt(text, mode=mode, custom_k_list=custom_k)
        except Exception as e:
            messagebox.showerror("Error Enkripsi", str(e))
            return

        self.last_elgamal_enc = enc

        # Tampilkan blok m_i
        block_desc = ", ".join([f"m_{b['index']}={b['m']} ('{b['text']}')" for b in enc["blocks"]])
        self.eg_lbl_blocks.configure(text=f"Blok: {block_desc}")

        # Tampilkan pasangan cipher
        cipher_str = ", ".join([f"({a}, {b})" for a, b in enc["cipher_pairs"]])
        self.eg_lbl_cipher.configure(text=f"Ciphertext:\n{cipher_str}")

        # Salin ke input dekripsi secara otomatis
        self.eg_entry_cipher_in.delete(0, tk.END)
        self.eg_entry_cipher_in.insert(0, cipher_str)

    def _on_eg_decrypt(self):
        cipher_input_str = self.eg_entry_cipher_in.get().strip()
        if not cipher_input_str:
            messagebox.showwarning("Peringatan", "Ciphertext untuk didekripsi tidak boleh kosong!")
            return

        # Parsing format "(a, b), (c, d)" atau list angka
        try:
            cleaned = cipher_input_str.replace("(", "").replace(")", "").replace("[", "").replace("]", "")
            nums = [int(n.strip()) for n in cleaned.split(",") if n.strip()]
            if len(nums) % 2 != 0:
                raise ValueError("Jumlah angka ciphertext harus genap (pasangan a_i dan b_i)!")
            pairs = [(nums[i], nums[i + 1]) for i in range(0, len(nums), 2)]
        except Exception as e:
            messagebox.showerror("Format Ciphertext Salah", f"Gagal membaca pasangan ciphertext:\n{e}\nContoh format: (1439, 74), (1439, 988)")
            return

        mode = self.eg_block_mode.get()
        try:
            dec = self.elgamal_sys.decrypt(pairs, mode=mode)
        except Exception as e:
            messagebox.showerror("Error Dekripsi", str(e))
            return

        self.eg_lbl_dec_m.configure(text=f"Blok Terdekripsi: {dec['decrypted_m']}")
        self.eg_lbl_restored.configure(text=f"Plainteks Terpulihkan:\n'{dec['restored_text']}'")

        if self.last_elgamal_enc:
            orig = self.last_elgamal_enc["processed_text"]
            if orig == dec["restored_text"]:
                self.eg_lbl_match_status.configure(
                    text="✅ Status: Plainteks Selesai Didekripsi & Cocok 100%!",
                    fg=self.THEME["accent_green"],
                )
            else:
                self.eg_lbl_match_status.configure(
                    text="⚠️ Status: Hasil dekripsi tidak persis sama dengan teks asli.",
                    fg=self.THEME["accent_gold"],
                )

            # Buat log komprehensif
            log_text = self.elgamal_sys.generate_detailed_log(self.last_elgamal_enc, dec)
            self._write_log(self.eg_log, log_text)

    # =========================================================================
    # TAB 3: PLAYGROUND MATEMATIKA DASAR
    # =========================================================================

    def _init_math_tab(self, parent):
        # Frame scrollable atau grid untuk menguji 5 fungsi dasar dari nol
        canvas = tk.Canvas(parent, bg=self.THEME["bg_app"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.THEME["bg_app"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set, yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        scrollbar.pack(side="right", fill="y")

        # Header Playground
        tk.Label(
            scrollable_frame,
            text="Test Bench: 5 Fungsi Matematika Kriptografi Murni (From Scratch)",
            font=("Segoe UI", 13, "bold"),
            fg=self.THEME["text_primary"],
            bg=self.THEME["bg_app"],
        ).pack(anchor="w", padx=12, pady=(10, 4))

        tk.Label(
            scrollable_frame,
            text="Seluruh fungsi di bawah ini dieksekusi menggunakan logika algoritma murni tanpa library eksternal.",
            font=("Segoe UI", 9),
            fg=self.THEME["text_secondary"],
            bg=self.THEME["bg_app"],
        ).pack(anchor="w", padx=12, pady=(0, 10))

        # 1. Mod Pow (Square-and-Multiply)
        self._build_math_tool_modpow(scrollable_frame)

        # 2. Euclidean & Extended Euclidean (GCD & Bezout)
        self._build_math_tool_gcd(scrollable_frame)

        # 3. Modular Inverse
        self._build_math_tool_modinv(scrollable_frame)

        # 4. Primality Test (is_prime)
        self._build_math_tool_prime(scrollable_frame)

        # 5. Primitive Root Verifier
        self._build_math_tool_primitive_root(scrollable_frame)

    def _build_math_tool_modpow(self, parent):
        card = self._create_card(parent)
        card.pack(fill="x", padx=12, pady=6)

        tk.Label(
            card,
            text="1. Pemangkatan Modular Efisien: mod_pow(base, exp, mod) [Square-and-Multiply]",
            font=("Segoe UI", 10, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=12, pady=(8, 4))

        f = tk.Frame(card, bg=self.THEME["bg_card"])
        f.pack(fill="x", padx=12, pady=4)

        tk.Label(f, text="Base:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).pack(side="left", padx=2)
        e_b = self._create_entry(f, width=10)
        e_b.pack(side="left", padx=4)
        e_b.insert(0, "3")

        tk.Label(f, text="Exp:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).pack(side="left", padx=2)
        e_e = self._create_entry(f, width=10)
        e_e.pack(side="left", padx=4)
        e_e.insert(0, "1463")

        tk.Label(f, text="Mod:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).pack(side="left", padx=2)
        e_m = self._create_entry(f, width=10)
        e_m.pack(side="left", padx=4)
        e_m.insert(0, "2273")

        lbl_res = tk.Label(card, text="Hasil: -", font=("Consolas", 10, "bold"), fg=self.THEME["code_success"], bg=self.THEME["bg_card"])

        def run_calc():
            try:
                b = int(e_b.get())
                e = int(e_e.get())
                m = int(e_m.get())
                res = mod_pow(b, e, m)
                lbl_res.configure(text=f"Hasil: ({b}^{e}) mod {m} = {res}  (Binary Exponentiation O(log e))")
            except Exception as err:
                lbl_res.configure(text=f"Error: {err}", fg=self.THEME["accent_rose"])

        btn = self._create_button(f, text="Hitung", command=run_calc, bg=self.THEME["accent_primary"], fg="#ffffff")
        btn.pack(side="left", padx=10)
        lbl_res.pack(anchor="w", padx=12, pady=(4, 8))

    def _build_math_tool_gcd(self, parent):
        card = self._create_card(parent)
        card.pack(fill="x", padx=12, pady=6)

        tk.Label(
            card,
            text="2. Algoritma Euclidean & Extended Euclidean: gcd(a, b) & ext_gcd(a, b)",
            font=("Segoe UI", 10, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=12, pady=(8, 4))

        f = tk.Frame(card, bg=self.THEME["bg_card"])
        f.pack(fill="x", padx=12, pady=4)

        tk.Label(f, text="Nilai a:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).pack(side="left", padx=2)
        e_a = self._create_entry(f, width=12)
        e_a.pack(side="left", padx=4)
        e_a.insert(0, "2273")

        tk.Label(f, text="Nilai b:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).pack(side="left", padx=2)
        e_b = self._create_entry(f, width=12)
        e_b.pack(side="left", padx=4)
        e_b.insert(0, "1463")

        lbl_res = tk.Label(card, text="Hasil: -", font=("Consolas", 10), fg=self.THEME["code_success"], bg=self.THEME["bg_card"])

        def run_calc():
            try:
                a = int(e_a.get())
                b = int(e_b.get())
                g, x, y = ext_gcd(a, b)
                lbl_res.configure(
                    text=f"FPB({a}, {b}) = {g} | Koefisien Bezout: ({a} × {x}) + ({b} × {y}) = {a*x + b*y}"
                )
            except Exception as err:
                lbl_res.configure(text=f"Error: {err}", fg=self.THEME["accent_rose"])

        btn = self._create_button(f, text="Hitung FPB & Bezout", command=run_calc, bg=self.THEME["accent_primary"], fg="#ffffff")
        btn.pack(side="left", padx=10)
        lbl_res.pack(anchor="w", padx=12, pady=(4, 8))

    def _build_math_tool_modinv(self, parent):
        card = self._create_card(parent)
        card.pack(fill="x", padx=12, pady=6)

        tk.Label(
            card,
            text="3. Balikan Modular: mod_inverse(a, m) [Extended Euclidean & Teorema Fermat]",
            font=("Segoe UI", 10, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=12, pady=(8, 4))

        f = tk.Frame(card, bg=self.THEME["bg_card"])
        f.pack(fill="x", padx=12, pady=4)

        tk.Label(f, text="Bilangan a:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).pack(side="left", padx=2)
        e_a = self._create_entry(f, width=12)
        e_a.pack(side="left", padx=4)
        e_a.insert(0, "461")

        tk.Label(f, text="Modulus m:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).pack(side="left", padx=2)
        e_m = self._create_entry(f, width=12)
        e_m.pack(side="left", padx=4)
        e_m.insert(0, "2273")

        lbl_res = tk.Label(card, text="Hasil: -", font=("Consolas", 10), fg=self.THEME["code_success"], bg=self.THEME["bg_card"])

        def run_calc():
            try:
                a = int(e_a.get())
                m = int(e_m.get())
                inv = mod_inverse(a, m)
                lbl_res.configure(
                    text=f"Balikan: {a}^(-1) mod {m} = {inv}  [Cek: ({a} × {inv}) mod {m} = {(a * inv) % m}]"
                )
            except Exception as err:
                lbl_res.configure(text=f"Gagal: {err}", fg=self.THEME["accent_rose"])

        btn = self._create_button(f, text="Cari Balikan Modular", command=run_calc, bg=self.THEME["accent_primary"], fg="#ffffff")
        btn.pack(side="left", padx=10)
        lbl_res.pack(anchor="w", padx=12, pady=(4, 8))

    def _build_math_tool_prime(self, parent):
        card = self._create_card(parent)
        card.pack(fill="x", padx=12, pady=6)

        tk.Label(
            card,
            text="4. Pengujian Bilangan Prima: is_prime(n)",
            font=("Segoe UI", 10, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=12, pady=(8, 4))

        f = tk.Frame(card, bg=self.THEME["bg_card"])
        f.pack(fill="x", padx=12, pady=4)

        tk.Label(f, text="Bilangan n:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).pack(side="left", padx=2)
        e_n = self._create_entry(f, width=15)
        e_n.pack(side="left", padx=4)
        e_n.insert(0, "2273")

        lbl_res = tk.Label(card, text="Hasil: -", font=("Consolas", 10), fg=self.THEME["code_success"], bg=self.THEME["bg_card"])

        def run_calc():
            try:
                n = int(e_n.get())
                status = is_prime(n)
                if status:
                    lbl_res.configure(text=f"n = {n} adalah BILANGAN PRIMA (Valid) ✅", fg=self.THEME["code_success"])
                else:
                    factors = get_prime_factors(n)
                    lbl_res.configure(
                        text=f"n = {n} BUKAN PRIMA (Komposit) ❌ | Faktor Prima: {factors}",
                        fg=self.THEME["accent_rose"],
                    )
            except Exception as err:
                lbl_res.configure(text=f"Error: {err}", fg=self.THEME["accent_rose"])

        btn = self._create_button(f, text="Uji Keprimaan", command=run_calc, bg=self.THEME["accent_primary"], fg="#ffffff")
        btn.pack(side="left", padx=10)
        lbl_res.pack(anchor="w", padx=12, pady=(4, 8))

    def _build_math_tool_primitive_root(self, parent):
        card = self._create_card(parent)
        card.pack(fill="x", padx=12, pady=6)

        tk.Label(
            card,
            text="5. Verifikasi & Pencarian Akar Primitif: is_primitive_root(g, p)",
            font=("Segoe UI", 10, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=12, pady=(8, 4))

        f = tk.Frame(card, bg=self.THEME["bg_card"])
        f.pack(fill="x", padx=12, pady=4)

        tk.Label(f, text="Kandidat g:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).pack(side="left", padx=2)
        e_g = self._create_entry(f, width=10)
        e_g.pack(side="left", padx=4)
        e_g.insert(0, "3")

        tk.Label(f, text="Prima p:", bg=self.THEME["bg_card"], fg=self.THEME["text_primary"]).pack(side="left", padx=2)
        e_p = self._create_entry(f, width=10)
        e_p.pack(side="left", padx=4)
        e_p.insert(0, "2273")

        lbl_res = tk.Label(
            card,
            text="Hasil: -",
            font=("Consolas", 9),
            fg=self.THEME["code_success"],
            bg=self.THEME["bg_card"],
            justify="left",
        )

        def run_calc():
            try:
                g = int(e_g.get())
                p = int(e_p.get())
                status, explanation = is_primitive_root(g, p)
                roots = find_primitive_roots(p, max_count=8)
                color = self.THEME["code_success"] if status else self.THEME["accent_rose"]
                txt = f"{explanation}\nContoh akar primitif lain mod {p}: {roots}"
                lbl_res.configure(text=txt, fg=color)
            except Exception as err:
                lbl_res.configure(text=f"Error: {err}", fg=self.THEME["accent_rose"])

        btn = self._create_button(f, text="Verifikasi Akar Primitif", command=run_calc, bg=self.THEME["accent_primary"], fg="#ffffff")
        btn.pack(side="left", padx=10)
        lbl_res.pack(anchor="w", padx=12, pady=(4, 8))

    # =========================================================================
    # TAB 4: PANDUAN & IDENTITAS KELOMPOK
    # =========================================================================

    def _init_about_tab(self, parent):
        canvas = tk.Canvas(parent, bg=self.THEME["bg_app"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.THEME["bg_app"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set, yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        scrollbar.pack(side="right", fill="y")

        # Card 1: Identitas Kelompok
        c1 = self._create_card(scrollable_frame)
        c1.pack(fill="x", padx=12, pady=8)

        tk.Label(
            c1,
            font=("Segoe UI", 12, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=14, pady=(10, 4))

        id_text = (
            "Implementasi Algoritma Pertukaran Kunci Diffie-Hellman dan Kriptografi Asimetris ElGamal\n"
            "Anggota     :\n"
            "  1. Muhammad Fachry Shalahuddin Rusamsi - NRP: 5027241031\n"
            "  2. Prabaswara Febrian Winandika - NRP: 5027241069\n"
            "  3. Gemilang Ananda Lingua - NRP: 5027241072\n"
        )
        tk.Label(
            c1,
            text=id_text,
            font=("Segoe UI", 10),
            fg=self.THEME["text_primary"],
            bg=self.THEME["bg_card"],
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 10))

        # Card 2: Teori Ringkas
        c2 = self._create_card(scrollable_frame)
        c2.pack(fill="x", padx=12, pady=8)

        tk.Label(
            c2,
            text="💡 RINGKASAN TEORI & ALGORITMA",
            font=("Segoe UI", 12, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(anchor="w", padx=14, pady=(10, 4))

        theory_text = (
            "1. Algoritma Square-and-Multiply (Binary Exponentiation):\n"
            "   Menghitung a^b mod m dalam kompleksitas waktu O(log b), menggantikan pemangkatan naif O(b)\n"
            "   yang menyebabkan integer overflow dan beban komputasi masif.\n\n"
            "2. Akar Primitif (Primitive Root) & Discrete Logarithm Problem (DLP):\n"
            "   Sebuah generator g mampu menghasilkan seluruh elemen grup multiplikatif Z_p*. Keamanan\n"
            "   Diffie-Hellman dan ElGamal bertumpu pada sulitnya membalikkan persamaan Y = g^x mod p\n"
            "   untuk mencari x (Discrete Logarithm Problem).\n\n"
            "3. Pertukaran Kunci Diffie-Hellman:\n"
            "   Memungkinkan dua pihak (Alice & Bob) menyepakati kunci rahasia simetris bersama (Shared Key)\n"
            "   melalui saluran publik tidak aman tanpa pernah mengirimkan kunci privat mereka.\n\n"
            "4. Kriptosistem Asimetris ElGamal:\n"
            "   Menggunakan kunci publik (y, g, p) untuk enkripsi dan kunci privat x untuk dekripsi.\n"
            "   Setiap proses enkripsi blok pesan menggunakan bilangan acak k (ephemeral key),\n"
            "   sehingga menghasilkan sifat nondeterministik (ciphertext berbeda untuk plainteks yang sama)."
        )
        tk.Label(
            c2,
            text=theory_text,
            font=("Segoe UI", 9),
            fg=self.THEME["text_secondary"],
            bg=self.THEME["bg_card"],
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 12))

    # =========================================================================
    # KOMPONEN REUSABLE UI
    # =========================================================================

    def _create_card(self, parent):
        return tk.Frame(
            parent,
            bg=self.THEME["bg_card"],
            bd=1,
            relief="solid",
            highlightbackground=self.THEME["border"],
            highlightthickness=1,
        )

    def _create_entry(self, parent, width=None):
        return tk.Entry(
            parent,
            bg=self.THEME["bg_entry"],
            fg=self.THEME["text_primary"],
            insertbackground=self.THEME["text_primary"],
            relief="flat",
            bd=3,
            font=("Consolas", 10),
            width=width,
        )

    def _create_button(self, parent, text, command, bg, fg):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=self.THEME["accent_hover"],
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
        )

    def _build_log_panel(self, parent, title="Catatan Eksekusi"):
        frame = self._create_card(parent)
        frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Bar Kontrol Log
        bar = tk.Frame(frame, bg=self.THEME["bg_card"], padx=10, pady=6)
        bar.pack(fill="x")

        tk.Label(
            bar,
            text=f"📜 {title}",
            font=("Segoe UI", 10, "bold"),
            fg=self.THEME["accent_cyan"],
            bg=self.THEME["bg_card"],
        ).pack(side="left")

        # Text Log Area
        text_widget = tk.Text(
            frame,
            bg=self.THEME["bg_log"],
            fg=self.THEME["text_primary"],
            insertbackground=self.THEME["text_primary"],
            font=("Consolas", 9),
            wrap="word",
            bd=0,
            padx=10,
            pady=8,
        )
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        text_widget.pack(side="left", fill="both", expand=True)

        # Tombol-tombol di bar log
        def copy_log():
            content = text_widget.get("1.0", tk.END).strip()
            self.clipboard_clear()
            self.clipboard_append(content)
            messagebox.showinfo("Berhasil", "Seluruh catatan eksekusi berhasil disalin ke clipboard!")

        def save_log():
            content = text_widget.get("1.0", tk.END).strip()
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text File", "*.txt"), ("All Files", "*.*")],
                title="Simpan Catatan Log Kriptografi",
            )
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Berhasil", f"Log berhasil disimpan di:\n{path}")

        btn_copy = self._create_button(
            bar,
            text="📋 Salin",
            command=copy_log,
            bg=self.THEME["bg_card_inner"],
            fg=self.THEME["text_secondary"],
        )
        btn_copy.pack(side="right", padx=2)

        btn_save = self._create_button(
            bar,
            text="💾 Simpan TXT",
            command=save_log,
            bg=self.THEME["bg_card_inner"],
            fg=self.THEME["text_secondary"],
        )
        btn_save.pack(side="right", padx=2)

        return text_widget

    def _write_log(self, text_widget: tk.Text, content: str):
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, content)
        text_widget.see("1.0")


if __name__ == "__main__":
    app = ModernCryptoGUI()
    app.mainloop()
