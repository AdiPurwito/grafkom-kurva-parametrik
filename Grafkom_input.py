from Grafkom_logic import (
    input_float, input_titik, rentang,
    hitung_lingkaran, hitung_elips, hitung_parabola, hitung_hiperbola,
)
from Grafkom_gui import visualisasi_interaktif

def lingkaran():
    print("\n--- Input Awal: LINGKARAN ---")
    xc = input_float("Pusat X      : ")
    yc = input_float("Pusat Y      : ")
    r  = input_float("Radius       : ")

    if r <= 0:
        print("Radius harus > 0")
        return

    n_low  = input_titik("Jumlah Titik Low Res ", 10)
    n_high = input_titik("Jumlah Titik High Res", 100)

    bx = rentang(xc, 50)
    by = rentang(yc, 50)
    br = rentang(r, 30, 0.5)

    specs = [
        dict(key='xc', label='Pusat X (xc)', vmin=bx[0], vmax=bx[1],
             vinit=xc, vstep=0.5),
        dict(key='yc', label='Pusat Y (yc)', vmin=by[0], vmax=by[1],
             vinit=yc, vstep=0.5),
        dict(key='r', label='Radius (r)', vmin=br[0], vmax=br[1],
             vinit=r, vstep=0.5),
        dict(key='n_low', label='Titik Low-Res', vmin=4,
             vmax=max(60, n_low + 20), vinit=n_low, vstep=1, fmt='%d'),
        dict(key='n_high', label='Titik High-Res', vmin=10,
             vmax=max(400, n_high + 100), vinit=n_high, vstep=5, fmt='%d'),
    ]

    visualisasi_interaktif(hitung_lingkaran, specs)

def elips():
    print("\n--- Input Awal: ELIPS ---")
    xc = input_float("Pusat X      : ")
    yc = input_float("Pusat Y      : ")
    a  = input_float("Semi Mayor a : ")
    b  = input_float("Semi Minor b : ")

    n_low  = input_titik("Jumlah Titik Low Res ", 10)
    n_high = input_titik("Jumlah Titik High Res", 100)

    bx = rentang(xc, 50)
    by = rentang(yc, 50)
    ba = rentang(a, 30, 0.5)
    bb = rentang(b, 30, 0.5)

    specs = [
        dict(key='xc', label='Pusat X (xc)', vmin=bx[0], vmax=bx[1],
             vinit=xc, vstep=0.5),
        dict(key='yc', label='Pusat Y (yc)', vmin=by[0], vmax=by[1],
             vinit=yc, vstep=0.5),
        dict(key='a', label='Semi Mayor (a)', vmin=ba[0], vmax=ba[1],
             vinit=a, vstep=0.5),
        dict(key='b', label='Semi Minor (b)', vmin=bb[0], vmax=bb[1],
             vinit=b, vstep=0.5),
        dict(key='n_low', label='Titik Low-Res', vmin=4,
             vmax=max(60, n_low + 20), vinit=n_low, vstep=1, fmt='%d'),
        dict(key='n_high', label='Titik High-Res', vmin=10,
             vmax=max(400, n_high + 100), vinit=n_high, vstep=5, fmt='%d'),
    ]

    visualisasi_interaktif(hitung_elips, specs)

def parabola():
    print("\n--- Input Awal: PARABOLA ---")
    xp = input_float("Vertex X     : ")
    yp = input_float("Vertex Y     : ")
    a  = input_float("Nilai a      : ")

    n_low  = input_titik("Jumlah Titik Low Res ", 10)
    n_high = input_titik("Jumlah Titik High Res", 100)

    bxp = rentang(xp, 50)
    byp = rentang(yp, 50)
    ba  = rentang(a, 20)

    specs = [
        dict(key='xp', label='Vertex X (xp)', vmin=bxp[0], vmax=bxp[1],
             vinit=xp, vstep=0.5),
        dict(key='yp', label='Vertex Y (yp)', vmin=byp[0], vmax=byp[1],
             vinit=yp, vstep=0.5),
        dict(key='a', label='Nilai a', vmin=ba[0], vmax=ba[1],
             vinit=a, vstep=0.5),
        dict(key='n_low', label='Titik Low-Res', vmin=4,
             vmax=max(60, n_low + 20), vinit=n_low, vstep=1, fmt='%d'),
        dict(key='n_high', label='Titik High-Res', vmin=10,
             vmax=max(400, n_high + 100), vinit=n_high, vstep=5, fmt='%d'),
    ]

    visualisasi_interaktif(hitung_parabola, specs)

def hiperbola():
    print("\n--- Input Awal: HIPERBOLA ---")
    xc = input_float("Pusat X      : ")
    yc = input_float("Pusat Y      : ")
    a  = abs(input_float("Nilai a      : "))
    b  = abs(input_float("Nilai b      : "))

    n_low  = input_titik("Jumlah Titik Low Res ", 10)
    n_high = input_titik("Jumlah Titik High Res", 100)

    bx = rentang(xc, 50)
    by = rentang(yc, 50)
    ba = rentang(a, 30, 0.5)
    bb = rentang(b, 30, 0.5)

    specs = [
        dict(key='xc', label='Pusat X (xc)', vmin=bx[0], vmax=bx[1],
             vinit=xc, vstep=0.5),
        dict(key='yc', label='Pusat Y (yc)', vmin=by[0], vmax=by[1],
             vinit=yc, vstep=0.5),
        dict(key='a', label='Nilai a', vmin=ba[0], vmax=ba[1],
             vinit=a, vstep=0.5),
        dict(key='b', label='Nilai b', vmin=bb[0], vmax=bb[1],
             vinit=b, vstep=0.5),
        dict(key='n_low', label='Titik Low-Res', vmin=4,
             vmax=max(60, n_low + 20), vinit=n_low, vstep=1, fmt='%d'),
        dict(key='n_high', label='Titik High-Res', vmin=10,
             vmax=max(400, n_high + 100), vinit=n_high, vstep=5, fmt='%d'),
    ]

    visualisasi_interaktif(hitung_hiperbola, specs)

def menu():
    while True:
        print("\n" + "=" * 50)
        print(" VISUALISASI KURVA PARAMETRIK ")
        print("=" * 50)
        print("1. Lingkaran")
        print("2. Elips")
        print("3. Parabola")
        print("4. Hiperbola")
        print("0. Keluar")
        print("=" * 50)

        pilih = input("Pilih Menu : ")

        if   pilih == "1": lingkaran()
        elif pilih == "2": elips()
        elif pilih == "3": parabola()
        elif pilih == "4": hiperbola()
        elif pilih == "0":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak tersedia!")


if __name__ == "__main__":
    menu()
