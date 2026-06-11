# Procesador de Compras

Proyecto integrador de CI/CD para procesar compras de supermercado desde un archivo CSV.

## Contenido

- Codigo Python del sistema
- Tests unitarios con `pytest`
- Pipeline de CI con GitHub Actions
- Rama principal protegida mediante Pull Requests y checks obligatorios

## Requisitos

- Python 3.13
- pip

## Instalacion

```bash
pip install -r requirements.txt
```

## Uso

```bash
python procesador_compras.py
```

Cuando el programa solicite el path del CSV, se puede usar:

```text
compras_desornadas.csv
```

## Tests

```bash
pytest -v
```

## CI/CD

El repositorio usa GitHub Actions para ejecutar automaticamente los tests en cada push y Pull Request hacia `main`.

Para cumplir el flujo del trabajo practico:

- No se trabaja directo sobre `main`
- Cada cambio se hace desde una branch secundaria
- Se abre un Pull Request hacia `main`
- La pipeline debe pasar antes de mergear
- La rama `main` debe estar protegida
