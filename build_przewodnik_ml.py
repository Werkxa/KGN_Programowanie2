# -*- coding: utf-8 -*-
"""Generator PDF: Wyczerpujący przewodnik tworzenia projektów ML.
Buduje Przewodnik_ML.pdf na podstawie PRZEWODNIK_ML.md i notatnika
P2Lab10_housing_essential_ml.ipynb. Używa frameworka pdf_framework.Notebook.
"""
from pdf_framework import Notebook

nb = Notebook(footer="Przewodnik ML — California Housing")

# ---------------------------------------------------------------------------
# Strona tytułowa + spis treści
# ---------------------------------------------------------------------------
nb.title_page(
    "Wyczerpujący przewodnik<br/>tworzenia projektów Machine Learning",
    "Od surowych danych CSV do dostrojonego modelu — na zbiorze California Housing",
    "Pipeline · Przeciwdziałanie overfittingowi · Najtrudniejsze kwestie",
    "Oparty o notatnik P2Lab10_housing_essential_ml.ipynb. Wyjaśnia nie tylko CO robi "
    "kod, ale DLACZEGO tak, JAK zbudowane są funkcje i GDZIE czyhają pułapki.",
)

nb.toc([
    "1.  Cykl życia projektu ML",
    "2.  Wczytanie i eksploracja danych",
    "3.  Podział danych — losowanie warstwowe",
    "4.  Inżynieria cech i korelacje",
    "CZĘŚĆ I — PIPELINE (serce projektu)",
    "5.  Pipeline krok po kroku",
    "6.  Własny transformer (BaseEstimator + TransformerMixin)",
    "7.  Łączenie pipeline'ów: ColumnTransformer",
    "CZĘŚĆ II — PRZECIWDZIAŁANIE OVERFITTINGOWI",
    "8.  Modele i diagnoza overfittingu",
    "9.  Walidacja krzyżowa (Cross-Validation)",
    "10. Strojenie hiperparametrów (Grid / Randomized Search)",
    "11. Ostateczna ewaluacja — moment prawdy",
    "12. Checklista i najczęstsze błędy",
])

# ---------------------------------------------------------------------------
# 1. Cykl życia
# ---------------------------------------------------------------------------
nb.h1("Cykl życia projektu ML", 1)
nb.p("Każdy projekt ML — niezależnie od dziedziny — przebiega według tego samego żelaznego "
     "cyklu. Kolejność kroków NIE jest przypadkowa.")
nb.code(
    "Dane -> PODZIAŁ (sejf testowy) -> Eksploracja (tylko train) -> Pipeline ->\n"
    "-> Trening wielu modeli -> Walidacja krzyżowa -> Strojenie -> OTWARCIE SEJFU (test)")
nb.note(
    "Jeżeli w jakikolwiek sposób użyjesz danych testowych przy budowie modelu (nawet do "
    "policzenia mediany do uzupełnienia braków!), model „podejrzy” odpowiedzi. Ocena na końcu "
    "będzie fałszywie świetna, a w produkcji model zawiedzie. Dlatego podział na train/test "
    "robimy PRZED eksploracją i czyszczeniem, a zbiór testowy zamykamy w „sejfie”.",
    title="Data Snooping Bias / Data Leakage")

# ---------------------------------------------------------------------------
# 2. Eksploracja
# ---------------------------------------------------------------------------
nb.h1("Wczytanie i eksploracja danych", 2)
nb.code(
    "import pandas as pd\n"
    "import numpy as np\n\n"
    "def load_housing_data(housing_path=\"content:housing.csv\"):\n"
    "    return pd.read_csv(housing_path)\n\n"
    "housing = load_housing_data()",
    caption="pd.read_csv() wczytuje plik CSV do obiektu DataFrame (tabela z indeksami) w RAM.")
