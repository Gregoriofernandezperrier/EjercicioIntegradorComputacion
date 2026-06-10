import csv
import os


def leer_csv(path):
    archivo = open(path, newline="", encoding="utf-8-sig")
    lector = csv.DictReader(archivo)
    filas = list(lector)
    encabezados = lector.fieldnames
    archivo.close()
    return filas, encabezados


def escribir_csv(path, filas, encabezados):
    archivo = open(path, "w", newline="", encoding="utf-8-sig")
    escritor = csv.DictWriter(archivo, fieldnames=encabezados)
    escritor.writeheader()
    escritor.writerows(filas)
    archivo.close()


def ordenar_burbuja(filas):
    n = len(filas)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if filas[j]["PRSUC"] > filas[j + 1]["PRSUC"]:
                filas[j], filas[j + 1] = filas[j + 1], filas[j]
    return filas


def procesar_corte_control(filas):
    n = len(filas)
    i = 0

    CANSUC = 0
    TOTALIMP = 0.0

    resultado = {
        "sucursales": [],
        "totales_generales": {}
    }

    while i < n:
        suc_actual = filas[i]["PRSUC"]

        TOTSUC_U = 0
        TOTSUC_P = 0.0
        MYPROD = None
        MYIMPOR = -1.0
        MNPROD = None
        MNIMPOR = float("inf")

        productos = []

        while i < n and filas[i]["PRSUC"] == suc_actual:
            prod_actual = filas[i]["PRCOD"]

            TOTUNI = 0
            TOTPES = 0.0

            while i < n and filas[i]["PRSUC"] == suc_actual and filas[i]["PRCOD"] == prod_actual:
                cant = int(filas[i]["PRCANT"])
                pre = float(filas[i]["PRPRE"])
                TOTUNI += cant
                TOTPES += cant * pre
                i += 1

            productos.append({
                "producto": prod_actual,
                "total_unidades": TOTUNI,
                "total_pesos": TOTPES
            })

            TOTSUC_U += TOTUNI
            TOTSUC_P += TOTPES

            if TOTPES > MYIMPOR:
                MYIMPOR = TOTPES
                MYPROD = prod_actual

            if TOTPES < MNIMPOR:
                MNIMPOR = TOTPES
                MNPROD = prod_actual

        resultado["sucursales"].append({
            "sucursal": suc_actual,
            "productos": productos,
            "total_unidades": TOTSUC_U,
            "mayor_producto": MYPROD,
            "mayor_importe": MYIMPOR,
            "menor_producto": MNPROD,
            "menor_importe": MNIMPOR
        })

        CANSUC += 1
        TOTALIMP += TOTSUC_P

    resultado["totales_generales"] = {
        "cantidad_sucursales": CANSUC,
        "total_importe": TOTALIMP
    }

    return resultado


def mostrar_resultado(resultado):
    for sucursal in resultado["sucursales"]:
        print("=" * 60)
        print(f"SUCURSAL: {sucursal['sucursal']}")
        print("=" * 60)

        for producto in sucursal["productos"]:
            print(f"  Producto: {producto['producto']}  |  "
                  f"Unidades: {producto['total_unidades']:>6,}  |  "
                  f"Pesos: ${producto['total_pesos']:>12,.2f}")

        print("-" * 60)
        print(f"  Total unidades : {sucursal['total_unidades']:,}")
        print(f"  Mayor compra   : {sucursal['mayor_producto']}  (${sucursal['mayor_importe']:,.2f})")
        print(f"  Menor compra   : {sucursal['menor_producto']}  (${sucursal['menor_importe']:,.2f})\n")

    print("=" * 60)
    print(f"  Total sucursales : {resultado['totales_generales']['cantidad_sucursales']}")
    print(f"  Compra total     : ${resultado['totales_generales']['total_importe']:,.2f}")
    print("=" * 60)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    ARCHIVO_ENTRADA = "COMPRAS_supermercado_desordenado_solo_sucursal.csv"
    ARCHIVO_ORDENADO = "COMPRAS_supermercado_ordenado.csv"

    filas, encabezados = leer_csv(ARCHIVO_ENTRADA)
    filas = ordenar_burbuja(filas)
    escribir_csv(ARCHIVO_ORDENADO, filas, encabezados)

    resultado = procesar_corte_control(filas)
    mostrar_resultado(resultado)


if __name__ == "__main__":
    main()
