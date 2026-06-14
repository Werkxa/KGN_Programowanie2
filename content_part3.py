# -*- coding: utf-8 -*-
"""Treść sekcji 8-14."""

def build(api):
    h1, h2, h3, p, bullets, code, formula, note, table, spacer, rule = (
        api["h1"], api["h2"], api["h3"], api["p"], api["bullets"], api["code"],
        api["formula"], api["note"], api["table"], api["spacer"], api["rule"])
    cm = api["cm"]

    # ====================================================================
    # 8. KLASYFIKACJA I REGRESJA
    # ====================================================================
    h1("Klasyfikacja i regresja w scikit-learn", 8)
    p("scikit-learn (sklearn) to biblioteka uczenia maszynowego. Każdy model ma ten sam, prosty "
      "interfejs: tworzymy estymator, uczymy go metodą <b>.fit(X, y)</b>, a potem przewidujemy "
      "metodą <b>.predict(X)</b>. X to macierz cech (wiersze = przykłady, kolumny = cechy), y to "
      "wektor odpowiedzi.")

    h2("8.1. Na czym polega problem klasyfikacji")
    p("Klasyfikacja to przewidywanie <b>etykiety/kategorii</b> (wartości dyskretnej): np. czy mail to "
      "spam (tak/nie), albo który z trzech gatunków irysa. Model uczy się granicy decyzyjnej "
      "rozdzielającej klasy na podstawie cech. Gdy klas są dwie — to klasyfikacja binarna, gdy "
      "więcej — wieloklasowa.")

    h2("8.2. Metody klasyfikacji w sklearn")
    table(["Metoda (klasa)", "Krótki opis"],
          [["Perceptron", "Najprostszy klasyfikator liniowy; szuka prostej/hiperpłaszczyzny rozdzielającej klasy."],
           ["LogisticRegression", "Regresja logistyczna — zwraca prawdopodobieństwo przynależności do klasy."],
           ["SGDClassifier", "Klasyfikatory liniowe uczone spadkiem gradientu (z loss='squared_error' działa jak Adaline)."],
           ["KNeighborsClassifier", "k najbliższych sąsiadów — klasa wybierana głosami najbliższych przykładów."],
           ["SVC (SVM)", "Maszyna wektorów nośnych — szuka marginesu maksymalnie oddzielającego klasy."],
           ["DecisionTreeClassifier", "Drzewo decyzyjne — ciąg pytań tak/nie na cechach."],
           ["RandomForestClassifier", "Las losowy — zespół wielu drzew, głosowanie większościowe."]],
          widths=[5.3*cm, 11.3*cm])
    p("Wzorcowy schemat klasyfikacji z repozytorium — perceptron na zbiorze irysów:")
    code(
"from sklearn import datasets\n"
"from sklearn.model_selection import train_test_split\n"
"from sklearn.preprocessing import StandardScaler\n"
"from sklearn.linear_model import Perceptron\n"
"from sklearn.metrics import accuracy_score\n"
"\n"
"iris = datasets.load_iris()           # wbudowany zbiór: 150 kwiatów, 4 cechy\n"
"X, y = iris.data, iris.target         # X = cechy, y = gatunek (0/1/2)\n"
"\n"
"# Podział 70% trening / 30% test; stratify zachowuje proporcje klas\n"
"X_train, X_test, y_train, y_test = train_test_split(\n"
"    X, y, test_size=0.3, random_state=42, stratify=y)\n"
"\n"
"sc = StandardScaler()                 # standaryzacja (perceptron jej wymaga)\n"
"X_train_std = sc.fit_transform(X_train)\n"
"X_test_std  = sc.transform(X_test)\n"
"\n"
"ppn = Perceptron(eta0=0.1, random_state=42)  # eta0 = szybkość uczenia\n"
"ppn.fit(X_train_std, y_train)         # UCZENIE modelu\n"
"y_pred = ppn.predict(X_test_std)      # PREDYKCJA na danych testowych\n"
"print('Dokładność:', accuracy_score(y_test, y_pred))  # ocena jakości\n",
        caption="Pełny przepływ klasyfikacji (P2W10_Klasyfikacje_scikit_learn.ipynb).")

    h2("8.3. Na czym polega regresja i jak ją policzyć")
    p("Regresja to przewidywanie wartości <b>ciągłej</b> (liczby), np. ceny domu czy temperatury. "
      "Model szuka funkcji najlepiej dopasowanej do danych. Regresja liniowa zakłada zależność "
      "y = w·x + b i dobiera wagę w oraz wyraz wolny b tak, by zminimalizować błąd (sumę kwadratów "
      "odchyleń). Przykład z repozytorium:")
    code(
"import numpy as np\n"
"from sklearn.linear_model import LinearRegression\n"
"\n"
"X = np.array([[1], [2], [3], [4]])    # cecha (kolumna)\n"
"y = np.array([3, 5, 7, 9])            # prawdziwa zależność: y = 2*x + 1\n"
"\n"
"model = LinearRegression()\n"
"model.fit(X, y)                       # model sam estymuje w i b\n"
"\n"
"print('waga w:', model.coef_[0])      # ~2.0\n"
"print('wyraz wolny b:', model.intercept_)  # ~1.0\n"
"print(model.predict([[10]]))          # przewidywanie dla x=10 -> ~21\n",
        caption="Regresja liniowa: model odkrywa zależność y = 2x + 1.")
    p("Dla zależności nieliniowych można rozszerzyć cechy o potęgi (regresja wielomianowa) — w "
      "repozytorium realizuje to PolynomialFeatures (plik P2Wyk11_PolyRegression_Wizualizacja.py).")

    # ====================================================================
    # 9. UCZENIE Z NADZOREM I BEZ
    # ====================================================================
    h1("Uczenie z nadzorem i bez nadzoru", 9)
    p("To dwa podstawowe paradygmaty uczenia maszynowego, różniące się tym, czy dysponujemy "
      "„poprawnymi odpowiedziami\" (etykietami y).")

    h2("9.1. Uczenie z nadzorem (supervised)")
    p("Mamy dane wejściowe X <b>oraz</b> znane prawidłowe odpowiedzi y. Model uczy się odwzorowania "
      "X → y, a potem przewiduje y dla nowych X. To jak nauka z nauczycielem, który sprawdza "
      "odpowiedzi. Dwa główne zadania:")
    bullets([
        "Klasyfikacja — odpowiedź to kategoria (gatunek irysa, spam/nie-spam). Przykłady: Perceptron, LogisticRegression, SVC, RandomForest.",
        "Regresja — odpowiedź to liczba (cena domu). Przykłady: LinearRegression, regresja wielomianowa.",
    ])

    h2("9.2. Uczenie bez nadzoru (unsupervised)")
    p("Mamy tylko dane X, <b>bez</b> etykiet. Model sam szuka ukrytej struktury — grupuje podobne "
      "przykłady albo upraszcza dane. To jak odkrywanie wzorców bez podpowiedzi. Główne zadania:")
    bullets([
        "Klasteryzacja (grupowanie) — dzielenie danych na grupy podobnych obiektów. Przykłady z repo: K-Means, DBSCAN.",
        "Redukcja wymiarów — sprowadzanie wielu cech do kilku najważniejszych, np. PCA (do wizualizacji/kompresji).",
    ])
    p("Przykład klasteryzacji K-Means z repozytorium (uwaga: NIE używamy y do uczenia):")
    code(
"from sklearn.cluster import KMeans\n"
"from sklearn.datasets import load_iris\n"
"from sklearn.preprocessing import StandardScaler\n"
"\n"
"X = load_iris().data[:, [2, 3]]          # tylko cechy, etykiety IGNORUJEMY\n"
"X_std = StandardScaler().fit_transform(X)# klasteryzacja liczy odległości\n"
"\n"
"# n_clusters=3: prosimy o 3 grupy (w praktyce dobiera się metodą łokcia)\n"
"kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\n"
"etykiety = kmeans.fit_predict(X_std)     # przypisanie każdego punktu do grupy\n",
        caption="K-Means — uczenie bez nadzoru (P2W10).")
    table(["", "Z nadzorem", "Bez nadzoru"],
          [["Dane", "X + etykiety y", "tylko X"],
           ["Cel", "przewidzieć y dla nowych X", "znaleźć strukturę/grupy"],
           ["Zadania", "klasyfikacja, regresja", "klasteryzacja, redukcja wymiarów"],
           ["Przykłady", "Perceptron, LinearRegression", "K-Means, DBSCAN, PCA"]],
          widths=[2.6*cm, 7.0*cm, 7.0*cm])

    # ====================================================================
    # 10. MIARY BŁĘDU
    # ====================================================================
    h1("Miary błędu: MSE, RMSE, MAE, accuracy, FP/FN", 10)
    p("Aby ocenić model, mierzymy, jak bardzo jego przewidywania ŷ odbiegają od prawdziwych wartości "
      "y. Inne miary stosujemy w regresji (błąd liczbowy), a inne w klasyfikacji (trafność etykiet).")

    h2("10.1. Miary błędu w regresji")
    p("Oznaczmy: yᵢ — wartość prawdziwa, ŷᵢ — przewidywana, n — liczba przykładów.")
    h3("MSE — błąd średniokwadratowy (Mean Squared Error)")
    formula("MSE = (1/n) · Σ (yᵢ − ŷᵢ)²")
    p("Średnia z KWADRATÓW błędów. Kwadrat sprawia, że duże pomyłki są karane wyjątkowo mocno "
      "(błąd 2× większy daje 4× większą karę). Wada: jednostka jest „kwadratowa\" (np. zł²), więc "
      "trudna w interpretacji.")
    h3("RMSE — pierwiastek z MSE (Root Mean Squared Error)")
    formula("RMSE = √MSE = √[ (1/n) · Σ (yᵢ − ŷᵢ)² ]")
    p("Pierwiastek przywraca pierwotną jednostkę (np. zł), więc wynik jest interpretowalny: „średnio "
      "mylimy się o tyle\". Wciąż mocno reaguje na duże błędy (jest na nie wrażliwy).")
    h3("MAE — średni błąd bezwzględny (Mean Absolute Error)")
    formula("MAE = (1/n) · Σ |yᵢ − ŷᵢ|")
    p("Średnia z WARTOŚCI BEZWZGLĘDNYCH błędów. Traktuje wszystkie błędy proporcjonalnie i jest "
      "odporna na wartości odstające (outliers nie są podnoszone do kwadratu).")
    table(["Miara", "Jednostka", "Reakcja na duże błędy", "Kiedy używać"],
          [["MSE", "kwadratowa", "bardzo silna (kara²)", "optymalizacja, gdy duże błędy są groźne"],
           ["RMSE", "oryginalna", "silna", "raportowanie wyniku w naturalnej jednostce"],
           ["MAE", "oryginalna", "umiarkowana, liniowa", "gdy w danych są wartości odstające"]],
          widths=[2.2*cm, 3.0*cm, 4.4*cm, 7.0*cm])
    p("Różnice w skrócie: RMSE ≥ MAE zawsze; im bardziej RMSE przewyższa MAE, tym więcej w danych "
      "dużych, pojedynczych błędów. MSE i RMSE „nie lubią\" outlierów, MAE jest na nie odporna.")
    code(
"from sklearn.metrics import mean_squared_error, mean_absolute_error\n"
"import numpy as np\n"
"\n"
"mse  = mean_squared_error(y_test, y_pred)      # MSE\n"
"rmse = np.sqrt(mse)                            # RMSE = pierwiastek z MSE\n"
"mae  = mean_absolute_error(y_test, y_pred)     # MAE\n"
"print(f'MSE={mse:.2f}  RMSE={rmse:.2f}  MAE={mae:.2f}')\n",
        caption="Liczenie miar błędu w sklearn.")

    h2("10.2. Dokładność (accuracy) — miara dla klasyfikacji")
    p("Dokładność to odsetek poprawnie sklasyfikowanych przykładów:")
    formula("accuracy = liczba trafnych predykcji / liczba wszystkich predykcji")
    code(
"from sklearn.metrics import accuracy_score\n"
"# Udział poprawnych odpowiedzi, np. 0.95 = 95% trafień\n"
"print(accuracy_score(y_test, y_pred))\n",
        caption="Dokładność klasyfikatora.")
    note("Dokładność bywa myląca przy niezrównoważonych klasach. Jeśli 99% maili to nie-spam, model "
         "mówiący zawsze „nie-spam\" ma 99% accuracy, a jest bezużyteczny. Dlatego patrzymy też na FP/FN.")

    h2("10.3. Błędy fałszywie pozytywny (FP) i fałszywie negatywny (FN)")
    p("W klasyfikacji binarnej (klasa „pozytywna\" = to, co wykrywamy, np. „chory\", „spam\") możliwe "
      "są cztery wyniki, zestawione w tzw. macierzy pomyłek:")
    table(["", "Prawda: POZYTYW", "Prawda: NEGATYW"],
          [["Model mówi POZYTYW", "TP — trafienie", "FP — fałszywy alarm"],
           ["Model mówi NEGATYW", "FN — przeoczenie", "TN — poprawne odrzucenie"]],
          widths=[5.0*cm, 5.8*cm, 5.8*cm])
    bullets([
        "Fałszywie pozytywny (False Positive, FP) — model TWIERDZI „pozytyw\", a naprawdę jest negatyw. Fałszywy alarm (np. zdrowy uznany za chorego, zwykły mail wpada do spamu).",
        "Fałszywie negatywny (False Negative, FN) — model TWIERDZI „negatyw\", a naprawdę jest pozytyw. Przeoczenie (np. chory uznany za zdrowego, spam przepuszczony do skrzynki).",
    ])
    p("Który błąd groźniejszy zależy od zastosowania: w diagnostyce raka FN (przeoczenie choroby) "
      "jest dużo groźniejszy niż FP. Stąd dodatkowe miary: precyzja = TP/(TP+FP) oraz czułość "
      "(recall) = TP/(TP+FN).")

    # ====================================================================
    # 11. OVERFITTING
    # ====================================================================
    h1("Przeuczenie (overfitting) i jak mu zapobiegać", 11)
    h2("11.1. Co to jest przeuczenie")
    p("Przeuczenie (overfitting) to sytuacja, w której model „nauczył się na pamięć\" danych "
      "treningowych — łącznie z ich szumem i przypadkowymi zależnościami — zamiast uchwycić ogólną "
      "regułę. Skutek: świetny wynik na treningu, ale słaby na nowych, niewidzianych danych. Model "
      "<b>nie generalizuje</b>.")
    p("Objaw rozpoznawczy: duża różnica między jakością na zbiorze treningowym (bardzo dobra) a "
      "testowym (wyraźnie gorsza). Przeciwieństwo to <b>niedouczenie</b> (underfitting) — model zbyt "
      "prosty, słaby na obu zbiorach.")
    note("Analogia: student, który wykuł na pamięć odpowiedzi do konkretnych zadań z przykładowego "
         "testu, dostanie 100% na nim, ale obleje egzamin z nowymi zadaniami.")

    h2("11.2. Jak przeciwdziałać przeuczeniu")
    bullets([
        "Więcej danych treningowych — trudniej „zapamiętać\" duży, różnorodny zbiór.",
        "Prostszy model — mniej parametrów/niższy stopień wielomianu ogranicza zdolność do dopasowania szumu.",
        "Regularyzacja — kara za zbyt duże wagi (L1/Lasso, L2/Ridge), zniechęca model do skrajnych dopasowań.",
        "Walidacja krzyżowa (cross-validation) — wielokrotny podział danych, by rzetelnie ocenić generalizację.",
        "Wczesne zatrzymanie (early stopping) — przerwanie uczenia, gdy błąd na zbiorze walidacyjnym zaczyna rosnąć.",
        "Dropout (w sieciach neuronowych) — losowe wyłączanie części neuronów podczas treningu.",
        "Augmentacja danych — sztuczne powiększanie zbioru (np. obroty, przesunięcia obrazów).",
    ])
    p("Dropout pojawia się w repozytorium (P2Wyk11_SieciNeuronowe) — losowo wyłącza np. 20% neuronów, "
      "co „rozprasza wiedzę\" sieci na więcej neuronów i zapobiega przeuczeniu:")
    code(
"from tensorflow.keras import layers, models\n"
"model = models.Sequential([\n"
"    layers.Flatten(input_shape=(28, 28)),  # spłaszcza obraz 28x28 do wektora 784\n"
"    layers.Dense(128, activation='relu'),  # warstwa ukryta 128 neuronów\n"
"    layers.Dropout(0.2),                   # losowo wyłącza 20% neuronów -> anty-overfitting\n"
"    layers.Dense(10, activation='softmax') # 10 wyjść = 10 cyfr (prawdopodobieństwa)\n"
"])\n",
        caption="Dropout jako regularyzacja w sieci dla zbioru MNIST.")

    # ====================================================================
    # 12. PODZIAŁ DANYCH
    # ====================================================================
    h1("Podział danych: zbiór treningowy i testowy", 12)
    p("Dzielimy dane na <b>treningowe</b> (model się na nich uczy) i <b>testowe</b> (sprawdzamy na "
      "nich jakość). Cel: oszacować, jak model poradzi sobie z <b>nowymi, niewidzianymi</b> danymi. "
      "Gdybyśmy oceniali model na tych samych danych, na których się uczył, nie wykrylibyśmy "
      "przeuczenia — model mógłby je po prostu pamiętać.")
    p("Typowy podział to 70–80% trening i 20–30% test. Kluczowa zasada: zbiór testowy „odkładamy na "
      "bok\" i NIE używamy go do żadnych decyzji o modelu aż do samego końca.")
    code(
"from sklearn.model_selection import train_test_split\n"
"\n"
"# test_size=0.3  -> 30% danych trafia do testu, 70% do treningu\n"
"# random_state   -> ustala losowość, by podział był POWTARZALNY\n"
"# stratify=y     -> zachowuje proporcje klas w obu zbiorach (ważne w klasyfikacji)\n"
"X_train, X_test, y_train, y_test = train_test_split(\n"
"    X, y, test_size=0.3, random_state=42, stratify=y)\n",
        caption="Podział danych funkcją train_test_split (wzorzec z repozytorium).")
    note("Czasem wydziela się jeszcze trzeci zbiór — WALIDACYJNY — do strojenia hiperparametrów. "
         "Wówczas: trening uczy wagi, walidacja wybiera ustawienia, test daje ostateczną, uczciwą ocenę.")

    # ====================================================================
    # 13. PERCEPTRON I FUNKCJE AKTYWACJI
    # ====================================================================
    h1("Perceptron i funkcje aktywacji", 13)
    h2("13.1. Jak działa perceptron")
    p("Perceptron to najprostszy model „sztucznego neuronu\" i podstawowy klasyfikator liniowy. "
      "Działa w trzech krokach:")
    bullets([
        "1. Suma ważona — mnoży każde wejście xⱼ przez wagę wⱼ i sumuje, odejmując próg θ (bias): z = w·x − θ.",
        "2. Funkcja aktywacji — przepuszcza z przez funkcję progową: wynik 1, jeśli z ≥ 0, w przeciwnym razie 0.",
        "3. Uczenie — porównuje wynik ŷ z prawdą y i koryguje wagi proporcjonalnie do błędu.",
    ])
    p("Regułę korekty wag (z wykładu) zapisujemy tak — η to współczynnik szybkości uczenia, y wartość "
      "docelowa, ŷ aktualny wynik perceptronu, xⱼ j-te wejście:")
    formula("Δwⱼ = η · (y − ŷ) · xⱼ")
    p("Jeśli perceptron trafił (y = ŷ), poprawka jest zerowa. Jeśli się pomylił, wagi przesuwają się "
      "w stronę zmniejszającą błąd. Implementacja z repozytorium (P2Wyk11_SieciNeuronowe):")
    code(
"import numpy as np\n"
"class Perceptron(object):\n"
"    def __init__(self, input_size, lr=0.2, epochs=4):\n"
"        self.W = np.array([0.3, -0.2])              # początkowe wagi\n"
"        self.lr = lr                                # szybkość uczenia (eta)\n"
"        self.epochs = epochs                        # liczba przejść po danych\n"
"        # funkcja aktywacji: skok jednostkowy (0 lub 1)\n"
"        self.activation_function = lambda x: 0 if x < 0 else 1\n"
"\n"
"    def predict(self, x, theta):\n"
"        z = self.W.T.dot(x) - theta                 # suma ważona minus próg\n"
"        a = self.activation_function(round(z, 2))   # przepuść przez aktywację\n"
"        return a                                    # zwróć 0 lub 1\n",
        caption="Rdzeń perceptronu: suma ważona + aktywacja progowa.")
    note("Perceptron z aktywacją zero-jedynkową może NIE zbiegać, jeśli dane nie są liniowo "
         "separowalne — wagi mogą się bez końca „przełączać\". Dane irysów (3 klasy) nie są w pełni "
         "liniowo separowalne, więc nie da się osiągnąć 100% trafności.")

    h2("13.2. Co to jest funkcja aktywacji")
    p("Funkcja aktywacji decyduje, jak neuron przekształca swoją sumę ważoną z na sygnał wyjściowy. "
      "Jej najważniejsza rola: wprowadza <b>nieliniowość</b>. Bez niej cała sieć — choćby "
      "wielowarstwowa — byłaby równoważna jednemu przekształceniu liniowemu i nie nauczyłaby się "
      "złożonych zależności (np. funkcji XOR). Dodatkowo funkcja aktywacji musi być <b>różniczkowalna</b>, "
      "by zadziałała wsteczna propagacja błędu (sekcja 14).")

    h2("13.3. Typowe funkcje aktywacji")
    table(["Funkcja", "Wzór", "Charakterystyka"],
          [["Skok jednostkowy", "1 gdy z≥0, inaczej 0", "klasyczny perceptron; nieróżniczkowalna"],
           ["Liniowa (Adaline)", "φ(z) = z", "wyjście wprost = suma ważona; różniczkowalna"],
           ["Sigmoid", "1 / (1 + e^−z)", "ściska do (0,1); daje prawdopodobieństwo (regresja log.)"],
           ["Tanh", "(eᶻ−e^−z)/(eᶻ+e^−z)", "ściska do (−1,1); wyśrodkowana w zerze"],
           ["ReLU", "max(0, z)", "szybka, popularna w sieciach głębokich"],
           ["Softmax", "e^{zᵢ} / Σ e^{zₙ}", "zamienia wektor na prawdopodobieństwa klas (wyjście)"]],
          widths=[3.2*cm, 4.4*cm, 9.0*cm])
    p("Z repozytorium — sigmoid i jej pochodna (potrzebna do uczenia sieci XOR), oraz definicje "
      "ReLU i softmax z wykładu:")
    code(
"import numpy as np\n"
"def sigmoid(x):\n"
"    return 1 / (1 + np.exp(-x))         # ściska dowolne x do przedziału (0,1)\n"
"\n"
"def sigmoid_derivative(y):\n"
"    # pochodna sigmoidu wyrażona przez jej WYJŚCIE y: s'(x) = s(x)*(1 - s(x))\n"
"    return y * (1 - y)\n"
"\n"
"def relu(x):\n"
"    return np.maximum(0, x)             # zeruje wartości ujemne, dodatnie zostawia\n",
        caption="Sigmoid, jej pochodna i ReLU (P2Wyk11_SieciNeuronowe.ipynb).")
    p("Adaline (ADAptive LInear NEuron) to wariant perceptronu z LINIOWĄ aktywacją φ(z)=z. Dzięki "
      "temu funkcja błędu jest różniczkowalna i wagi można uczyć spadkiem gradientu:")
    formula("J(w) = ½ · Σᵢ (yⁱ − φ(zⁱ))²")

    # ====================================================================
    # 14. BACKPROPAGATION
    # ====================================================================
    h1("Wsteczna propagacja błędu (backpropagation)", 14)
    p("Pojedynczy neuron (perceptron) potrafi rozdzielać tylko dane liniowo separowalne — nie nauczy "
      "się np. funkcji XOR. Rozwiązaniem jest sieć <b>wielowarstwowa</b> (warstwa wejściowa, jedna lub "
      "więcej warstw ukrytych, warstwa wyjściowa). Problem: jak ustawić wagi w warstwach ukrytych, "
      "skoro nie znamy ich „prawidłowych\" wartości? Odpowiedzią jest backpropagation.")

    h2("14.1. Czemu służy propagacja błędu")
    p("Wsteczna propagacja błędu to algorytm <b>uczenia</b> sieci wielowarstwowej: efektywnie oblicza, "
      "jak każda waga w sieci wpływa na końcowy błąd, i wskazuje, w którą stronę ją poprawić, aby błąd "
      "zmalał. Jest to sposób na rozdzielenie „winy\" za błąd pomiędzy wszystkie wagi, łącznie z tymi "
      "głęboko w warstwach ukrytych.")

    h2("14.2. Jak to działa (w skrócie)")
    bullets([
        "1. Propagacja w przód (forward pass) — dane wejściowe przechodzą przez kolejne warstwy aż do wyjścia; sieć generuje predykcję ŷ.",
        "2. Obliczenie błędu — porównujemy ŷ z prawdziwą wartością y funkcją straty (np. MSE), otrzymując jedną liczbę — koszt.",
        "3. Propagacja wstecz (backward pass) — błąd „cofa się\" od wyjścia do wejścia. Korzystając z REGUŁY ŁAŃCUCHOWEJ liczenia pochodnych, wyznaczamy gradient (pochodną) kosztu względem KAŻDEJ wagi.",
        "4. Aktualizacja wag — każdą wagę przesuwamy w kierunku PRZECIWNYM do gradientu (spadek gradientu): w ← w − η · ∂J/∂w.",
        "5. Powtarzanie — kroki 1–4 powtarzamy przez wiele epok, aż błąd przestanie maleć.",
    ])
    p("Dlatego funkcje aktywacji muszą być różniczkowalne — reguła łańcuchowa wymaga pochodnych na "
      "każdym etapie. Aktualizacja wagi to: nowa_waga = stara_waga − η · gradient.")
    formula("wⱼ ← wⱼ − η · ∂J/∂wⱼ")
    p("Fragment z repozytorium — sieć dwuwarstwowa ucząca się XOR. Widać forward pass, liczenie błędu "
      "na wyjściu i cofanie go do warstwy ukrytej przez pochodne (sigmoid_derivative):")
    code(
"# Krok 1: FORWARD — sygnał płynie wejście -> warstwa ukryta -> wyjście\n"
"hidden = sigmoid(np.dot(X, self.W1) + self.b1)      # aktywacje warstwy ukrytej\n"
"output = sigmoid(np.dot(hidden, self.W2) + self.b2) # predykcja sieci\n"
"\n"
"# Krok 2: BŁĄD na wyjściu (różnica prawda - predykcja)\n"
"error = y - output\n"
"\n"
"# Krok 3: BACKWARD — delta = błąd * pochodna aktywacji (reguła łańcuchowa)\n"
"d_output = error * sigmoid_derivative(output)        # ile 'winy' na wyjściu\n"
"error_hidden = d_output.dot(self.W2.T)               # cofnij błąd do warstwy ukrytej\n"
"d_hidden = error_hidden * sigmoid_derivative(hidden) # delta warstwy ukrytej\n"
"\n"
"# Krok 4: AKTUALIZACJA wag w stronę malejącego błędu (lr = szybkość uczenia)\n"
"self.W2 += hidden.T.dot(d_output) * self.lr\n"
"self.W1 += X.T.dot(d_hidden) * self.lr\n",
        caption="Wsteczna propagacja błędu w sieci uczącej się XOR (P2Wyk11_SieciNeuronowe.ipynb).")
    note("Backpropagation to po prostu skuteczny sposób policzenia gradientu funkcji kosztu po "
         "wszystkich wagach. Samego „uczenia\" (przesuwania wag) dokonuje spadek gradientu, a "
         "w nowoczesnych sieciach jego ulepszona wersja — optymalizator Adam (adaptacyjna szybkość "
         "uczenia dla każdej wagi).")
