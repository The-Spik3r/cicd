# Procesador de Compras

Trabajo practico integrador de CI/CD.

El proyecto procesa compras de supermercado desde un archivo CSV y calcula informacion como totales por sucursal y producto mas vendido.

## Archivos del proyecto

- `procesador_compras.py`: codigo principal del sistema
- `test_procesador_compras.py`: pruebas unitarias
- `requirements.txt`: dependencias necesarias
- `.github/workflows/ci.yml`: pipeline de GitHub Actions
- `compras_desornadas.csv`: archivo de datos usado como ejemplo

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

Cuando el programa pide el path del CSV, se puede ingresar:

```text
compras_desornadas.csv
```

## Tests

Para ejecutar las pruebas localmente:

```bash
pytest -v
```

Las pruebas validan:

- lectura del archivo CSV
- calculo de totales
- totales por sucursal
- producto mas vendido
- validacion de datos invalidos
- ordenamiento de compras

## GitHub Actions

Se agrego un workflow de GitHub Actions llamado `CI`.

La pipeline se ejecuta en:

- push a `main`
- Pull Requests hacia `main`

El job `build` hace lo siguiente:

- descarga el codigo
- configura Python
- instala dependencias desde `requirements.txt`
- ejecuta los tests con `pytest -v`

## Proteccion de la rama main

La rama `main` esta protegida.

Para poder mergear cambios se requiere:

- abrir un Pull Request
- que pase el check obligatorio `build`
- que la branch este actualizada antes del merge

## Pull Requests realizados

Se trabajo con ramas secundarias y Pull Requests.

PRs principales:

- implementacion del procesador de compras
- agregado de tests unitarios
- agregado de pipeline de GitHub Actions

Tambien se dejaron dos PRs abiertas con errores intencionales, como pide el trabajo.

## Simulacion de errores

### Fallo en tests

Se creo una PR donde se modifica un test para que espere un resultado incorrecto.

Error detectado:

- falla `pytest`
- el test de producto mas vendido no coincide con el resultado real

Comportamiento observado:

- GitHub Actions ejecuta la pipeline
- el job `build` falla
- GitHub bloquea el merge porque el check obligatorio no pasa

### Fallo en pipeline

Se creo otra PR donde se cambia el comando del workflow por un comando inexistente.

Error detectado:

- falla el paso de ejecucion de tests
- el comando configurado en el workflow no existe

Comportamiento observado:

- GitHub Actions inicia la pipeline
- el job `build` falla
- GitHub no permite mergear la PR a `main`

## Conclusion

Con esto se verifica el flujo de integracion continua: los cambios se hacen en ramas, se validan con Pull Requests, GitHub Actions ejecuta los tests automaticamente y la rama principal queda protegida frente a errores.
