# -*- coding: utf-8 -*-
"""CZĘŚĆ I — Funkcje z pierwszego semestru (podstawy Pythona)."""

def build(nb):
    nb.part("CZĘŚĆ I\nFunkcje z pierwszego semestru\n— podstawy Pythona")

    # ----------------------------------------------------------------
    nb.h1("Funkcje, typy podstawowe i instrukcje warunkowe", 1)
    nb.p("Zanim przejdziemy do konkretnych zadań, ustalmy fundament. <b>Funkcja</b> to nazwany "
         "fragment kodu, który przyjmuje dane wejściowe (argumenty), wykonuje obliczenia i zwraca "
         "wynik (słowem kluczowym return). Definiujemy ją słowem <b>def</b>. Dzięki funkcjom kod "
         "piszemy raz, a używamy wielokrotnie.")
    nb.definition("Składnia: <b>def nazwa(argumenty):</b> a pod spodem, wcięty o spację/tabulator, "
                  "blok instrukcji. Wcięcie (indentacja) w Pythonie nie jest kosmetyką — to ono "
                  "wyznacza, co należy do funkcji. return kończy działanie funkcji i oddaje wartość.")
    nb.h2("1.1. Typy podstawowe (proste)")
    nb.table(["Typ", "Znaczenie", "Przykład"],
             [["int", "liczba całkowita", "5, -3, 0"],
              ["float", "liczba zmiennoprzecinkowa (ułamkowa)", "3.14, -0.5"],
              ["bool", "wartość logiczna", "True, False"],
              ["str", "napis (ciąg znaków)", "'ala', \"kot\""],
              ["None", "brak wartości", "None"]],
             widths=[2.4*nb.cm, 8.6*nb.cm, 5.6*nb.cm])

    nb.h2("1.2. Funkcja is_even — parzystość, operator modulo, typ bool")
    nb.p("Pierwsze zadanie: sprawdzić, czy liczba całkowita jest parzysta. Kluczem jest operator "
         "<b>%</b> (modulo) — zwraca resztę z dzielenia. Liczba jest parzysta dokładnie wtedy, gdy "
         "reszta z dzielenia przez 2 wynosi 0.")
    nb.code(
"# Składnia 'i: int' to PODPOWIEDŹ TYPU (type hint): mówi, że argument ma być int.\n"
"# '-> bool' informuje, że funkcja zwraca wartość logiczną. Hinty są opcjonalne\n"
"# (Python ich nie wymusza), ale czynią kod czytelniejszym.\n"
"def is_even(i: int) -> bool:\n"
"    return i % 2 == 0       # i % 2 to reszta z dzielenia; == 0 daje True/False\n"
"\n"
"is_even(2)                  # 2 % 2 == 0 -> True\n",
        caption="Zadanie 1: sprawdzanie parzystości.", out="True")
    nb.note("Wyrażenie i % 2 == 0 samo w sobie jest typu bool, więc nie trzeba pisać "
            "if ...: return True else: return False — wystarczy zwrócić to wyrażenie.")

    nb.h2("1.3. Funkcja max_of_three — instrukcje warunkowe i szukanie maksimum")
    nb.p("Zadanie: zwrócić największą z trzech liczb. Pokazuje ono <b>instrukcję warunkową if</b> "
         "oraz wzorzec „przechowuj dotychczasowego lidera\". Zbieramy liczby do listy i przechodzimy "
         "ją pętlą, zapamiętując największy dotąd element:")
    nb.code(
"def max_of_three(a, b, c):\n"
"    l = [a, b, c]              # umieść trzy liczby w liście\n"
"    counter = l[0]             # załóż, że pierwsza jest największa (kandydat)\n"
"    for elem in l:             # przejdź po wszystkich elementach\n"
"        if elem > counter:     # jeśli któryś jest większy od kandydata...\n"
"            counter = elem     # ...to on staje się nowym kandydatem\n"
"    return counter             # po pętli counter trzyma maksimum\n"
"\n"
"max_of_three(-3, 8, 8)         # -> 8\n",
        caption="Zadanie 2: największa z trzech liczb.", out="8")
    nb.note("W notatniku zostawiono zakomentowaną PRÓBĘ z warunkiem `a > b | c`. To częsty błąd "
            "początkującego: | to bitowy operator OR, a nie „lub\", i nie znaczy „a większe od b oraz "
            "od c\". Poprawnie byłoby `a > b and a > c`. Wersja z pętlą jest pewniejsza i działa dla "
            "dowolnej liczby elementów.")

    # ----------------------------------------------------------------
    nb.h1("Pętle: while, for i funkcja range", 2)
    nb.p("Pętla powtarza blok kodu. W Pythonie są dwie: <b>while</b> (powtarzaj, dopóki warunek jest "
         "prawdziwy) oraz <b>for</b> (przejdź po elementach kolekcji albo zakresu).")

    nb.h2("2.1. count_down — pętla while i wypisywanie")
    nb.p("Zadanie: wypisać liczby od n do 0, każdą w nowej linii. Pętla while działa, dopóki warunek "
         "jest spełniony; wewnątrz musimy zmieniać zmienną, inaczej pętla nigdy się nie skończy "
         "(pętla nieskończona).")
    nb.code(
"def count_down(n):\n"
"    while n != 0:        # powtarzaj, dopóki n jest różne od zera\n"
"        print(n)         # wypisz aktualną wartość\n"
"        n -= 1           # zmniejsz n o 1 (skrót od n = n - 1)\n"
"\n"
"count_down(5)            # wypisze 5, 4, 3, 2, 1\n",
        caption="Zadanie 3: odliczanie w dół (while).", out="5\n4\n3\n2\n1")

    nb.h2("2.2. cout_down_rev — odliczanie w górę i pętla for z range")
    nb.p("Tę samą logikę można odwrócić (liczyć w górę). Wersja z while pokazana niżej, a obok "
         "wygodniejsza alternatywa z for i funkcją <b>range</b>, która generuje kolejne liczby:")
    nb.code(
"# Wersja while:\n"
"def cout_down_rev(n):\n"
"    start = 1\n"
"    while start != n + 1:    # licz od 1 aż do n włącznie\n"
"        print(start)\n"
"        start += 1\n"
"\n"
"# Równoważna, krótsza wersja z for + range:\n"
"def cout_down_rev2(n):\n"
"    for elem in range(1, n + 1):   # range(1, n+1) = 1,2,...,n (n+1 jest WYŁĄCZONE)\n"
"        print(elem)\n"
"\n"
"cout_down_rev(5)               # 1, 2, 3, 4, 5\n",
        caption="Zadanie 3b: odliczanie w górę.", out="1\n2\n3\n4\n5")
    nb.definition("range(start, stop, step) tworzy ciąg liczb od start do stop-1 (stop jest "
                  "WYŁĄCZONY!) z krokiem step. range(5) to 0,1,2,3,4; range(1,6) to 1,2,3,4,5; "
                  "range(10, 0, -1) liczy w dół.")

    # ----------------------------------------------------------------
    nb.h1("Listy i wyrażenia listowe (list comprehensions)", 3)
    nb.definition("Lista to uporządkowany, ZMIENIALNY (mutable) zbiór elementów w nawiasach "
                  "kwadratowych: [1, 2, 3]. Elementy mogą być dowolnego typu, indeksujemy je od 0. "
                  "Najważniejsze metody: append (dodaj na koniec), len (długość).")

    nb.h2("3.1. sum_list — sumowanie elementów (akumulator)")
    nb.p("Zadanie: zsumować elementy listy. Wzorzec <b>akumulatora</b>: zaczynamy od 0 i w pętli "
         "dodajemy kolejne elementy:")
    nb.code(
"def sum_list(lst):\n"
"    counter = 0              # akumulator startuje od zera\n"
"    for elem in lst:         # przejdź po wszystkich elementach listy\n"
"        counter += elem      # dodaj element do sumy\n"
"    return counter\n"
"\n"
"sum_list([1, 1, 1, 1, 1])    # -> 5\n",
        caption="Zadanie 4: suma elementów listy.", out="5")
    nb.note("Python ma wbudowaną funkcję sum(lst), która robi to samo. Pisanie własnej wersji służy "
            "nauce wzorca pętli akumulującej.")

    nb.h2("3.2. count_positive — filtrowanie i metoda append")
    nb.p("Zadanie (wg treści): policzyć elementy dodatnie. Implementacja z notatnika zbiera dodatnie "
         "elementy do nowej listy metodą append i ją zwraca:")
    nb.code(
"def count_positive(lst):\n"
"    new = []                 # pusta lista na wyniki\n"
"    for elem in lst:\n"
"        if elem > 0:         # warunek: tylko liczby dodatnie\n"
"            new.append(elem) # dołącz element na koniec listy 'new'\n"
"    return new\n"
"\n"
"count_positive([-1, 2, 3, 4, 0, -9])   # -> [2, 3, 4]\n",
        caption="Zadanie 5: dodatnie elementy (wersja z notatnika).", out="[2, 3, 4]")
    nb.note("Uwaga merytoryczna: treść mówi „zwracająca LICZBĘ elementów dodatnich\", a powyższy kod "
            "zwraca LISTĘ tych elementów. Aby zwrócić liczbę, należałoby zwrócić len(new) albo "
            "zliczać licznikiem. Poprawna wersja: zamień ostatnią linię na `return len(new)`. "
            "Warto znać tę różnicę na kolokwium.")

    nb.h2("3.3. Wyrażenia listowe (list comprehension)")
    nb.p("To zwięzły sposób tworzenia listy w jednej linii. Schemat: [wyrażenie for element in "
         "kolekcja if warunek]. Czyta się jak zdanie: „weź wyrażenie dla każdego elementu, dla "
         "których warunek jest prawdziwy\".")
    nb.code(
"# Lista kwadratów liczb 0..4:\n"
"[x**2 for x in range(5)]               # -> [0, 1, 4, 9, 16]\n"
"\n"
"# count_positive jako jedna linia (wersja zwracająca liczbę):\n"
"def count_positive2(lst):\n"
"    return len([e for e in lst if e > 0])   # długość listy dodatnich = ich liczba\n",
        caption="List comprehension — krótszy zapis pętli budującej listę.")

    # ----------------------------------------------------------------
    nb.h1("Krotki, indeksowanie i wycinki (slicing)", 4)
    nb.definition("Krotka (tuple) to uporządkowany, ale NIEZMIENIALNY (immutable) zbiór elementów w "
                  "nawiasach okrągłych: (1, 2, 3). Po utworzeniu nie da się zmienić jej zawartości. "
                  "Używamy jej dla danych, które nie powinny się zmieniać (np. współrzędne).")
    nb.h2("4.1. Indeksowanie i wycinki")
    nb.p("Elementy numerujemy od 0. Indeksy ujemne liczą od końca (-1 to ostatni). <b>Wycinek</b> "
         "[start:stop:step] zwraca fragment; szczególnie [::-1] odwraca kolejność:")
    nb.code(
"t = (10, 20, 30, 40)\n"
"t[0]      # 10  -> pierwszy element\n"
"t[-1]     # 40  -> ostatni element\n"
"t[1:3]    # (20, 30) -> od indeksu 1 do 3 (3 WYŁĄCZNIE)\n"
"t[::-1]   # (40, 30, 20, 10) -> krok -1 odwraca kolejność\n",
        caption="Indeksowanie i wycinki na krotce.")
    nb.h2("4.2. reverse_tuple — odwracanie krotki")
    nb.code(
"def reverse_tuple(t):\n"
"    return t[::-1]           # wycinek z krokiem -1 = nowa krotka od końca\n"
"\n"
"reverse_tuple((1, 2, 3, 4))  # -> (4, 3, 2, 1)\n",
        caption="Zadanie 6: odwrócenie krotki jednym wycinkiem.", out="(4, 3, 2, 1)")

    # ----------------------------------------------------------------
    nb.h1("Napisy (ciągi znaków)", 5)
    nb.definition("Napis (str) to niezmienialny ciąg znaków. Możemy go indeksować i wycinać jak "
                  "krotkę, iterować po znakach pętlą for, sprawdzać zawieranie operatorem in, oraz "
                  "używać metod takich jak split (podziel na słowa), lower/upper (zmiana wielkości).")

    nb.h2("5.1. count_vowels — zliczanie samogłosek, operator in")
    nb.code(
"def count_vowels(text):\n"
"    vowels = 'a,o,e,u,i,y'   # zbiór samogłosek (jako napis)\n"
"    counter = 0\n"
"    for ch in text:          # iteruj po KAŻDYM znaku napisu\n"
"        if ch in vowels:     # 'in' sprawdza, czy znak należy do napisu vowels\n"
"            counter += 1\n"
"    return counter\n"
"\n"
"count_vowels('mateusz')      # a, e, u -> 3\n",
        caption="Zadanie 7: liczenie samogłosek.", out="3")
    nb.note("Drobiazg: vowels zawiera też przecinki, ale ponieważ sprawdzamy pojedyncze litery "
            "słowa, nie wpływa to na wynik. Czyściej byłoby napisać vowels = 'aoeuiy'.")

    nb.h2("5.2. is_palindrome — palindrom przez porównanie z odwróceniem")
    nb.p("Palindrom czyta się tak samo od przodu i od tyłu. Najprościej: porównać napis z jego "
         "odwróceniem (wycinek [::-1]):")
    nb.code(
"def is_palindrome(text):\n"
"    return text == text[::-1]    # napis równy swojemu odwróceniu?\n"
"\n"
"is_palindrome('anna')            # 'anna' == 'anna' -> True\n",
        caption="Zadanie 8: sprawdzanie palindromu.", out="True")

    nb.h2("5.3. word_lengths — split i długości słów")
    nb.p("Zadanie łączy metodę split (dzieli napis na listę słów po spacjach) z wyrażeniem listowym "
         "i funkcją len:")
    nb.code(
"def word_lengths(sentence):\n"
"    lst = sentence.split()       # 'ala ma kota' -> ['ala', 'ma', 'kota']\n"
"    return [len(i) for i in lst] # długość każdego słowa\n"
"\n"
"word_lengths('ala ma kota')      # -> [3, 2, 4]\n",
        caption="Zadanie 9: długości kolejnych słów.", out="[3, 2, 4]")

    # ----------------------------------------------------------------
    nb.h1("Słowniki", 6)
    nb.definition("Słownik (dict) przechowuje pary KLUCZ → WARTOŚĆ w nawiasach klamrowych: "
                  "{'a': 1, 'b': 2}. Klucze są unikalne; wartość pobieramy przez d[klucz]. Metoda "
                  "keys() zwraca klucze, values() wartości, items() pary. Sprawdzenie klucz in d "
                  "mówi, czy klucz istnieje.")

    nb.h2("6.1. invert_dict — zamiana kluczy z wartościami")
    nb.code(
"def invert_dict(d):\n"
"    new = {}                     # pusty słownik wynikowy\n"
"    for key in d.keys():         # przejdź po kluczach oryginału\n"
"        new[d[key]] = key        # stara WARTOŚĆ staje się kluczem, klucz wartością\n"
"    return new\n"
"\n"
"invert_dict({'a': 1, 'b': 2, 'c': 3})   # -> {1: 'a', 2: 'b', 3: 'c'}\n",
        caption="Zadanie 10: odwrócenie słownika.", out="{1: 'a', 2: 'b', 3: 'c'}")
    nb.note("Działa poprawnie tylko gdy wartości są UNIKALNE — inaczej różne klucze nadpisałyby się "
            "po odwróceniu. To założenie podano w treści zadania.")

    nb.h2("6.2. count_occurrences — zliczanie liczności (histogram)")
    nb.p("Bardzo częsty wzorzec: zliczyć, ile razy występuje każdy element. Słownik mapuje "
         "element → licznik. Jeśli element już widzieliśmy, zwiększamy licznik; jeśli nie — zakładamy 1:")
    nb.code(
"def count_occurrences(lst):\n"
"    d = {}\n"
"    for elem in lst:\n"
"        if elem in d:            # widzieliśmy już ten element?\n"
"            d[elem] += 1         # tak -> zwiększ licznik\n"
"        else:\n"
"            d[elem] = 1          # nie -> załóż licznik = 1\n"
"    return d\n"
"\n"
"count_occurrences([1, 1, 2, 2, 3, 3, 4, 4])   # -> {1: 2, 2: 2, 3: 2, 4: 2}\n",
        caption="Zadanie 11: słownik liczności elementów.", out="{1: 2, 2: 2, 3: 2, 4: 2}")

    # ----------------------------------------------------------------
    nb.h1("Rekurencja", 7)
    nb.definition("Rekurencja to funkcja, która wywołuje samą siebie dla mniejszego przypadku. "
                  "Wymaga DWÓCH elementów: (1) warunku bazowego, który zatrzymuje wywołania, oraz "
                  "(2) kroku rekurencyjnego sprowadzającego problem do prostszego. Bez warunku "
                  "bazowego dostaniemy nieskończoną rekursję i błąd przepełnienia stosu.")
    nb.h2("7.1. factorial — silnia rekurencyjnie")
    nb.p("Silnia: n! = n · (n−1) · ... · 1, przy czym 0! = 1. Definicja sama jest rekurencyjna: "
         "n! = n · (n−1)!.")
    nb.code(
"def factorial(n):\n"
"    if n == 0:               # WARUNEK BAZOWY: 0! = 1, zatrzymuje rekurencję\n"
"        return 1\n"
"    else:                    # KROK REKURENCYJNY:\n"
"        return n * factorial(n - 1)   # n! = n * (n-1)!\n"
"\n"
"factorial(8)                 # 8*7*6*5*4*3*2*1 = 40320\n",
        caption="Zadanie 12: silnia rekurencyjna.", out="40320")
    nb.note("Prześledź factorial(3): 3*factorial(2) -> 3*(2*factorial(1)) -> 3*(2*(1*factorial(0))) "
            "-> 3*(2*(1*1)) = 6. Wywołania „zwijają się\" po dotarciu do warunku bazowego.")

    # ----------------------------------------------------------------
    nb.h1("Obsługa wyjątków (try / except)", 8)
    nb.definition("Wyjątek to błąd zgłaszany w trakcie działania programu (np. dzielenie przez zero). "
                  "Blok try/except pozwala go „złapać\" i obsłużyć zamiast przerywać program. "
                  "W try umieszczamy kod, który MOŻE się nie powieść; w except — reakcję na błąd.")
    nb.h2("8.1. safe_divide — bezpieczne dzielenie")
    nb.code(
"def safe_divide(a, b):\n"
"    try:\n"
"        return a / b                 # próba dzielenia (może rzucić wyjątek)\n"
"    except ZeroDivisionError as e:   # łapiemy KONKRETNY wyjątek dzielenia przez 0\n"
"        print(f\"{e}\")                # wypisz komunikat błędu...\n"
"        # funkcja nic nie zwraca -> automatycznie zwróci None\n"
"\n"
"safe_divide(6, 0)                    # wypisze: division by zero, zwróci None\n",
        caption="Zadanie 13: dzielenie odporne na dzielenie przez zero.", out="division by zero")
    nb.note("Łapiemy konkretny typ ZeroDivisionError, a nie wszystkie błędy — to dobra praktyka: "
            "obsługujemy dokładnie tę sytuację, której się spodziewamy. `as e` daje dostęp do "
            "obiektu wyjątku (zawiera komunikat).")

    # ----------------------------------------------------------------
    nb.h1("Wyrażenia regularne (regex)", 9)
    nb.definition("Wyrażenie regularne to wzorzec opisujący zbiór napisów. Moduł re pozwala "
                  "wyszukiwać takie wzorce. re.findall(wzorzec, tekst) zwraca LISTĘ wszystkich "
                  "dopasowań. Wzorzec \\d oznacza cyfrę, a + znaczy „jeden lub więcej\", więc "
                  "\\d+ pasuje do całych liczb.")
    nb.h2("9.1. extract_numbers — wyciąganie liczb z tekstu")
    nb.code(
"import re                            # moduł wyrażeń regularnych\n"
"\n"
"def extract_numbers(text):\n"
"    # r'\\d+' to 'surowy' napis (raw string): r zapobiega interpretacji \\ przez Pythona.\n"
"    # \\d = cyfra, + = jedna lub więcej -> dopasuj ciągi cyfr (liczby)\n"
"    return re.findall(r'\\d+', text)\n"
"\n"
"extract_numbers('asdfha23lh3423hl45l33llhl6')   # -> ['23','3423','45','33','6']\n",
        caption="Zadanie 14: znajdowanie liczb w napisie.", out="['23', '3423', '45', '33', '6']")
    nb.note("findall zwraca liczby jako NAPISY (str), nie int. Aby otrzymać liczby całkowite, "
            "trzeba je przekształcić: [int(x) for x in re.findall(r'\\d+', text)].")

    # ----------------------------------------------------------------
    nb.h1("Pliki i format JSON", 10)
    nb.definition("JSON (JavaScript Object Notation) to tekstowy format zapisu danych, bardzo "
                  "podobny do słowników/list Pythona. Moduł json zamienia obiekty Pythona na tekst "
                  "JSON (json.dump — zapis do pliku, json.dumps — do napisu) i odwrotnie "
                  "(json.load — z pliku, json.loads — z napisu).")
    nb.h2("10.1. Zapis słownika do pliku JSON")
    nb.p("Konstrukcja <b>with open(...) as plik:</b> otwiera plik i — co ważne — sam go zamyka po "
         "wyjściu z bloku (nawet przy błędzie). Tryb 'w' oznacza zapis (write):")
    nb.code(
"import json\n"
"\n"
"osoba = {\"name\": \"Anna\", \"surname\": \"Kowalska\", \"grades\": [4, 5, 3, 5]}\n"
"\n"
"# 'w' = tryb zapisu; with samo zamknie plik po bloku\n"
"with open('student.json', 'w') as plik:\n"
"    # indent=4 -> ładne wcięcia; ensure_ascii=False -> zachowaj polskie znaki\n"
"    json.dump(osoba, plik, indent=4, ensure_ascii=False)\n",
        caption="Zapis słownika Pythona do pliku JSON (zadanie 15, część 1).")
    nb.h2("10.2. names — odczyt danych z pliku JSON")
    nb.p("Odczyt jest analogiczny: tryb domyślny to odczyt ('r'), a json.load zamienia tekst JSON z "
         "powrotem na słownik Pythona, z którego pobieramy pola:")
    nb.code(
"import json\n"
"\n"
"def names(filename):\n"
"    with open(filename) as plik:         # domyślny tryb 'r' (odczyt)\n"
"        dane = json.load(plik)           # JSON z pliku -> słownik Pythona\n"
"        print(f\"{dane['name']} {dane['surname']}\")  # f-string sklejający pola\n"
"\n"
"names('student.json')                    # -> Anna Kowalska\n",
        caption="Zadanie 15: wczytanie imienia i nazwiska z JSON.", out="Anna Kowalska")
    nb.note("f-string (litera f przed cudzysłowem) pozwala wstawiać wartości zmiennych wprost w "
            "napis w nawiasach klamrowych {}. To najczytelniejszy sposób formatowania tekstu w Pythonie.")
