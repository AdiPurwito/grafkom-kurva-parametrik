import numpy as np

CLR_LINE_LOW    = '#00E5FF'   # cyan terang   → garis kurva low-res
CLR_POINT_LOW   = '#FF4081'   # pink/merah    → titik koordinat low-res
CLR_CENTER_LOW  = '#FF4081'   # sama          → pusat low-res
CLR_LINE_HIGH   = '#FFD600'   # kuning emas   → garis kurva high-res
CLR_POINT_HIGH  = "#efefef"   # putih         → titik koordinat high-res
CLR_CENTER_HI   = '#efefef'   # sama          → pusat high-res
CLR_AXIS        = '#546E7A'   # abu gelap     → sumbu X/Y
CLR_GRID        = '#37474F'   # abu lebih gelap → grid
BG_PANEL        = '#0D1117'   # hitam biru    → background panel
BG_FIG          = '#161B22'   # sedikit lebih terang → background figure
CLR_PANEL_SLD   = '#1C2128'   # background panel slider/tombol
CLR_BORDER      = '#444C56'   # garis tepi panel
CLR_TEXT        = '#ECEFF1'   # teks utama
CLR_TEXT_MUTE   = '#90A4AE'   # teks sekunder/label slider
CLR_ACCENT      = '#1D9E75'   # hijau teal    → tombol & status sukses


# HELPER PARSING INPUT (murni konversi nilai, tanpa UI)

def input_float(pesan):
    while True:
        try:
            return float(input(pesan))
        except ValueError:
            print("Input harus angka!")


def input_titik(pesan, default):
    while True:
        try:
            raw = input(f"{pesan} [default={default}]: ").strip()
            nilai = int(raw) if raw else default
            if nilai > 0:
                return nilai
            print("Jumlah titik harus > 0")
        except ValueError:
            print("Input harus bilangan bulat!")


def rentang(nilai, lebar, batas_bawah=None):
    """Hitung (vmin, vmax) yang pasti memuat nilai awal di tengah."""
    bawah = nilai - lebar
    atas  = nilai + lebar
    if batas_bawah is not None:
        bawah = max(bawah, batas_bawah)
        if atas <= bawah:
            atas = bawah + lebar
    return bawah, atas


def hitung_lingkaran(p):
    # ── [INPUT] ambil nilai dari slider
    xc, yc = p['xc'], p['yc']
    r  = max(p['r'], 0.1)
    nl = int(round(p['n_low']))
    nh = int(round(p['n_high']))

    # ── [INPUT] low res & high res (titik sampel) ──
    t_low  = np.linspace(0, 2 * np.pi, nl)
    t_high = np.linspace(0, 2 * np.pi, nh)

    # ── [RUMUS] 
    x_low  = xc + r * np.cos(t_low)
    y_low  = yc + r * np.sin(t_low)
    x_high = xc + r * np.cos(t_high)
    y_high = yc + r * np.sin(t_high)

    # ── [OUTPUT] GUI 
    return dict(x_low=x_low, y_low=y_low, x_high=x_high, y_high=y_high,
                center_x=xc, center_y=yc, t_low=t_low, t_high=t_high,
                judul="LINGKARAN",
                rumus="x = xc + r·cos(t)\ny = yc + r·sin(t)")


def hitung_elips(p):
    # ── [INPUT] ambil dari slider
    xc, yc = p['xc'], p['yc']
    a = max(abs(p['a']), 0.1)
    b = max(abs(p['b']), 0.1)
    nl = int(round(p['n_low']))
    nh = int(round(p['n_high']))

    # ── [INPUT] low res & high res (titik sampel) ──
    t_low  = np.linspace(0, 2 * np.pi, nl)
    t_high = np.linspace(0, 2 * np.pi, nh)

    # ── [RUMUS] 
    x_low  = xc + a * np.cos(t_low)
    y_low  = yc + b * np.sin(t_low)
    x_high = xc + a * np.cos(t_high)
    y_high = yc + b * np.sin(t_high)

    # ── [OUTPUT] GUI
    return dict(x_low=x_low, y_low=y_low, x_high=x_high, y_high=y_high,
                center_x=xc, center_y=yc, t_low=t_low, t_high=t_high,
                judul="ELIPS",
                rumus="x = xc + a·cos(t)\ny = yc + b·sin(t)")


