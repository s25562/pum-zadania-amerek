# Podsumowanie modeli – Zadanie 2

## 1. Strategia łączenia datasetów

Wybrano strategię „osobne gałęzie, wspólny pipeline”.

Zbiory `Titanic_train.csv` i `Datasets_orders.csv` pochodzą z zupełnie różnych domen
(pasażerowie statku vs. zamówienia koszulek) i nie mają wspólnego klucza, więc ich
łączenie (join/concat) byłoby sztuczne i pozbawione sensu. Każdy dataset ma dlatego
własny preprocessing, trening i ewaluację, a pipeline `data_science` składa obie gałęzie
w jeden graf. Pipeline jest zarejestrowany w `__default__`, więc jedno polecenie
`kedro run` uruchamia całość.

Zastosowano też elementy strategii „wspólny schemat”: obie gałęzie mają tę samą strukturę
kroków (prepare → train → evaluate) i są parametryzowane w
`conf/base/parameters_data_science.yml` (osobne bloki `titanic` i `orders`).

Graf pipeline'u -> docs/pipeline_graph.png

### Przepływ danych

| Etap | Titanic | Datasets_orders |
|---|---|---|
| `01_raw` | `titanic_train` | `datasets_orders` |
| `03_primary` | `titanic_train_primary` | `datasets_orders_primary` |
| `06_models` | `titanic_train_model` | `datasets_orders_model` |
| `08_reporting` | `titanic_train_metrics`, `titanic_train_confusion_matrix` | `datasets_orders_metrics`, `datasets_orders_confusion_matrix` |

Zbiory `X_test` i `y_test` są przekazywane między node'ami `train` i `evaluate` w pamięci.

### Node'y

- `prepare_titanic`, `prepare_orders` – preprocessing,
- `train_titanic`, `train_orders` – podział train/test (80/20, `stratify`) i trening Random Forest,
- `evaluate_model` – Accuracy, Precision, Recall, F1, confusion matrix.

## 2. Titanic

**Cel:** `Survived` (0/1).
**Model:** Random Forest, 200 drzew, `random_state=42`.
**Podział:** 80% trening / 20% test (179 pasażerów w teście), `stratify=y`.

### Preprocessing

- usunięto `PassengerId`, `Name`, `Ticket`, `Cabin` (`Cabin` ma ok. 77% braków),
- `Age` (177 braków) uzupełniono **medianą**,
- `Embarked` (2 braki) uzupełniono **dominantą**,
- `Sex` zakodowano jako 0/1, `Embarked` kodowaniem one-hot.

### Wyniki

| Metryka | Wartość |
|---|---|
| Accuracy | 0,810 |
| Precision | 0,787 |
| Recall | 0,696 |
| F1 | 0,738 |

Confusion matrix (wiersze: stan rzeczywisty, kolumny: predykcja):

|  | Predykcja: 0 | Predykcja: 1 |
|---|---|---|
| **Rzeczywiste: 0** | 97 (TN) | 13 (FP) |
| **Rzeczywiste: 1** | 21 (FN) | 48 (TP) |

Confusion matrix – Titanic -> docs/titanic_train_confusion_matrix.png

### Wniosek

Model osiągnął accuracy 0,81 i F1 = 0,74, co jest dobrym wynikiem dla danych tabelarycznych
bez strojenia hiperparametrów. Precision (0,79) jest wyższa niż recall (0,70): model
rzadziej błędnie przewiduje przeżycie (13 fałszywych alarmów), ale częściej przeocza osoby,
które przeżyły (21 przypadków), czyli jest nieco zachowawczy. Możliwe ulepszenia to
inżynieria cech (np. tytuł wyciągnięty z `Name`, wielkość rodziny z `SibSp` + `Parch`),
walidacja krzyżowa i strojenie hiperparametrów.

## 3. Datasets_orders

**Cel:** zbiór nie zawiera gotowej zmiennej docelowej, więc zdefiniowano
`big_order = (tshirt_quantity >= 3)`. Próg 3 odpowiada górnemu kwartylowi ilości.
Duże zamówienia stanowią **29,7%** danych (klasy są niezbalansowane).
**Model:** Random Forest, 200 drzew, `random_state=42`.
**Podział:** 80% trening / 20% test (5303 zamówienia w teście), `stratify=y`.