nb.h2("Cztery narzędzia diagnostyczne")
nb.table(
    ["Metoda", "Co pokazuje", "Czego szukasz"],
    [["housing.info()", "typy kolumn, liczba non-null", "braki danych i kolumny tekstowe (object)"],
     ["housing.describe()", "mean, std, kwartyle", "skośność (mean != mediana), skala"],
     ["...value_counts()", "liczność każdej kategorii", "proporcje klas"],
     ["housing.hist(bins=50)", "histogramy rozkładów", "wartości ucięte (capped), różne skale"]],
    widths=[4.6 * nb.cm, 5.5 * nb.cm, 6.5 * nb.cm])
nb.h3("Jak czytać info()")
nb.code(
    "total_bedrooms   20433 non-null float64   # ALARM: 207 braków (NaN) -> potrzebny Imputer\n"
    "ocean_proximity  20640 non-null object    # tekst -> potrzebny OneHotEncoder")
nb.h3("Co wychwycić na histogramach")
nb.bullets([
    "Wartości ucięte (capped): pionowy słupek przy median_house_value = 500 000 oznacza, że "
    "wszystkie droższe domy wpisano jako 500k. Model nauczy się fałszywego sufitu cen.",
    "Różne skale: jedne cechy to dziesiątki, inne dziesiątki tysięcy -> konieczny Feature Scaling.",
])

# ---------------------------------------------------------------------------
# 3. Podział
# ---------------------------------------------------------------------------
nb.h1("Podział danych — losowanie warstwowe", 3)
nb.p("Losowy train_test_split może przypadkiem dać niereprezentatywny zbiór testowy. Skoro "
     "median_income to najsilniejszy predyktor ceny, chcemy by proporcje grup dochodowych były "
     "identyczne w train i test. To Stratified Sampling (losowanie warstwowe).")
nb.h2("Krok 1: stworzenie kategorii dochodu (warstwy)")
nb.code(
    "housing[\"income_cat\"] = np.ceil(housing[\"median_income\"] / 1.5)  # ~5 koszyków\n"
    "housing[\"income_cat\"] = housing[\"income_cat\"].clip(upper=5)       # wszystko >5 -> 5")
nb.bullets([
    "/ 1.5 — zmniejsza liczbę kategorii (zagęszcza koszyki).",
    "np.ceil() — „sufit”, zaokrąglenie w górę -> dyskretne klasy 1.0, 2.0, 3.0...",
    ".clip(upper=5) — przycina górę: rzadkie wysokie dochody scalamy w jeden koszyk 5.",
])
nb.h2("Krok 2: podział z zachowaniem proporcji")
nb.code(
    "from sklearn.model_selection import StratifiedShuffleSplit\n\n"
    "split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)\n"
    "for train_index, test_index in split.split(housing, housing[\"income_cat\"]):\n"
    "    strat_train_set = housing.loc[train_index]   # .loc = dostęp po etykiecie indeksu\n"
    "    strat_test_set  = housing.loc[test_index]")
nb.note(
    "Subtelność: .split() to GENERATOR zwracający tablice INDEKSÓW (nie gotowe dane). Pierwszy "
    "argument to dane, drugi — kolumna wg której zachować proporcje. Stąd pętla for z .loc[...].",
    title="Najtrudniejsze")
nb.h2("Krok 3: sprzątanie i izolacja")
nb.code(
    "for set_ in (strat_train_set, strat_test_set):\n"
    "    set_.drop([\"income_cat\"], axis=1, inplace=True)  # axis=1 = kolumna; inplace = nadpisz\n\n"
    "housing = strat_train_set.copy()   # kopia: zbiór testowy jest „święty”")
nb.note("Od tej chwili strat_test_set nie istnieje. Nie analizujemy go, nie wizualizujemy, nie "
        "liczymy z niego statystyk. Wraca dopiero w sekcji 11.", title="Sejf zamknięty")

# ---------------------------------------------------------------------------
# 4. Inżynieria cech
# ---------------------------------------------------------------------------
nb.h1("Inżynieria cech i korelacje", 4)
nb.p("Surowa cecha bywa bezużyteczna bez kontekstu. „Liczba pokoi w całej dzielnicy” nic nie "
     "mówi — ale „pokoje na gospodarstwo” już tak.")
