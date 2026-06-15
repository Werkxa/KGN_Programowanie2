# Wyczerpujący przewodnik tworzenia projektów Machine Learning

> Oparty o notatnik [P2Lab10_housing_essential_ml.ipynb](Lab/P2Lab10_housing_essential_ml.ipynb) (zbiór California Housing).
> Cel: nie tylko *co* robi kod, ale *dlaczego* tak, *jak* zbudowane są funkcje i *gdzie* czyhają najtrudniejsze pułapki.
>
> **Trzy filary na których skupia się ten dokument:**
> 1. 🔧 Jak prawidłowo zbudować **Pipeline** (sekcje 5–7)
> 2. 🛡️ Jak **przeciwdziałać overfittingowi** (sekcje 8–11)
> 3. 🧠 **Najtrudniejsze kwestie** (oznaczone ⚠️ w całym tekście — data leakage, `fit` vs `transform`, `__`, sparse matrix)

---

## Spis treści

1. [Cykl życia projektu ML](#1-cykl-życia-projektu-ml)
2. [Wczytanie i eksploracja danych](#2-wczytanie-i-eksploracja-danych)
3. [Podział danych — losowanie warstwowe](#3-podział-danych--losowanie-warstwowe)
4. [Inżynieria cech i korelacje](#4-inżynieria-cech-i-korelacje)
5. [PIPELINE — serce projektu (krok po kroku)](#5-pipeline--serce-projektu)
6. [Własny transformer (BaseEstimator + TransformerMixin)](#6-własny-transformer)
7. [Łączenie pipeline'ów: ColumnTransformer](#7-łączenie-pipelineów-columntransformer)
8. [Modele i diagnoza overfittingu](#8-modele-i-diagnoza-overfittingu)
9. [Walidacja krzyżowa (Cross-Validation)](#9-walidacja-krzyżowa)
10. [Strojenie: Grid Search i Randomized Search](#10-strojenie-hiperparametrów)
11. [Ostateczna ewaluacja — moment prawdy](#11-ostateczna-ewaluacja)
12. [Checklista i najczęstsze błędy](#12-checklista-i-najczęstsze-błędy)

---

## 1. Cykl życia projektu ML

Każdy projekt ML — niezależnie od dziedziny — przebiega według tego samego żelaznego cyklu:

```
Dane → PODZIAŁ (sejf testowy) → Eksploracja (tylko train) → Pipeline →
→ Trening wielu modeli → Walidacja krzyżowa → Strojenie → OTWARCIE SEJFU (test)
```

**Kolejność nie jest przypadkowa.** Najważniejsza zasada brzmi:

> ⚠️ **Data Snooping Bias / Data Leakage** — jeżeli w jakikolwiek sposób użyjesz danych testowych przy budowie modelu (nawet do policzenia mediany do uzupełnienia braków!), model „podejrzy" odpowiedzi. Ocena na końcu będzie fałszywie świetna, a w produkcji model zawiedzie.

Dlatego **podział na train/test robimy PRZED eksploracją i czyszczeniem.** Zbiór testowy zamykamy w „sejfie" i nie patrzymy na niego aż do ostatniego rozdziału.

---

## 2. Wczytanie i eksploracja danych

```python
import pandas as pd
import numpy as np

def load_housing_data(housing_path="content:housing.csv"):
    return pd.read_csv(housing_path)

housing = load_housing_data()
```

`pd.read_csv()` wczytuje plik CSV do obiektu **`DataFrame`** (tabela z indeksami) w pamięci RAM.

### Cztery narzędzia diagnostyczne

| Metoda | Co pokazuje | Czego szukasz |
|--------|-------------|---------------|
| `housing.info()` | typy kolumn, liczba `non-null` | **braki danych** i kolumny tekstowe (`object`) |
| `housing.describe()` | mean, std, kwartyle (25/50/75%) | skośność (mean ≠ mediana), skala |
| `housing["ocean_proximity"].value_counts()` | liczność każdej kategorii | proporcje klas |
| `housing.hist(bins=50, figsize=(20,15))` | histogramy rozkładów | wartości ucięte (capped), różne skale |

**Jak czytać `info()`:**

```
total_bedrooms   20433 non-null float64   ← ALARM: 20640-20433 = 207 braków (NaN) → potrzebny Imputer
ocean_proximity  20640 non-null object    ← tekst → potrzebny OneHotEncoder
```

**Co wychwycić na histogramach:**
- **Wartości ucięte (capped):** pionowy słupek przy `median_house_value = 500 000` oznacza, że wszystkie droższe domy wpisano jako 500k. Model nauczy się fałszywego sufitu cen.
- **Różne skale:** jedne cechy to dziesiątki, inne dziesiątki tysięcy → konieczny **Feature Scaling**.

---

## 3. Podział danych — losowanie warstwowe

### Dlaczego nie zwykły `train_test_split`?

```python
from sklearn.model_selection import train_test_split
# train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)  # ❌ zbyt naiwne
```

Losowy podział może przypadkiem dać niereprezentatywny zbiór testowy (analogia: ankieta, w której wylosowano 900 kobiet i 100 mężczyzn). Skoro `median_income` to najsilniejszy predyktor ceny, chcemy by **proporcje grup dochodowych były identyczne w train i test**. To **Stratified Sampling (losowanie warstwowe)**.

### Krok 1: stworzenie kategorii dochodu (warstwy)

```python
housing["income_cat"] = np.ceil(housing["median_income"] / 1.5)  # zagęszczenie do ~5 koszyków
housing["income_cat"] = housing["income_cat"].clip(upper=5)       # wszystko >5 → 5
```

- `/ 1.5` — zmniejsza liczbę kategorii (zagęszcza koszyki).
- `np.ceil()` — „sufit", zaokrąglenie w górę → dyskretne klasy 1.0, 2.0, 3.0…
- `.clip(upper=5)` — przycina górę: rzadkie bardzo wysokie dochody scalamy w jeden koszyk 5, by nie tworzyć mikro-grup pojedynczych bogaczy.

### Krok 2: podział z zachowaniem proporcji

```python
from sklearn.model_selection import StratifiedShuffleSplit

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]   # .loc = dostęp po etykiecie indeksu
    strat_test_set  = housing.loc[test_index]
```

⚠️ Subtelność: `.split()` to **generator** zwracający tablice **indeksów** (nie gotowe dane). Pierwszy argument to dane, drugi — kolumna wg której zachować proporcje. Dlatego pętla `for` z `.loc[...]`.

### Krok 3: sprzątanie i izolacja

```python
# income_cat spełnił zadanie — usuwamy z obu zbiorów
for set_ in (strat_train_set, strat_test_set):
    set_.drop(["income_cat"], axis=1, inplace=True)   # axis=1 = kolumna; inplace = nadpisz

housing = strat_train_set.copy()   # ⚠️ kopia: zbiór testowy jest "święty"
```

> ⚠️ **Od tej chwili `strat_test_set` nie istnieje.** Nie analizujemy go, nie wizualizujemy, nie liczymy z niego statystyk. Wraca dopiero w sekcji 11.

---

## 4. Inżynieria cech i korelacje

Surowa cecha bywa bezużyteczna bez kontekstu. „Liczba pokoi w całej dzielnicy" nic nie mówi — ale „pokoje na gospodarstwo" już tak.

```python
housing["rooms_per_household"]      = housing['total_rooms'] / housing['households']
housing["bedrooms_per_room"]        = housing['total_bedrooms'] / housing['total_rooms']
housing["population_per_household"]  = housing['population'] / housing['households']
```

### Korelacja Pearsona

```python
corr_mat = housing_num.corr()
corr_mat["median_house_value"].sort_values(ascending=False)
```

Współczynnik `r ∈ [-1, 1]`:
- `+0.68` (`median_income`) → silny związek dodatni: rosną dochody → rosną ceny.
- bliski `0` → brak związku **liniowego** (nieliniowy może istnieć!).
- `-1` → ruch przeciwny.

Nowa cecha `bedrooms_per_room` ma zwykle **silniejszą** (ujemną) korelację z ceną niż surowe `total_bedrooms` — to dowód, że inżynieria cech działa.

### Oddzielenie etykiet (X i y)

```python
housing        = strat_train_set.drop("median_house_value", axis=1)  # X — cechy
housing_labels = strat_train_set["median_house_value"].copy()         # y — to co przewidujemy
```

---

## 5. PIPELINE — serce projektu

To najważniejszy etap. Modele to maszyny matematyczne: jedzą wektory liczb. Tekst, puste komórki czy cechy różnej skali je psują.

### Dlaczego w ogóle Pipeline, a nie ręczne czyszczenie?

Trzy twarde powody:

1. **Powtarzalność train↔produkcja.** W produkcji przetwarzasz pojedyncze próbki. Pipeline wykonuje *dokładnie ten sam* ciąg operacji co na treningu — z *zapamiętanymi* parametrami.
2. **Brak data leakage.** Pipeline uczy parametry (medianę, średnią, skalę) **tylko** na treningu i stosuje je na teście.
3. **Strojenie.** Cały pipeline (łącznie z krokami czyszczenia) można optymalizować w Grid Search.

### Święta Trójca metod scikit-learn

Każdy element pipeline'u musi mieć (tzw. duck-typing):

| Metoda | Rola | Zwraca |
|--------|------|--------|
| `fit(X)` | **uczy się** z danych (liczy medianę, std, listę kategorii) | `self` |
| `transform(X)` | **stosuje** wyuczone parametry, zwraca przekształcone dane | nową tablicę |
| `fit_transform(X)` | uczy się i od razu przekształca (szybsze) | nową tablicę |

> ⚠️ **NAJWAŻNIEJSZE ROZRÓŻNIENIE W CAŁYM ML:**
> - `fit_transform()` — **tylko na zbiorze treningowym** (uczy + przekształca).
> - `transform()` — na teście i w produkcji (przekształca **starymi** parametrami z treningu).
>
> Użycie `fit_transform()` na teście = data leakage = katastrofa (patrz sekcja 11).

### Pipeline numeryczny — trzy ogniwa

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

num_pipeline = Pipeline([
    ('imputer',       SimpleImputer(strategy="median")),   # 1. uzupełnij braki
    ('attribs_adder', CombinedAttributesAdder()),          # 2. dodaj nowe cechy
    ('std_scaler',    StandardScaler()),                   # 3. wyskaluj
])
```

`Pipeline` przyjmuje listę krotek `("nazwa", obiekt)`. Wykonuje `fit_transform` na pierwszym ogniwie, wynik podaje do drugiego itd. Na ostatnim estymatorze (jeśli to model) woła `fit`.

**1. `SimpleImputer(strategy="median")`** — uzupełnia `NaN`.
W `fit()` liczy i zapamiętuje medianę każdej kolumny. W `transform()` wstawia ją w miejsce braków.
*Dlaczego mediana, nie średnia?* Mediana jest odporna na anomalie (skrajnie drogie domy nie wypaczą jej tak jak średniej).

**2. `CombinedAttributesAdder()`** — nasz własny transformer (sekcja 6).

**3. `StandardScaler()`** — standaryzacja (z-score):

```
X_scaled = (X − μ) / σ
```

Po niej każda cecha ma średnią ≈ 0 i odchylenie ≈ 1 (wartości mniej więcej od −2.5 do 2.5). Bez tego cechy w milionach „przygłuszają" cechy w dziesiątkach przy liczeniu odległości/gradientu.

> 💡 **Mit:** „skalowanie nie jest potrzebne dla drzew". Prawda — drzewa i lasy są niewrażliwe na skalę. Ale skalowanie nie szkodzi, a ten sam pipeline obsługuje też regresję liniową, więc trzymamy je dla spójności.

### Pipeline kategorialny — OneHotEncoder

```python
from sklearn.preprocessing import OneHotEncoder

cat_pipeline = Pipeline([
    ('one_hot', OneHotEncoder()),
])
```

⚠️ **Dlaczego nie zwykłe liczby** `INLAND=1, NEAR BAY=2`? Bo model uzna, że `2 > 1`, czyli że „NEAR BAY jest większe/lepsze od INLAND" — to fałszywa relacja porządku.

**One-Hot** tworzy osobną kolumnę 0/1 dla każdej kategorii:

```
ocean_proximity = "INLAND"  →  [0, 1, 0, 0, 0]
ocean_proximity = "NEAR BAY"→  [0, 0, 0, 1, 0]
```

> ⚠️ Wynikiem jest **macierz rzadka (sparse matrix)** — niemal same zera, przechowywane oszczędnie. To normalne; jeśli potrzebujesz zwykłej tablicy, użyj `OneHotEncoder(sparse_output=False)`.

---

## 6. Własny transformer

Gdy chcemy dołożyć cechy *wewnątrz* pipeline'u (a nie ręcznie), piszemy własną klasę. Musi dziedziczyć po dwóch klasach bazowych:

```python
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

# indeksy kolumn (NumPy gubi nazwy, zostają tylko pozycje!)
rooms_ix, bedrooms_ix, population_ix, household_ix = 3, 4, 5, 6

class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room=True):   # przełącznik = hiperparametr do strojenia
        self.add_bedrooms_per_room = add_bedrooms_per_room

    def fit(self, X, y=None):
        return self                                   # nic się nie uczy → zwraca self

    def transform(self, X, y=None):
        rooms_per_household      = X[:, rooms_ix] / X[:, household_ix]
        population_per_household = X[:, population_ix] / X[:, household_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]
        return np.c_[X, rooms_per_household, population_per_household]
```

**Rozbiór najtrudniejszych elementów:**

- **`BaseEstimator`** → daje za darmo `get_params()` / `set_params()`. ⚠️ Bez tego **Grid Search nie umiałby ustawiać hiperparametrów** tej klasy.
- **`TransformerMixin`** → daje za darmo `fit_transform()` (kombinację `fit` + `transform`).
- **`__init__` bez `*args`/`**kwargs`** → wymóg sklearn: każdy hiperparametr musi być osobnym, nazwanym argumentem przypisanym do `self` bez zmian. `add_bedrooms_per_room` jako przełącznik pozwala w Grid Search sprawdzić, *czy ta cecha w ogóle pomaga*.
- **`X[:, rooms_ix]`** → notacja NumPy: `:` = „wszystkie wiersze", `rooms_ix` = kolumna nr 3. Dostajemy cały pionowy wektor. Dzielenie dwóch wektorów to operacja **zwektoryzowana** (błyskawiczna, bez pętli).
- **`np.c_[...]`** → skleja kolumny obok siebie („dokłada z prawej"). `X` ma N kolumn, wynik N+2 lub N+3.

⚠️ Dlaczego indeksy liczbowe a nie nazwy? Bo zanim ten transformer dostanie dane, `SimpleImputer` zamienił już `DataFrame` na **tablicę NumPy** — a NumPy nie ma nazw kolumn, tylko pozycje. Stąd `rooms_ix = 3`.

---

## 7. Łączenie pipeline'ów: ColumnTransformer

Mamy dwa pipeline'y (liczbowy i kategorialny) — trzeba skierować odpowiednie kolumny do odpowiedniego.

```python
from sklearn.compose import ColumnTransformer

num_attribs = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',
               'total_bedrooms', 'population', 'households', 'median_income']
cat_attribs = ["ocean_proximity"]

full_pipeline = ColumnTransformer([
    ("num_pipeline", num_pipeline, num_attribs),   # te kolumny → pipeline liczbowy
    ("cat_pipeline", cat_pipeline, cat_attribs),   # te kolumny → pipeline OHE
])

housing_prepared = full_pipeline.fit_transform(housing)   # ⚠️ fit_transform TYLKO tu (train)
```

`ColumnTransformer` to „inteligentna brama": kieruje wskazane kolumny do wskazanego transformera, a wyniki **skleja w jedną macierz**. Po tej linii `housing_prepared` to czysta, liczbowa macierz NumPy gotowa do treningu.

---

## 8. Modele i diagnoza overfittingu

To centralna sekcja o **przeciwdziałaniu overfittingowi**. Trenujemy trzy modele od najprostszego do najlepszego i obserwujemy, jak overfitting się ujawnia i jak go zwalczać.

### Model 1: Regresja liniowa — UNDERfitting

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

lin_reg = LinearRegression()
lin_reg.fit(housing_prepared, housing_labels)

housing_predictions = lin_reg.predict(housing_prepared)
lin_rmse = np.sqrt(mean_squared_error(housing_labels, housing_predictions))
# ≈ 68 628 $ — model myli się średnio o ~70 tys. USD
```

Model: `ŷ = θ₀ + θ₁x₁ + … + θₙxₙ` (hiperpłaszczyzna). `fit()` dobiera wagi `θ` minimalizujące sumę kwadratów błędów.

**RMSE = 68 628 $ to UNDERFITTING** — model jest *za prosty*, by uchwycić nieliniowe zależności. Objaw: duży błąd **już na treningu**.

*Leki na underfitting:* mocniejszy model, więcej/lepsze cechy, mniej regularyzacji.

### Model 2: Drzewo decyzyjne — OVERfitting podręcznikowy

```python
from sklearn.tree import DecisionTreeRegressor

tree_reg = DecisionTreeRegressor()
tree_reg.fit(housing_prepared, housing_labels)

housing_predictions = tree_reg.predict(housing_prepared)
tree_rmse = np.sqrt(mean_squared_error(housing_labels, housing_predictions))
# ≈ 0.0 $ (!!!)
```

> ⚠️ **RMSE = 0 to NIE sukces — to czerwony alarm.**
> Drzewo bez ograniczeń rozrasta się aż „zapamięta na blachę" każdy dom z treningu. Na zbiorze testowym (którego nie widziało) wypadnie fatalnie. Model nauczył się odpowiedzi na pamięć, zamiast **generalizować**.

To klasyczny **overfitting**: idealny wynik na treningu, słaby na nowych danych.

*Jak zdiagnozować, skoro na treningu wynik = 0?* → **walidacja krzyżowa** (sekcja 9) — pokaże prawdziwy błąd ~71 tys., gorszy nawet od regresji liniowej.

*Leki na overfitting drzewa (regularyzacja przez pruning):*
- `max_depth` — ogranicz głębokość,
- `min_samples_leaf` — minimalna liczba próbek w liściu,
- `min_samples_split`, `max_leaf_nodes`.

### Model 3: Las losowy — kompromis przez Ensemble

```python
from sklearn.ensemble import RandomForestRegressor

forest_reg = RandomForestRegressor()
forest_reg.fit(housing_prepared, housing_labels)
# RMSE na treningu ~18 tys.; w walidacji krzyżowej ~50 tys. — najlepszy z trójki
```

**Random Forest = Ensemble Learning + Bagging (Bootstrap Aggregating):**
1. Buduje setki drzew, każde na **innej losowej próbce** danych (bootstrap) i **losowym podzbiorze cech** (random subspaces).
2. Każde drzewo jest słabe i przeuczone *inaczej* — ich błędy są niezależne.
3. Wynik to **uśrednienie** wszystkich drzew → szumy i anomalie się znoszą.

> 🛡️ **Dlaczego las redukuje overfitting?** Pojedyncze drzewo ma niską stronniczość, ale ogromną wariancję. Uśrednienie wielu zdekorelowanych drzew **drastycznie tnie wariancję** zachowując niską stronniczość. To esencja walki z overfittingiem przez „mądrość tłumu".

---

## 9. Walidacja krzyżowa

### Po co, skoro mamy zbiór testowy?

Bo zbioru testowego **wolno użyć tylko raz, na samym końcu**. Gdybyśmy zaglądali do niego po każdej zmianie modelu, pośrednio „uczylibyśmy się" na nim → leakage. Potrzebujemy sposobu oceny *bez* dotykania sejfu.

### K-Fold Cross-Validation

Dzieli zbiór treningowy na K równych części (foldów). W pętli K razy: trenuje na K−1 foldach, ocenia na pozostałym. Zwraca K wyników → stabilna **średnia + odchylenie** (miara pewności).

```python
from sklearn.model_selection import cross_val_score

lin_scores = cross_val_score(lin_reg, housing_prepared, housing_labels,
                             scoring="neg_mean_squared_error", cv=10)
lin_rmse_scores = np.sqrt(-lin_scores)

def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Std:", scores.std())     # ← niska = stabilny model

display_scores(lin_rmse_scores)
```

> ⚠️ **Pułapka znaku.** `cross_val_score` działa wg konwencji „im więcej, tym lepiej". Skoro błąd ma być *mały*, sklearn używa `neg_mean_squared_error` (wartości **ujemne**). Dlatego liczymy `np.sqrt(-scores)` — najpierw negacja, potem pierwiastek.

**Co odkrywa CV:**
| Model | RMSE (CV) | Wniosek |
|-------|-----------|---------|
| Linear | ~69 tys. | underfitting |
| Tree | ~71 tys. | overfitting (na treningu było 0!) |
| Forest | ~50 tys. | najlepiej generalizuje → idzie do strojenia |

> 🛡️ Jeśli **RMSE_train ≪ RMSE_CV** → overfitting. Jeśli **oba wysokie** → underfitting. To Twój główny detektor.

---

## 10. Strojenie hiperparametrów

**Parametry** (`θ`) model uczy sam. **Hiperparametry** (np. liczba drzew, głębokość) ustawiasz Ty — i wpływają wprost na overfitting/underfitting.

### Grid Search — brutalna siła (każdy z każdym)

```python
from sklearn.model_selection import GridSearchCV

param_grid = [
    {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},          # 3×4 = 12 kombinacji
    {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]},  # 2×3 = 6
]

forest_reg = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(forest_reg, param_grid, cv=5,
                           scoring='neg_mean_squared_error',
                           return_train_score=True)
grid_search.fit(housing_prepared, housing_labels)   # (12+6) × 5 foldów = 90 treningów!

print(grid_search.best_params_)        # najlepsza kombinacja
best_model = grid_search.best_estimator_   # gotowy, dostrojony model
```

⚠️ `param_grid` to **lista słowników**. Grid Search testuje każdą kombinację w każdym słowniku osobno, dla każdej robi pełną walidację krzyżową. Liczba treningów rośnie mnożnikowo — łatwo o **eksplozję kombinatoryczną**.

### Randomized Search — inteligentne losowanie

Gdy siatka byłaby ogromna, losuj `n_iter` kombinacji z rozkładów zamiast sprawdzać wszystko:

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

final_pipeline = Pipeline([
    ('regressor', forest_reg),
])

param_distribs = {
    'regressor__n_estimators': randint(low=3, high=200),
    'regressor__max_features': randint(low=2, high=20),
}

rnd_search = RandomizedSearchCV(final_pipeline, param_distributions=param_distribs,
                                n_iter=10, cv=3,
                                scoring='neg_root_mean_squared_error', random_state=42)
rnd_search.fit(housing_prepared, housing_labels)
print(rnd_search.best_params_)
```

> ⚠️ **Podwójny underscore `__`** to jedna z najtrudniejszych składni sklearn.
> `'regressor__n_estimators'` znaczy: „wejdź do kroku pipeline'u o nazwie `regressor` i ustaw jego parametr `n_estimators`". Schemat: `nazwa_kroku__nazwa_parametru`.
> Dla zagnieżdżeń: `preprocessor__num_pipeline__std_scaler__with_mean`. **Jeden błąd w nazwie = `ValueError`.**

**Grid vs Randomized:** Grid — gdy mało parametrów i chcesz pewności. Randomized — gdy przestrzeń jest wielka i liczy się czas (często znajduje lepsze ustawienia w mniej prób).

---

## 11. Ostateczna ewaluacja

Czas otworzyć sejf. **Tylko raz.**

```python
X_test = strat_test_set.drop("median_house_value", axis=1)
y_test = strat_test_set["median_house_value"].copy()

X_test_prepared = full_pipeline.transform(X_test)        # ⚠️ transform, NIGDY fit_transform!
test_pred = best_model.predict(X_test_prepared)

final_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
print(final_rmse)   # ≈ 47 tys. USD
```

> ⚠️⚠️ **NAJGROŹNIEJSZY BŁĄD CAŁEGO PROJEKTU**
> Na zbiorze testowym wołasz **`full_pipeline.transform(X_test)`**, a **NIGDY** `.fit_transform()`.
>
> Gdybyś użył `fit_transform`, pipeline policzyłby **nową medianę i nową skalę z danych testowych**. To by:
> 1. wpuściło informację z testu do przetwarzania (data leakage),
> 2. przesunęło proporcje względem tych, na których uczył się model → predykcje liczone w „innym układzie współrzędnych".
>
> **Reguła na całe życie:** Trening = `fit_transform()`. Test i produkcja = tylko `transform()`.

### Podsumowanie wyników

```
Regresja liniowa:  ~68 600 $   (underfitting)
Drzewo (CV):       ~71 000 $   (overfitting)
Las losowy (CV):   ~50 000 $
Las po strojeniu (TEST): ~47 000 $   ← finalny błąd generalizacji
```

Od „prostej linii" 70k zeszliśmy do 47k — przez inżynierię cech, ensemble i strojenie.

> 💡 Po finalnej ewaluacji **już nie wracasz** do strojenia pod ten wynik — inaczej znów zaczynasz uczyć się na teście. Jeśli wynik jest zły, zmień podejście i… zdobądź nowy zbiór testowy lub zaakceptuj wynik.

---

## 12. Checklista i najczęstsze błędy

### ✅ Checklista projektu

- [ ] Podział train/test **przed** eksploracją (`StratifiedShuffleSplit`)
- [ ] Stratyfikacja wg najważniejszej cechy
- [ ] `housing = strat_train_set.copy()` — izolacja testu
- [ ] Cały preprocessing w `Pipeline` / `ColumnTransformer`
- [ ] Imputer + scaler + OHE w pipeline (nie ręcznie!)
- [ ] `fit_transform` tylko na train
- [ ] Ocena modeli przez **cross-validation**, nie na teście
- [ ] Strojenie przez Grid/Randomized Search z `cv`
- [ ] `transform` (nie `fit_transform`) na teście
- [ ] Test użyty **raz**, na końcu

### ⚠️ TOP 7 najtrudniejszych pułapek

| # | Pułapka | Skutek | Lek |
|---|---------|--------|-----|
| 1 | `fit_transform` na teście | data leakage, zawyżona ocena | tylko `transform` |
| 2 | Analiza/statystyki z testu | data snooping bias | sejf do końca |
| 3 | RMSE=0 mylone z sukcesem | ukryty overfitting | cross-validation |
| 4 | Kodowanie kategorii liczbami | fałszywy porządek | OneHotEncoder |
| 5 | Brak skalowania | dominacja dużych cech | StandardScaler |
| 6 | Zła nazwa w `__` | ValueError w strojeniu | `krok__parametr` |
| 7 | Zapominanie `random_state` | brak powtarzalności | ustaw wszędzie `=42` |

### 🧭 Szybka diagnoza fitu

```
RMSE_train niski,  RMSE_CV niski   → ✅ dobrze
RMSE_train ≈ 0,    RMSE_CV wysoki  → 🔴 OVERFITTING  → regularyzacja, więcej danych, ensemble
RMSE_train wysoki, RMSE_CV wysoki  → 🟡 UNDERFITTING → mocniejszy model, lepsze cechy
```
