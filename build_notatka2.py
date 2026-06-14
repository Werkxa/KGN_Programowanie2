# -*- coding: utf-8 -*-
"""Buduje Notatka_Kolokwium_Housing.pdf: funkcje semestr 1 + projekt housing + narzędzia sklearn."""
from pdf_framework import Notebook
import nb2_part1, nb2_part2, nb2_part3

nb = Notebook(footer="Programowanie 2 — notatka na kolokwium (funkcje + projekt housing)")

nb.title_page(
    title="Notatka na kolokwium",
    subtitle="Funkcje z 1. semestru &amp; pełny projekt analizy danych (housing)",
    tagline="Python od podstaw &bull; pandas &bull; NumPy &bull; scikit-learn &bull; SimpleImputer, StandardScaler, OneHotEncoder",
    intro="Materiał opracowany na podstawie repozytorium <b>KGN_Programowanie2</b>: notatnika "
          "<b>funkcje_semestr_1.ipynb</b> oraz projektu <b>P2Lab10 (housing)</b> w wariantach "
          "analizy i ML. Notatka tłumaczy każdą funkcję i każdą linijkę kodu projektu od zera, "
          "tak aby po jej przerobieniu swobodnie operować omawianymi pojęciami i narzędziami.")

nb.toc([
    "CZĘŚĆ I — Funkcje z pierwszego semestru (podstawy Pythona)",
    "   1. Funkcje, typy podstawowe i instrukcje warunkowe",
    "   2. Pętle: while, for i funkcja range",
    "   3. Listy i wyrażenia listowe",
    "   4. Krotki, indeksowanie i wycinki",
    "   5. Napisy (ciągi znaków)",
    "   6. Słowniki",
    "   7. Rekurencja",
    "   8. Obsługa wyjątków (try/except)",
    "   9. Wyrażenia regularne (regex)",
    "   10. Pliki i format JSON",
    "CZĘŚĆ II — Projekt analizy danych: California Housing",
    "   1. Wczytanie i eksploracja danych",
    "   2. Podział na zbiór treningowy i testowy (stratyfikacja)",
    "   3. Wizualizacje i korelacje",
    "   4. Oddzielenie etykiet (X i y)",
    "   5. Czyszczenie i przygotowanie danych — potok (pipeline)",
    "   6. Trenowanie i ocena modeli",
    "   7. Strojenie hiperparametrów i ocena końcowa",
    "CZĘŚĆ III — Kluczowe narzędzia scikit-learn (dogłębnie)",
    "   1. Wspólny interfejs sklearn: fit/transform",
    "   2. SimpleImputer — uzupełnianie braków",
    "   3. StandardScaler — standaryzacja",
    "   4. OneHotEncoder — kodowanie kategorii",
    "   5. Pipeline i ColumnTransformer",
    "   6. Modele, metryki i walidacja — podsumowanie",
])

nb2_part1.build(nb)
nb2_part2.build(nb)
nb2_part3.build(nb)

nb.build("Notatka_Kolokwium_Housing.pdf")
print("OK: zapisano Notatka_Kolokwium_Housing.pdf")
