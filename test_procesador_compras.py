import csv

import pytest

from procesador_compras import (
    Compra,
    calcular_total,
    calcular_total_por_sucursal,
    calcular_unidades_por_producto,
    crear_compra,
    leer_compras,
    ordenar_compras,
    producto_mas_vendido,
    resumen_compras,
    validar_archivo,
)


@pytest.fixture
def compras():
    return [
        Compra("SUC02", "P200", "2025-01-02", "PROV01", 3, 20.0),
        Compra("SUC01", "P100", "2025-01-01", "PROV02", 2, 10.0),
        Compra("SUC01", "P200", "2025-01-03", "PROV03", 5, 20.0),
    ]


def test_validar_archivo_existente(tmp_path):
    archivo = tmp_path / "compras.csv"
    archivo.write_text("PRSUC,PRCOD,PRFEC,PRPROV,PRCANT,PRPRE\n", encoding="utf-8")

    assert validar_archivo(archivo) is True


def test_validar_archivo_inexistente(tmp_path):
    assert validar_archivo(tmp_path / "no_existe.csv") is False


def test_crear_compra_convierte_tipos():
    compra = crear_compra(
        {
            "PRSUC": "SUC01",
            "PRCOD": "P100",
            "PRFEC": "2025-01-01",
            "PRPROV": "PROV01",
            "PRCANT": "4",
            "PRPRE": "15.5",
        }
    )

    assert compra.cantidad == 4
    assert compra.precio == 15.5


def test_crear_compra_rechaza_cantidad_invalida():
    fila = {
        "PRSUC": "SUC01",
        "PRCOD": "P100",
        "PRFEC": "2025-01-01",
        "PRPROV": "PROV01",
        "PRCANT": "0",
        "PRPRE": "15.5",
    }

    with pytest.raises(ValueError):
        crear_compra(fila)


def test_leer_compras_desde_csv(tmp_path):
    path = tmp_path / "compras.csv"
    with open(path, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["PRSUC", "PRCOD", "PRFEC", "PRPROV", "PRCANT", "PRPRE"])
        writer.writerow(["SUC01", "P100", "2025-01-01", "PROV01", "2", "10.0"])

    resultado = leer_compras(path)

    assert resultado == [Compra("SUC01", "P100", "2025-01-01", "PROV01", 2, 10.0)]


def test_calcular_total(compras):
    assert calcular_total(compras) == pytest.approx(180.0)


def test_calcular_total_por_sucursal(compras):
    assert calcular_total_por_sucursal(compras) == {
        "SUC01": 120.0,
        "SUC02": 60.0,
    }


def test_calcular_unidades_por_producto(compras):
    assert calcular_unidades_por_producto(compras) == {
        "P100": 2,
        "P200": 8,
    }


def test_producto_mas_vendido(compras):
    assert producto_mas_vendido(compras) == ("P100", 8)


def test_producto_mas_vendido_sin_compras():
    assert producto_mas_vendido([]) is None


def test_ordenar_compras(compras):
    ordenadas = ordenar_compras(compras)

    assert [(compra.sucursal, compra.producto) for compra in ordenadas] == [
        ("SUC01", "P100"),
        ("SUC01", "P200"),
        ("SUC02", "P200"),
    ]


def test_resumen_compras(compras):
    resumen = resumen_compras(compras)

    assert resumen["cantidad_compras"] == 3
    assert resumen["total_general"] == pytest.approx(180.0)
    assert resumen["producto_mas_vendido"] == ("P200", 8)