nb.code(
    "housing[\"rooms_per_household\"]     = housing['total_rooms'] / housing['households']\n"
    "housing[\"bedrooms_per_room\"]       = housing['total_bedrooms'] / housing['total_rooms']\n"
    "housing[\"population_per_household\"] = housing['population'] / housing['households']")
nb.h2("Korelacja Pearsona")
nb.code(
    "corr_mat = housing_num.corr()\n"
    "corr_mat[\"median_house_value\"].sort_values(ascending=False)")
nb.bullets([
    "+0.68 (median_income) -> silny związek dodatni: rosną dochody -> rosną ceny.",
    "bliski 0 -> brak związku LINIOWEGO (nieliniowy może istnieć!).",
    "-1 -> ruch przeciwny.",
])
nb.p("Nowa cecha bedrooms_per_room ma zwykle silniejszą (ujemną) korelację z ceną niż surowe "
     "total_bedrooms — to dowód, że inżynieria cech działa.")
nb.h2("Oddzielenie etykiet (X i y)")
nb.code(
    "housing        = strat_train_set.drop(\"median_house_value\", axis=1)  # X — cechy\n"
    "housing_labels = strat_train_set[\"median_house_value\"].copy()         # y — cel")

# ---------------------------------------------------------------------------
# CZĘŚĆ I — PIPELINE
# ---------------------------------------------------------------------------
nb.part("CZĘŚĆ I\nPIPELINE — serce projektu")

nb.h1("Pipeline krok po kroku", 5)
nb.p("Modele to maszyny matematyczne: jedzą wektory liczb. Tekst, puste komórki czy cechy "
     "różnej skali je psują. Dlatego cały preprocessing zamykamy w Pipeline.")
nb.h2("Dlaczego Pipeline, a nie ręczne czyszczenie? Trzy twarde powody")
nb.bullets([
    "Powtarzalność train<->produkcja: w produkcji przetwarzasz pojedyncze próbki; pipeline "
    "wykonuje dokładnie ten sam ciąg operacji z zapamiętanymi parametrami.",
    "Brak data leakage: pipeline uczy parametry (medianę, skalę) tylko na treningu.",
    "Strojenie: cały pipeline (łącznie z czyszczeniem) można optymalizować w Grid Search.",
])
nb.h2("Święta Trójca metod scikit-learn")
nb.table(
    ["Metoda", "Rola", "Zwraca"],
    [["fit(X)", "uczy się z danych (mediana, std, lista kategorii)", "self"],
     ["transform(X)", "stosuje wyuczone parametry, przekształca dane", "nową tablicę"],
     ["fit_transform(X)", "uczy się i od razu przekształca (szybsze)", "nową tablicę"]],
    widths=[4.2 * nb.cm, 8.4 * nb.cm, 4.0 * nb.cm])
nb.note(
    "fit_transform() — TYLKO na zbiorze treningowym (uczy + przekształca). "
    "transform() — na teście i w produkcji (przekształca STARYMI parametrami z treningu). "
    "Użycie fit_transform() na teście = data leakage = katastrofa (patrz sekcja 11).",
    title="NAJWAŻNIEJSZE ROZRÓŻNIENIE W CAŁYM ML")
nb.h2("Pipeline numeryczny — trzy ogniwa")
nb.code(
    "from sklearn.pipeline import Pipeline\n"
    "from sklearn.impute import SimpleImputer\n"
    "from sklearn.preprocessing import StandardScaler\n\n"
    "num_pipeline = Pipeline([\n"
    "    ('imputer',       SimpleImputer(strategy=\"median\")),   # 1. uzupełnij braki\n"
    "    ('attribs_adder', CombinedAttributesAdder()),          # 2. dodaj nowe cechy\n"
    "    ('std_scaler',    StandardScaler()),                   # 3. wyskaluj\n"
    "])")
nb.p("Pipeline przyjmuje listę krotek (\"nazwa\", obiekt). Wykonuje fit_transform na pierwszym "
     "ogniwie, wynik podaje do drugiego itd. Na ostatnim estymatorze (jeśli to model) woła fit.")
