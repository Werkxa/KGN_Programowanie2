import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error

# --- 1. Generowanie nieliniowych danych z szumem ---
np.random.seed(42)
# Generujemy 30 punktów w przedziale od -3 do 3
X = np.sort(np.random.uniform(-3, 3, 30))[:, np.newaxis]
# Prawdziwa funkcja: fragment sinusoidy plus lekki trend kwadratowy i szum Gaussa
y = np.sin(2 * X).ravel() + 0.5 * X.ravel()**2 + np.random.normal(0, 0.5, 30)

# Gęsta siatka punktów x do narysowania gładkiej krzywej predykcji
# Zakres jest celowo nieco szerszy (-3.5 do 3.5), aby pokazać zjawisko Rungego na brzegach
X_plot = np.linspace(-3.5, 3.5, 500)[:, np.newaxis]

# --- 2. Konfiguracja okna i wykresu ---
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25) # Zostawiamy miejsce na suwak na dole

# Rysujemy surowe dane treningowe
ax.scatter(X, y, color='black', s=40, label='Dane treningowe', zorder=5)

# Inicjalizacja pustej linii reprezentującej model
line, = ax.plot(X_plot, np.zeros_like(X_plot), color='red', linewidth=2.5, label='Krzywa modelu')

# Blokujemy osie na stałe, aby podczas oscylacji wielomianów wysokiego stopnia
# wykres nie "odjeżdżał" w nieskończoność i łatwiej było zaobserwować błędy na brzegach
ax.set_xlim(-3.6, 3.6)
ax.set_ylim(-2, 7)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper right')

# Pole tekstowe do wyświetlania błędu treningowego
error_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                     fontsize=12, verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# --- 3. Konfiguracja interfejsu (Suwak) ---
ax_slider = plt.axes([0.15, 0.1, 0.7, 0.04])
slider = Slider(
    ax=ax_slider,
    label='Stopień wielomianu',
    valmin=1,
    valmax=15,
    valinit=1,
    valstep=1,
    color='cornflowerblue'
)

# --- 4. Główna logika (Aktualizacja modelu) ---
def update(val):
    degree = int(slider.val)

    # Tworzenie modelu: Połączenie generowania cech wielomianowych i regresji liniowej
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())

    # Trenowanie modelu
    model.fit(X, y)

    # Predykcje dla gładkiej krzywej (do rysowania)
    y_plot_pred = model.predict(X_plot)

    # Predykcje dla danych treningowych (do obliczenia błędu)
    y_train_pred = model.predict(X)
    mse = mean_squared_error(y, y_train_pred)

    # Aktualizacja elementów wykresu
    line.set_ydata(y_plot_pred)
    error_text.set_text(f'Błąd treningowy (MSE): {mse:.2f}')
    ax.set_title(f'Regresja Wielomianowa\nZjawisko dopasowania do krzywej (Stopień: {degree})', fontsize=14)

    # Wymuszenie odświeżenia widoku
    fig.canvas.draw_idle()

# --- 5. Uruchomienie ---
update(1) # Wywołujemy raz dla stanu początkowego
slider.on_changed(update) # Podpinamy aktualizację pod ruch suwaka
plt.show()
