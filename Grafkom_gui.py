import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.widgets import Slider, Button

try:
    import mplcursors
    _CURSORS_OK = True
except ImportError:
    _CURSORS_OK = False

from Grafkom_logic import (
    CLR_LINE_LOW, CLR_POINT_LOW, CLR_CENTER_LOW,
    CLR_LINE_HIGH, CLR_POINT_HIGH, CLR_CENTER_HI,
    CLR_AXIS, BG_PANEL, BG_FIG, CLR_PANEL_SLD,
    CLR_BORDER, CLR_TEXT, CLR_TEXT_MUTE, CLR_ACCENT,
    print_statistik,
)

plt.style.use('dark_background')

def _render_plot(ax_low, ax_high, fig, data):
    ax_low.clear()
    ax_high.clear()

    for a in (ax_low, ax_high):
        a.set_facecolor(BG_PANEL)
        for spine in a.spines.values():
            spine.set_edgecolor('#30363D')

    x_low, y_low   = data['x_low'], data['y_low']
    x_high, y_high = data['x_high'], data['y_high']
    cx, cy         = data['center_x'], data['center_y']

    # ── LOW RESOLUTION ────────────────────────────────────────────────
    start_render_low = time.perf_counter()
    ax_low.plot(x_low, y_low,
                color=CLR_LINE_LOW, linestyle='-', linewidth=1.8,
                label='Garis Kurva', zorder=2)
    sc_low = ax_low.scatter(x_low[~np.isnan(x_low)], y_low[~np.isnan(y_low)],
                  color=CLR_POINT_LOW, s=52, zorder=4, label='Titik Koordinat',
                  edgecolors='white', linewidths=0.4)
    sc_center_low = ax_low.scatter(cx, cy,
                  color=CLR_CENTER_LOW, s=160, zorder=5, label='Pusat Kurva',
                  marker='*', edgecolors='white', linewidths=0.5)
    ax_low.axhline(0, color=CLR_AXIS, linewidth=0.8, zorder=1)
    ax_low.axvline(0, color=CLR_AXIS, linewidth=0.8, zorder=1)
    ax_low.grid(True, linestyle='--', alpha=0.25, color='#90A4AE', zorder=0)
    n_low_titik = int(np.sum(~np.isnan(x_low)))
    ax_low.set_title(f"Low Resolution  ·  {n_low_titik} titik",
                    color=CLR_TEXT, fontsize=12, pad=10, fontweight='bold')
    ax_low.axis('equal')
    ax_low.tick_params(colors='#78909C', labelsize=8)
    end_render_low = time.perf_counter()

    # ── HIGH RESOLUTION ───────────────────────────────────────────────
    start_render_high = time.perf_counter()
    ax_high.plot(x_high, y_high,
               color=CLR_LINE_HIGH, linewidth=1.8, label='Garis Kurva', zorder=2)
    sc_high = ax_high.scatter(x_high[~np.isnan(x_high)], y_high[~np.isnan(y_high)],
                  color=CLR_POINT_HIGH, s=18, zorder=4, label='Titik Koordinat')
    sc_center_high = ax_high.scatter(cx, cy,
                  color=CLR_CENTER_HI, s=160, zorder=5, label='Pusat Kurva',
                  marker='*', edgecolors='white', linewidths=0.5)
    ax_high.axhline(0, color=CLR_AXIS, linewidth=0.8, zorder=1)
    ax_high.axvline(0, color=CLR_AXIS, linewidth=0.8, zorder=1)
    ax_high.grid(True, linestyle='--', alpha=0.25, color='#90A4AE', zorder=0)
    n_high_titik = int(np.sum(~np.isnan(x_high)))
    ax_high.set_title(f"High Resolution  ·  {n_high_titik} titik",
                    color=CLR_TEXT, fontsize=12, pad=10, fontweight='bold')
    ax_high.axis('equal')
    ax_high.tick_params(colors='#78909C', labelsize=8)
    end_render_high = time.perf_counter()

    # ── Judul utama ───────────────────────────────────────────────────
    fig.suptitle(f"VISUALISASI KURVA PARAMETRIK  ·  {data['judul']}",
                 fontsize=15, color=CLR_TEXT, fontweight='bold', y=0.965)

    # ── Legend LOW (kiri atas, luar kotak plot) ──────────────────────
    handles_low = [
        Line2D([0], [0], color=CLR_LINE_LOW,  linewidth=2,  label='Garis Kurva'),
        Line2D([0], [0], color=CLR_POINT_LOW, marker='o', linestyle='None',
               markersize=7, label='Titik Koordinat'),
        Line2D([0], [0], color=CLR_CENTER_LOW, marker='*', linestyle='None',
               markersize=10, label='Pusat Kurva'),
    ]
    ax_low.legend(handles=handles_low,
                 facecolor=CLR_PANEL_SLD, edgecolor=CLR_BORDER,
                 labelcolor=CLR_TEXT, fontsize=8.5,
                 markerscale=1.1,
                 loc='upper left',
                 bbox_to_anchor=(0.0, 1.0),
                 bbox_transform=ax_low.transAxes)

    handles_high = [
        Line2D([0], [0], color=CLR_LINE_HIGH,  linewidth=2,  label='Garis Kurva'),
        Line2D([0], [0], color=CLR_POINT_HIGH, marker='o', linestyle='None',
               markersize=7, label='Titik Koordinat'),
        Line2D([0], [0], color=CLR_CENTER_HI,  marker='*', linestyle='None',
               markersize=10, label='Pusat Kurva'),
    ]
    ax_high.legend(handles=handles_high,
                 facecolor=CLR_PANEL_SLD, edgecolor=CLR_BORDER,
                 labelcolor=CLR_TEXT, fontsize=8.5,
                 markerscale=1.1,
                 loc='upper right',
                 bbox_to_anchor=(1.0, 1.0),
                 bbox_transform=ax_high.transAxes)

    waktu_render_low  = end_render_low  - start_render_low
    waktu_render_high = end_render_high - start_render_high

    return sc_low, sc_high, sc_center_low, sc_center_high, waktu_render_low, waktu_render_high