nb.h3("1. SimpleImputer(strategy=\"median\")")
nb.p("Uzupełnia NaN. W fit() liczy i zapamiętuje medianę każdej kolumny; w transform() wstawia "
     "ją w miejsce braków. Dlaczego mediana, nie średnia? Mediana jest odporna na anomalie "
     "(skrajnie drogie domy nie wypaczą jej tak jak średniej).")
nb.h3("2. CombinedAttributesAdder()")
nb.p("Nasz własny transformer (sekcja 6).")
nb.h3("3. StandardScaler() — standaryzacja (z-score)")
nb.formula("X_scaled = (X − μ) / σ")
nb.p("Po niej każda cecha ma średnią ≈ 0 i odchylenie ≈ 1 (wartości od ok. −2.5 do 2.5). Bez "
     "tego cechy w milionach „przygłuszają” cechy w dziesiątkach przy liczeniu odległości/gradientu.")
nb.note("Mit: „skalowanie nie jest potrzebne dla drzew”. Prawda — drzewa i lasy są niewrażliwe "
        "na skalę. Ale skalowanie nie szkodzi, a ten sam pipeline obsługuje też regresję liniową, "
        "więc trzymamy je dla spójności.", title="Wskazówka")
nb.h2("Pipeline kategorialny — OneHotEncoder")
nb.code(
    "from sklearn.preprocessing import OneHotEncoder\n\n"
    "cat_pipeline = Pipeline([\n"
    "    ('one_hot', OneHotEncoder()),\n"
    "])")
nb.p("Dlaczego nie zwykłe liczby INLAND=1, NEAR BAY=2? Bo model uzna, że 2 > 1, czyli że "
     "„NEAR BAY jest większe/lepsze od INLAND” — to fałszywa relacja porządku.")
nb.code(
    "ocean_proximity = \"INLAND\"   ->  [0, 1, 0, 0, 0]\n"
    "ocean_proximity = \"NEAR BAY\" ->  [0, 0, 0, 1, 0]",
    caption="One-Hot tworzy osobną kolumnę 0/1 dla każdej kategorii.")
nb.note("Wynikiem jest macierz rzadka (sparse matrix) — niemal same zera, przechowywane "
        "oszczędnie. To normalne; jeśli potrzebujesz zwykłej tablicy: OneHotEncoder(sparse_output=False).",
        title="Sparse matrix")

# ---------------------------------------------------------------------------
# 6. Własny transformer
# ---------------------------------------------------------------------------
nb.h1("Własny transformer", 6)
nb.p("Gdy chcemy dołożyć cechy wewnątrz pipeline'u (a nie ręcznie), piszemy własną klasę. Musi "
     "dziedziczyć po dwóch klasach bazowych.")
nb.code(
    "from sklearn.base import BaseEstimator, TransformerMixin\n"
    "import numpy as np\n\n"
    "# indeksy kolumn (NumPy gubi nazwy, zostają tylko pozycje!)\n"
    "rooms_ix, bedrooms_ix, population_ix, household_ix = 3, 4, 5, 6\n\n"
    "class CombinedAttributesAdder(BaseEstimator, TransformerMixin):\n"
    "    def __init__(self, add_bedrooms_per_room=True):   # przełącznik = hiperparametr\n"
    "        self.add_bedrooms_per_room = add_bedrooms_per_room\n\n"
    "    def fit(self, X, y=None):\n"
    "        return self                                   # nic się nie uczy -> zwraca self\n\n"
    "    def transform(self, X, y=None):\n"
    "        rooms_per_household      = X[:, rooms_ix] / X[:, household_ix]\n"
    "        population_per_household = X[:, population_ix] / X[:, household_ix]\n"
    "        if self.add_bedrooms_per_room:\n"
    "            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]\n"
    "            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]\n"
    "        return np.c_[X, rooms_per_household, population_per_household]")
