# -*- coding: utf-8 -*-
"""Treść sekcji 1-7. Importowane przez build_notatka.py."""

def build(api):
    h1, h2, h3, p, bullets, code, formula, note, table, spacer, rule = (
        api["h1"], api["h2"], api["h3"], api["p"], api["bullets"], api["code"],
        api["formula"], api["note"], api["table"], api["spacer"], api["rule"])

    # ====================================================================
    # 1. PODSTAWY SQL
    # ====================================================================
    h1("Podstawy języka SQL", 1)
    p("SQL (ang. <b>Structured Query Language</b>) to język zapytań do relacyjnych baz danych. "
      "Baza relacyjna przechowuje dane w <b>tabelach</b> — prostokątnych strukturach złożonych z "
      "<b>kolumn</b> (atrybutów, np. imię, ocena) i <b>wierszy</b> (rekordów, czyli pojedynczych "
      "krotek danych, np. konkretnego studenta). SQL pozwala te dane pobierać, filtrować, łączyć, "
      "grupować i podsumowywać, nie mówiąc komputerowi „jak\" to zrobić, a jedynie „co\" chcemy uzyskać "
      "(jest to język deklaratywny).")

    h2("1.1. Budowa (struktura) kwerendy SQL")
    p("Kwerenda (zapytanie) to pojedyncze polecenie pobrania danych. Najważniejsze polecenie to "
      "<b>SELECT</b>. Pełny szkielet zapytania wybierającego dane wygląda następująco:")
    code(
"SELECT   nazwy_i_definicje_kolumn      -- CO chcemy zobaczyć (które kolumny)\n"
"FROM     nazwy_tabel_i_ich_złączenia   -- SKĄD bierzemy dane (z których tabel)\n"
"WHERE    warunek_selekcji_wierszy      -- KTÓRE wiersze zostawić (filtr)\n"
"GROUP BY kolumny_grupujące             -- jak POGRUPOWAĆ wiersze w paczki\n"
"HAVING   warunek_po_grupowaniu         -- filtr działający NA GRUPACH\n"
"ORDER BY kolumny_sortowania [ASC|DESC];-- jak POSORTOWAĆ wynik\n",
        caption="Ogólny szkielet kwerendy SQL (komentarze po -- nie są wykonywane).")
    note("Klauzule WHERE, GROUP BY, HAVING i ORDER BY są opcjonalne. Wymagane jest jedynie "
         "SELECT (co wybrać) oraz najczęściej FROM (skąd). Średnik ; kończy zapytanie.")

    h2("1.2. Słowa kluczowe i ich znaczenie")
    table(["Słowo kluczowe", "Znaczenie / co robi"],
          [["SELECT", "Określa, które kolumny (lub wyrażenia) znajdą się w wyniku. SELECT * oznacza „wszystkie kolumny\"."],
           ["FROM", "Wskazuje tabelę lub tabele będące źródłem danych; tutaj definiujemy też złączenia tabel."],
           ["WHERE", "Filtruje pojedyncze wiersze — zostają tylko te, dla których warunek logiczny jest prawdziwy."],
           ["GROUP BY", "Grupuje wiersze o tej samej wartości wskazanej kolumny w jedną „paczkę\", na której liczymy funkcje agregujące."],
           ["HAVING", "Filtruje już utworzone grupy (np. zostaw grupy mające średnią > 3). Działa po GROUP BY."],
           ["ORDER BY", "Sortuje wynik rosnąco (ASC, domyślnie) lub malejąco (DESC) po wskazanych kolumnach."]],
          widths=[3.2*api["cm"], 13.4*api["cm"]])
    note("W treści zagadnień pojawia się skrót „SORT\" — w standardzie SQL klauzula sortująca nosi "
         "nazwę ORDER BY i to jej należy używać.")

    h2("1.3. Kolejność WYKONYWANIA klauzul (logiczna)")
    p("Zapytanie zapisujemy zaczynając od SELECT, ale baza danych <b>wykonuje</b> je w innej kolejności. "
      "Zrozumienie tej kolejności jest kluczowe, bo tłumaczy np. dlaczego w WHERE nie można jeszcze "
      "używać aliasów kolumn z SELECT:")
    bullets([
        "FROM — najpierw tworzone jest jedno wspólne źródło danych (łączenie tabel w jedną).",
        "WHERE — odrzucane są wiersze niespełniające warunku (zanim cokolwiek pogrupujemy).",
        "GROUP BY — pozostałe wiersze są grupowane po wskazanych atrybutach.",
        "HAVING — odrzucane są całe grupy na podstawie wartości funkcji grupujących.",
        "SELECT — wyliczane są ostateczne kolumny wyniku (i aliasy).",
        "ORDER BY — na samym końcu wynik jest sortowany.",
    ])

    h2("1.4. Funkcje grupujące (agregujące)")
    p("Funkcje agregujące zwijają wiele wierszy w jedną liczbę. Używamy ich najczęściej razem z GROUP BY:")
    bullets([
        "count(*) — zlicza WSZYSTKIE wiersze w grupie (także te z wartościami NULL).",
        "count(atrybut) — zlicza tylko wiersze, w których atrybut jest różny od NULL.",
        "avg(atrybut) — średnia arytmetyczna wartości w kolumnie.",
        "max(atrybut) / min(atrybut) — wartość największa / najmniejsza.",
        "sum(atrybut) — suma wartości w kolumnie.",
    ])
    note("NULL to brak wartości (nie to samo co 0 ani pusty napis). Większość funkcji agregujących "
         "po prostu pomija wartości NULL.")

    h2("1.5. Złączenia tabel (JOIN)")
    p("Dane bywają rozbite na kilka tabel (np. osobno studenci, osobno oceny). Złączenie (JOIN) "
      "łączy wiersze różnych tabel w jeden wiersz wyniku na podstawie wspólnej kolumny (klucza). "
      "Poniżej najważniejsze typy złączeń:")
    table(["Typ złączenia", "Działanie"],
          [["NATURAL JOIN", "Łączy automatycznie po WSPÓLNYCH kolumnach (o tej samej nazwie). Bierze tylko krotki o zgodnych wartościach w tych kolumnach."],
           ["JOIN / INNER JOIN", "Łączy po jawnie podanym warunku: T1 JOIN T2 ON T1.A = T2.B. W wyniku zostają tylko pasujące pary wierszy."],
           ["LEFT OUTER JOIN", "Wszystkie wiersze z LEWEJ tabeli; brakujące dopasowania z prawej uzupełniane są wartościami NULL."],
           ["RIGHT OUTER JOIN", "Analogicznie — wszystkie wiersze z PRAWEJ tabeli; braki z lewej uzupełniane NULL-ami."],
           ["FULL OUTER JOIN", "Wszystkie wiersze z OBU tabel; niepasujące dopasowania po obu stronach wypełniane NULL."],
           ["CROSS JOIN", "Iloczyn kartezjański — każdy wiersz z jednej tabeli łączony z każdym wierszem drugiej (bez warunku)."]],
          widths=[3.6*api["cm"], 13.0*api["cm"]])
    p("CROSS JOIN można zapisać też przez przecinek — oba zapisy są równoważne:")
    code(
"SELECT * FROM A CROSS JOIN B;   -- iloczyn kartezjański, zapis jawny\n"
"SELECT * FROM A, B;             -- dokładnie to samo, zapis skrócony\n",
        caption="Dwa równoważne zapisy iloczynu kartezjańskiego.")
    note("Słowo OUTER jest opcjonalne: LEFT JOIN znaczy to samo co LEFT OUTER JOIN. "
         "Jeśli w INNER JOIN zapomnimy warunku ON, baza policzy iloczyn kartezjański — zwykle to błąd.")

    h2("1.6. Przykład z repozytorium (plik P2Lab02_SQL.ipynb)")
    p("W laboratorium dane są tworzone w pandas i zapisywane do bazy SQLite, a następnie odpytywane "
      "magią %%sql. Najpierw przygotowanie tabel:")
    code(
"import pandas as pd\n"
"import sqlite3                       # wbudowana, plikowa baza danych SQLite\n"
"\n"
"# Tabela studentów: id, imię, kierunek\n"
"df_studenci = pd.DataFrame({\n"
"    'id_stud': [101, 102, 103, 104],\n"
"    'imie': ['Adam', 'Beata', 'Cezary', 'Daria'],\n"
"    'kierunek': ['Filozofia', 'Kognitywistyka', 'Filozofia', 'Informatyka']\n"
"})\n"
"\n"
"# Tabela ocen: 105 to ocena studenta spoza listy studentów (celowo!)\n"
"df_oceny = pd.DataFrame({\n"
"    'id_stud': [101, 101, 102, 103, 103, 105],\n"
"    'przedmiot': ['Logika I','Etyka','Logika I','Logika I','Metafizyka','Logika I'],\n"
"    'ocena': [5.0, 4.0, 4.5, 3.0, 3.5, 2.0]\n"
"})\n"
"\n"
"conn = sqlite3.connect('uczelnia.db')         # otwiera/tworzy plik bazy\n"
"# zapisuje DataFrame jako tabelę 'studenci'; replace = nadpisz, jeśli istnieje\n"
"df_studenci.to_sql('studenci', conn, index=False, if_exists='replace')\n"
"df_oceny.to_sql('oceny', conn, index=False, if_exists='replace')\n"
"conn.close()                                   # zamyka połączenie z bazą\n",
        caption="Tworzenie tabel w bazie SQLite na podstawie ramek pandas.")
    p("Następnie zapytanie łączące studentów z ocenami i liczące statystyki dla każdego studenta. "
      "Użyto LEFT JOIN, dzięki czemu student bez ocen (Daria, id 104) także pojawi się w wyniku:")
    code(
"%%sql\n"
"SELECT\n"
"    s.imie,\n"
"    s.kierunek,\n"
"    COUNT(o.ocena)          AS liczba_egzaminow,  -- ile ocen ma student\n"
"    ROUND(AVG(o.ocena), 2)  AS srednia            -- średnia, zaokrąglona do 2 miejsc\n"
"FROM studenci s                                   -- s = alias tabeli studenci\n"
"LEFT JOIN oceny o ON s.id_stud = o.id_stud        -- dołącz oceny po wspólnym id\n"
"GROUP BY s.id_stud;                               -- jeden wiersz na studenta\n",
        caption="Złączenie LEFT JOIN + grupowanie + funkcje agregujące.")
    p("Przykład podzapytania (zapytania zagnieżdżonego) z repozytorium — ile przedmiotów NIE może "
      "prowadzić dany wykładowca. NOT IN sprawdza przynależność do zbioru zwróconego przez wewnętrzne SELECT:")
    code(
"%%sql\n"
"SELECT w.nazwisko, COUNT(DISTINCT g.przedmiot)    -- DISTINCT = licz różne przedmioty\n"
"FROM grafik g JOIN wykladowcy w\n"
"WHERE w.id_wykl NOT IN (                           -- wykładowca, którego NIE ma\n"
"        SELECT g2.id_wykl FROM grafik g2           -- wśród prowadzących dany przedmiot\n"
"        WHERE g2.przedmiot = g.przedmiot)\n"
"GROUP BY w.nazwisko\n"
"ORDER BY w.nazwisko;\n",
        caption="Podzapytanie skorelowane z operatorem NOT IN.")

    # ====================================================================
    # 2. SQL W PANDAS
    # ====================================================================
    h1("SQL w praktyce pakietu pandas", 2)
    p("pandas to biblioteka Pythona do pracy z danymi tabelarycznymi. Każda operacja SQL ma swój "
      "odpowiednik w pandas. Poniżej omawiamy je po kolei, korzystając z tych samych tabel "
      "(df_studenci, df_oceny) co w sekcji 1.")

    h2("2.1. Jak wykonać kwerendę SQL w pandas?")
    p("Są trzy podejścia. (a) Napisać prawdziwy SQL do bazy i wczytać wynik funkcją pd.read_sql; "
      "(b) użyć metody .query() na ramce; (c) odtworzyć logikę zapytania metodami pandas. "
      "Najpierw wariant z prawdziwym SQL:")
    code(
"import pandas as pd, sqlite3\n"
"conn = sqlite3.connect('uczelnia.db')\n"
"# pd.read_sql wykonuje zapytanie w bazie i zwraca wynik od razu jako DataFrame\n"
"wynik = pd.read_sql('SELECT * FROM studenci WHERE kierunek = \"Filozofia\"', conn)\n"
"conn.close()\n"
"print(wynik)\n",
        caption="Wariant (a): pełny SQL wykonany w bazie, wynik jako DataFrame.")
    code(
"# Wariant (b): metoda .query() przyjmuje warunek w stylu SQL/WHERE jako napis\n"
"df_studenci.query('kierunek == \"Filozofia\"')\n",
        caption="Wariant (b): .query() — odpowiednik klauzuli WHERE.")

    h2("2.2. Selekcja wierszy warunkiem logicznym (WHERE)")
    p("To tzw. <b>indeksowanie logiczne (boolean masking)</b>. W nawiasie kwadratowym podajemy "
      "warunek, który dla każdego wiersza daje True/False; zostają tylko wiersze z True:")
    code(
"# Zostaw studentów z kierunku Filozofia (odpowiednik: WHERE kierunek = 'Filozofia')\n"
"df_studenci[df_studenci['kierunek'] == 'Filozofia']\n"
"\n"
"# Warunek złożony: oceny >= 4 ORAZ przedmiot Logika I.\n"
"# & to logiczne I, | to logiczne LUB. KAŻDY warunek MUSI być w nawiasach!\n"
"df_oceny[(df_oceny['ocena'] >= 4) & (df_oceny['przedmiot'] == 'Logika I')]\n",
        caption="Filtrowanie wierszy maską logiczną — odpowiednik WHERE.")
    note("W pandas używamy &, |, ~ (nie and/or/not) i obowiązkowo otaczamy każdy człon nawiasami, "
         "bo operatory & i | mają wyższy priorytet niż porównania.")

    h2("2.3. Instrukcja grupująca (GROUP BY)")
    p("Metoda .groupby() dzieli ramkę na grupy, a następnie na każdej grupie liczymy agregat. "
      "Przykład wprost z repozytorium — średnia i liczba ocen każdego studenta:")
    code(
"# .merge   = złączenie (JOIN) studentów z ocenami po kolumnie id_stud, typ left\n"
"# .groupby = pogrupuj po imieniu\n"
"# .agg     = policz na kolumnie 'ocena' dwie funkcje: liczność i średnią\n"
"df1 = (df_studenci\n"
"       .merge(df_oceny, on='id_stud', how='left')\n"
"       .groupby('imie')['ocena']\n"
"       .agg(['count', 'mean']))\n"
"print(df1)\n",
        caption="GROUP BY + agregacja w pandas (P2Lab03_pandas.ipynb).")
    code(
"# Średnia WSZYSTKICH ocen (agregacja bez grupowania) — jak SELECT AVG(ocena)\n"
"print(f\"Średnia ocen to: {df_oceny['ocena'].mean()}\")\n"
"\n"
"# Średnia ocen z każdego PRZEDMIOTU osobno (GROUP BY przedmiot)\n"
"df_oceny.groupby('przedmiot')['ocena'].mean()\n",
        caption="Agregacja całości oraz grupowanie po przedmiocie.")

    h2("2.4. Wybór kolumn (SELECT)")
    code(
"df_studenci['imie']                    # jedna kolumna -> obiekt Series\n"
"df_studenci[['imie', 'kierunek']]      # lista kolumn -> DataFrame (dwa nawiasy!)\n",
        caption="Rzutowanie na wybrane kolumny — odpowiednik SELECT imie, kierunek.")
    note("Pojedyncze nawiasy zwracają Series (jedną kolumnę), podwójne (lista) zwracają DataFrame.")

    h2("2.5. Złączenie tabel (JOIN)")
    p("W pandas złączeń dokonujemy metodą .merge(). Parametr on wskazuje wspólną kolumnę, a how "
      "określa typ złączenia i wprost odpowiada SQL-owym JOIN-om:")
    table(["pandas (how=...)", "Odpowiednik SQL"],
          [["how='inner'", "INNER JOIN (tylko pasujące pary — wartość domyślna)"],
           ["how='left'", "LEFT OUTER JOIN"],
           ["how='right'", "RIGHT OUTER JOIN"],
           ["how='outer'", "FULL OUTER JOIN"],
           ["how='cross'", "CROSS JOIN (iloczyn kartezjański)"]],
          widths=[4.5*api["cm"], 12.1*api["cm"]])
    code(
"# LEFT JOIN: wszyscy studenci + ich oceny (student bez ocen też zostanie, z NaN)\n"
"df_studenci.merge(df_oceny, on='id_stud', how='left')\n",
        caption="Złączenie ramek metodą .merge().")

    h2("2.6. Usuwanie kolumn")
    code(
"# axis=1 oznacza 'działaj na kolumnach' (axis=0 = wiersze)\n"
"df_studenci.drop(columns=['kierunek'])        # zwraca NOWĄ ramkę bez kolumny\n"
"df_studenci.drop('kierunek', axis=1)          # zapis równoważny\n"
"\n"
"# inplace=True zmienia ramkę „w miejscu\" i nic nie zwraca (przykład z repo):\n"
"strat_train_set.drop(['income_cat'], axis=1, inplace=True)\n",
        caption="Usuwanie kolumn metodą .drop() (ostatnia linia z P2Lab09_housing).")

    h2("2.7. Nowa kolumna jako wynik funkcji na kolumnach")
    p("Najczęściej tworzymy kolumnę przez wektorowe działanie na istniejących kolumnach albo przez "
      ".apply() (funkcja stosowana wiersz po wierszu):")
    code(
"# (a) Operacja wektorowa — działa od razu na całej kolumnie (szybkie):\n"
"df_oceny['ocena_proc'] = df_oceny['ocena'] / 5.0 * 100   # ocena w procentach\n"
"\n"
"# (b) Funkcja własna na każdej wartości przez .apply():\n"
"df_oceny['zdany'] = df_oceny['ocena'].apply(lambda o: 'tak' if o >= 3.0 else 'nie')\n"
"\n"
"# (c) Złożony warunek między kolumnami przez np.where:\n"
"import numpy as np\n"
"df_oceny['status'] = np.where(df_oceny['ocena'] >= 4.5, 'wyróżnienie', 'zwykły')\n",
        caption="Trzy sposoby definiowania nowej kolumny.")

    # ====================================================================
    # 3. Series, DataFrame, loc/iloc, info
    # ====================================================================
    h1("pandas: Series, DataFrame, loc/iloc, informacje o tabeli", 3)

    h2("3.1. Czym jest Series, czym DataFrame i czym się różnią")
    p("<b>Series</b> to jednowymiarowa, etykietowana tablica — pojedyncza kolumna danych wraz z "
      "indeksem (etykietami wierszy). <b>DataFrame</b> to dwuwymiarowa tabela: zbiór kolumn, z których "
      "każda jest obiektem Series, połączonych wspólnym indeksem. Można powiedzieć: DataFrame to "
      "słownik Series o wspólnym indeksie.")
    table(["Cecha", "Series", "DataFrame"],
          [["Wymiary", "1D (jedna kolumna)", "2D (wiersze × kolumny)"],
           ["Etykiety", "indeks wierszy", "indeks wierszy + nazwy kolumn"],
           ["Analogia", "jedna kolumna w arkuszu", "cały arkusz kalkulacyjny"],
           ["Powstaje gdy", "df['kolumna']", "df[['k1','k2']] lub pd.DataFrame(...)"]],
          widths=[3.2*api["cm"], 6.0*api["cm"], 7.4*api["cm"]])
    code(
"import pandas as pd\n"
"s = pd.Series([5.0, 4.0, 4.5], index=['Logika', 'Etyka', 'Statystyka'])\n"
"print(s)            # po lewej indeks (etykiety), po prawej wartości\n"
"print(type(s))      # <class 'pandas.core.series.Series'>\n"
"\n"
"df = pd.DataFrame({'ocena': [5.0, 4.0], 'przedmiot': ['Logika', 'Etyka']})\n"
"print(type(df['ocena']))   # <class '...Series'> -> kolumna ramki to Series\n",
        caption="Tworzenie Series i DataFrame; kolumna DataFrame jest typu Series.")

    h2("3.2. Różnica między loc a iloc")
    p("Oba służą do wybierania wierszy/kolumn, ale używają innych „adresów\":")
    bullets([
        "loc — indeksowanie po ETYKIETACH (nazwach). Zakresy są DOMKNIĘTE (koniec włącznie).",
        "iloc — indeksowanie po POZYCJACH liczbowych 0,1,2,... Zakresy jak w Pythonie: koniec WYŁĄCZNIE.",
    ])
    code(
"import pandas as pd\n"
"df = pd.DataFrame(\n"
"    {'imie': ['Adam','Beata','Cezary'], 'wiek': [20, 22, 21]},\n"
"    index=['a', 'b', 'c'])     # własne etykiety wierszy: 'a','b','c'\n"
"\n"
"# --- loc: po ETYKIETACH ---\n"
"df.loc['b']                    # cały wiersz o etykiecie 'b' (Beata)\n"
"df.loc['a':'c', 'imie']        # od 'a' do 'c' WŁĄCZNIE, kolumna 'imie'\n"
"df.loc[df['wiek'] > 20, 'imie']# loc przyjmuje też maskę logiczną (WHERE)\n"
"\n"
"# --- iloc: po POZYCJACH (numerach) ---\n"
"df.iloc[0]                     # pierwszy wiersz (pozycja 0) = Adam\n"
"df.iloc[0:2, 0]                # wiersze 0 i 1 (2 WYŁĄCZNIE), kolumna numer 0\n"
"df.iloc[-1]                    # ostatni wiersz (Cezary)\n",
        caption="Porównanie loc (etykiety, koniec włącznie) i iloc (pozycje, koniec wyłącznie).")
    note("Najczęstsza pomyłka: df.loc[0:2] przy domyślnym indeksie liczbowym zwraca wiersze 0,1,2 "
         "(3 sztuki), a df.iloc[0:2] zwraca tylko 0,1 (2 sztuki).")

    h2("3.3. Podstawowe informacje o tabeli")
    code(
"df.head(5)        # pierwsze 5 wierszy (podgląd danych)\n"
"df.tail(3)        # ostatnie 3 wiersze\n"
"df.shape          # krotka (liczba_wierszy, liczba_kolumn)\n"
"df.columns        # nazwy kolumn\n"
"df.dtypes         # typ danych każdej kolumny (int64, float64, object...)\n"
"df.info()         # podsumowanie: typy, liczba wartości niepustych, pamięć\n"
"df.describe()     # statystyki kolumn liczbowych: count, mean, std, min, kwartyle, max\n"
"df.isnull().sum() # liczba braków (NaN) w każdej kolumnie\n",
        caption="Najważniejsze metody diagnostyczne ramki danych.")
    p("Przykład z repozytorium (P2Lab06) — head i describe na wygenerowanych danych:")
    code(
"import numpy as np, pandas as pd\n"
"np.random.seed(42)                                  # powtarzalność losowania\n"
"wiek   = np.random.randint(18, 65, 100)             # 100 liczb 18..64\n"
"dochód = np.random.normal(5000, 1500, 100)          # rozkład normalny\n"
"df = pd.DataFrame({'wiek': wiek, 'dochód': dochód})\n"
"print(df.head())       # podgląd pierwszych wierszy\n"
"print(df.describe())   # statystyki opisowe obu kolumn\n",
        caption="Generowanie danych i szybki przegląd (P2Lab06_NumPy_Pandas.ipynb).")
