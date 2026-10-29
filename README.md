# pum_zadania_amerek

This project will be common base for Exercise 1 and Exercise2

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

This is your new Kedro project with PySpark setup, which was generated using `kedro 1.7.0`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Zadanie 2 – Model ML i połączenie datasetów w jednym pipeline

Zadanie zrealizowano w tym samym projekcie Kedro co Zadanie 1, na branchu `zadanie-2`.
Raport z analizy EDA (Zadanie 1) znajduje się w [`raport.md`](raport.md).

Do projektu dodano pipeline `data_science`, który przetwarza oba datasety, trenuje modele
klasyfikacyjne i ocenia ich jakość.

### Jak datasety są połączone w pipeline

Zastosowano strategię „osobne gałęzie, wspólny pipeline”. Zbiory `Titanic_train.csv`
i `Datasets_orders.csv` pochodzą z różnych domen i nie mają wspólnego klucza, więc nie są
łączone joinem. Każdy z nich ma własną gałąź (prepare → train → evaluate), a pipeline
`data_science` składa je w jeden graf (`titanic + orders`). Pipeline jest zarejestrowany
w `__default__` (`src/pum_zadania_amerek/pipeline_registry.py`), więc jedno polecenie
`kedro run` uruchamia cały przepływ.

```
titanic_train ───► prepare_titanic ─► train_titanic ─► evaluate_titanic ─► metryki + wykres
datasets_orders ─► prepare_orders ──► train_orders ──► evaluate_orders ──► metryki + wykres
```

Obie gałęzie używają tego samego schematu kroków i są parametryzowane osobnymi blokami
(`titanic`, `orders`) w `conf/base/parameters_data_science.yml`.

### Modele

| Dataset | Cel | Model | Preprocessing |
|---|---|---|---|
| Titanic | `Survived` | Random Forest (200 drzew) | usunięcie `PassengerId`, `Name`, `Ticket`, `Cabin`; mediana dla `Age`; kodowanie `Sex` i `Embarked` |
| Datasets_orders | `big_order` (ilość ≥ 3) | Random Forest (200 drzew, `class_weight=balanced`) | usunięcie duplikatów, ujednolicenie kategorii, cecha `month`, usunięcie `tshirt_quantity` (data leakage), kodowanie one-hot |

### Struktura katalogów

```
conf/base/
  catalog.yml                       # definicje danych, modeli i raportów
  parameters_data_science.yml       # parametry obu gałęzi
data/
  01_raw/                           # surowe CSV
  03_primary/                       # dane po preprocessingu
  06_models/                        # wytrenowane modele (.pkl)
  08_reporting/                     # metryki (.json) i confusion matrix (.png)
src/pum_zadania_amerek/pipelines/
  data_science/
    nodes.py                        # funkcje: preprocessing, trening, ewaluacja
    pipeline.py                     # połączenie node'ów w graf
docs/                               # wykresy i schemat pipeline'u
raport.md                           # raport z Zadania 1
model_summary.md                    # metryki, confusion matrix, wnioski (Zadanie 2)
```

Katalog `data/` jest ignorowany przez git zgodnie z konwencją Kedro. Pliki
`Titanic_train.csv` i `Datasets_orders.csv` należy umieścić w `data/01_raw/`.

### Uruchomienie

```bash
pip install -r requirements.txt
kedro run                           # cały pipeline
kedro run --pipeline=data_science   # tylko modele
kedro viz run                       # wizualizacja grafu
```

### Wyniki (skrót)

| Dataset | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Titanic | 0,810 | 0,787 | 0,696 | 0,738 |
| Datasets_orders | 0,520 | 0,307 | 0,492 | 0,378 |

Pełne metryki, macierze pomyłek i wnioski znajdują się w [`model_summary.md`](model_summary.md).

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the files `tests/test_run.py` and `tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:

```
pytest
```

You can configure the coverage threshold in your project's `pyproject.toml` file under the `[tool.coverage.report]` section.

## Project dependencies

To see and update the dependency requirements for your project use `requirements.txt`. Install the project requirements with `pip install -r requirements.txt`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can use tools like [`nbstripout`](https://github.com/kynan/nbstripout). For example, you can add a hook in `.git/config` with `nbstripout --install`. This will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html)

