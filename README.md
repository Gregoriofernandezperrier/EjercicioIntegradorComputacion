# Sistema de Procesamiento de Compras de Supermercado

Procesamiento y análisis de registros de compras de múltiples sucursales a partir de un archivo CSV.
Implementa ordenamiento burbuja y corte de control para generar reportes por sucursal.

## Descripción del algoritmo

El sistema realiza los siguientes pasos:

1. **Lectura** del CSV de entrada con registros de compras desordenados
2. **Ordenamiento** de los registros por sucursal usando el algoritmo de burbuja
3. **Corte de control** por sucursal y producto para acumular totales
4. **Reporte** con totales por sucursal, producto de mayor y menor importe, y totales generales

## Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `compras_supermercado.py` | Código principal: lectura de CSV, ordenamiento burbuja, corte de control y generación de reporte |
| `COMPRAS_supermercado_desordenado_solo_sucursal.csv` | Datos de entrada con registros de compras desordenados |
| `test_compras.py` | Tests unitarios con pytest |
| `requirements.txt` | Dependencias del proyecto |
| `.github/workflows/ci.yml` | Pipeline de integración continua con GitHub Actions |

## Cómo correr los tests

**Instalar dependencias:**

```bash
pip install -r requirements.txt
```

**Ejecutar los tests:**

```bash
pytest test_compras.py -v
```

## Cobertura de tests

Los tests cubren:

- Ordenamiento burbuja (lista desordenada, ya ordenada, un elemento, orden inverso)
- Cálculo de total de unidades y pesos por producto
- Detección del producto con mayor y menor importe por sucursal
- Procesamiento completo de una sucursal
- Conteo de sucursales y total de importe general

## Integración continua

Cada pull request hacia `main` dispara automáticamente el pipeline de CI definido en `.github/workflows/ci.yml`.
El merge solo se permite si todos los tests pasan.