def _setup_rumus_text(fig, ax_high, rumus):
    """Kotak rumus ditempel di dalam pojok kanan-bawah panel High-Res
    (sedikit digeser ke atas dibanding versi awal, supaya tidak
    bertabrakan dengan panel slider di bawahnya)."""
    fig.canvas.draw()
    pos1 = ax_high.get_position()
    return fig.text(
        pos1.x1 - 0.005, pos1.y0 + 0.015,
        rumus,
        ha='right', va='bottom',
        fontsize=10, color='#CFD8DC', family='monospace',
        fontweight='semibold',
        bbox=dict(facecolor=CLR_PANEL_SLD, edgecolor=CLR_BORDER,
                  boxstyle='round,pad=0.5', alpha=0.95)
    )


def _setup_hover(sc_low, sc_high, sc_center_low, sc_center_high):
    cursors = []
    if not _CURSORS_OK:
        return cursors

    def _fmt(sel, label_prefix="Titik", show_no=True):
        x_val, y_val = sel.target
        no_line = f"No. {sel.index + 1}\n" if show_no else ""
        sel.annotation.set_text(
            f"{label_prefix}\n{no_line}X = {x_val:.4f}\nY = {y_val:.4f}"
        )
        sel.annotation.get_bbox_patch().set(
            facecolor=CLR_PANEL_SLD, edgecolor=CLR_BORDER, alpha=0.95)
        sel.annotation.set_color(CLR_TEXT)
        sel.annotation.set_fontsize(9)
        sel.annotation.set_fontfamily('monospace')

    c1 = mplcursors.cursor(sc_low, hover=True)
    c1.connect("add", lambda sel: _fmt(sel, "Titik Low", True))
    cursors.append(c1)

    c2 = mplcursors.cursor(sc_center_low, hover=True)
    c2.connect("add", lambda sel: _fmt(sel, "Pusat", False))
    cursors.append(c2)

    c3 = mplcursors.cursor(sc_high, hover=True)
    c3.connect("add", lambda sel: _fmt(sel, "Titik High", True))
    cursors.append(c3)

    c4 = mplcursors.cursor(sc_center_high, hover=True)
    c4.connect("add", lambda sel: _fmt(sel, "Pusat", False))
    cursors.append(c4)

    return cursors


