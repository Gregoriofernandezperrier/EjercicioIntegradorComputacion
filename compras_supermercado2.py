import csv
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ARCHIVO_ENTRADA  = "COMPRAS_supermercado_desordenado_solo_sucursal.csv"
ARCHIVO_ORDENADO = "COMPRAS_supermercado_ordenado.csv"

# --- Lectura ---
with open(ARCHIVO_ENTRADA, newline="", encoding="utf-8-sig") as f:
    lector = csv.DictReader(f)
    campos = lector.fieldnames
    registros = list(lector)

# --- Bubble sort por sucursal ---
n = len(registros)
for i in range(n - 1):
    for j in range(n - 1 - i):
        if registros[j]["PRSUC"] > registros[j + 1]["PRSUC"]:
            registros[j], registros[j + 1] = registros[j + 1], registros[j]

# --- Grabado del archivo ordenado ---
with open(ARCHIVO_ORDENADO, "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(registros)

# --- Corte de control ---
total_registros = len(registros)
i = 0

def leer(idx):
    if idx < total_registros:
        r = registros[idx]
        return r["PRSUC"], r["PRCOD"], int(r["PRCANT"]), float(r["PRPRE"])
    return None

CANSUC   = 0
TOTALIMP = 0.0

reg = leer(i)
i += 1

while reg is not None:
    suc_actual = reg[0]
    CANSUC += 1
    TOTSUC_U = 0
    TOTSUC_P = 0.0
    MYPROD = MNPROD = None
    MYIMPOR = -1.0
    MNIMPOR = float("inf")

    print("=" * 60)
    print(f"SUCURSAL: {suc_actual}")
    print("=" * 60)

    while reg is not None and reg[0] == suc_actual:
        prod_actual = reg[1]
        TOTUNI = 0
        TOTPES = 0.0

        while reg is not None and reg[0] == suc_actual and reg[1] == prod_actual:
            _, _, cant, pre = reg
            TOTUNI += cant
            TOTPES += cant * pre
            reg = leer(i)
            i += 1

        TOTSUC_U += TOTUNI
        TOTSUC_P += TOTPES

        if TOTPES > MYIMPOR:
            MYPROD, MYIMPOR = prod_actual, TOTPES
        if TOTPES < MNIMPOR:
            MNPROD, MNIMPOR = prod_actual, TOTPES

        print(f"  Producto: {prod_actual}  |  Unidades: {TOTUNI:>6,}  |  Pesos: ${TOTPES:>12,.2f}")

    TOTALIMP += TOTSUC_P
    print("-" * 60)
    print(f"  Total unidades : {TOTSUC_U:,}")
    print(f"  Total pesos    : ${TOTSUC_P:,.2f}")
    print(f"  Mayor compra   : {MYPROD}  (${MYIMPOR:,.2f})")
    print(f"  Menor compra   : {MNPROD}  (${MNIMPOR:,.2f})\n")

print("=" * 60)
print(f"  Total sucursales : {CANSUC}")
print(f"  Compra total     : ${TOTALIMP:,.2f}")
print("=" * 60)