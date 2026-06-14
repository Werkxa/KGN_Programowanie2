# -*- coding: utf-8 -*-
"""Treść sekcji 4-7."""

def build(api):
    h1, h2, h3, p, bullets, code, formula, note, table, spacer, rule = (
        api["h1"], api["h2"], api["h3"], api["p"], api["bullets"], api["code"],
        api["formula"], api["note"], api["table"], api["spacer"], api["rule"])
    cm = api["cm"]

    # ====================================================================
    # 4. KSZTAŁT ndarray
    # ====================================================================
    h1("NumPy: kształt obiektu ndarray i jego zmiana", 4)
    p("NumPy to fundament obliczeń numerycznych w Pythonie. Jego główny typ to <b>ndarray</b> "
      "(N-wymiarowa tablica) — siatka elementów <b>tego samego typu</b>, ułożona w ciągłym bloku "
      "pamięci. Dzięki temu operacje na całych tablicach są bardzo szybkie. „Kształt\" (shape) opisuje, "
      "ile elementów ma tablica w każdym wymiarze.")

    h2("4.1. Jak sprawdzić kształt tablicy")
    code(
"import numpy as np\n"
"x = np.arange(0, 12)          # wektor 0,1,2,...,11 (12 elementów)\n"
"x = x.reshape(3, 4)           # przekształć na 3 wiersze i 4 kolumny\n"
"\n"
"x.shape    # (3, 4)  -> krotka: (liczba_wierszy, liczba_kolumn)\n"
"x.ndim     # 2       -> liczba wymiarów (osi)\n"
"x.size     # 12      -> łączna liczba elementów (3*4)\n"
"x.dtype    # dtype('int64') -> typ przechowywanych liczb\n",
        caption="Atrybuty opisujące tablicę: shape, ndim, size, dtype.")
    note("shape to zawsze KROTKA. Dla wektora (1D) ma jeden element, np. (12,) — przecinek "
         "odróżnia krotkę jednoelementową od zwykłego nawiasu.")

    h2("4.2. Jak zmienić kształt tablicy")
    p("Służy do tego metoda .reshape(). Warunek: iloczyn nowych wymiarów musi równać się liczbie "
      "elementów (size). Przykład z repozytorium (P2Lab04_NumPy):")
    code(
"x = np.arange(0, 12).reshape(3, 4)   # 12 liczb -> 3 x 4\n"
"x.reshape(2, 6)                      # te same 12 liczb -> 2 x 6\n"
"\n"
"# -1 oznacza: 'policz ten wymiar sam'. Tu: 12/4 = 3 wiersze.\n"
"x.reshape(-1, 4)\n"
"\n"
"x.ravel()      # spłaszcza do 1D (wektor 12-elementowy)\n"
"x.T            # transpozycja: zamienia wiersze z kolumnami (kształt 4 x 3)\n",
        caption="reshape, użycie -1, spłaszczanie i transpozycja.")
    note("reshape zwykle zwraca WIDOK (referencję) tych samych danych, a nie kopię — patrz sekcja 6.")

    # ====================================================================
    # 5. broadcasting, wektoryzacja, axis
    # ====================================================================
    h1("NumPy: broadcasting, wektoryzacja, wydajność, axis", 5)

    h2("5.1. Broadcasting (rozgłaszanie)")
    p("Broadcasting to mechanizm pozwalający wykonywać operacje na tablicach o RÓŻNYCH kształtach "
      "bez ręcznego ich powielania. NumPy „rozciąga\" mniejszą tablicę wzdłuż brakującego wymiaru, "
      "tak jakby ją skopiował — ale bez faktycznego zużywania pamięci. Reguła: wymiary porównuje się "
      "od prawej; pasują, gdy są równe albo jeden z nich wynosi 1.")
    code(
"import numpy as np\n"
"x = np.array([[2, 3],\n"
"              [4, 5]])      # kształt (2, 2)\n"
"y = np.array([1, 2])        # kształt (2,)\n"
"\n"
"# y jest 'rozgłaszane' na każdy wiersz x: do każdego wiersza dodaje [1, 2]\n"
"y + x\n"
"# wynik:\n"
"# [[3, 5],\n"
"#  [5, 7]]\n",
        caption="Broadcasting wektora na macierz (przykład z P2Lab04).")
    code(
"# Klasyczny przykład: skalar rozgłasza się na całą tablicę\n"
"a = np.array([10, 20, 30])\n"
"a * 2          # [20, 40, 60]  -> 2 'rozciąga się' na każdy element\n"
"a + 100        # [110, 120, 130]\n",
        caption="Skalar jako najprostszy przypadek broadcastingu.")

    h2("5.2. Wektoryzacja")
    p("Wektoryzacja to wykonywanie operacji na <b>całej tablicy naraz</b>, jedną instrukcją, zamiast "
      "pisać pętlę po elementach. Kod jest krótszy i wielokrotnie szybszy, bo właściwa pętla wykonuje "
      "się w skompilowanym C wewnątrz NumPy, a nie w wolnym Pythonie.")
    code(
"import numpy as np\n"
"x = np.arange(1_000_000)\n"
"\n"
"# Podejście NIEzwektoryzowane (wolne) — pętla w Pythonie:\n"
"# wynik = [v**2 for v in x]\n"
"\n"
"# Podejście ZWEKTORYZOWANE (szybkie) — jedna operacja na całej tablicy:\n"
"wynik = x ** 2\n",
        caption="Ta sama operacja: pętla kontra wersja zwektoryzowana.")
    p("Normalizacja min-max z repozytorium to także wektoryzacja — odejmowanie i dzielenie dzieją "
      "się na całym wektorze jednocześnie:")
    code(
"v = np.array([10, 20, 30, 40, 50])\n"
"v_norm = (v - v.min()) / (v.max() - v.min())   # cała operacja na raz\n"
"# v_norm = [0., 0.25, 0.5, 0.75, 1.]\n",
        caption="Wektorowa normalizacja min-max (P2Lab04_NumPy.ipynb).")

    h2("5.3. Dlaczego obliczenia w NumPy są wydajne")
    bullets([
        "Ciągła pamięć — elementy leżą obok siebie w jednym bloku, więc procesor czyta je bardzo szybko (lepsze użycie pamięci podręcznej).",
        "Jednolity typ (dtype) — brak narzutu Pythonowych obiektów na każdą liczbę; tablica miliona int64 to po prostu 8 MB liczb.",
        "Pętle w C — operacje wykonują wstępnie skompilowane funkcje w języku C/Fortran, bez interpretera Pythona.",
        "Wektoryzacja sprzętowa (SIMD) — procesor potrafi przetwarzać kilka liczb jedną instrukcją.",
        "Brak kopiowania przy broadcastingu — oszczędność pamięci i czasu.",
    ])

    h2("5.4. np.vectorize(math.sin)(x) kontra np.sin(x)")
    p("To pytanie sprawdza, czy rozumiemy różnicę między <b>prawdziwą</b> wektoryzacją a jedynie "
      "wygodnym „opakowaniem\" pętli:")
    bullets([
        "np.sin(x) — funkcja UNIWERSALNA (ufunc) napisana w C; działa na całej tablicy naprawdę równolegle, jest szybka.",
        "np.vectorize(math.sin)(x) — to tylko PĘTLA Pythona w przebraniu: dla każdego elementu wywołuje zwykłą math.sin. Daje ten sam WYNIK, ale jest znacznie wolniejsza (NumPy sam ostrzega, że to udogodnienie składniowe, a nie optymalizacja).",
    ])
    code(
"import numpy as np, math\n"
"x = np.linspace(0, math.pi, 5)\n"
"\n"
"np.sin(x)                       # ufunc w C — szybkie, prawdziwa wektoryzacja\n"
"np.vectorize(math.sin)(x)       # pętla po elementach — ten sam wynik, ale wolno\n"
"# Wniosek: WYNIK identyczny, WYDAJNOŚĆ dramatycznie różna na rzecz np.sin.\n",
        caption="Prawdziwa ufunc vs. opakowana pętla.")

    h2("5.5. Czym są osie (axis) i jak zmienia się wymiar")
    p("Oś (axis) to numer wymiaru, WZDŁUŻ którego wykonujemy operację. W tablicy 2D: axis=0 biegnie "
      "w dół (po wierszach → wynik na kolumnę), axis=1 biegnie w bok (po kolumnach → wynik na wiersz). "
      "Po agregacji (sum, mean...) wskazana oś <b>znika</b> z kształtu.")
    code(
"import numpy as np\n"
"x = np.random.randint(1, 100, 25).reshape(5, 5)   # macierz 5 x 5\n"
"\n"
"np.mean(x, axis=0)   # średnia w każdej KOLUMNIE (oś 0 znika -> wynik (5,))\n"
"np.sum(x, axis=1)    # suma w każdym WIERSZU   (oś 1 znika -> wynik (5,))\n"
"np.sum(x)            # bez axis: jedna liczba — suma wszystkich elementów\n",
        caption="Działanie axis na macierzy 5x5 (przykład z P2Lab04).")
    p("Reguła ogólna: dla tablicy o kształcie (2, 3, 4) wywołanie np.fun(x, axis=i) USUWA i-ty wymiar:")
    table(["Wywołanie", "Co znika", "Kształt wyniku"],
          [["np.fun(x, axis=0)", "wymiar 0 (rozmiar 2)", "(3, 4)"],
           ["np.fun(x, axis=1)", "wymiar 1 (rozmiar 3)", "(2, 4)"],
           ["np.fun(x, axis=2)", "wymiar 2 (rozmiar 4)", "(2, 3)"]],
          widths=[5.0*cm, 6.0*cm, 5.6*cm])
    note("Jeśli dodamy keepdims=True, oś nie znika, lecz kurczy się do rozmiaru 1 (np. (2,3,4) -> "
         "(1,3,4) dla axis=0) — przydatne, by wynik dało się rozgłosić z powrotem na oryginał.")

    # ====================================================================
    # 6. REFERENCJE vs KOPIE
    # ====================================================================
    h1("NumPy: referencje (widoki) kontra kopie", 6)
    p("Kluczowe dla unikania trudnych błędów: niektóre operacje zwracają <b>widok</b> (referencję do "
      "tych samych danych w pamięci), a inne <b>kopię</b> (nowy, niezależny blok pamięci). Zmiana "
      "widoku zmienia oryginał; zmiana kopii — nie.")

    h2("6.1. Na czym polega różnica")
    bullets([
        "Widok (view) — nowa „etykieta\" na te same dane. Modyfikacja przez widok zmienia tablicę źródłową. Oszczędza pamięć i czas.",
        "Kopia (copy) — całkowicie niezależny duplikat danych. Modyfikacja kopii NIE wpływa na oryginał.",
    ])
    code(
"import numpy as np\n"
"x = np.arange(6)            # [0 1 2 3 4 5]\n"
"\n"
"# WYCINEK (slicing) zwraca WIDOK:\n"
"w = x[1:4]                  # widok na elementy [1 2 3]\n"
"w[0] = 999                  # zmieniamy widok...\n"
"print(x)                    # [0 999 2 3 4 5]  -> ORYGINAŁ też się zmienił!\n"
"\n"
"# Jawna KOPIA jest niezależna:\n"
"k = x[1:4].copy()\n"
"k[0] = -1                   # zmiana kopii...\n"
"print(x)                    # [0 999 2 3 4 5]  -> oryginał bez zmian\n",
        caption="Wycinek to widok; .copy() tworzy niezależny duplikat.")
    note("Możesz sprawdzić, czy obiekt jest widokiem: atrybut w.base wskazuje na tablicę źródłową "
         "(dla kopii base jest None).")

    h2("6.2. Które operacje dają widok, a które kopię")
    table(["Zwracają WIDOK (referencję)", "Zwracają KOPIĘ"],
          [["proste wycinki, np. x[1:4], x[:, 0]", "indeksowanie listą / tablicą indeksów (fancy indexing): x[[0,2,4]]"],
           ["reshape (gdy się da bez przenoszenia danych)", "indeksowanie logiczne (maska): x[x > 5]"],
           ["transpozycja x.T, ravel() (zwykle)", "jawne .copy(), np.array(x), flatten()"],
           ["zmiana kształtu przez x.shape = (...)", "operacje arytmetyczne: x + 1, x * 2 (tworzą nową tablicę)"]],
          widths=[8.3*cm, 8.3*cm])
    note("Dobra praktyka: jeśli zamierzasz modyfikować fragment, a nie chcesz ruszać oryginału — "
         "wykonaj jawnie .copy(). Operacje arytmetyczne i tak zwracają nową tablicę, więc x = x + 1 "
         "jest bezpieczne, ale x[mask] = 0 modyfikuje w miejscu.")

    # ====================================================================
    # 7. CZYSZCZENIE I STANDARYZACJA DANYCH
    # ====================================================================
    h1("Czyszczenie i standaryzacja danych", 7)

    h2("7.1. Co to jest czyszczenie danych")
    p("Czyszczenie danych (data cleaning) to przygotowanie surowych danych do analizy i modelowania: "
      "naprawienie lub usunięcie błędów, braków i niespójności. Zasada „garbage in, garbage out\" "
      "mówi, że nawet najlepszy model nauczy się bzdur, jeśli nakarmimy go złymi danymi. W praktyce "
      "to często najbardziej czasochłonny etap pracy z danymi.")

    h2("7.2. Typowe operacje czyszczenia danych")
    bullets([
        "Obsługa braków (NaN/NULL) — usunięcie wierszy/kolumn (dropna) albo wypełnienie wartością (fillna): średnią, medianą, najczęstszą wartością.",
        "Usuwanie duplikatów — powtórzone wiersze (drop_duplicates).",
        "Poprawa typów — np. tekst '12' zamieniany na liczbę, daty parsowane do typu datetime.",
        "Ujednolicanie kategorii — 'TAK', 'tak', 'Tak' sprowadzane do jednej formy.",
        "Obsługa wartości odstających (outliers) — wykrywanie i ewentualne przycinanie skrajnych wartości.",
        "Kodowanie zmiennych kategorycznych — np. one-hot encoding (tekst -> kolumny 0/1).",
        "Skalowanie/standaryzacja cech liczbowych (patrz niżej).",
    ])
    code(
"import pandas as pd, numpy as np\n"
"\n"
"df.isnull().sum()                       # ile braków w każdej kolumnie\n"
"df = df.drop_duplicates()               # usuń powtórzone wiersze\n"
"df = df.dropna(subset=['dochód'])       # usuń wiersze bez dochodu\n"
"\n"
"# Wypełnij braki MEDIANĄ kolumny (odporna na wartości odstające):\n"
"df['wiek'] = df['wiek'].fillna(df['wiek'].median())\n",
        caption="Typowe operacje czyszczące w pandas.")
    p("W scikit-learn braki uzupełnia się estymatorem SimpleImputer, co pozwala wpiąć tę operację "
      "w spójny potok (pipeline):")
    code(
"from sklearn.impute import SimpleImputer\n"
"# strategy='median' -> brakujące wartości zastępuje medianą każdej kolumny\n"
"imputer = SimpleImputer(strategy='median')\n"
"imputer.fit(dane_liczbowe)              # policz mediany (uczenie na danych)\n"
"X = imputer.transform(dane_liczbowe)    # zastąp braki wyliczonymi medianami\n",
        caption="Uzupełnianie braków estymatorem SimpleImputer (jak w P2Lab09_housing).")

    h2("7.3. Standaryzacja danych — na czym polega i po co")
    p("Standaryzacja przekształca każdą cechę tak, aby miała <b>średnią 0</b> i <b>odchylenie "
      "standardowe 1</b>. Dla wartości x odejmujemy średnią μ i dzielimy przez odchylenie σ:")
    formula("z = (x − μ) / σ")
    p("Po co to robimy? Bo wiele algorytmów porównuje cechy „po równo\". Jeśli jedna cecha to dochód "
      "(rzędu tysięcy), a druga to wiek (rzędu dziesiątek), to bez skalowania dochód zdominuje "
      "obliczenia odległości i gradientów. Standaryzacja wyrównuje wpływ cech i przyspiesza zbieżność "
      "(perceptron, Adaline, regresja logistyczna, sieci, K-Means — wszystkie tego wymagają).")
    code(
"import numpy as np\n"
"from sklearn.preprocessing import StandardScaler\n"
"\n"
"data = np.array([[160], [170], [180], [190]])   # np. wzrost w cm\n"
"\n"
"scaler = StandardScaler()       # estymator standaryzacji\n"
"scaler.fit(data)                # ETAP UCZENIA: policz średnią i wariancję\n"
"print(scaler.mean_[0])          # wyestymowana średnia = 175.0\n"
"print(scaler.var_[0])           # wyestymowana wariancja\n"
"\n"
"scaled = scaler.transform(data) # ETAP STOSOWANIA: przelicz na z = (x-mean)/std\n"
"print(scaled)                   # wartości wokół zera, odchylenie 1\n",
        caption="Standaryzacja estymatorem StandardScaler (P2W10_Klasyfikacje_scikit_learn.ipynb).")
    note("Najważniejsza zasada poprawności: scaler UCZYMY (fit) wyłącznie na zbiorze TRENINGOWYM, a "
         "potem TYLKO przekształcamy (transform) zbiór testowy tymi samymi parametrami. Inaczej "
         "dojdzie do „przecieku\" informacji z testu do treningu. W repozytorium widać to wzorcowo: "
         "sc.fit_transform(X_train) oraz sc.transform(X_test).")
    code(
"sc = StandardScaler()\n"
"X_train_std = sc.fit_transform(X_train)   # ucz na treningu I przekształć trening\n"
"X_test_std  = sc.transform(X_test)        # test TYLKO przekształć (bez fit!)\n",
        caption="Poprawna kolejność: fit na treningu, transform na teście.")