nb.h2("Rozbiór najtrudniejszych elementów")
nb.bullets([
    "BaseEstimator -> daje za darmo get_params() / set_params(). Bez tego Grid Search nie "
    "umiałby ustawiać hiperparametrów tej klasy.",
    "TransformerMixin -> daje za darmo fit_transform() (kombinację fit + transform).",
    "__init__ bez *args/**kwargs -> wymóg sklearn: każdy hiperparametr musi być osobnym, "
    "nazwanym argumentem przypisanym do self bez zmian. add_bedrooms_per_room pozwala w Grid "
    "Search sprawdzić, czy ta cecha w ogóle pomaga.",
    "X[:, rooms_ix] -> notacja NumPy: ':' = wszystkie wiersze, rooms_ix = kolumna nr 3. "
    "Dzielenie dwóch wektorów to operacja zwektoryzowana (błyskawiczna, bez pętli).",
    "np.c_[...] -> skleja kolumny obok siebie („dokłada z prawej”). X ma N kolumn, wynik N+2 lub N+3.",
])
nb.note("Dlaczego indeksy liczbowe a nie nazwy? Bo zanim transformer dostanie dane, SimpleImputer "
        "zamienił DataFrame na tablicę NumPy — a NumPy nie ma nazw kolumn, tylko pozycje. Stąd "
        "rooms_ix = 3.", title="Najtrudniejsze")

# ---------------------------------------------------------------------------
# 7. ColumnTransformer
# ---------------------------------------------------------------------------
nb.h1("Łączenie pipeline'ów: ColumnTransformer", 7)
nb.p("Mamy dwa pipeline'y (liczbowy i kategorialny) — trzeba skierować odpowiednie kolumny do "
     "odpowiedniego.")
nb.code(
    "from sklearn.compose import ColumnTransformer\n\n"
    "num_attribs = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',\n"
    "               'total_bedrooms', 'population', 'households', 'median_income']\n"
    "cat_attribs = [\"ocean_proximity\"]\n\n"
    "full_pipeline = ColumnTransformer([\n"
    "    (\"num_pipeline\", num_pipeline, num_attribs),   # te kolumny -> pipeline liczbowy\n"
    "    (\"cat_pipeline\", cat_pipeline, cat_attribs),   # te kolumny -> pipeline OHE\n"
    "])\n\n"
    "housing_prepared = full_pipeline.fit_transform(housing)   # fit_transform TYLKO tu (train)")
nb.p("ColumnTransformer to „inteligentna brama”: kieruje wskazane kolumny do wskazanego "
     "transformera, a wyniki skleja w jedną macierz. Po tej linii housing_prepared to czysta, "
     "liczbowa macierz NumPy gotowa do treningu.")

# ---------------------------------------------------------------------------
# CZĘŚĆ II — OVERFITTING
# ---------------------------------------------------------------------------
nb.part("CZĘŚĆ II\nPRZECIWDZIAŁANIE OVERFITTINGOWI")

nb.h1("Modele i diagnoza overfittingu", 8)
nb.p("Trenujemy trzy modele od najprostszego do najlepszego i obserwujemy, jak overfitting się "
     "ujawnia i jak go zwalczać.")
nb.h2("Model 1: Regresja liniowa — UNDERfitting")
nb.code(
    "from sklearn.linear_model import LinearRegression\n"
    "from sklearn.metrics import mean_squared_error\n\n"
    "lin_reg = LinearRegression()\n"
    "lin_reg.fit(housing_prepared, housing_labels)\n\n"
    "housing_predictions = lin_reg.predict(housing_prepared)\n"
    "lin_rmse = np.sqrt(mean_squared_error(housing_labels, housing_predictions))",
    out="lin_rmse ≈ 68 628 $   # model myli się średnio o ~70 tys. USD")
nb.p("Model: ŷ = θ0 + θ1·x1 + ... + θn·xn (hiperpłaszczyzna). fit() dobiera wagi θ minimalizujące "
     "sumę kwadratów błędów. RMSE 68 628 $ to UNDERFITTING — model jest za prosty, by uchwycić "
     "nieliniowe zależności. Objaw: duży błąd już na treningu. Leki: mocniejszy model, lepsze "
     "cechy, mniej regularyzacji.")
