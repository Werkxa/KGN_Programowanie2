import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons

# --- 1. Generator danych ---
def generate_data():
    """Generuje strukturę dwóch półksiężyców i dodaje losowy szum."""
    # Podstawowa struktura (nieliniowa)
    X_core, _ = make_moons(n_samples=250, noise=0.07)

    # Dodanie tła w postaci losowego szumu (outliery)
    X_noise = np.random.uniform(low=-1.5, high=2.5, size=(40, 2))

    return np.vstack([X_core, X_noise])

# Inicjalizacja danych
X = generate_data()

# --- 2. Konfiguracja okna i wykresu ---
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.35) # Zostawiamy miejsce na suwaki i przyciski na dole

# Rysujemy początkowy scatter plot (wszystkie punkty szare przed klastrowaniem)
scatter = ax.scatter(X[:, 0], X[:, 1], c='gray', s=50, edgecolors='black', alpha=0.8)
ax.grid(True, linestyle='--', alpha=0.5)

# --- 3. Definicja suwaków i przycisków ---
# [lewo, dół, szerokość, wysokość]
ax_eps = plt.axes([0.15, 0.20, 0.7, 0.03])
ax_minpts = plt.axes([0.15, 0.12, 0.7, 0.03])
ax_button = plt.axes([0.4, 0.03, 0.2, 0.05])

# Inicjalizacja komponentów UI
slider_eps = Slider(ax_eps, r'Epsilon ($\epsilon$)', valmin=0.05, valmax=0.5, valinit=0.15, valstep=0.01)
slider_minpts = Slider(ax_minpts, 'MinPts', valmin=2, valmax=15, valinit=5, valfmt='%0.0f')
btn_new_data = Button(ax_button, 'Generuj nowe dane', hovercolor='lightblue')

# --- 4. Główna logika (Aktualizacja Klastrów) ---
def update(val=None):
    """Funkcja przeliczająca klastry DBSCAN i aktualizująca wykres."""
    eps_val = slider_eps.val
    minpts_val = int(slider_minpts.val)

    # Uruchomienie algorytmu DBSCAN
    dbscan = DBSCAN(eps=eps_val, min_samples=minpts_val)
    labels = dbscan.fit_predict(X)

    # Zliczanie klastrów i szumu (szum ma etykietę -1)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)

    # Przypisywanie kolorów i rozmiarów
    # Paleta tab10 dla klastrów
    colors = plt.cm.tab10(labels % 10)
    sizes = np.full(len(labels), 60)   # Domyślny rozmiar

    # Modyfikacja wyglądu dla szumu (-1)
    noise_mask = (labels == -1)
    colors[noise_mask] = [0.4, 0.4, 0.4, 0.5] # Półprzezroczysty szary
    sizes[noise_mask] = 15                    # Mniejszy rozmiar

    # Aktualizacja punktów na wykresie
    scatter.set_facecolor(colors)
    scatter.set_sizes(sizes)

    # Aktualizacja tytułu
    ax.set_title(f'DBSCAN\nZnalezione klastry: {n_clusters} | Punkty szumu: {n_noise}', fontsize=12, fontweight='bold')

    fig.canvas.draw_idle()

def on_new_data(event):
    """Reakcja na kliknięcie przycisku - losuje nowe dane z zachowaniem struktury."""
    global X
    X = generate_data()
    scatter.set_offsets(X)
    update()

# --- 5. Przypisanie zdarzeń i uruchomienie ---
slider_eps.on_changed(update)
slider_minpts.on_changed(update)
btn_new_data.on_clicked(on_new_data)

# Wymuszenie pierwszego narysowania
update()
plt.show()