### Preprocessing

- usunięto duplikaty `order_id` (41 wierszy),
- ujednolicono nazwy kategorii (`Wh Tshirt M` → `White T-Shirt M`, `Bl Tshirt F` → `Black T-Shirt F` itd.),
- dodano cechę `month` z `order_date`,
- usunięto `order_id`, `customer_id`, `order_date` oraz **`tshirt_quantity`**
  (z tej kolumny wyliczono cel, jej pozostawienie byłoby *data leakage*),
- `tshirt_category` zakodowano one-hot.

### Wyniki – dwa warianty

Porównano model domyślny z modelem z `class_weight="balanced"` (parametr w `parameters_data_science.yml`).

| Metryka | RF domyślny | RF `class_weight=balanced` |
|---|---|---|
| Accuracy | 0,686 | 0,520 |
| Precision | 0,350 | 0,307 |
| Recall | 0,066 | 0,492 |
| F1 | 0,111 | 0,378 |

Confusion matrix – wariant domyślny:

|  | Predykcja: 0 | Predykcja: 1 |
|---|---|---|
| **Rzeczywiste: 0** | 3534 (TN) | 193 (FP) |
| **Rzeczywiste: 1** | 1472 (FN) | 104 (TP) |

Confusion matrix – wariant `balanced`:

|  | Predykcja: 0 | Predykcja: 1 |
|---|---|---|
| **Rzeczywiste: 0** | 1981 (TN) | 1746 (FP) |
| **Rzeczywiste: 1** | 801 (FN) | 775 (TP) |

Confusion matrix – Datasets_orders -> docs/datasets_orders_confusion_matrix.png

*(wykres przedstawia wariant `balanced`, czyli aktualny wynik `kedro run`)*

### Wniosek

Klasyfikator zawsze odpowiadający „0” miałby accuracy 0,703. Domyślny model osiągnął
0,686, czyli mniej, przy recall zaledwie 0,066 (104 z 1576 dużych zamówień wykrytych), więc
w praktyce nie rozpoznaje klasy dodatniej. Sama accuracy jest tu mylącą miarą, bo klasy są
niezbalansowane.

Zastosowanie `class_weight="balanced"` zwiększyło recall do 0,492 i F1 do 0,378, ale kosztem
accuracy (0,520) i precision (0,307). Precision jest tylko nieznacznie wyższa od udziału
klasy dodatniej w danych (0,297), a odsetek fałszywych alarmów (1746 / 3727 ≈ 0,47) jest
zbliżony do recall. Oznacza to, że poprawa wynika głównie z przesunięcia progu decyzyjnego
(model częściej odpowiada „1”), a nie z lepszego rozróżniania klas.

Główna przyczyna: dostępne cechy niosą niewiele informacji o wielkości zamówienia. Najważniejsze
okazały się `pages_visited` i `month`, a cena i kategoria mają niewielki wpływ. Realna poprawa
wymagałaby dodatkowych danych (np. historii zakupów klienta) albo innego sformułowania problemu
(np. regresja ilości zamiast klasyfikacji).

## 4. Wnioski ogólne

- Oba modele pokazują, że **sama accuracy nie wystarcza**: na zbiorze niezbalansowanym
  (orders) trzeba ją porównywać z baseline'em i analizować precision/recall.
- Titanic ma cechy dobrze opisujące cel, więc model działa poprawnie (F1 = 0,74).
  W orders cechy są słabymi predyktorami wielkości zamówienia (F1 = 0,38 przy `balanced`).
- Całość działa jako jeden projekt Kedro: `kedro run` uruchamia obie gałęzie, a parametry,
  katalog i artefakty są wersjonowane w repozytorium.

### Ograniczenia i możliwe ulepszenia

- jeden podział train/test zamiast walidacji krzyżowej,
- brak strojenia hiperparametrów (np. `max_depth`, `min_samples_leaf`),
- dla orders: dodatkowe cechy (historia klienta), inna definicja celu, dobór progu decyzyjnego,
  metryka ROC AUC.

## 5. Uruchomienie

kedro run                          # cały pipeline
kedro run --pipeline=data_science  # tylko modele
kedro viz run                      # wizualizacja grafu