nb.h2("Model 2: Drzewo decyzyjne — OVERfitting podręcznikowy")
nb.code(
    "from sklearn.tree import DecisionTreeRegressor\n\n"
    "tree_reg = DecisionTreeRegressor()\n"
    "tree_reg.fit(housing_prepared, housing_labels)\n\n"
    "housing_predictions = tree_reg.predict(housing_prepared)\n"
    "tree_rmse = np.sqrt(mean_squared_error(housing_labels, housing_predictions))",
    out="tree_rmse ≈ 0.0 $   (!!!)")
nb.note("RMSE = 0 to NIE sukces — to czerwony alarm. Drzewo bez ograniczeń rozrasta się aż "
        "„zapamięta na blachę” każdy dom z treningu. Na zbiorze testowym wypadnie fatalnie. "
        "Model nauczył się odpowiedzi na pamięć zamiast GENERALIZOWAĆ.", title="OVERFITTING")
nb.p("Jak zdiagnozować, skoro na treningu wynik = 0? -> walidacja krzyżowa (sekcja 9) pokaże "
     "prawdziwy błąd ~71 tys., gorszy nawet od regresji liniowej. Leki (regularyzacja przez "
     "pruning): max_depth, min_samples_leaf, min_samples_split, max_leaf_nodes.")
nb.h2("Model 3: Las losowy — kompromis przez Ensemble")
nb.code(
    "from sklearn.ensemble import RandomForestRegressor\n\n"
    "forest_reg = RandomForestRegressor()\n"
    "forest_reg.fit(housing_prepared, housing_labels)",
    out="RMSE train ~18 tys.; w walidacji krzyżowej ~50 tys. — najlepszy z trójki")
nb.p("Random Forest = Ensemble Learning + Bagging (Bootstrap Aggregating): (1) buduje setki "
     "drzew, każde na innej losowej próbce danych (bootstrap) i losowym podzbiorze cech; (2) każde "
     "drzewo jest słabe i przeuczone inaczej — ich błędy są niezależne; (3) wynik to uśrednienie "
     "wszystkich drzew -> szumy i anomalie się znoszą.")
nb.note("Dlaczego las redukuje overfitting? Pojedyncze drzewo ma niską stronniczość, ale ogromną "
        "wariancję. Uśrednienie wielu zdekorelowanych drzew drastycznie tnie wariancję zachowując "
        "niską stronniczość. To esencja walki z overfittingiem przez „mądrość tłumu”.",
        title="Kluczowa intuicja")

# ---------------------------------------------------------------------------
# 9. Cross-validation
# ---------------------------------------------------------------------------
nb.h1("Walidacja krzyżowa", 9)
nb.p("Zbioru testowego wolno użyć tylko raz, na samym końcu. Gdybyśmy zaglądali do niego po "
     "każdej zmianie modelu, pośrednio „uczylibyśmy się” na nim -> leakage. Potrzebujemy oceny "
     "bez dotykania sejfu.")
nb.p("K-Fold dzieli zbiór treningowy na K części (foldów). W pętli K razy: trenuje na K−1 "
     "foldach, ocenia na pozostałym. Zwraca K wyników -> stabilna średnia + odchylenie.")
nb.code(
    "from sklearn.model_selection import cross_val_score\n\n"
    "lin_scores = cross_val_score(lin_reg, housing_prepared, housing_labels,\n"
    "                             scoring=\"neg_mean_squared_error\", cv=10)\n"
    "lin_rmse_scores = np.sqrt(-lin_scores)\n\n"
    "def display_scores(scores):\n"
    "    print(\"Scores:\", scores)\n"
    "    print(\"Mean:\", scores.mean())\n"
    "    print(\"Std:\", scores.std())     # niska = stabilny model\n\n"
    "display_scores(lin_rmse_scores)")
nb.note("Pułapka znaku. cross_val_score działa wg konwencji „im więcej, tym lepiej”. Skoro błąd "
        "ma być mały, sklearn używa neg_mean_squared_error (wartości UJEMNE). Dlatego liczymy "
        "np.sqrt(-scores) — najpierw negacja, potem pierwiastek.", title="Najtrudniejsze")