def _bersihkan_cursor(cursors):
    for c in cursors:
        try:
            c.remove()
        except Exception:
            pass
    cursors.clear()

def _buat_slider(fig, rect, spec):
    ax_s = fig.add_axes(rect)
    ax_s.set_facecolor('none')          # panel transparan, track yang gambar bentuknya
    for sp in ax_s.spines.values():
        sp.set_visible(False)           # hilangkan kotak kaku di sekeliling slider

    s = Slider(ax_s, spec['label'], spec['vmin'], spec['vmax'],
               valinit=spec['vinit'], valstep=spec['vstep'],
               valfmt=spec.get('fmt', '%.2f'),
               initcolor='none')        # buang garis merah penanda nilai awal

    # ── track: lebih tipis & ujung membulat (kesan pill-shape) ─────────
    if hasattr(s, 'track'):
        s.track.set_facecolor('#0D1117')
        s.track.set_edgecolor(CLR_BORDER)
        s.track.set_linewidth(0.8)
        try:
            h_baru = s.track.get_height() * 0.4
            s.track.set_y(0.5 - h_baru / 2)
            s.track.set_height(h_baru)
            s.track.set_capstyle('round')
        except Exception:
            pass

    # ── poly: bagian terisi, warna cyan, dipertipis senada dgn track ───
    s.poly.set_facecolor(CLR_LINE_LOW)
    s.poly.set_edgecolor('none')
    s.poly.set_capstyle('round')
    try:
        verts = s.poly.get_xy()
        ymin, ymax = verts[:, 1].min(), verts[:, 1].max()
        ymid = (ymin + ymax) / 2
        h_baru = (ymax - ymin) * 0.4
        verts[:, 1] = np.where(verts[:, 1] > ymid, ymid + h_baru / 2, ymid - h_baru / 2)
        s.poly.set_xy(verts)
    except Exception:
        pass

    # ── handle (lingkaran geser): perbesar & beri outline aksen cyan ───
    if hasattr(s, '_handle'):
        s._handle.set_markersize(11)
        s._handle.set_markerfacecolor(CLR_TEXT)
        s._handle.set_markeredgecolor(CLR_LINE_LOW)
        s._handle.set_markeredgewidth(1.6)
        s._handle.set_zorder(5)

    # ── label & valtext: ditaruh DI ATAS track, di dalam batas axes ────
    # (default matplotlib menaruhnya di luar kiri/kanan axes, sehingga
    #  nabrak kolom slider tetangga saat jaraknya mepet)
    s.label.set_position((0.0, -0.55))
    s.label.set_ha('left')
    s.label.set_va('top')
    s.label.set_color(CLR_TEXT_MUTE)
    s.label.set_fontsize(8.5)

    s.valtext.set_position((1.0, -0.55))
    s.valtext.set_ha('right')
    s.valtext.set_va('top')
    s.valtext.set_color(CLR_LINE_LOW)
    s.valtext.set_fontsize(9.5)
    s.valtext.set_fontweight('bold')
    return s


def _buat_tombol(fig, rect, label):
    ax_b = fig.add_axes(rect)
    btn = Button(ax_b, label, color=CLR_PANEL_SLD, hovercolor=CLR_ACCENT)
    btn.label.set_color(CLR_TEXT)
    btn.label.set_fontsize(11)
    btn.label.set_fontweight('bold')
    for sp in ax_b.spines.values():
        sp.set_color(CLR_ACCENT)
        sp.set_linewidth(1.2)
    return btn


