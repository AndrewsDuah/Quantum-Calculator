import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
try:
    from scipy import constants as const
except Exception:
    # Fallback constants (SI)
    class _Const:
        h = 6.62607015e-34
        c = 299792458.0
        eV = 1.602176634e-19
        R = 8.314462618
        electron_mass = 9.1093837015e-31
        proton_mass = 1.67262192369e-27
        neutron_mass = 1.67492749804e-27
    const = _Const()

APP_TITLE = "PHYSICS 112 CALCULATOR — Student Edition"

# ---------- Small helpers ----------
def fmt_si(x, unit="", sig=4):
    """Format with sensible units (m→nm/µm, J→eV, Hz→kHz/MHz/GHz)."""
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "—"
    u = unit.strip().lower()
    val, sfx = x, unit
    if u in ["m", "meter", "meters"]:
        if abs(x) >= 1e-2: val, sfx = x, " m"
        elif abs(x) >= 1e-6: val, sfx = x*1e6, " µm"
        elif abs(x) >= 1e-9: val, sfx = x*1e9, " nm"
        elif abs(x) >= 1e-12: val, sfx = x*1e12, " pm"
        else: val, sfx = x, " m"
    elif u in ["hz"]:
        if abs(x) >= 1e9: val, sfx = x/1e9, " GHz"
        elif abs(x) >= 1e6: val, sfx = x/1e6, " MHz"
        elif abs(x) >= 1e3: val, sfx = x/1e3, " kHz"
        else: val, sfx = x, " Hz"
    elif u in ["j", "joule", "joules"]:
        if abs(x) >= const.eV:
            val, sfx = x/const.eV, " eV"
        else:
            val, sfx = x, " J"
    else:
        sfx = f" {unit}" if unit else ""
    try:
        return f"{val:.{sig}g}{sfx}"
    except Exception:
        return f"{val}{sfx}"

def photon_region_nm(wavelength_m):
    if wavelength_m <= 0: return "—"
    lam_nm = wavelength_m*1e9
    if lam_nm < 10: return "Gamma"
    if lam_nm < 400: return "UV"
    if lam_nm < 700: return "Visible"
    if lam_nm < 1e6: return "IR"
    if lam_nm < 1e9: return "Microwave"
    return "Radio"