nb.h2("Co odkrywa CV")
nb.table(
    ["Model", "RMSE (CV)", "Wniosek"],
    [["Linear", "~69 tys.", "underfitting"],
     ["Tree", "~71 tys.", "overfitting (na treningu było 0!)"],
     ["Forest", "~50 tys.", "najlepiej generalizuje -> idzie do strojenia"]],
    widths=[4.0 * nb.cm, 4.0 * nb.cm, 8.6 * nb.cm])
nb.note("Jeśli RMSE_train << RMSE_CV -> overfitting. Jeśli oba wysokie -> underfitting. To Twój "
        "główny detektor.", title="Detektor fitu")

# ---------------------------------------------------------------------------
# 10. Strojenie
# ---------------------------------------------------------------------------
nb.h1("Strojenie hiperparametrów", 10)
nb.p("Parametry (θ) model uczy sam. Hiperparametry (liczba drzew, głębokość) ustawiasz Ty — i "
     "wpływają wprost na overfitting/underfitting.")
nb.h2("Grid Search — brutalna siła (każdy z każdym)")
nb.code(
    "from sklearn.model_selection import GridSearchCV\n\n"
    "param_grid = [\n"
    "    {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},          # 3x4 = 12\n"
    "    {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]},  # 2x3 = 6\n"
    "]\n\n"
    "forest_reg = RandomForestRegressor(random_state=42)\n"
    "grid_search = GridSearchCV(forest_reg, param_grid, cv=5,\n"
    "                           scoring='neg_mean_squared_error',\n"
    "                           return_train_score=True)\n"
    "grid_search.fit(housing_prepared, housing_labels)   # (12+6) x 5 = 90 treningów!\n\n"
    "print(grid_search.best_params_)            # najlepsza kombinacja\n"
    "best_model = grid_search.best_estimator_   # gotowy, dostrojony model")
nb.note("param_grid to LISTA słowników. Grid Search testuje każdą kombinację w każdym słowniku, "
        "dla każdej robi pełną walidację krzyżową. Liczba treningów rośnie mnożnikowo — łatwo o "
        "eksplozję kombinatoryczną.", title="Uwaga")
nb.h2("Randomized Search — inteligentne losowanie")
nb.code(
    "from sklearn.model_selection import RandomizedSearchCV\n"
    "from scipy.stats import randint\n\n"
    "final_pipeline = Pipeline([\n"
    "    ('regressor', forest_reg),\n"
    "])\n\n"
    "param_distribs = {\n"
    "    'regressor__n_estimators': randint(low=3, high=200),\n"
    "    'regressor__max_features': randint(low=2, high=20),\n"
    "}\n\n"
    "rnd_search = RandomizedSearchCV(final_pipeline, param_distributions=param_distribs,\n"
    "                                n_iter=10, cv=3,\n"
    "                                scoring='neg_root_mean_squared_error', random_state=42)\n"
    "rnd_search.fit(housing_prepared, housing_labels)\n"
    "print(rnd_search.best_params_)")
nb.note("Podwójny underscore __ to jedna z najtrudniejszych składni sklearn. "
        "'regressor__n_estimators' znaczy: wejdź do kroku pipeline'u o nazwie 'regressor' i ustaw "
        "jego parametr n_estimators. Schemat: nazwa_kroku__nazwa_parametru. Dla zagnieżdżeń: "
        "preprocessor__num_pipeline__std_scaler__with_mean. Jeden błąd w nazwie = ValueError.",
        title="Najtrudniejsze")
nb.p("Grid vs Randomized: Grid — gdy mało parametrów i chcesz pewności. Randomized — gdy "
     "przestrzeń jest wielka i liczy się czas (często znajduje lepsze ustawienia w mniej prób).")

