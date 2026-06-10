import pytest
from compras_supermercado import ordenar_burbuja, procesar_corte_control


def fila(suc, cod, cant, pre):
    return {"PRSUC": suc, "PRCOD": cod, "PRFEC": "2025-01-01", "PRPROV": "PROV01",
            "PRCANT": str(cant), "PRPRE": str(pre)}


# --- ordenar_burbuja ---

def test_ordenar_burbuja_desordenado():
    filas = [fila("SUC03", "P001", 1, 10), fila("SUC01", "P001", 1, 10), fila("SUC02", "P001", 1, 10)]
    resultado = ordenar_burbuja(filas)
    sucursales = [r["PRSUC"] for r in resultado]
    assert sucursales == ["SUC01", "SUC02", "SUC03"]


def test_ordenar_burbuja_ya_ordenado():
    filas = [fila("SUC01", "P001", 1, 10), fila("SUC02", "P001", 1, 10)]
    resultado = ordenar_burbuja(filas)
    assert resultado[0]["PRSUC"] == "SUC01"
    assert resultado[1]["PRSUC"] == "SUC02"


def test_ordenar_burbuja_un_elemento():
    filas = [fila("SUC01", "P001", 5, 100)]
    resultado = ordenar_burbuja(filas)
    assert len(resultado) == 1
    assert resultado[0]["PRSUC"] == "SUC01"


def test_ordenar_burbuja_orden_inverso():
    filas = [fila("SUC05", "P001", 1, 10), fila("SUC04", "P001", 1, 10),
             fila("SUC03", "P001", 1, 10), fila("SUC02", "P001", 1, 10)]
    resultado = ordenar_burbuja(filas)
    sucursales = [r["PRSUC"] for r in resultado]
    assert sucursales == ["SUC02", "SUC03", "SUC04", "SUC05"]


# --- procesar_corte_control ---

FILAS_SUC01 = [
    fila("SUC01", "P001", 10, 100.0),
    fila("SUC01", "P001", 5, 100.0),
    fila("SUC01", "P002", 3, 50.0),
]
# P001: (10+5)*100 = 1500.0  |  P002: 3*50 = 150.0
# total_unidades = 18, total_pesos = 1650.0


def test_total_unidades_sucursal():
    resultado = procesar_corte_control(FILAS_SUC01)
    suc = resultado["sucursales"][0]
    assert suc["total_unidades"] == 18


def test_total_pesos_producto():
    resultado = procesar_corte_control(FILAS_SUC01)
    suc = resultado["sucursales"][0]
    prod_p001 = next(p for p in suc["productos"] if p["producto"] == "P001")
    assert prod_p001["total_pesos"] == pytest.approx(1500.0)


def test_mayor_importe():
    resultado = procesar_corte_control(FILAS_SUC01)
    suc = resultado["sucursales"][0]
    assert suc["mayor_producto"] == "P001"
    assert suc["mayor_importe"] == pytest.approx(1500.0)


def test_menor_importe():
    resultado = procesar_corte_control(FILAS_SUC01)
    suc = resultado["sucursales"][0]
    assert suc["menor_producto"] == "P002"
    assert suc["menor_importe"] == pytest.approx(150.0)


def test_procesamiento_sucursal_completa():
    resultado = procesar_corte_control(FILAS_SUC01)
    assert len(resultado["sucursales"]) == 1
    suc = resultado["sucursales"][0]
    assert suc["sucursal"] == "SUC01"
    assert len(suc["productos"]) == 2
    assert suc["total_unidades"] == 18
    assert suc["mayor_producto"] == "P001"
    assert suc["menor_producto"] == "P002"


def test_cantidad_sucursales():
    filas = FILAS_SUC01 + [fila("SUC02", "P001", 2, 200.0)]
    resultado = procesar_corte_control(filas)
    assert resultado["totales_generales"]["cantidad_sucursales"] == 2


def test_total_importe_general():
    filas = FILAS_SUC01 + [fila("SUC02", "P001", 2, 200.0)]
    resultado = procesar_corte_control(filas)
    # SUC01: 1650.0 + SUC02: 2*200 = 400.0 => 2050.0
    assert resultado["totales_generales"]["total_importe"] == pytest.approx(2050.0)


def test_error_intencional():
    # Este test falla intencionalmente para verificar que el pipeline bloquea el merge
    resultado = procesar_corte_control(FILAS_SUC01)
    assert resultado["totales_generales"]["cantidad_sucursales"] == 99
