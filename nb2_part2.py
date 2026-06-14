# -*- coding: utf-8 -*-
"""CZĘŚĆ II — Projekt analizy danych: California Housing (P2Lab10), krok po kroku."""

def build(nb):
    nb.part("CZĘŚĆ II\nProjekt analizy danych\nCalifornia Housing — krok po kroku")

    nb.h1("Wprowadzenie do projektu", 0)
    nb.p("Projekt rozwiązuje klasyczne zadanie uczenia maszynowego z książki A. Gérona: na podstawie "
         "danych o dzielnicach Kalifornii (z amerykańskiego spisu z 1990 r.) przewidzieć "
         "<b>medianę ceny domu</b> w dzielnicy. To problem <b>regresji z nadzorem</b> — cel "
         "(median_house_value) jest liczbą, a w danych mamy poprawne odpowiedzi do uczenia.")
    nb.p("Cały proces przebiega według stałego schematu projektu ML, który warto zapamiętać:")
    nb.bullets([
        "1. Wczytanie i eksploracja danych (poznajemy zbiór).",
        "2. Podział na zbiór treningowy i testowy (test odkładamy na bok).",
        "3. Wizualizacje i analiza korelacji (szukamy zależności).",
        "4. Oddzielenie etykiet (X = cechy, y = to, co przewidujemy).",
        "5. Czyszczenie i przygotowanie danych w potoku (pipeline).",
        "6. Trenowanie kilku modeli i ich porównanie (walidacja krzyżowa).",
        "7. Strojenie hiperparametrów najlepszego modelu (Grid/Randomized Search).",
        "8. Ostateczna ocena na zbiorze testowym.",
    ])

    # ================================================================
    nb.h1("Wczytanie i eksploracja danych", 1)
    nb.p("Najpierw pobieramy plik CSV z danymi. Wykrzyknik ! przed poleceniem oznacza wykonanie "
         "komendy systemowej (powłoki) z poziomu notatnika Colab:")
    nb.code(
"# Pobranie pliku CSV z danymi (komenda powłoki w Colab)\n"
"!wget https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv\n",
        caption="Cela [2]: pobranie surowych danych.")
    nb.p("Wczytujemy dane do ramki pandas. Funkcja pd.read_csv parsuje plik CSV i zwraca DataFrame:")
    nb.code(
"import pandas as pd\n"
"import numpy as np\n"
"\n"
"def load_housing_data(housing_path=\"/content/housing.csv\"):\n"
"    return pd.read_csv(housing_path)   # wczytaj CSV -> DataFrame\n"
"\n"
"housing = load_housing_data()          # 'housing' to nasza tabela danych\n",
        caption="Cela [3]: wczytanie danych do DataFrame.")

    nb.h2("1.1. housing.info() — struktura tabeli")
    nb.p("Metoda .info() wypisuje podsumowanie: liczbę wierszy, nazwy kolumn, liczbę wartości "
         "NIEpustych w każdej kolumnie oraz ich typy. To pierwszy krok diagnozy — od razu widać braki danych.")
    nb.code(
"housing.info()\n",
        caption="Cela [4]: informacje o tabeli.",
        out="RangeIndex: 20640 entries  (20640 dzielnic)\n"
            "total_bedrooms   20433 non-null  (207 BRAKÓW!)  <- reszta kolumn ma 20640\n"
            "ocean_proximity  20640 non-null  object         <- jedyna kolumna tekstowa\n"
            "dtypes: float64(9), object(1)")
    nb.note("Najważniejsza obserwacja: total_bedrooms ma tylko 20433 wartości zamiast 20640 — brakuje "
            "207. Te braki trzeba będzie uzupełnić (zrobi to SimpleImputer). Wszystkie kolumny poza "
            "ocean_proximity są liczbowe (float64).")

    nb.h2("1.2. value_counts() — rozkład kolumny kategorycznej")
    nb.p("ocean_proximity to kolumna tekstowa (kategoryczna) — opisuje położenie względem oceanu. "
         "Metoda .value_counts() liczy, ile razy występuje każda kategoria:")
    nb.code(
"housing[\"ocean_proximity\"].value_counts()   # ile dzielnic w każdej kategorii\n",
        caption="Cela [5]: liczności kategorii.",
        out="<1H OCEAN     9136\nINLAND        6551\nNEAR OCEAN    2658\nNEAR BAY      2290\nISLAND           5")
    nb.note("To pięć kategorii tekstowych. Modele ML nie rozumieją tekstu — tę kolumnę trzeba "
            "zamienić na liczby (zrobi to OneHotEncoder, omówiony szczegółowo w Części III).")

    nb.h2("1.3. describe() i histogramy — rozkłady cech liczbowych")
    nb.p(".describe() podaje statystyki opisowe każdej kolumny liczbowej: liczność (count), średnią "
         "(mean), odchylenie standardowe (std), minimum, kwartyle (25%, 50%=mediana, 75%) i maksimum.")
    nb.code(
"housing.describe()   # statystyki opisowe wszystkich kolumn liczbowych\n",
        caption="Cela [6]: statystyki opisowe.")
    nb.p("Histogram pokazuje rozkład wartości każdej cechy — ile dzielnic mieści się w danym przedziale. "
         "Metoda .hist() rysuje histogramy dla wszystkich kolumn liczbowych naraz:")
    nb.code(
"%matplotlib inline                    # rysuj wykresy wewnątrz notatnika\n"
"import matplotlib.pyplot as plt\n"
"\n"
"# bins=50 -> 50 słupków na histogram; figsize -> rozmiar rysunku w calach\n"
"housing.hist(bins=50, figsize=(20, 15))\n"
"plt.show()                            # wyświetl wykresy\n",
        caption="Cela [7]: histogramy wszystkich cech liczbowych.")
    nb.note("Z histogramów uczymy się, że: (a) median_income jest w dziwnej skali (ok. 0–15, bo "
            "przeskalowano dochód), (b) median_house_value i housing_median_age są „ucięte\" u góry "
            "(sztuczny limit), (c) wiele cech jest „skośnych w prawo\" (długi ogon dużych wartości). "
            "To ważne, bo modele lepiej działają na cechach o zbliżonej skali — stąd potrzeba standaryzacji.")

    # ================================================================
    nb.h1("Podział na zbiór treningowy i testowy", 2)
    nb.p("Zanim cokolwiek zaczniemy modelować, odkładamy część danych jako zbiór TESTOWY, którego "
         "nie wolno nam podglądać do samego końca. Inaczej oszukalibyśmy sami siebie co do jakości "
         "modelu (patrz Część I poprzedniej notatki — przeuczenie).")
    nb.code(
"from sklearn.model_selection import train_test_split\n"
"\n"
"# test_size=0.2 -> 20% danych na test, 80% na trening\n"
"# random_state=42 -> stała losowość, by podział był POWTARZALNY\n"
"train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)\n",
        caption="Cela [9]: prosty podział losowy 80/20.")

    nb.h2("2.1. Stratyfikacja — reprezentatywny podział")
    nb.p("Czysto losowy podział może przez przypadek dać zbiór testowy o innym rozkładzie dochodów "
         "niż całość. Ponieważ dochód mocno wpływa na cenę, chcemy, by proporcje grup dochodowych "
         "były takie same w treningu i teście. To <b>stratyfikacja</b> (podział warstwowy). Najpierw "
         "tworzymy pomocniczą kolumnę kategorii dochodu:")
    nb.code(
"# Dzielimy dochód przez 1.5 i zaokrąglamy w górę (ceil), by zrobić DYSKRETNE\n"
"# kategorie dochodowe (1, 2, 3, ...). To grupuje ciągły dochód w przedziały.\n"
"housing[\"income_cat\"] = np.ceil(housing[\"median_income\"] / 1.5)\n"
"\n"
"# Wszystkie kategorie powyżej 5 'spłaszczamy' do 5 (clip = przytnij od góry),\n"
"# by nie było rzadkich, licznościowo małych grup.\n"
"housing[\"income_cat\"] = housing[\"income_cat\"].clip(upper=5)\n",
        caption="Cele [11]/[12]: utworzenie kategorii dochodu income_cat.")
    nb.p("Teraz dzielimy dane tak, by w obu częściach proporcje income_cat były zachowane. Służy do "
         "tego StratifiedShuffleSplit:")
    nb.code(
"from sklearn.model_selection import StratifiedShuffleSplit\n"
"\n"
"# n_splits=1 -> jeden podział; test_size=0.2 -> 20% na test\n"
"split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)\n"
"\n"
"# split.split zwraca INDEKSY wierszy treningowych i testowych,\n"
"# dobrane tak, by rozkład income_cat był zachowany w obu zbiorach.\n"
"for train_index, test_index in split.split(housing, housing[\"income_cat\"]):\n"
"    strat_train_set = housing.loc[train_index]   # wiersze treningowe (po etykietach)\n"
"    strat_test_set = housing.loc[test_index]      # wiersze testowe\n",
        caption="Cela [12]: stratyfikowany podział danych.")
    nb.code(
"# Sprawdzenie: udział każdej kategorii dochodu w całości danych\n"
"housing[\"income_cat\"].value_counts() / len(housing)\n",
        caption="Cela [13]: proporcje kategorii dochodu.",
        out="3.0  0.350581\n2.0  0.318847\n4.0  0.176308\n5.0  0.114438\n1.0  0.039826")
    nb.p("Kolumna income_cat zrobiła już swoje (posłużyła tylko do podziału), więc ją usuwamy z obu "
         "zbiorów, aby wrócić do oryginalnych cech:")
    nb.code(
"# Usuń pomocniczą kolumnę income_cat z OBU zbiorów\n"
"for set_ in (strat_train_set, strat_test_set):\n"
"    set_.drop([\"income_cat\"], axis=1, inplace=True)   # axis=1 = kolumna; inplace = w miejscu\n"
"\n"
"housing = strat_train_set.copy()   # dalej pracujemy na KOPII zbioru treningowego\n",
        caption="Cele [14]/[15]: sprzątanie i kopia zbioru treningowego.")
    nb.note("Dlaczego .copy()? Żeby eksperymenty (dodawanie kolumn, wykresy) nie zmieniały oryginalnego "
            "strat_train_set. To zabezpieczenie przed przypadkową modyfikacją danych źródłowych.")

    # ================================================================
    nb.h1("Wizualizacje i korelacje", 3)
    nb.p("Teraz badamy zależności w danych treningowych. Najpierw mapa geograficzna — rysujemy "
         "dzielnice według długości i szerokości geograficznej, kolorując je ceną:")
    nb.code(
"housing.plot(kind=\"scatter\", x=\"longitude\", y=\"latitude\", alpha=0.4,\n"
"    s=housing[\"population\"]/100,        # rozmiar punktu = liczba ludności / 100\n"
"    label=\"population\",\n"
"    c=\"median_house_value\",             # KOLOR punktu = cena domu\n"
"    cmap=plt.get_cmap(\"jet\"), colorbar=True)  # mapa kolorów jet + pasek skali\n"
"plt.legend()\n",
        caption="Cela [17]: mapa cen domów. alpha=0.4 (przezroczystość) uwidacznia zagęszczenia.")
    nb.note("Wniosek z mapy: najdroższe domy (czerwone) są przy wybrzeżu i w dużych skupiskach "
            "ludności — położenie i gęstość zaludnienia mają znaczenie dla ceny.")

    nb.h2("3.1. Macierz korelacji")
    nb.definition("Korelacja (Pearsona) to liczba z przedziału [−1, 1] mierząca LINIOWĄ zależność "
                  "dwóch cech. +1 = idealna zależność rosnąca, −1 = idealna malejąca, 0 = brak "
                  "zależności liniowej. Metoda .corr() liczy korelacje wszystkich par kolumn.")
    nb.code(
"attributes = [\"median_house_value\", \"median_income\",\n"
"              \"total_rooms\", \"housing_median_age\"]\n"
"corr_matrix = housing[attributes].corr()         # macierz korelacji wybranych cech\n"
"\n"
"# Jak każda cecha koreluje z CENĄ, posortowane malejąco:\n"
"corr_matrix[\"median_house_value\"].sort_values(ascending=False)\n",
        caption="Cela [18]: korelacja cech z ceną domu.",
        out="median_house_value   1.000000\nmedian_income        0.687  <- NAJSILNIEJSZA\n"
            "total_rooms          0.135\nhousing_median_age   0.114")
    nb.note("median_income ma korelację 0.69 z ceną — to zdecydowanie najsilniejszy predyktor. "
            "Im wyższy dochód mieszkańców, tym droższe domy. To kluczowa cecha dla modelu.")
    nb.p("Macierz wykresów rozrzutu (scatter_matrix) rysuje każdą cechę względem każdej innej — "
         "pozwala wzrokowo wychwycić zależności:")
    nb.code(
"from pandas.plotting import scatter_matrix\n"
"attributes = [\"median_house_value\", \"median_income\",\n"
"              \"total_rooms\", \"housing_median_age\"]\n"
"scatter_matrix(housing[attributes], figsize=(12, 8))   # siatka wykresów par cech\n",
        caption="Cela [19]: macierz wykresów rozrzutu.")
    nb.code(
"# Powiększenie najsilniejszej zależności: dochód vs cena\n"
"housing.plot(kind=\"scatter\", x=\"median_income\", y=\"median_house_value\", alpha=0.1)\n",
        caption="Cela [20]: dochód kontra cena (widać też poziome 'linie' od ucięcia ceny).")

    nb.h2("3.2. Tworzenie nowych, sensowniejszych cech")
    nb.p("Surowe „łączna liczba pokoi w dzielnicy\" mało mówi — lepsza jest „liczba pokoi na "
         "gospodarstwo\". Tworzymy więc cechy pochodne (feature engineering) jako iloraz istniejących kolumn:")
    nb.code(
"# Cechy względne niosą więcej informacji niż wartości bezwzględne:\n"
"housing[\"rooms_per_household\"] = housing[\"total_rooms\"] / housing[\"households\"]\n"
"housing[\"bedrooms_per_room\"] = housing[\"total_bedrooms\"] / housing[\"total_rooms\"]\n"
"housing[\"population_per_household\"] = housing[\"population\"] / housing[\"households\"]\n",
        caption="Cela [22]: nowe cechy jako ilorazy kolumn (wektoryzacja pandas).")
    nb.code(
"housing_num = housing.drop(\"ocean_proximity\", axis=1)  # usuń kolumnę TEKSTOWĄ\n"
"corr_matrix = housing_num.corr()                        # korelacje już z nowymi cechami\n"
"corr_matrix[\"median_house_value\"].sort_values(ascending=False)\n",
        caption="Cele [23]/[24]: korelacja po dodaniu nowych cech (bez kolumny tekstowej).",
        out="median_income          0.687\nrooms_per_household     0.146  <- nowa cecha, lepsza niż total_rooms\n"
            "bedrooms_per_room      -0.260  <- silna UJEMNA korelacja (nowa, wartościowa cecha)")
    nb.note("bedrooms_per_room (udział sypialni w pokojach) ma korelację −0.26 — silniejszą niż "
            "surowe total_rooms (0.13). Mniej sypialni na pokój = droższe domy. Dobre cechy pochodne "
            "potrafią znacząco poprawić model.")

    # ================================================================
    nb.h1("Oddzielenie etykiet (X i y)", 4)
    nb.p("W uczeniu z nadzorem rozdzielamy CECHY (X — to, na podstawie czego przewidujemy) od "
         "ETYKIET (y — to, co przewidujemy). Etykietą jest median_house_value:")
    nb.code(
"# X = wszystkie kolumny OPRÓCZ ceny (cechy wejściowe)\n"
"housing = strat_train_set.drop(\"median_house_value\", axis=1)\n"
"\n"
"# y = sama kolumna ceny (cel/etykiety); .copy() dla bezpieczeństwa\n"
"housing_labels = strat_train_set[\"median_house_value\"].copy()\n",
        caption="Cela [26]: rozdzielenie cech (housing) i etykiet (housing_labels).")
    nb.note("Od tej chwili 'housing' to czyste cechy bez ceny. Etykiety (housing_labels) podamy "
            "modelowi osobno w metodzie .fit(X, y). Cena NIE może być częścią X — inaczej model "
            "„oszukiwałby\", widząc odpowiedź.")

    # ================================================================
    nb.h1("Czyszczenie i przygotowanie danych — potok (pipeline)", 5)
    nb.p("To serce projektu. Dane wymagają kilku przekształceń: uzupełnienia braków, dodania cech "
         "pochodnych, standaryzacji liczb i zakodowania kolumny tekstowej. Zamiast robić to ręcznie, "
         "budujemy <b>potok (Pipeline)</b> — listę kroków wykonywanych po kolei, automatycznie i "
         "powtarzalnie. Szczegóły każdego narzędzia są w Części III; tu pokazujemy, jak składają się w całość.")

    nb.h2("5.1. Własny transformator dodający cechy (CombinedAttributesAdder)")
    nb.p("scikit-learn pozwala pisać własne transformatory. Dziedziczymy po BaseEstimator i "
         "TransformerMixin, dzięki czemu nasz obiekt ma standardowe metody fit/transform i pasuje do "
         "potoku. Ten transformator dodaje cechy pochodne, ale operuje na tablicy NumPy (indeksy kolumn):")
    nb.code(
"from sklearn.base import BaseEstimator, TransformerMixin\n"
"\n"
"# Indeksy (numery) kolumn w tablicy NumPy, których będziemy używać:\n"
"rooms_ix, bedrooms_ix, population_ix, household_ix = 3, 4, 5, 6\n"
"\n"
"class CombinedAttributesAdder(BaseEstimator, TransformerMixin):\n"
"    def __init__(self, add_bedrooms_per_room=True):   # hiperparametr: czy dodać bedrooms_per_room\n"
"        self.add_bedrooms_per_room = add_bedrooms_per_room\n"
"    def fit(self, X, y=None):\n"
"        return self                                    # nic nie 'uczymy' -> zwróć siebie\n"
"    def transform(self, X, y=None):\n"
"        rooms_per_household = X[:, rooms_ix] / X[:, household_ix]       # pokoje / gosp. domowe\n"
"        population_per_household = X[:, population_ix] / X[:, household_ix]\n"
"        if self.add_bedrooms_per_room:\n"
"            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]\n"
"            # np.c_ skleja kolumny obok siebie (column stack)\n"
"            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]\n"
"        return np.c_[X, rooms_per_household, population_per_household]\n",
        caption="Cela [28]: własny transformator dodający cechy pochodne.")
    nb.definition("Para fit/transform to wzorzec scikit-learn. fit UCZY się parametrów na danych "
                  "(np. mediany, średnie), transform STOSUJE je, przekształcając dane. Tutaj fit nic "
                  "nie liczy (zwraca self), bo dodanie ilorazu nie wymaga uczenia. TransformerMixin "
                  "dorzuca za darmo metodę fit_transform (fit + transform w jednym).")

    nb.h2("5.2. Selektor kolumn (DataFrameSelector)")
    nb.p("Pomocniczy transformator wybierający tylko wskazane kolumny z DataFrame i zwracający je "
         "jako tablicę NumPy (potrzebną kolejnym krokom potoku):")
    nb.code(
"class DataFrameSelector(BaseEstimator, TransformerMixin):\n"
"    def __init__(self, attribute_names):\n"
"        self.attribute_names = attribute_names    # nazwy kolumn do wybrania\n"
"    def fit(self, X, y=None):\n"
"        return self\n"
"    def transform(self, X):\n"
"        return X[self.attribute_names].values     # .values -> z DataFrame na tablicę NumPy\n",
        caption="Cela [29]: selektor wybranych kolumn.")

    nb.h2("5.3. Dwa potoki: liczbowy i kategoryczny + ich połączenie")
    nb.p("Liczby i tekst wymagają innego przygotowania, więc budujemy DWA osobne potoki, a potem "
         "łączymy je w jeden. Wersja z notatnika ANALIZY używa FeatureUnion i własnego "
         "MyLabelBinarizer do kodowania tekstu:")
    nb.code(
"from sklearn.pipeline import FeatureUnion, Pipeline\n"
"from sklearn.preprocessing import StandardScaler\n"
"from sklearn.impute import SimpleImputer\n"
"\n"
"num_attribs = ['longitude','latitude','housing_median_age','total_rooms',\n"
"               'total_bedrooms','population','households','median_income']\n"
"cat_attribs = [\"ocean_proximity\"]\n"
"\n"
"# POTOK LICZBOWY — kroki wykonywane PO KOLEI na kolumnach liczbowych:\n"
"num_pipeline = Pipeline([\n"
"    ('selector', DataFrameSelector(num_attribs)),    # 1. wybierz kolumny liczbowe\n"
"    ('imputer', SimpleImputer(strategy=\"median\")),   # 2. uzupełnij braki MEDIANĄ\n"
"    ('attribs_adder', CombinedAttributesAdder()),    # 3. dodaj cechy pochodne\n"
"    ('std_scaler', StandardScaler()),                # 4. standaryzuj (średnia 0, std 1)\n"
"])\n"
"\n"
"# POTOK KATEGORYCZNY — przetwarza kolumnę tekstową:\n"
"cat_pipeline = Pipeline([\n"
"    ('selector', DataFrameSelector(cat_attribs)),    # 1. wybierz kolumnę tekstową\n"
"    ('label_binarizer', MyLabelBinarizer()),         # 2. zamień tekst na kolumny 0/1\n"
"])\n"
"\n"
"# FeatureUnion uruchamia OBA potoki RÓWNOLEGLE i SKLEJA ich wyniki w jedną tablicę:\n"
"full_pipeline = FeatureUnion(transformer_list=[\n"
"    (\"num_pipeline\", num_pipeline),\n"
"    (\"cat_pipeline\", cat_pipeline),\n"
"])\n",
        caption="Cela [31]: pełny potok przetwarzania (wersja FeatureUnion z notatnika analizy).")
    nb.p("Uruchomienie potoku — fit_transform uczy wszystkie kroki na danych treningowych i od razu "
         "je przekształca:")
    nb.code(
"housing_prepared = full_pipeline.fit_transform(housing)   # surowe cechy -> gotowa tablica liczb\n"
"housing_prepared.shape                                    # (16512, 17) -> 16512 wierszy, 17 kolumn\n",
        caption="Cele [32]/[33]: wykonanie potoku. Wynik to czysto liczbowa tablica gotowa dla modelu.")
    nb.note("Po przetworzeniu mamy 17 kolumn: 8 oryginalnych liczbowych + 3 cechy pochodne + "
            "kategorie ocean_proximity zakodowane jako kolumny 0/1. Wszystko liczbowe, bez braków, "
            "wystandaryzowane — dokładnie to, czego oczekują modele sklearn.")

    nb.h2("5.4. Wersja nowocześniejsza: ColumnTransformer + OneHotEncoder")
    nb.p("Drugi notatnik (P2Lab10_..._ml) realizuje to samo czyściej, używając wbudowanych narzędzi "
         "<b>ColumnTransformer</b> (zamiast FeatureUnion + selektory) i <b>OneHotEncoder</b> (zamiast "
         "własnego binaryzera). To dzisiejszy standard:")
    nb.code(
"from sklearn.pipeline import Pipeline\n"
"from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
"from sklearn.impute import SimpleImputer\n"
"from sklearn.compose import ColumnTransformer\n"
"\n"
"num_pipeline = Pipeline([\n"
"    ('imputer', SimpleImputer(strategy=\"median\")),   # uzupełnij braki medianą\n"
"    ('attribs_adder', CombinedAttributesAdder()),    # dodaj cechy pochodne\n"
"    ('std_scaler', StandardScaler()),                # standaryzuj\n"
"])\n"
"cat_pipeline = Pipeline([\n"
"    ('one_hot', OneHotEncoder()),                    # tekst -> kolumny 0/1\n"
"])\n"
"\n"
"# ColumnTransformer SAM kieruje wskazane kolumny do właściwego potoku:\n"
"full_pipeline = ColumnTransformer([\n"
"    (\"num_pipeline\", num_pipeline, num_attribs),     # te kolumny -> potok liczbowy\n"
"    (\"cat_pipeline\", cat_pipeline, cat_attribs),     # te kolumny -> potok kategoryczny\n"
"])\n"
"\n"
"housing_prepared = full_pipeline.fit_transform(housing)\n",
        caption="Cele [31]/[32] z notatnika ML: ten sam efekt, czytelniej (ColumnTransformer).")
    nb.note("Różnica: FeatureUnion wymaga ręcznych selektorów kolumn w każdym potoku, a "
            "ColumnTransformer przyjmuje listę kolumn jako trzeci element krotki i sam je rozdziela. "
            "Efekt końcowy (gotowa tablica liczb) jest taki sam.")

    # ================================================================
    nb.h1("Trenowanie i ocena modeli", 6)
    nb.p("Mając przygotowane dane, trenujemy kolejno trzy modele regresji i porównujemy ich błąd. "
         "Miarą jest <b>RMSE</b> (pierwiastek z błędu średniokwadratowego) — średnia pomyłka w dolarach.")

    nb.h2("6.1. Regresja liniowa")
    nb.code(
"from sklearn.linear_model import LinearRegression\n"
"\n"
"lin_reg = LinearRegression()                  # utwórz model\n"
"lin_reg.fit(housing_prepared, housing_labels) # UCZENIE: dopasuj do danych (X, y)\n",
        caption="Cela [36]: trening regresji liniowej.")
    nb.code(
"from sklearn.metrics import mean_squared_error\n"
"\n"
"housing_predictions = lin_reg.predict(housing_prepared)         # przewidywania na treningu\n"
"lin_mse = mean_squared_error(housing_labels, housing_predictions) # błąd średniokwadratowy\n"
"lin_rmse = np.sqrt(lin_mse)                                      # RMSE = pierwiastek z MSE\n"
"lin_rmse\n",
        caption="Cela [37]: błąd RMSE regresji liniowej.", out="68628.0  (średnia pomyłka ok. 68 600 $)")
    nb.note("RMSE ≈ 68 600 $ przy cenach w przedziale 120–265 tys. $ to dużo — model jest "
            "NIEDOUCZONY (underfitting). Regresja liniowa jest zbyt prosta, by uchwycić zależności w danych.")

    nb.h2("6.2. Walidacja krzyżowa (cross-validation)")
    nb.definition("Walidacja krzyżowa k-krotna (k-fold) dzieli dane treningowe na k części. Model "
                  "trenuje się k razy, za każdym razem ucząc na k−1 częściach i testując na jednej "
                  "pominiętej. Otrzymujemy k wyników, których średnia jest rzetelną oceną modelu — "
                  "bez podglądania prawdziwego zbioru testowego.")
    nb.code(
"def display_scores(scores):\n"
"    print(\"Scores:\", scores)             # wyniki w każdej z k iteracji\n"
"    print(\"Mean:\", scores.mean())        # średni wynik\n"
"    print(\"Standard deviation:\", scores.std())  # rozrzut (stabilność)\n"
"\n"
"from sklearn.model_selection import cross_val_score\n"
"\n"
"# scoring='neg_mean_squared_error': sklearn maksymalizuje wynik, więc używa\n"
"# UJEMNEGO MSE (większy = lepszy). cv=10 -> 10-krotna walidacja.\n"
"lin_scores = cross_val_score(lin_reg, housing_prepared, housing_labels,\n"
"                             scoring=\"neg_mean_squared_error\", cv=10)\n"
"lin_rmse_scores = np.sqrt(-lin_scores)   # minus, by wrócić do dodatniego MSE, potem pierwiastek\n"
"display_scores(lin_rmse_scores)\n",
        caption="Cele [38]/[39]: 10-krotna walidacja krzyżowa regresji liniowej.",
        out="Mean: ~69050   Std: ~2730")
    nb.note("Sztuczka ze znakiem minus: scoring zwraca UJEMNE MSE (bo sklearn zawsze „maksymalizuje\" "
            "wynik). Dlatego piszemy np.sqrt(-lin_scores), by uzyskać zwykłe, dodatnie RMSE.")

    nb.h2("6.3. Drzewo decyzyjne — pułapka przeuczenia")
    nb.code(
"from sklearn.tree import DecisionTreeRegressor\n"
"\n"
"tree_reg = DecisionTreeRegressor()\n"
"tree_reg.fit(housing_prepared, housing_labels)\n"
"\n"
"tree_predictions = tree_reg.predict(housing_prepared)\n"
"tree_rmse = np.sqrt(mean_squared_error(housing_labels, tree_predictions))\n"
"print(f\"Decision Tree Training RMSE: {tree_rmse:.2f}\")\n",
        caption="Cele [41]/[42]: trening drzewa i jego błąd na TRENINGU.", out="Decision Tree Training RMSE: 0.00")
    nb.note("RMSE = 0 na danych treningowych wygląda na ideał, ale to ALARM: drzewo nauczyło się "
            "danych NA PAMIĘĆ (klasyczne przeuczenie). Prawdziwą jakość pokaże dopiero walidacja krzyżowa.")
    nb.code(
"tree_scores = cross_val_score(tree_reg, housing_prepared, housing_labels,\n"
"                              scoring=\"neg_mean_squared_error\", cv=10)\n"
"tree_rmse_scores = np.sqrt(-tree_scores)\n"
"display_scores(tree_rmse_scores)   # Decision Tree model is overfitting\n",
        caption="Cele [43]/[46]: walidacja krzyżowa ujawnia przeuczenie.",
        out="Mean: ~71400  (gorzej niż regresja liniowa! mimo zerowego błędu na treningu)")
    nb.note("Po walidacji drzewo wypada ~71 400 $ — GORZEJ niż prosta regresja liniowa. To dowód "
            "przeuczenia: model świetny na danych, które widział, słaby na nowych. Walidacja "
            "krzyżowa jest jedynym sposobem, by to wykryć bez ruszania zbioru testowego.")

    nb.h2("6.4. Las losowy (Random Forest) — najlepszy z trzech")
    nb.definition("Las losowy to ZESPÓŁ (ensemble) wielu drzew decyzyjnych, z których każde uczy się "
                  "na losowym podzbiorze danych i cech. Końcowa predykcja to ŚREDNIA przewidywań "
                  "wszystkich drzew. Uśrednianie redukuje przeuczenie pojedynczych drzew i daje "
                  "stabilniejszy, dokładniejszy model.")
    nb.code(
"from sklearn.ensemble import RandomForestRegressor\n"
"\n"
"forest_reg = RandomForestRegressor()\n"
"forest_reg.fit(housing_prepared, housing_labels)\n"
"\n"
"housing_predictions = forest_reg.predict(housing_prepared)\n"
"forest_rmse = np.sqrt(mean_squared_error(housing_labels, housing_predictions))\n"
"forest_rmse\n",
        caption="Cela [48]: trening lasu losowego i błąd na treningu.", out="~18600 (niski błąd treningowy)")
    nb.code(
"scores = cross_val_score(forest_reg, housing_prepared, housing_labels,\n"
"                         scoring=\"neg_mean_squared_error\", cv=10)\n"
"forest_rmse_scores = np.sqrt(-scores)\n"
"display_scores(forest_rmse_scores)\n",
        caption="Cele [49]/[50]: walidacja krzyżowa lasu losowego.", out="Mean: ~50300  Std: ~2000")
    nb.note("Las losowy: ~50 300 $ na walidacji — wyraźnie najlepszy z trzech modeli. Wciąż jest "
            "różnica między błędem treningowym (~18 600) a walidacyjnym (~50 300), więc model nadal "
            "trochę się przeucza, ale to najlepszy kandydat do dalszego strojenia.")
    nb.table(["Model", "RMSE (walidacja krzyżowa)", "Wniosek"],
             [["Regresja liniowa", "~69 050 $", "niedouczony (za prosty)"],
              ["Drzewo decyzyjne", "~71 400 $", "przeuczony (0 na treningu, źle na walidacji)"],
              ["Las losowy", "~50 300 $", "najlepszy — wybieramy do strojenia"]],
             widths=[3.8*nb.cm, 5.0*nb.cm, 7.8*nb.cm])

    # ================================================================
    nb.h1("Strojenie hiperparametrów i ocena końcowa", 7)
    nb.definition("Hiperparametry to ustawienia modelu, których NIE uczy on sam (np. liczba drzew w "
                  "lesie). Dobieramy je z zewnątrz. GridSearchCV automatycznie sprawdza wszystkie "
                  "kombinacje podanych wartości, każdą oceniając walidacją krzyżową, i wybiera najlepszą.")
    nb.h2("7.1. Grid Search — przeszukiwanie siatki")
    nb.code(
"from sklearn.model_selection import GridSearchCV\n"
"\n"
"param_grid = [\n"
"    # 1. zestaw: 3 wartości n_estimators × 4 wartości max_features = 12 kombinacji\n"
"    {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},\n"
"    # 2. zestaw: z bootstrap=False -> 2 × 3 = 6 kombinacji\n"
"    {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]},\n"
"]\n"
"\n"
"forest_reg = RandomForestRegressor(random_state=42)\n"
"# cv=5 -> każda z 12+6=18 kombinacji testowana 5 razy = 90 treningów\n"
"grid_search = GridSearchCV(forest_reg, param_grid, cv=5,\n"
"                           scoring='neg_mean_squared_error',\n"
"                           return_train_score=True)\n"
"grid_search.fit(housing_prepared, housing_labels)   # uruchom przeszukiwanie\n",
        caption="Cela [51]: definicja i uruchomienie Grid Search.")
    nb.code(
"grid_search.best_params_       # najlepsza znaleziona kombinacja hiperparametrów\n"
"grid_search.best_estimator_    # gotowy, najlepszy model (już wytrenowany)\n",
        caption="Cele [52]/[53]: odczyt najlepszych ustawień.",
        out="{'max_features': 6, 'n_estimators': 30}  (przykładowo)")

    nb.h2("7.2. Ostateczna ocena na zbiorze testowym")
    nb.p("Dopiero TERAZ, na samym końcu, sięgamy po odłożony zbiór testowy — by uczciwie oszacować, "
         "jak model poradzi sobie z nowymi danymi. Kluczowe: na teście używamy <b>transform</b> "
         "(NIE fit_transform!) tym samym potokiem, co na treningu:")
    nb.code(
"best_model = grid_search.best_estimator_           # najlepszy model z Grid Search\n"
"\n"
"X_test = strat_test_set.drop(\"median_house_value\", axis=1)  # cechy testowe\n"
"y_test = strat_test_set[\"median_house_value\"].copy()         # prawdziwe ceny testowe\n"
"\n"
"# UWAGA: transform, NIE fit_transform! Potok został już nauczony na treningu.\n"
"# Używamy mediany i średnich Z TRENINGU, by nie 'podejrzeć' testu.\n"
"X_test_prepared = full_pipeline.transform(X_test)\n"
"\n"
"test_pred = best_model.predict(X_test_prepared)    # przewidywania na teście\n"
"final_rmse = np.sqrt(mean_squared_error(y_test, test_pred))   # ostateczny błąd\n"
"final_rmse\n",
        caption="Cele [55]–[60]: przygotowanie testu i ostateczna ocena.", out="~47700 (finalny RMSE)")
    nb.note("To NAJWAŻNIEJSZA zasada całego projektu: zbiór testowy przetwarzamy metodą transform z "
            "potoku nauczonego na TRENINGU. Gdybyśmy wywołali fit_transform na teście, potok policzyłby "
            "mediany/średnie z danych testowych — to byłby „przeciek danych\" (data leakage), a wynik "
            "byłby zawyżony i nieuczciwy.")

    nb.h2("7.3. Randomized Search — losowe przeszukiwanie")
    nb.p("Gdy kombinacji jest bardzo dużo, zamiast sprawdzać wszystkie (Grid Search), losujemy ich "
         "ograniczoną liczbę. RandomizedSearchCV próbkuje wartości z podanych ROZKŁADÓW — często "
         "znajduje dobre ustawienia znacznie szybciej:")
    nb.code(
"from sklearn.model_selection import RandomizedSearchCV\n"
"from scipy.stats import randint                 # rozkład losowych liczb całkowitych\n"
"\n"
"forest_reg = RandomForestRegressor(random_state=42)\n"
"final_pipeline = Pipeline([('regressor', forest_reg)])\n"
"\n"
"param_distribs = {\n"
"    # losuj liczbę drzew z przedziału [3, 200) i liczbę cech z [2, 20)\n"
"    'regressor__n_estimators': randint(low=3, high=200),\n"
"    'regressor__max_features': randint(low=2, high=20),\n"
"}\n"
"\n"
"# n_iter=10 -> wylosuj i przetestuj tylko 10 kombinacji (zamiast wszystkich)\n"
"rnd_search = RandomizedSearchCV(final_pipeline, param_distributions=param_distribs,\n"
"                                n_iter=10, cv=3,\n"
"                                scoring='neg_root_mean_squared_error', random_state=42)\n"
"rnd_search.fit(housing_prepared, housing_labels)\n"
"rnd_search.best_params_                         # najlepsza wylosowana kombinacja\n",
        caption="Cele [63]/[64]: Randomized Search jako szybsza alternatywa Grid Search.")
    nb.note("Zapis z podwójnym podkreśleniem 'regressor__n_estimators' to sposób adresowania "
            "parametru KROKU potoku: nazwa_kroku + '__' + nazwa_parametru. Dzięki temu search wie, "
            "którego elementu potoku dotyczy strojony hiperparametr.")
