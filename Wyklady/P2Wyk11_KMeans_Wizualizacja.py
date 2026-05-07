import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from sklearn.datasets import make_blobs

# --- 1. Konfiguracja i generowanie danych ---
np.random.seed(43)
k = 4 # Liczba klastrów
# Generujemy 150 punktów skupionych w 4 grupach
X, _ = make_blobs(n_samples=150, centers=k, cluster_std=0.9, random_state=43)

# Zmienne przechowujące stan algorytmu
centroids = None
labels = None
state = 'start' # Możliwe stany: 'start', 'init', 'assign', 'update', 'done'
iteration = 0

# --- 2. Konfiguracja wykresu ---
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.2) # Zostawiamy miejsce na przycisk na dole

def draw_plot():
    """Funkcja rysująca aktualny stan algorytmu na wykresie."""
    ax.clear()
    ax.grid(True, linestyle='--', alpha=0.5)

    # Rysowanie punktów
    if labels is None:
        # Przed przypisaniem - wszystkie punkty szare
        ax.scatter(X[:, 0], X[:, 1], c='gray', alpha=0.6, s=50, edgecolors='w')
    else:
        # Po przypisaniu - kolory odpowiadające klastrom
        ax.scatter(X[:, 0], X[:, 1], c=labels, cmap='tab10', alpha=0.6, s=50, edgecolors='w')

    # Rysowanie centroidów
    if centroids is not None:
        # Używamy cmap='tab10', aby kolory centroidów pasowały do kolorów punktów
        colors = plt.cm.tab10(np.arange(k))
        ax.scatter(centroids[:, 0], centroids[:, 1], c=colors, marker='X', s=300, edgecolors='black', linewidths=2, zorder=10)

    # Aktualizacja tytułu w zależności od stanu
    if state == 'start':
        ax.set_title("K-Means: Dane początkowe (Kliknij 'Następny krok')", fontsize=14)
    elif state == 'init':
        ax.set_title("K-Means: Losowa inicjalizacja centroidów", fontsize=14)
    elif state == 'assign':
        ax.set_title(f"Iteracja {iteration} - Krok 1: Przypisanie punktów do najbliższych centroidów", fontsize=14)
    elif state == 'update':
        ax.set_title(f"Iteracja {iteration} - Krok 2: Przesunięcie centroidów do średniej", fontsize=14)
    elif state == 'done':
        ax.set_title(f"K-Means: Zbieżność osiągnięta w {iteration} iteracjach!", fontsize=14, color='green')

    plt.draw()

# --- 3. Logika algorytmu K-Means (Krok po kroku) ---
def next_step(event):
    """Funkcja wywoływana po kliknięciu przycisku."""
    global centroids, labels, state, iteration

    if state == 'done':
        return # Jeśli algorytm skończył, przycisk nic nie robi

    if state == 'start':
        # Losujemy k początkowych punktów jako centroidy
        random_indices = np.random.choice(len(X), k, replace=False)
        centroids = X[random_indices].copy()
        state = 'init'

    elif state == 'init' or state == 'update':
        # Krok oczekiwania (Expectation): Przypisanie punktów
        iteration += 1
        # Obliczamy odległość każdego punktu od każdego centroidu używając broadastingu numpy
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        new_labels = np.argmin(distances, axis=1)

        # Sprawdzamy warunek zbieżności (czy żadne przypisanie się nie zmieniło)
        if labels is not None and np.array_equal(new_labels, labels):
            state = 'done'
        else:
            labels = new_labels
            state = 'assign'

    elif state == 'assign':
        # Krok maksymalizacji (Maximization): Aktualizacja pozycji centroidów
        for i in range(k):
            # Wybieramy tylko punkty należące do klastra 'i'
            points_in_cluster = X[labels == i]
            if len(points_in_cluster) > 0:
                # Nowy centroid to średnia (środek ciężkości) tych punktów
                centroids[i] = np.mean(points_in_cluster, axis=0)
        state = 'update'

    draw_plot()

# --- 4. Interfejs Użytkownika (Przycisk) ---
# Tworzymy oś dla przycisku: [lewo, dół, szerokość, wysokość]
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
btn = Button(ax_button, 'Następny krok', hovercolor='lightblue')
btn.on_clicked(next_step) # Podpinamy logikę pod kliknięcie

# Rysujemy stan początkowy i uruchamiamy okno
draw_plot()
plt.show()
