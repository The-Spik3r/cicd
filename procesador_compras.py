import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Compra:
    sucursal: str
    producto: str
    fecha: str
    proveedor: str
    cantidad: int
    precio: float


def validar_archivo(path_csv):
    return Path(path_csv).is_file()


def crear_compra(fila):
    try:
        cantidad = int(fila["PRCANT"])
        precio = float(fila["PRPRE"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("La fila tiene datos invalidos") from exc

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a cero")
    if precio <= 0:
        raise ValueError("El precio debe ser mayor a cero")

    return Compra(
        sucursal=fila["PRSUC"].strip(),
        producto=fila["PRCOD"].strip(),
        fecha=fila["PRFEC"].strip(),
        proveedor=fila["PRPROV"].strip(),
        cantidad=cantidad,
        precio=precio,
    )


def leer_compras(path_csv):
    if not validar_archivo(path_csv):
        raise FileNotFoundError(f"No existe el archivo: {path_csv}")

    with open(path_csv, newline="", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        return [crear_compra(fila) for fila in reader]


def calcular_total(compras):
    return sum(compra.cantidad * compra.precio for compra in compras)


def calcular_total_por_sucursal(compras):
    totales = {}
    for compra in compras:
        totales[compra.sucursal] = totales.get(compra.sucursal, 0) + compra.cantidad * compra.precio
    return totales


def calcular_unidades_por_producto(compras):
    unidades = {}
    for compra in compras:
        unidades[compra.producto] = unidades.get(compra.producto, 0) + compra.cantidad
    return unidades


def producto_mas_vendido(compras):
    unidades = calcular_unidades_por_producto(compras)
    if not unidades:
        return None
    return max(unidades.items(), key=lambda item: item[1])


def ordenar_compras(compras):
    return sorted(compras, key=lambda compra: (compra.sucursal, compra.producto, compra.fecha))


def resumen_compras(compras):
    return {
        "cantidad_compras": len(compras),
        "total_general": calcular_total(compras),
        "total_por_sucursal": calcular_total_por_sucursal(compras),
        "producto_mas_vendido": producto_mas_vendido(compras),
    }


def main():
    path_csv = input("Ingrese el path del CSV: ").strip()
    compras = leer_compras(path_csv)
    resumen = resumen_compras(compras)

    print("=== Resumen de compras ===")
    print(f"Compras procesadas: {resumen['cantidad_compras']}")
    print(f"Total general: ${resumen['total_general']:.2f}")
    print("Totales por sucursal:")
    for sucursal, total in sorted(resumen["total_por_sucursal"].items()):
        print(f"- {sucursal}: ${total:.2f}")

    producto = resumen["producto_mas_vendido"]
    if producto:
        codigo, unidades = producto
        print(f"Producto mas vendido: {codigo} ({unidades} unidades)")


if __name__ == "__main__":
    main()
