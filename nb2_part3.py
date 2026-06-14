# -*- coding: utf-8 -*-
"""CZĘŚĆ III — Kluczowe narzędzia scikit-learn (dogłębnie)."""

def build(nb):
    nb.part("CZĘŚĆ III\nKluczowe narzędzia scikit-learn\nSimpleImputer · StandardScaler · OneHotEncoder · Pipeline")

    # ================================================================
    nb.h1("Wspólny interfejs scikit-learn: estymatory, transformatory, fit/transform", 1)
    nb.p("Cała biblioteka scikit-learn opiera się na kilku spójnych pojęciach. Zrozumienie ich raz "
         "sprawia, że każdy nowy obiekt (imputer, skaler, encoder, model) używa się tak samo.")
    nb.definition("ESTYMATOR — dowolny obiekt, który UCZY się czegoś z danych metodą fit(X[, y]). "
                  "Nauczone wartości zapisuje w atrybutach zakończonych podkreśleniem, np. mean_, "
                  "statistics_, categories_.")
    nb.definition("TRANSFORMATOR — estymator, który dodatkowo PRZEKSZTAŁCA dane metodą transform(X) "
                  "(np. uzupełnia braki, skaluje, koduje). Ma też skrót fit_transform(X) = fit + transform.")
    nb.definition("PREDYKTOR (model) — estymator, który po nauczeniu PRZEWIDUJE metodą predict(X) "
                  "(np. LinearRegression, RandomForestRegressor).")
    nb.h2("1.1. Złota zasada: fit na treningu, transform na teście")
    nb.p("To najważniejsza reguła higieny danych. Parametry przekształceń (mediany, średnie, listy "
         "kategorii) wyliczamy WYŁĄCZNIE z danych treningowych. Zbiór testowy tylko przekształcamy "
         "tymi samymi parametrami. Naruszenie tej zasady to „przeciek danych\" (data leakage) — "
         "model widzi informacje z testu i jego ocena staje się zawyżona, nieuczciwa.")
    nb.code(
"transformator.fit(X_train)            # NAUKA parametrów tylko na treningu\n"
"X_train_t = transformator.transform(X_train)   # przekształć trening\n"
"X_test_t  = transformator.transform(X_test)    # przekształć test TYMI SAMYMI parametrami\n"
"\n"
"# Skrót dla treningu (fit + transform naraz):\n"
"X_train_t = transformator.fit_transform(X_train)\n"
"# Dla testu NIGDY fit_transform — tylko transform!\n",
        caption="Schemat poprawnego użycia każdego transformatora w sklearn.")

    # ================================================================
    nb.h1("SimpleImputer — uzupełnianie braków danych", 2)
    nb.p("SimpleImputer zastępuje brakujące wartości (NaN) wartością wyliczoną z kolumny. W projekcie "
         "housing rozwiązuje problem 207 braków w total_bedrooms. Modele sklearn nie potrafią uczyć "
         "się z brakami — trzeba je uzupełnić albo usunąć; imputacja zwykle jest lepsza niż usuwanie wierszy.")
    nb.h2("2.1. Strategie uzupełniania")
    nb.table(["strategy", "Czym wypełnia braki", "Kiedy używać"],
             [["'median'", "medianą kolumny", "dane liczbowe; ODPORNA na wartości odstające (użyta w housing)"],
              ["'mean'", "średnią kolumny", "dane liczbowe o rozkładzie zbliżonym do symetrycznego"],
              ["'most_frequent'", "najczęstszą wartością", "dane kategoryczne lub liczbowe"],
              ["'constant'", "stałą (parametr fill_value)", "gdy chcemy własną wartość zastępczą"]],
             widths=[3.2*nb.cm, 5.4*nb.cm, 8.0*nb.cm])
    nb.note("W projekcie wybrano medianę, bo dane o nieruchomościach bywają mocno skośne (kilka "
            "ogromnych dzielnic). Mediana nie daje się zaburzyć takim wartościom odstającym, w "
            "przeciwieństwie do średniej.")
    nb.h2("2.2. Jak działa krok po kroku")
    nb.code(
"import numpy as np\n"
"from sklearn.impute import SimpleImputer\n"
"\n"
"imputer = SimpleImputer(strategy=\"median\")   # 1. utwórz imputer (strategia: mediana)\n"
"\n"
"# 2. fit -> policz medianę KAŻDEJ kolumny i zapamiętaj w atrybucie statistics_\n"
"imputer.fit(housing_num)                      # housing_num = tylko kolumny liczbowe\n"
"print(imputer.statistics_)                    # wyliczone mediany wszystkich kolumn\n"
"\n"
"# 3. transform -> wstaw zapamiętane mediany w miejsca NaN; zwraca tablicę NumPy\n"
"X = imputer.transform(housing_num)\n",
        caption="SimpleImputer: fit liczy mediany, transform je wstawia.")
    nb.note("imputer.fit liczy mediany na DANYCH TRENINGOWYCH i przechowuje je w statistics_. Na "
            "zbiorze testowym wywołujemy tylko transform — braki w teście wypełni medianą z TRENINGU. "
            "To gwarantuje brak przecieku danych.")
    nb.p("W projekcie housing SimpleImputer jest drugim krokiem potoku liczbowego — działa "
         "automatycznie na każdej kolumnie liczbowej, zanim dane trafią do skalera i modelu.")

    # ================================================================
    nb.h1("StandardScaler — standaryzacja cech", 3)
    nb.p("StandardScaler sprowadza każdą cechę do tej samej skali: <b>średnia 0, odchylenie "
         "standardowe 1</b>. To kluczowe, gdy cechy mają różne jednostki/rzędy wielkości "
         "(np. dochód w dziesiątkach tysięcy vs. wiek w dziesiątkach).")
    nb.h2("3.1. Wzór i intuicja")
    nb.formula("z = (x − μ) / σ      (μ = średnia cechy, σ = odchylenie standardowe)")
    nb.p("Od każdej wartości odejmujemy średnią cechy (centrowanie wokół zera), a wynik dzielimy "
         "przez odchylenie standardowe (ujednolicenie rozrzutu). Po tej operacji wszystkie cechy są "
         "„równe szansami\" — żadna nie dominuje tylko dlatego, że ma większe liczby.")
    nb.h2("3.2. Po co standaryzować")
    nb.bullets([
        "Algorytmy liczące ODLEGŁOŚCI (K-Means, KNN) bez skalowania kierują się głównie cechą o największych wartościach.",
        "Metody gradientowe (regresja logistyczna, sieci, SGD) zbiegają SZYBCIEJ i stabilniej na danych wystandaryzowanych.",
        "Regularyzacja (Ridge/Lasso) karze wagi sprawiedliwie tylko wtedy, gdy cechy są w tej samej skali.",
    ])
    nb.h2("3.3. Działanie krok po kroku (przykład z wykładu)")
    nb.code(
"import numpy as np\n"
"from sklearn.preprocessing import StandardScaler\n"
"\n"
"data = np.array([[160], [170], [180], [190]])   # np. wzrost w cm\n"
"\n"
"scaler = StandardScaler()\n"
"scaler.fit(data)                  # fit: policz średnią i wariancję kolumny\n"
"print(scaler.mean_[0])            # 175.0  -> zapamiętana średnia\n"
"print(scaler.var_[0])             # 125.0  -> zapamiętana wariancja\n"
"\n"
"scaled = scaler.transform(data)   # transform: z = (x - 175) / sqrt(125)\n"
"print(scaled.ravel())             # [-1.34, -0.45, 0.45, 1.34] -> średnia 0, std 1\n",
        caption="StandardScaler: fit zapamiętuje mean_ i var_, transform standaryzuje.",
        out="175.0\n125.0\n[-1.34164079 -0.4472136  0.4472136  1.34164079]")
    nb.note("Standaryzacja NIE zmienia kształtu rozkładu (nie czyni go „dzwonowym\") — jedynie "
            "przesuwa go do średniej 0 i skaluje do odchylenia 1. Wartości odstające pozostają "
            "odstające, choć w nowej skali.")
    nb.note("StandardScaler vs MinMaxScaler: Standard centruje wokół 0 (zakres nieograniczony), "
            "MinMax ściska liniowo do przedziału [0, 1] wzorem (x−min)/(max−min). W projekcie "
            "housing użyto StandardScaler jako ostatniego kroku potoku liczbowego.")

    # ================================================================
    nb.h1("OneHotEncoder — kodowanie zmiennych kategorycznych", 4)
    nb.p("Modele ML operują na liczbach, a kolumna ocean_proximity zawiera tekst (<1H OCEAN, INLAND, "
         "ISLAND, NEAR BAY, NEAR OCEAN). OneHotEncoder zamienia każdą kategorię na osobną kolumnę "
         "0/1 (tzw. kodowanie „gorącojedynkowe\").")
    nb.h2("4.1. Na czym polega kodowanie one-hot")
    nb.p("Dla k kategorii powstaje k kolumn. W danym wierszu kolumna odpowiadająca jego kategorii ma "
         "1, a wszystkie pozostałe 0 — stąd „one hot\" (jedna gorąca jedynka). Przykład:")
    nb.table(["ocean_proximity", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN", "<1H OCEAN"],
             [["INLAND", "1", "0", "0", "0", "0"],
              ["NEAR BAY", "0", "0", "1", "0", "0"],
              ["<1H OCEAN", "0", "0", "0", "0", "1"]],
             widths=[3.4*nb.cm, 2.0*nb.cm, 2.0*nb.cm, 2.3*nb.cm, 2.5*nb.cm, 2.4*nb.cm])
    nb.h2("4.2. Dlaczego nie zwykłe liczby 0,1,2,3,4")
    nb.p("Kuszące jest ponumerowanie kategorii (INLAND=0, ISLAND=1, ...). To jednak BŁĄD: model "
         "uznałby wtedy, że istnieje porządek i odległości — np. że ISLAND (1) jest „bliżej\" INLAND "
         "(0) niż NEAR OCEAN (4), albo że NEAR OCEAN jest „4 razy większe\". Kategorie nieuporządkowane "
         "nie mają takich relacji. One-hot temu zapobiega: każda kategoria jest niezależną, równorzędną kolumną.")
    nb.h2("4.3. Działanie krok po kroku")
    nb.code(
"from sklearn.preprocessing import OneHotEncoder\n"
"import numpy as np\n"
"\n"
"cat = np.array([[\"INLAND\"], [\"NEAR BAY\"], [\"<1H OCEAN\"], [\"INLAND\"]])\n"
"\n"
"encoder = OneHotEncoder()\n"
"# fit -> wykryj i zapamiętaj listę unikalnych kategorii (atrybut categories_)\n"
"# transform -> zamień każdy wiersz na wektor 0/1\n"
"onehot = encoder.fit_transform(cat)\n"
"\n"
"print(encoder.categories_)        # [array(['<1H OCEAN','INLAND','NEAR BAY'])]\n"
"print(onehot.toarray())           # macierz 0/1 (patrz niżej)\n",
        caption="OneHotEncoder: fit poznaje kategorie, transform tworzy kolumny 0/1.",
        out="[array(['<1H OCEAN', 'INLAND', 'NEAR BAY'], dtype=object)]\n"
            "[[0. 1. 0.]\n [0. 0. 1.]\n [1. 0. 0.]\n [0. 1. 0.]]")
    nb.note("OneHotEncoder domyślnie zwraca MACIERZ RZADKĄ (sparse) — oszczędną strukturę "
            "przechowującą tylko jedynki (bo zer jest mnóstwo). Metoda .toarray() zamienia ją na "
            "zwykłą, gęstą tablicę NumPy. W potoku sklearn radzi sobie z formatem rzadkim sam.")
    nb.note("Gdy w zbiorze testowym pojawi się kategoria niewidziana podczas fit, domyślnie wystąpi "
            "błąd. Można to obejść parametrem handle_unknown='ignore', który zakoduje nieznaną "
            "kategorię jako same zera.")
    nb.h2("4.4. Alternatywy spotykane w repozytorium")
    nb.p("W starszym notatniku analizy zamiast OneHotEncoder użyto LabelBinarizer opakowanego we "
         "własną klasę MyLabelBinarizer. Efekt jest podobny (kolumny 0/1), ale LabelBinarizer "
         "powstał z myślą o ETYKIETACH (y), nie cechach (X), i jego API gorzej pasuje do potoków — "
         "dlatego nowszy notatnik słusznie przechodzi na OneHotEncoder. Istnieje też LabelEncoder, "
         "który nadaje kategoriom liczby 0,1,2,... — ale jego do cech nieuporządkowanych NIE należy "
         "używać z powodów z punktu 4.2.")

    # ================================================================
    nb.h1("Pipeline i ColumnTransformer — łączenie kroków", 5)
    nb.h2("5.1. Pipeline — łańcuch przekształceń")
    nb.definition("Pipeline łączy kilka transformatorów (i opcjonalnie model na końcu) w jeden obiekt. "
                  "Wywołanie fit/transform na potoku uruchamia kroki PO KOLEI: wyjście jednego jest "
                  "wejściem następnego. Dzięki temu cały preprocessing to jedno wywołanie, identyczne "
                  "na treningu i teście — koniec z ręcznym powtarzaniem operacji.")
    nb.code(
"from sklearn.pipeline import Pipeline\n"
"from sklearn.impute import SimpleImputer\n"
"from sklearn.preprocessing import StandardScaler\n"
"\n"
"# Lista par (nazwa_kroku, obiekt). Kroki wykonują się w podanej kolejności:\n"
"num_pipeline = Pipeline([\n"
"    ('imputer', SimpleImputer(strategy=\"median\")),  # 1. uzupełnij braki medianą\n"
"    ('attribs_adder', CombinedAttributesAdder()),   # 2. dodaj cechy pochodne\n"
"    ('std_scaler', StandardScaler()),               # 3. standaryzuj wynik\n"
"])\n"
"\n"
"# fit_transform: każdy krok uczy się i przekształca, wynik wędruje dalej\n"
"X_num = num_pipeline.fit_transform(housing_num)\n",
        caption="Pipeline — trzy przekształcenia w jednym łańcuchu.")
    nb.note("Nazwy kroków ('imputer', 'std_scaler'...) są ważne: pozwalają adresować parametry przy "
            "strojeniu, np. 'std_scaler__with_mean'. Wszystkie kroki POZA ostatnim muszą być "
            "transformatorami; ostatni może być modelem (wtedy potok ma też metodę predict).")
    nb.h2("5.2. ColumnTransformer — różne kolumny, różne potoki")
    nb.definition("ColumnTransformer pozwala zastosować RÓŻNE przekształcenia do RÓŻNYCH kolumn w "
                  "jednym kroku: kolumny liczbowe przepuszcza przez potok liczbowy, a tekstowe przez "
                  "kategoryczny, po czym SKLEJA wyniki w jedną tablicę. To dziś standardowy sposób "
                  "przygotowania danych mieszanych (liczby + tekst).")
    nb.code(
"from sklearn.compose import ColumnTransformer\n"
"\n"
"num_attribs = ['longitude','latitude','housing_median_age','total_rooms',\n"
"               'total_bedrooms','population','households','median_income']\n"
"cat_attribs = [\"ocean_proximity\"]\n"
"\n"
"# Każda krotka: (nazwa, transformator, lista_kolumn)\n"
"full_pipeline = ColumnTransformer([\n"
"    (\"num\", num_pipeline, num_attribs),       # te kolumny -> potok liczbowy\n"
"    (\"cat\", OneHotEncoder(), cat_attribs),    # ta kolumna -> kodowanie one-hot\n"
"])\n"
"\n"
"housing_prepared = full_pipeline.fit_transform(housing)   # jedno wywołanie = całe przygotowanie\n",
        caption="ColumnTransformer kieruje kolumny do właściwych przekształceń i scala wyniki.")
    nb.table(["Narzędzie", "Rola"],
             [["Pipeline", "łączy kroki SZEREGOWO (jeden po drugim, na tych samych danych)"],
              ["ColumnTransformer", "kieruje RÓŻNE kolumny do różnych potoków i scala wyniki obok siebie"],
              ["FeatureUnion", "uruchamia kilka potoków RÓWNOLEGLE na tych samych danych i scala wyniki (starszy odpowiednik)"]],
             widths=[4.0*nb.cm, 12.6*nb.cm])

    # ================================================================
    nb.h1("Modele, metryki i walidacja — szybkie podsumowanie API", 6)
    nb.h2("6.1. Modele regresji użyte w projekcie")
    nb.table(["Model", "Zasada działania", "Wynik w projekcie"],
             [["LinearRegression", "dopasowuje prostą/hiperpłaszczyznę (minimum sumy kwadratów)", "niedouczony (~69k)"],
              ["DecisionTreeRegressor", "drzewo pytań tak/nie dzielące dane na obszary", "przeuczony (~71k)"],
              ["RandomForestRegressor", "średnia z wielu losowych drzew (ensemble)", "najlepszy (~50k)"]],
             widths=[4.6*nb.cm, 8.2*nb.cm, 3.8*nb.cm])
    nb.h2("6.2. Metryki i walidacja")
    nb.code(
"from sklearn.metrics import mean_squared_error\n"
"import numpy as np\n"
"\n"
"mse  = mean_squared_error(y_true, y_pred)   # średni kwadrat błędu\n"
"rmse = np.sqrt(mse)                          # RMSE = pierwiastek (w jednostce ceny, czytelny)\n"
"\n"
"from sklearn.model_selection import cross_val_score\n"
"# 10-krotna walidacja; minus, bo scoring zwraca UJEMNE MSE\n"
"scores = cross_val_score(model, X, y, scoring=\"neg_mean_squared_error\", cv=10)\n"
"rmse_scores = np.sqrt(-scores)              # 10 wartości RMSE -> średnia = ocena modelu\n",
        caption="Najczęstsze metryki i walidacja krzyżowa w projekcie regresji.")
    nb.h2("6.3. Najważniejsze metody każdego obiektu sklearn — ściąga")
    nb.table(["Metoda", "Co robi", "Na czym"],
             [[".fit(X, y)", "uczy estymator (model lub transformator)", "zbiór treningowy"],
              [".transform(X)", "przekształca dane wg nauczonych parametrów", "trening i test"],
              [".fit_transform(X)", "fit + transform w jednym (skrót)", "tylko trening"],
              [".predict(X)", "zwraca przewidywania modelu", "dowolne nowe dane"],
              [".score(X, y)", "domyślna miara jakości modelu", "ocena modelu"]],
             widths=[3.4*nb.cm, 8.6*nb.cm, 4.6*nb.cm])
    nb.note("Cały projekt housing to powtarzanie tego samego wzorca: utwórz obiekt → fit na treningu "
            "→ transform/predict. Jeśli zapamiętasz parę fit/transform oraz zasadę „test tylko "
            "transform\", rozumiesz 90% mechaniki scikit-learn.")