# Posisi grid slider: 2 baris x 3 kolom di panel bawah (figure-fraction coords)
_KOL_X  = [0.07, 0.385, 0.70]
_KOL_W  = 0.255
_ROW_Y  = [0.225, 0.135]
_ROW_H  = 0.038



def visualisasi_interaktif(hitung_data, slider_specs):
    params = {sp['key']: sp['vinit'] for sp in slider_specs}
    data = hitung_data(params)

    fig, (ax_low, ax_high) = plt.subplots(
        1, 2, figsize=(17, 11.5), facecolor=BG_FIG,
        gridspec_kw={'wspace': 0.08}
    )
    fig.subplots_adjust(top=0.90, bottom=0.34, left=0.06, right=0.97)

    sc_low, sc_high, sc_center_low, sc_center_high, wl, wh = _render_plot(
        ax_low, ax_high, fig, data)
    teks_rumus = _setup_rumus_text(fig, ax_high, data['rumus'])

    print(f"\n[INFO] Membuka visualisasi interaktif — {data['judul']}.")
    print("[INFO] Geser slider lalu klik 'Terapkan Perubahan' untuk update.")
    print("[INFO] Tutup jendela grafik untuk kembali ke menu.")
    if not _CURSORS_OK:
        print("[INFO] Install mplcursors untuk fitur hover: pip install mplcursors")

    print_statistik(data, wl, wh)

    cursors = _setup_hover(sc_low, sc_high, sc_center_low, sc_center_high)

    # ── Panel kontrol (garis pemisah + judul panel) ──────────────────
    fig.add_artist(Line2D([0.05, 0.95], [0.305, 0.305],
                           transform=fig.transFigure,
                           color=CLR_BORDER, linewidth=1))
    fig.text(0.07, 0.282, "KONTROL PARAMETER (SLIDER)",
              fontsize=10.5, color=CLR_ACCENT, fontweight='bold',
              family='monospace')
    fig.text(0.07, 0.263, "Geser nilai, lalu klik tombol di bawah untuk menerapkan",
              fontsize=8.5, color=CLR_TEXT_MUTE)

    # ── Buat slider sesuai grid 2x3 ───────────────────────────────────
    posisi = [(c, r) for r in _ROW_Y for c in _KOL_X]
    sliders = []
    for spec, (x, y) in zip(slider_specs, posisi):
        rect = [x, y, _KOL_W, _ROW_H]
        sliders.append(_buat_slider(fig, rect, spec))

    # ── Tombol Terapkan + status ──────────────────────────────────────
    tombol_terapkan = _buat_tombol(fig, [0.40, 0.045, 0.20, 0.05],
                                    "✓ Terapkan Perubahan")
    status_text = fig.text(0.64, 0.07, "Status: nilai awal aktif",
                            fontsize=9.5, color=CLR_TEXT_MUTE, va='center')

    def on_terapkan(event):
        for spec, sld in zip(slider_specs, sliders):
            params[spec['key']] = sld.val

        data_baru = hitung_data(params)
        sc_l, sc_h, sc_cl, sc_ch, wl2, wh2 = _render_plot(
            ax_low, ax_high, fig, data_baru)

        _bersihkan_cursor(cursors)
        cursors.extend(_setup_hover(sc_l, sc_h, sc_cl, sc_ch))

        print_statistik(data_baru, wl2, wh2)

        waktu_sekarang = time.strftime('%H:%M:%S')
        status_text.set_text(f"✓ Diperbarui pukul {waktu_sekarang}")
        status_text.set_color(CLR_ACCENT)

        fig.canvas.draw_idle()

    tombol_terapkan.on_clicked(on_terapkan)

    plt.show(block=True)
    plt.close(fig)
    print("\n[INFO] Jendela ditutup. Kembali ke menu.\n")