def copy_to_clipboard(root, text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

# Simple tooltip
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)
    def show(self, _=None):
        if self.tip: return
        x, y, cx, cy = self.widget.bbox("insert") if self.widget.winfo_exists() else (0,0,0,0)
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(tw, text=self.text, justify="left",
                       background="#111", foreground="#fff",
                       relief="solid", borderwidth=1,
                       font=("Segoe UI", 9))
        lbl.pack(ipadx=6, ipady=3)
    def hide(self, _=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None

# ---------- Main App ----------
class Phys112App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.minsize(1100, 700)
        self.geometry("1250x820")
        self.configure(bg="#0f172a")  # slate-900
        self.style = ttk.Style(self)
        self._dark = True
        self._set_theme(dark=True)
        self._make_menu()
        self._make_header()
        self._make_body()
        self._make_statusbar()
        self.history = []  # (tab, description, value)
        self.bind_all("<Control-Return>", lambda e: self._smart_calculate())
        self.bind_all("<F2>", lambda e: self.toggle_theme())

    # ---------- UI chrome ----------
    def _set_theme(self, dark=True):
        self._dark = dark
        base_bg = "#0f172a" if dark else "#f8fafc"
        card_bg = "#111827" if dark else "#ffffff"
        fg = "#e5e7eb" if dark else "#0f172a"
        subfg = "#cbd5e1" if dark else "#334155"
        accent = "#22d3ee" if dark else "#0ea5e9"

        self.configure(bg=base_bg)
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background=base_bg, foreground=fg, borderwidth=0)
        self.style.configure("TNotebook.Tab", padding=(16, 10), font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", card_bg)], foreground=[("selected", fg)])
        self.style.configure("Card.TFrame", background=card_bg)
        self.style.configure("TLabel", background=card_bg, foreground=fg, font=("Segoe UI", 10))
        self.style.configure("Hdr.TLabel", background=base_bg, foreground=fg, font=("Segoe UI Semibold", 18))
        self.style.configure("SubHdr.TLabel", background=base_bg, foreground=subfg, font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI Semibold", 10))
        self.style.configure("Accent.TButton", foreground="#0f172a", background=accent)
        self.style.map("Accent.TButton", background=[("active", "#67e8f9")])
        self.style.configure("TEntry", fieldbackground="#0b1220" if dark else "#ffffff", foreground=fg)
        self.style.configure("Result.TLabel", background=card_bg, foreground=accent, font=("Consolas", 10, "bold"))
        self.style.configure("Status.TLabel", background=base_bg, foreground=subfg, font=("Segoe UI", 9))
        self.card_bg = card_bg
        self.fg = fg
        self.accent = accent

    def toggle_theme(self):
        self._set_theme(not self._dark)
        self._set_status("Theme toggled (F2).")

    def _make_menu(self):
        m = tk.Menu(self, tearoff=False)
        file_m = tk.Menu(m, tearoff=False)
        file_m.add_command(label="Export History to CSV…", command=self._export_history)
        file_m.add_separator()
        file_m.add_command(label="Exit", command=self.destroy)
        m.add_cascade(label="File", menu=file_m)

        view_m = tk.Menu(m, tearoff=False)
        view_m.add_command(label="Toggle Dark/Light (F2)", command=self.toggle_theme)
        m.add_cascade(label="View", menu=view_m)

        help_m = tk.Menu(m, tearoff=False)
        help_m.add_command(label="About…", command=lambda: messagebox.showinfo("About", "PHYSICS 112 Calculator\nMade nicer with Tkinter + ttk.\nShortcuts: Ctrl+Enter to calculate, F2 toggle theme."))
        m.add_cascade(label="Help", menu=help_m)
        self.config(menu=m)

    def _make_header(self):
        top = ttk.Frame(self, style="Card.TFrame")
        top.pack(fill="x", padx=16, pady=(16, 8))
        ttk.Label(top, text=APP_TITLE, style="Hdr.TLabel").pack(anchor="w")
        ttk.Label(top, text="Atomic transitions, de Broglie wavelengths, nuclear stats, thermodynamics — with units, validation, & history.", style="SubHdr.TLabel").pack(anchor="w")

    def _make_body(self):
        body = ttk.Frame(self, style="Card.TFrame")
        body.pack(fill="both", expand=True, padx=16, pady=8)

        # Left: notebook
        self.nb = ttk.Notebook(body)
        self.nb.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=8)

        # Right: history panel
        right = ttk.Frame(body, style="Card.TFrame")
        right.pack(side="right", fill="y", padx=(8, 0), pady=8)
        ttk.Label(right, text="📜 History", font=("Segoe UI Semibold", 12)).pack(anchor="w", padx=12, pady=(12, 4))
        self.history_list = tk.Listbox(right, height=30, activestyle="dotbox", selectmode="browse",
                                       bg="#0b1220" if self._dark else "#ffffff",
                                       fg=self.fg, highlightthickness=0, bd=0)
        self.history_list.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        btns = ttk.Frame(right, style="Card.TFrame")
        btns.pack(fill="x", padx=12, pady=(0, 12))
        ttk.Button(btns, text="Copy Selected", command=self._copy_selected_history).pack(side="left")
        ttk.Button(btns, text="Clear", command=self._clear_history).pack(side="right")

        # Tabs
        self._tab_atomic()
        self._tab_binding()
        self._tab_electron()
        self._tab_neutron()
        self._tab_proton()
        self._tab_nucleus_bohr()
        self._tab_thermo()

    def _make_statusbar(self):
        bar = ttk.Frame(self, style="Card.TFrame")
        bar.pack(fill="x", padx=16, pady=(0, 12))
        self.status_lbl = ttk.Label(bar, text="Ready.", style="Status.TLabel")
        self.status_lbl.pack(anchor="w")

    def _set_status(self, msg):
        self.status_lbl.config(text=msg)

    def _log(self, tab, desc, val):
        entry = f"[{tab}] {desc}: {val}"
        self.history.append((tab, desc, val))
        self.history_list.insert(tk.END, entry)

    def _copy_selected_history(self):
        sel = self.history_list.curselection()
        if not sel: return
        text = self.history_list.get(sel[0])
        copy_to_clipboard(self, text)
        self._set_status("Copied to clipboard.")

    def _clear_history(self):
        self.history.clear()
        self.history_list.delete(0, tk.END)
        self._set_status("History cleared.")

    def _export_history(self):
        if not self.history:
            messagebox.showinfo("Export", "Nothing to export yet.")
            return
        fp = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="Export History")
        if not fp: return
        with open(fp, "w", encoding="utf-8") as f:
            f.write("tab,description,value\n")
            for t, d, v in self.history:
                v = str(v).replace("\n", " ").replace(",", ";")
                f.write(f"{t},{d},{v}\n")
        self._set_status(f"Exported: {fp}")

    def _smart_calculate(self):
        # Press Ctrl+Enter → run the first "Calculate" button on current tab
        tab = self.nb.select()
        for child in self.nametowidget(tab).winfo_children():
            if isinstance(child, ttk.Button) and "Calculate" in child.cget("text"):
                child.invoke()
                return

    # ---------- Tabs ----------
    def _wrap_card(self, parent, title):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill="both", expand=True, padx=12, pady=12)
        hdr = ttk.Label(card, text=title, font=("Segoe UI Semibold", 13))
        hdr.grid(row=0, column=0, columnspan=6, sticky="w", pady=(4, 10))
        return card

    def _add_copy_row(self, parent, row, label_text, var_ref):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="e", padx=6, pady=4)
        out = ttk.Label(parent, text="—", style="Result.TLabel")
        out.grid(row=row, column=1, columnspan=4, sticky="w", padx=6, pady=4)
        def _copy():
            txt = out.cget("text")
            copy_to_clipboard(self, txt)
            self._set_status("Copied result.")
        btn = ttk.Button(parent, text="Copy", command=_copy)
        btn.grid(row=row, column=5, sticky="e", padx=6)
        var_ref.append(out)

    # --- Atomic transitions ---
    def _tab_atomic(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Atomic Transitions")
        card = self._wrap_card(tab, "Hydrogen-like (Rydberg) transition")

        # Inputs
        ttk.Label(card, text="Initial n₁ (integer ≥1)").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        self.n1 = ttk.Entry(card, width=10)
        self.n1.grid(row=1, column=1, sticky="w")

        ttk.Label(card, text="Final n₂ (integer ≥1)").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        self.n2 = ttk.Entry(card, width=10)
        self.n2.grid(row=2, column=1, sticky="w")

        ttk.Label(card, text="Atomic number Z (default 1)").grid(row=3, column=0, sticky="e", padx=6, pady=4)
        self.z_entry = ttk.Entry(card, width=10)
        self.z_entry.insert(0, "1")
        self.z_entry.grid(row=3, column=1, sticky="w")

        # Actions
        calc = ttk.Button(card, text="Calculate wavelength / frequency / energy", style="Accent.TButton",
                          command=self._calc_transition)
        calc.grid(row=4, column=1, sticky="w", pady=(6, 8))
        clear = ttk.Button(card, text="Clear", command=lambda: (self.n1.delete(0, tk.END), self.n2.delete(0, tk.END)))
        clear.grid(row=4, column=2, sticky="w")

        # Outputs with copy buttons
        self.at_outputs = []
        self._add_copy_row(card, 6, "Wavelength:", self.at_outputs)
        self._add_copy_row(card, 7, "Frequency:", self.at_outputs)
        self._add_copy_row(card, 8, "Photon energy:", self.at_outputs)
        self._add_copy_row(card, 9, "Region:", self.at_outputs)

        # Tip
        Tooltip(calc, "Ctrl+Enter to calculate on any tab.")

    def _calc_transition(self):
        try:
            n1 = int(self.n1.get().strip())
            n2 = int(self.n2.get().strip())
            z = int(self.z_entry.get().strip() or "1")
            if n1 < 1 or n2 < 1 or z < 1:
                raise ValueError("Levels and Z must be ≥ 1.")
            # Energy levels: E_n = -13.6 Z^2 / n^2 (eV)
            e1 = -13.6 * z*z / (n1*n1)
            e2 = -13.6 * z*z / (n2*n2)
            dE_eV = abs(e2 - e1)
            dE_J = dE_eV * const.eV
            if dE_J == 0:
                raise ValueError("n1 and n2 are identical.")
            lam = (const.h * const.c) / dE_J
            freq = dE_J / const.h
            region = photon_region_nm(lam)
            self.at_outputs[0].config(text=f"{fmt_si(lam,'m',sig=5)}")
            self.at_outputs[1].config(text=f"{fmt_si(freq,'Hz',sig=5)}")
            self.at_outputs[2].config(text=f"{dE_eV:.5g} eV  |  {fmt_si(dE_J,'J',sig=5)}")
            self.at_outputs[3].config(text=region)
            self._log("Atomic", f"n1={n1}, n2={n2}, Z={z}", f"λ={fmt_si(lam,'m')}, f={fmt_si(freq,'Hz')}, E={dE_eV:.4g} eV")
            self._set_status("Atomic transition computed.")
        except ValueError as ve:
            messagebox.showerror("Input error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    # --- Binding energy / mass deficit ---
    def _tab_binding(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Binding Energy")
        card = self._wrap_card(tab, "Binding energy & mass deficit")

        ttk.Label(card, text="Element symbol (e.g., Fe)").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        self.elm_sym = ttk.Entry(card, width=10)
        self.elm_sym.grid(row=1, column=1, sticky="w")

        ttk.Label(card, text="Atomic mass (u)").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        self.atomic_mass_u = ttk.Entry(card, width=12)
        self.atomic_mass_u.grid(row=2, column=1, sticky="w")

        ttk.Label(card, text="Atomic number Z").grid(row=3, column=0, sticky="e", padx=6, pady=4)
        self.Z_be = ttk.Entry(card, width=8)
        self.Z_be.grid(row=3, column=1, sticky="w")

        ttk.Label(card, text="Mass number A").grid(row=4, column=0, sticky="e", padx=6, pady=4)
        self.A_be = ttk.Entry(card, width=8)
        self.A_be.grid(row=4, column=1, sticky="w")

        calc = ttk.Button(card, text="Calculate", style="Accent.TButton", command=self._calc_binding)
        calc.grid(row=5, column=1, sticky="w", pady=(6, 8))
        self.be_outputs = []
        self._add_copy_row(card, 7, "Mass defect Δm:", self.be_outputs)
        self._add_copy_row(card, 8, "Binding energy:", self.be_outputs)
        self._add_copy_row(card, 9, "Binding energy per nucleon:", self.be_outputs)

    def _calc_binding(self):
        try:
            sym = self.elm_sym.get().strip()
            if not sym.isalpha():
                raise ValueError("Enter a valid element symbol.")
            m_u = float(self.atomic_mass_u.get().strip())
            Z = int(self.Z_be.get().strip())
            A = int(self.A_be.get().strip())
            if m_u <= 0 or Z <= 0 or A <= 0:
                raise ValueError("Mass, Z, A must be positive.")
            if Z > A:
                raise ValueError("Z cannot exceed A.")

            # masses in atomic mass units
            m_p = 1.007276466621
            m_n = 1.00866491595
            m_e = 0.000548579909065
            N = A - Z
            m_constituents = Z*(m_p + m_e) + N*m_n
            dm = m_constituents - m_u  # in u
            # 1 u = 931.49410242 MeV/c^2
            BE_MeV = dm * 931.49410242
            BE_J = BE_MeV * 1e6 * const.eV
            BE_per_nucl = BE_MeV / A if A else float("nan")

            self.be_outputs[0].config(text=f"{dm:.6f} u")
            self.be_outputs[1].config(text=f"{BE_MeV:.5g} MeV  |  {fmt_si(BE_J,'J')}")
            self.be_outputs[2].config(text=f"{BE_per_nucl:.5g} MeV / nucleon")
            self._log("Binding", f"{sym}-{A}", f"Δm={dm:.6f} u, BE={BE_MeV:.5g} MeV")
            self._set_status("Binding energy computed.")
        except ValueError as ve:
            messagebox.showerror("Input error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    # --- Electron de Broglie ---
    def _tab_electron(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Electron λ (de Broglie)")
        card = self._wrap_card(tab, "Electron de Broglie wavelength")

        ttk.Label(card, text="Velocity v (m/s)").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        self.e_v = ttk.Entry(card, width=16); self.e_v.grid(row=1, column=1, sticky="w")
        ttk.Button(card, text="Calculate (v)", style="Accent.TButton", command=self._calc_e_v).grid(row=1, column=2, sticky="w", padx=6)

        ttk.Label(card, text="Kinetic energy (eV)").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        self.e_ke = ttk.Entry(card, width=16); self.e_ke.grid(row=2, column=1, sticky="w")
        ttk.Button(card, text="Calculate (KE)", command=self._calc_e_ke).grid(row=2, column=2, sticky="w", padx=6)

        ttk.Label(card, text="Momentum p (kg·m/s)").grid(row=3, column=0, sticky="e", padx=6, pady=4)
        self.e_p = ttk.Entry(card, width=16); self.e_p.grid(row=3, column=1, sticky="w")
        ttk.Button(card, text="Calculate (p)", command=self._calc_e_p).grid(row=3, column=2, sticky="w", padx=6)

        self.e_outputs = []
        self._add_copy_row(card, 5, "λ:", self.e_outputs)

    def _calc_e_v(self):
        try:
            v = float(self.e_v.get().strip())
            if v <= 0: raise ValueError("v must be > 0")
            lam = const.h/(const.electron_mass*v)
            self.e_outputs[0].config(text=f"{fmt_si(lam,'m')}")
            self._log("e⁻", "λ(v)", fmt_si(lam, "m"))
            self._set_status("Electron λ from velocity.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    def _calc_e_ke(self):
        try:
            ke_eV = float(self.e_ke.get().strip())
            if ke_eV < 0: raise ValueError("KE must be ≥ 0")
            lam = const.h/math.sqrt(2*ke_eV*const.eV*const.electron_mass)
            self.e_outputs[0].config(text=f"{fmt_si(lam,'m')}")
            self._log("e⁻", "λ(KE)", fmt_si(lam, "m"))
            self._set_status("Electron λ from KE.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    def _calc_e_p(self):
        try:
            p = float(self.e_p.get().strip())
            if p <= 0: raise ValueError("p must be > 0")
            lam = const.h/p
            self.e_outputs[0].config(text=f"{fmt_si(lam,'m')}")
            self._log("e⁻", "λ(p)", fmt_si(lam, "m"))
            self._set_status("Electron λ from momentum.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    # --- Neutron de Broglie ---
    def _tab_neutron(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Neutron λ")
        card = self._wrap_card(tab, "Neutron de Broglie wavelength")

        ttk.Label(card, text="Velocity v (m/s)").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        self.n_v = ttk.Entry(card, width=16); self.n_v.grid(row=1, column=1, sticky="w")
        ttk.Button(card, text="Calculate (v)", style="Accent.TButton", command=self._calc_n_v).grid(row=1, column=2, sticky="w", padx=6)

        ttk.Label(card, text="Kinetic energy (eV)").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        self.n_ke = ttk.Entry(card, width=16); self.n_ke.grid(row=2, column=1, sticky="w")
        ttk.Button(card, text="Calculate (KE)", command=self._calc_n_ke).grid(row=2, column=2, sticky="w", padx=6)

        ttk.Label(card, text="Momentum p (kg·m/s)").grid(row=3, column=0, sticky="e", padx=6, pady=4)
        self.n_p = ttk.Entry(card, width=16); self.n_p.grid(row=3, column=1, sticky="w")
        ttk.Button(card, text="Calculate (p)", command=self._calc_n_p).grid(row=3, column=2, sticky="w", padx=6)

        self.n_outputs = []
        self._add_copy_row(card, 5, "λ:", self.n_outputs)

    def _calc_n_v(self):
        try:
            v = float(self.n_v.get().strip())
            if v <= 0: raise ValueError("v must be > 0")
            lam = const.h/(const.neutron_mass*v)
            self.n_outputs[0].config(text=f"{fmt_si(lam,'m')}")
            self._log("n⁰", "λ(v)", fmt_si(lam, "m"))
            self._set_status("Neutron λ from velocity.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    def _calc_n_ke(self):
        try:
            ke_eV = float(self.n_ke.get().strip())
            if ke_eV < 0: raise ValueError("KE must be ≥ 0")
            lam = const.h/math.sqrt(2*ke_eV*const.eV*const.neutron_mass)
            self.n_outputs[0].config(text=f"{fmt_si(lam,'m')}")
            self._log("n⁰", "λ(KE)", fmt_si(lam, "m"))
            self._set_status("Neutron λ from KE.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    def _calc_n_p(self):
        try:
            p = float(self.n_p.get().strip())
            if p <= 0: raise ValueError("p must be > 0")
            lam = const.h/p
            self.n_outputs[0].config(text=f"{fmt_si(lam,'m')}")
            self._log("n⁰", "λ(p)", fmt_si(lam, "m"))
            self._set_status("Neutron λ from momentum.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    # --- Proton de Broglie ---
    def _tab_proton(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Proton λ")
        card = self._wrap_card(tab, "Proton de Broglie wavelength")

        ttk.Label(card, text="Velocity v (m/s)").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        self.p_v = ttk.Entry(card, width=16); self.p_v.grid(row=1, column=1, sticky="w")
        ttk.Button(card, text="Calculate (v)", style="Accent.TButton", command=self._calc_p_v).grid(row=1, column=2, sticky="w", padx=6)

        ttk.Label(card, text="Kinetic energy (eV)").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        self.p_ke = ttk.Entry(card, width=16); self.p_ke.grid(row=2, column=1, sticky="w")
        ttk.Button(card, text="Calculate (KE)", command=self._calc_p_ke).grid(row=2, column=2, sticky="w", padx=6)

        ttk.Label(card, text="Momentum p (kg·m/s)").grid(row=3, column=0, sticky="e", padx=6, pady=4)
        self.p_p = ttk.Entry(card, width=16); self.p_p.grid(row=3, column=1, sticky="w")
        ttk.Button(card, text="Calculate (p)", command=self._calc_p_p).grid(row=3, column=2, sticky="w", padx=6)

        self.p_outputs = []
        self._add_copy_row(card, 5, "λ:", self.p_outputs)

    def _calc_p_v(self):
        try:
            v = float(self.p_v.get().strip())
            if v <= 0: raise ValueError("v must be > 0")
            lam = const.h/(const.proton_mass*v)
            self.p_outputs[0].config(text=f"{fmt_si(lam,'m')}")
            self._log("p⁺", "λ(v)", fmt_si(lam, "m"))
            self._set_status("Proton λ from velocity.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    def _calc_p_ke(self):
        try:
            ke_eV = float(self.p_ke.get().strip())
            if ke_eV < 0: raise ValueError("KE must be ≥ 0")
            lam = const.h/math.sqrt(2*ke_eV*const.eV*const.proton_mass)
            self.p_outputs[0].config(text=f"{fmt_si(lam,'m')}")
            self._log("p⁺", "λ(KE)", fmt_si(lam, "m"))
            self._set_status("Proton λ from KE.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    def _calc_p_p(self):
        try:
            p = float(self.p_p.get().strip())
            if p <= 0: raise ValueError("p must be > 0")
            lam = const.h/p
            self.p_outputs[0].config(text=f"{fmt_si(lam,'m')}")
            self._log("p⁺", "λ(p)", fmt_si(lam, "m"))
            self._set_status("Proton λ from momentum.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    # --- Nuclear radius & Bohr radius ---
    def _tab_nucleus_bohr(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Nuclear & Bohr")
        card = self._wrap_card(tab, "Nuclear radius & Bohr radius")

        ttk.Label(card, text="Element symbol").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        self.nr_sym = ttk.Entry(card, width=10); self.nr_sym.grid(row=1, column=1, sticky="w")
        ttk.Label(card, text="Atomic number Z").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        self.nr_Z = ttk.Entry(card, width=10); self.nr_Z.grid(row=2, column=1, sticky="w")
        ttk.Label(card, text="Mass number A").grid(row=3, column=0, sticky="e", padx=6, pady=4)
        self.nr_A = ttk.Entry(card, width=10); self.nr_A.grid(row=3, column=1, sticky="w")
        ttk.Button(card, text="Calculate Nuclear Radius", style="Accent.TButton", command=self._calc_nuclear_radius).grid(row=4, column=1, sticky="w", pady=(6, 8))
        self.nr_outputs = []
        self._add_copy_row(card, 5, "R (fm):", self.nr_outputs)

        ttk.Separator(card).grid(row=6, column=0, columnspan=6, sticky="ew", pady=8)

        ttk.Label(card, text="Bohr level n (integer ≥1)").grid(row=7, column=0, sticky="e", padx=6, pady=4)
        self.bohr_n = ttk.Entry(card, width=10); self.bohr_n.grid(row=7, column=1, sticky="w")
        ttk.Button(card, text="Calculate Bohr Radius", command=self._calc_bohr).grid(row=7, column=2, sticky="w")
        self.bohr_outputs = []
        self._add_copy_row(card, 8, "aₙ (pm):", self.bohr_outputs)

    def _calc_nuclear_radius(self):
        try:
            sym = self.nr_sym.get().strip()
            z = int(self.nr_Z.get().strip())
            a = int(self.nr_A.get().strip())
            if not sym.isalpha(): raise ValueError("Symbol must be letters.")
            if z <= 0 or a <= 0: raise ValueError("Z and A must be positive.")
            if z > a: raise ValueError("Z cannot exceed A.")
            R = 1.2 * (a ** (1/3))  # in fm
            # Pretty isotope: e.g. C¹²₆
            superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
            subscripts  = "₀₁₂₃₄₅₆₇₈₉"
            supA = "".join(superscripts[int(d)] for d in str(a))
            subZ = "".join(subscripts[int(d)] for d in str(z))
            txt = f"{sym}{supA}{subZ}  →  {R:.4f} fm"
            self.nr_outputs[0].config(text=txt)
            self._log("Nuclear R", f"{sym}-{a}", f"{R:.4f} fm")
            self._set_status("Nuclear radius computed.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    def _calc_bohr(self):
        try:
            n = int(self.bohr_n.get().strip())
            if n < 1: raise ValueError("n must be ≥ 1")
            a0_pm = 52.917721092  # pm
            an_pm = a0_pm * n * n
            self.bohr_outputs[0].config(text=f"{an_pm:.4f} pm")
            self._log("Bohr", f"n={n}", f"{an_pm:.4f} pm")
            self._set_status("Bohr radius computed.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

    # --- Thermodynamics ---
    def _tab_thermo(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="Thermodynamics")
        card = self._wrap_card(tab, "Conversions, Ideal Gas, Carnot")

        # Conversions
        ttk.Label(card, text="Temperature value").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        self.tmp_val = ttk.Entry(card, width=12); self.tmp_val.grid(row=1, column=1, sticky="w")
        ttk.Button(card, text="°F → °C", command=self._f_to_c).grid(row=1, column=2, padx=4)
        ttk.Button(card, text="°C → °F", command=self._c_to_f).grid(row=1, column=3, padx=4)
        ttk.Button(card, text="°C → K", command=self._c_to_k).grid(row=1, column=4, padx=4)
        ttk.Button(card, text="°F → K", command=self._f_to_k).grid(row=1, column=5, padx=4)
        self.temp_outputs = []
        self._add_copy_row(card, 2, "Result:", self.temp_outputs)

        ttk.Separator(card).grid(row=3, column=0, columnspan=6, sticky="ew", pady=8)

        # Ideal gas
        ttk.Label(card, text="Set exactly one of P, V, n, T to 0 to solve for it. Units: P[Pa], V[m³], n[mol], T[K]").grid(row=4, column=0, columnspan=6, sticky="w", padx=6, pady=4)
        ttk.Label(card, text="P").grid(row=5, column=0, sticky="e")
        ttk.Label(card, text="V").grid(row=5, column=2, sticky="e")
        ttk.Label(card, text="n").grid(row=5, column=4, sticky="e")
        ttk.Label(card, text="T").grid(row=5, column=5, sticky="e")

        self.P = ttk.Entry(card, width=14); self.P.grid(row=5, column=1, sticky="w")
        self.V = ttk.Entry(card, width=14); self.V.grid(row=5, column=3, sticky="w")
        self.nmol = ttk.Entry(card, width=14); self.nmol.grid(row=5, column=5, sticky="w")
        self.T = ttk.Entry(card, width=14); self.T.grid(row=5, column=6, sticky="w")
        ttk.Button(card, text="Calculate (Ideal Gas)", style="Accent.TButton", command=self._ideal_gas).grid(row=6, column=1, pady=6, sticky="w")
        self.ideal_outputs = []
        self._add_copy_row(card, 7, "Answer:", self.ideal_outputs)

        ttk.Separator(card).grid(row=8, column=0, columnspan=7, sticky="ew", pady=8)

        # Carnot
        ttk.Label(card, text="Carnot efficiency  η = 1 - Tc/Th").grid(row=9, column=0, columnspan=6, sticky="w", padx=6, pady=4)
        ttk.Label(card, text="Tc (K)").grid(row=10, column=0, sticky="e", padx=6)
        self.Tc = ttk.Entry(card, width=12); self.Tc.grid(row=10, column=1, sticky="w")
        ttk.Label(card, text="Th (K)").grid(row=10, column=2, sticky="e", padx=6)
        self.Th = ttk.Entry(card, width=12); self.Th.grid(row=10, column=3, sticky="w")
        ttk.Button(card, text="Calculate Efficiency", command=self._carnot).grid(row=10, column=4, sticky="w")
        self.carnot_outputs = []
        self._add_copy_row(card, 11, "η (%):", self.carnot_outputs)

    # Thermo calcs
    def _f_to_c(self):
        try:
            F = float(self.tmp_val.get().strip())
            C = (5/9)*(F-32)
            self.temp_outputs[0].config(text=f"{C:.4f} °C")
            self._log("Thermo", "F→C", f"{C:.4f} °C")
        except: messagebox.showerror("Input error", "Enter a valid number.")

    def _c_to_f(self):
        try:
            C = float(self.tmp_val.get().strip())
            F = (9/5)*C + 32
            self.temp_outputs[0].config(text=f"{F:.4f} °F")
            self._log("Thermo", "C→F", f"{F:.4f} °F")
        except: messagebox.showerror("Input error", "Enter a valid number.")

    def _c_to_k(self):
        try:
            C = float(self.tmp_val.get().strip())
            K = C + 273.15
            self.temp_outputs[0].config(text=f"{K:.4f} K")
            self._log("Thermo", "C→K", f"{K:.4f} K")
        except: messagebox.showerror("Input error", "Enter a valid number.")

    def _f_to_k(self):
        try:
            F = float(self.tmp_val.get().strip())
            K = (5/9)*(F-32)+273.15
            self.temp_outputs[0].config(text=f"{K:.4f} K")
            self._log("Thermo", "F→K", f"{K:.4f} K")
        except: messagebox.showerror("Input error", "Enter a valid number.")

    def _ideal_gas(self):
        try:
            P = float(self.P.get().strip() or "0")
            V = float(self.V.get().strip() or "0")
            n = float(self.nmol.get().strip() or "0")
            T = float(self.T.get().strip() or "0")
            if sum(x==0 for x in [P,V,n,T]) != 1:
                raise ValueError("Set exactly one variable to 0 to solve for it.")
            if any(x < 0 for x in [P,V,n,T] if x != 0):
                raise ValueError("Non-zero variables must be positive.")
            R = const.R
            if P == 0:
                P = (n*R*T)/V; ans = f"P = {fmt_si(P,'Pa')}"
            elif V == 0:
                V = (n*R*T)/P; ans = f"V = {V:.6g} m³"
            elif n == 0:
                n = (P*V)/(R*T); ans = f"n = {n:.6g} mol"
            else:  # T == 0
                T = (P*V)/(n*R); ans = f"T = {T:.6g} K"
            self.ideal_outputs[0].config(text=ans)
            self._log("Ideal Gas", "Result", ans)
            self._set_status("Ideal gas solved.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))
        except Exception as e: messagebox.showerror("Error", f"Unexpected error: {e}")

    def _carnot(self):
        try:
            Tc = float(self.Tc.get().strip())
            Th = float(self.Th.get().strip())
            if Tc < 0 or Th <= 0: raise ValueError("Temperatures must be ≥ 0 K, Th>0.")
            if Tc > Th: raise ValueError("Tc must be ≤ Th (cold ≤ hot).")
            eta = (1 - Tc/Th)*100.0
            eta = max(0.0, min(eta, 100.0))
            self.carnot_outputs[0].config(text=f"{eta:.2f} %")
            self._log("Carnot", f"Tc={Tc}, Th={Th}", f"{eta:.2f} %")
            self._set_status("Carnot efficiency computed.")
        except ValueError as ve: messagebox.showerror("Input error", str(ve))

if __name__ == "__main__":
    app = Phys112App()
    app.mainloop()