# ---------------------------------------------------------------------------
# 11. Ewaluacja
# ---------------------------------------------------------------------------
nb.h1("Ostateczna ewaluacja — moment prawdy", 11)
nb.p("Czas otworzyć sejf. Tylko raz.")
nb.code(
    "X_test = strat_test_set.drop(\"median_house_value\", axis=1)\n"
    "y_test = strat_test_set[\"median_house_value\"].copy()\n\n"
    "X_test_prepared = full_pipeline.transform(X_test)        # transform, NIGDY fit_transform!\n"
    "test_pred = best_model.predict(X_test_prepared)\n\n"
    "final_rmse = np.sqrt(mean_squared_error(y_test, test_pred))",
    out="final_rmse ≈ 47 tys. USD")
nb.note("Na zbiorze testowym wołasz full_pipeline.transform(X_test), a NIGDY .fit_transform(). "
        "Gdybyś użył fit_transform, pipeline policzyłby nową medianę i nową skalę z danych "
        "testowych. To by (1) wpuściło informację z testu do przetwarzania (data leakage) i "
        "(2) przesunęło proporcje względem tych, na których uczył się model. Reguła na całe "
        "życie: Trening = fit_transform(). Test i produkcja = tylko transform().",
        title="NAJGROŹNIEJSZY BŁĄD CAŁEGO PROJEKTU")
nb.h2("Podsumowanie wyników")
nb.code(
    "Regresja liniowa:        ~68 600 $   (underfitting)\n"
    "Drzewo (CV):             ~71 000 $   (overfitting)\n"
    "Las losowy (CV):         ~50 000 $\n"
    "Las po strojeniu (TEST): ~47 000 $   <- finalny błąd generalizacji")
nb.p("Od „prostej linii” 70k zeszliśmy do 47k — przez inżynierię cech, ensemble i strojenie.")
nb.note("Po finalnej ewaluacji już nie wracasz do strojenia pod ten wynik — inaczej znów "
        "zaczynasz uczyć się na teście.", title="Wskazówka")

# ---------------------------------------------------------------------------
# 12. Checklista
# ---------------------------------------------------------------------------
nb.h1("Checklista i najczęstsze błędy", 12)
nb.h2("Checklista projektu")
nb.bullets([
    "Podział train/test PRZED eksploracją (StratifiedShuffleSplit).",
    "Stratyfikacja wg najważniejszej cechy.",
    "housing = strat_train_set.copy() — izolacja testu.",
    "Cały preprocessing w Pipeline / ColumnTransformer (Imputer + scaler + OHE).",
    "fit_transform tylko na train.",
    "Ocena modeli przez cross-validation, nie na teście.",
    "Strojenie przez Grid/Randomized Search z cv.",
    "transform (nie fit_transform) na teście; test użyty RAZ, na końcu.",
])
nb.h2("TOP 7 najtrudniejszych pułapek")
nb.table(
    ["Pułapka", "Skutek", "Lek"],
    [["fit_transform na teście", "data leakage, zawyżona ocena", "tylko transform"],
     ["Analiza/statystyki z testu", "data snooping bias", "sejf do końca"],
     ["RMSE=0 mylone z sukcesem", "ukryty overfitting", "cross-validation"],
     ["Kodowanie kategorii liczbami", "fałszywy porządek", "OneHotEncoder"],
     ["Brak skalowania", "dominacja dużych cech", "StandardScaler"],
     ["Zła nazwa w __", "ValueError w strojeniu", "krok__parametr"],
     ["Brak random_state", "brak powtarzalności", "ustaw wszędzie =42"]],
    widths=[5.6 * nb.cm, 6.0 * nb.cm, 5.0 * nb.cm])
nb.h2("Szybka diagnoza fitu")
nb.code(
    "RMSE_train niski,  RMSE_CV niski   -> OK, dobrze\n"
    "RMSE_train ~ 0,    RMSE_CV wysoki  -> OVERFITTING  -> regularyzacja, więcej danych, ensemble\n"
    "RMSE_train wysoki, RMSE_CV wysoki  -> UNDERFITTING -> mocniejszy model, lepsze cechy")

nb.build("/Users/weronikalewandowska/Desktop/repo_prog2/KGN_Programowanie2/Przewodnik_ML.pdf")
print("OK -> Przewodnik_ML.pdf")