def hitung_parabola(p):
    # ── [INPUT] ambil dari slider
    xp, yp = p['xp'], p['yp']
    a = p['a']
    if abs(a) < 0.1:
        a = 0.1 if a >= 0 else -0.1
    nl = int(round(p['n_low']))
    nh = int(round(p['n_high']))

    # ── [INPUT] low res & high res (titik sampel) ──
    t_low  = np.linspace(-3, 3, nl)
    t_high = np.linspace(-3, 3, nh)

    # ── [RUMUS] 
    x_low  = xp + a * t_low ** 2
    y_low  = yp + 2 * a * t_low
    x_high = xp + a * t_high ** 2
    y_high = yp + 2 * a * t_high

    # ── [OUTPUT] GUI 
    return dict(x_low=x_low, y_low=y_low, x_high=x_high, y_high=y_high,
                center_x=xp, center_y=yp, t_low=t_low, t_high=t_high,
                judul="PARABOLA",
                rumus="x = xp + a·t²\ny = yp + 2a·t")


def hitung_hiperbola(p):
    # ── [INPUT] ambil dari slider
    xc, yc = p['xc'], p['yc']
    a = max(abs(p['a']), 0.1)
    b = max(abs(p['b']), 0.1)
    nl = int(round(p['n_low']))
    nh = int(round(p['n_high']))

    # ── [INPUT] siasat eps bagi titik jadi 2 kelompok (cabang kanan/kiri)
    eps = 0.05
    half   = max(nl // 2, 2)
    half_h = max(nh // 2, 2)
    t1_l = np.linspace(-np.pi/2 + eps, np.pi/2 - eps, half)   # cabang kanan
    t2_l = np.linspace( np.pi/2 + eps, 3*np.pi/2 - eps, half) # cabang kiri

    # ── [RUMUS] 
    x1_l = xc + a / np.cos(t1_l); 
    y1_l = yc + b * np.tan(t1_l)
    x2_l = xc + a / np.cos(t2_l); 
    y2_l = yc + b * np.tan(t2_l)

    # ── [INPUT] sambung dua cabang pakai NaN biar gak ke-plot nyambung ──
    nanv = np.array([np.nan])
    x_low = np.concatenate([x1_l, nanv, x2_l])
    y_low = np.concatenate([y1_l, nanv, y2_l])
    t_low = np.concatenate([t1_l, nanv, t2_l])

    # (diulang lagi semua di atas, untuk versi high-res)
    t1_h = np.linspace(-np.pi/2 + eps, np.pi/2 - eps, half_h)
    t2_h = np.linspace( np.pi/2 + eps, 3*np.pi/2 - eps, half_h)

    # ── [RUMUS] rumus hiperbola lagi, versi high-res ────────────────────
    x1_h = xc + a / np.cos(t1_h); y1_h = yc + b * np.tan(t1_h)
    x2_h = xc + a / np.cos(t2_h); y2_h = yc + b * np.tan(t2_h)

    x_high = np.concatenate([x1_h, nanv, x2_h])
    y_high = np.concatenate([y1_h, nanv, y2_h])
    t_high = np.concatenate([t1_h, nanv, t2_h])

    # ── [OUTPUT] bungkus buat GUI ────────────────────────────────────────
    return dict(x_low=x_low, y_low=y_low, x_high=x_high, y_high=y_high,
                center_x=xc, center_y=yc, t_low=t_low, t_high=t_high,
                judul="HIPERBOLA",
                rumus="x = xc + a·sec(t)\ny = yc + b·tan(t)")


# STATISTIK TERMINAL — dipanggil ulang setiap "Terapkan Perubahan"

def print_statistik(data, waktu_render_low, waktu_render_high):
    x_low, y_low   = data['x_low'], data['y_low']
    x_high, y_high = data['x_high'], data['y_high']
    t_low, t_high  = data['t_low'], data['t_high']

    if t_low is not None:
        delta_t = np.diff(t_low)
    else:
        delta_t = np.full(max(len(x_low) - 1, 0), np.nan)
    jarak = np.sqrt(np.diff(x_low) ** 2 + np.diff(y_low) ** 2)

    n_low_valid  = int(np.sum(~np.isnan(x_low)))
    n_high_valid = int(np.sum(~np.isnan(x_high)))
    dt_valid = delta_t[~np.isnan(delta_t)]

    print("\n" + "=" * 40)
    print("  INFORMASI TITIK")
    print("=" * 40)
    print(f"  Jumlah Titik Low  : {n_low_valid}")
    print(f"  Jumlah Titik High : {n_high_valid}")
    if len(dt_valid) > 0:
        print(f"  Delta t Low  (Δt) : {dt_valid[0]:.6f} rad  (≈ {np.degrees(dt_valid[0]):.2f}°)")
    print("=" * 40)
    print("=" * 40)
    print("  WAKTU RENDER")
    print("=" * 40)
    print(f"  Low Resolution    : {waktu_render_low:.6f} detik")
    print(f"  High Resolution   : {waktu_render_high:.6f} detik")
    print(f"  Selisih (Hi - Lo) : {(waktu_render_high - waktu_render_low):.6f} detik")
    print("=" * 40)

    #  KOORDINAT LOW RESOLUTION 
    print("\n" + "=" * 64)
    print(f"KOORDINAT LOW RESOLUTION ({n_low_valid} titik)")
    print("=" * 64)
    print(f"{'No':<5} {'X':>12} {'Y':>12} {'Δt (rad)':>12} {'Jarak':>12}")
    print("-" * 64)
    no = 1
    for i, (xi, yi) in enumerate(zip(x_low, y_low)):
        if not (np.isnan(xi) or np.isnan(yi)):
            if i == 0 or np.isnan(delta_t[i - 1]):
                dt_str = "-"
                jr_str = "-"
            else:
                dt_str = f"{delta_t[i - 1]:.4f}"
                jr_str = f"{jarak[i - 1]:.4f}"
            print(f"{no:<5} {xi:>12.4f} {yi:>12.4f} {dt_str:>12} {jr_str:>12}")
            no += 1
    print("=" * 64)

    #  KOORDINAT HIGH RESOLUTION (10 titik sampel) 
    idx_valid_h = [i for i, (xi, yi) in enumerate(zip(x_high, y_high))
                   if not (np.isnan(xi) or np.isnan(yi))]
    N_SAMPEL = 10
    if len(idx_valid_h) <= N_SAMPEL:
        idx_sampel = idx_valid_h
    else:
        step = (len(idx_valid_h) - 1) / (N_SAMPEL - 1)
        idx_sampel = [idx_valid_h[round(i * step)] for i in range(N_SAMPEL)]

    jarak_h = np.sqrt(np.diff(x_high) ** 2 + np.diff(y_high) ** 2)

    if t_high is not None:
        delta_t_h = np.diff(t_high)
    else:
        delta_t_h = np.full(max(len(x_high) - 1, 0), np.nan)

    print("\n" + "=" * 64)
    print(f"KOORDINAT HIGH RESOLUTION  (sampel {len(idx_sampel)} dari {n_high_valid} titik)")
    print("=" * 64)
    print(f"{'No':<5} {'X':>12} {'Y':>12} {'Δt (rad)':>12} {'Jarak':>12}")
    print("-" * 64)
    for urut, idx in enumerate(idx_sampel, start=1):
        xi = x_high[idx]
        yi = y_high[idx]
        if idx == 0 or (idx > 0 and np.isnan(delta_t_h[idx - 1])):
            dt_str = "-"
        else:
            dt_str = f"{delta_t_h[idx - 1]:.4f}"
        if idx < len(x_high) - 1 and not np.isnan(jarak_h[idx]):
            jr_str = f"{jarak_h[idx]:.4f}"
        else:
            jr_str = "-"
        print(f"{urut:<5} {xi:>12.4f} {yi:>12.4f} {dt_str:>12} {jr_str:>12}")
    print("=" * 64)
