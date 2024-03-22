import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.patches import Circle
import pandas as pd
import os

# Parámetros
Radio_star = 10
while True:
    try:
        Rpf = float(input("Agrega el radio del planeta con respecto al radio de la estrella: "))
    except ValueError:
        print("Debes escribir un número positivo entre 0.01 y 0.4")
        continue

    if Rpf < 0.01:
        print("Debes escribir un número positivo entre 0.01 y 0.4")
        continue
    else:
        if Rpf > 0.4:
            print("Debe ser un número menor a 0.4")
            continue
        else:
            break

Radio_planet = Rpf * Radio_star

while True:
    try:
        R_orbf = float(input("Agrega el radio orbital del planeta: "))
    except ValueError:
        print("Debes escribir un número positivo entre 2 y 10")
        continue

    if R_orbf < 2:
        print("Debes escribir un número positivo entre 2 y 10")
        continue
    else:
        if R_orbf > 10:
            print("Debe ser un número menor a 10")
            continue
        else:
            break

Orbita = R_orbf * Radio_star

Pasos = 800

while True:
    try:
        Angulo_inclinacion = float(input("Agrega el ángulo de inclinación del planeta (en grados): "))
    except ValueError:
        print("Debes escribir un número entre -90 y 90.")
        continue

    if -90 <= Angulo_inclinacion <= 90:
        break
    else:
        print("El ángulo de inclinación debe estar entre 0 y 90 grados.")

Caja = 1.5 * Orbita
Inclinacion = np.radians(90 + Angulo_inclinacion)

def area_interseccion_circulos(x1, y1, r1, x2, y2, z1, r2):
    d = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    if d >= r1 + r2:  # No hay intersección
        return 0
    elif d <= abs(r1 - r2) and z1 < 0:  # El círculo 2 está completamente dentro del círculo 1
        return np.pi * (r2**2)
    elif d <= abs(r1 - r2) and z1 >= 0:  # El círculo 1 tapa completamente al círculo 2
        return 0
    else:  # Hay intersección
        a = (r1**2 - r2**2 + d**2) / (2 * d)
        h = np.sqrt(r1**2 - a**2)
        term1 = r1**2 * np.arccos((d**2 + r1**2 - r2**2) / (2 * d * r1))
        term2 = r2**2 * np.arccos((d**2 + r2**2 - r1**2) / (2 * d * r2))
        term3 = 0.5 * np.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
        return term1 + term2 - term3

# Crear la figura y los ejes para tres subgráficas
fig, axs = plt.subplots(2, 1, figsize=(10, 15))  # Modificación aquí para crear 4 subgráficas

# Configurar la primera subgráfica (axs[0]) para la animación
axs[0].set_xlim(-1 * Caja, Caja)
axs[0].set_ylim(-1 * Caja, Caja)
axs[0].set_aspect('equal')
circle_central = plt.Circle((0, 0), Radio_star, color='yellow')
axs[0].add_artist(circle_central)
circle = plt.Circle((-1 * Orbita, 0), Radio_planet, color='red')
axs[0].add_artist(circle)
time_text = axs[0].text(0.05, 0.95, '', transform=axs[0].transAxes, color='black')

# Leer los datos adicionales
os.chdir("C:\\Users\\Administrador\\Downloads")
workbook1= "kplr008191672-2009231120729_slc_t1.csv"
df = pd.read_csv(workbook1)
# Definir los límites del corte
cut_limits = [(210, 211)]

# Inicializar una lista para almacenar los puntos dentro del rango
puntos_dentro_rango = []

# Iterar sobre los límites de corte
for x_min, x_max in cut_limits:
    # Filtrar los puntos dentro del rango
    mask = (df['200.324688'] >= x_min) & (df['200.324688'] <= x_max)
    puntos_dentro_rango.extend(df.loc[mask, '6.15E+04'])

# Calcular el promedio de los puntos dentro del rango
promedio = sum(puntos_dentro_rango) / len(puntos_dentro_rango)
print("El promedio de los puntos entre 210 y 211 es:", promedio)

cut_limites = [(202.738, 206.262), (206.262, 209.9), (209.9, 213.312), (213.312, 216.837), (216.837, 220.362)]

# Inicializar una lista para almacenar los mínimos de cada intervalo
minimos_por_intervalo = []

# Iterar sobre los límites de corte
for x_min, x_max in cut_limites:
    # Filtrar los puntos dentro del intervalo
    mask = (df['200.324688'] >= x_min) & (df['200.324688'] < x_max)
    intervalo = df.loc[mask, '6.15E+04']
    # Encontrar el mínimo del intervalo y agregarlo a la lista
    minimo_intervalo = intervalo.min()
    minimos_por_intervalo.append(minimo_intervalo)

# Calcular el promedio de los mínimos de los intervalos
promedio_de_minimos = sum(minimos_por_intervalo) / len(minimos_por_intervalo)

print("Los mínimos de cada intervalo son:", minimos_por_intervalo)
print("El promedio de los mínimos de los intervalos es:", promedio_de_minimos)



# Superponer la segunda y la cuarta gráfica
axs[1].set_xlim(0, Pasos)
axs[1].set_ylim(98, 101)
axs[1].set_xlabel('Tiempo')
axs[1].set_ylabel('Brillo (%)')
area_dif_values = []
line, = axs[1].plot([], [], 'r-')
moving_circle = Circle((0, 100), 0.1, color='blue')
axs[1].add_patch(moving_circle)

# Graficar los datos de Kepler sobre la segunda gráfica
cut_limits = [(209.9, 213.312)]
for x_min, x_max in cut_limits:
    mask2 = (df['200.324688'] >= x_min) & (df['200.324688'] <= x_max)
    df_cut = df[mask2]
    # Escalar los datos de Kepler para que 62000 sea el 100% de brillo
    brightness_scaled = df_cut['6.15E+04'] / 61361 * 100
    axs[1].scatter((df_cut['200.324688'] - x_min) / (x_max - x_min) * Pasos, brightness_scaled, label=f'({x_min}, {x_max})', color='green')


# Agrega leyenda
axs[1].legend()

def init():
    circle.set_center((-1 * Orbita, 0))
    time_text.set_text('')
    line.set_data([], [])
    moving_circle.center = (0, 100)
    return circle, circle_central, time_text, line,  moving_circle

def animate(frame):
    x = np.cos(0.5*np.pi + 2 * np.pi * frame / Pasos) * Orbita
    y = np.sin(0.5*np.pi + 2 * np.pi * frame / Pasos) * Orbita * np.cos(Inclinacion)
    z = np.sin(0.5*np.pi + 2 * np.pi * frame / Pasos) * Orbita
    circle.set_center((x, y))
    if z > 0:
        circle.set_zorder(0)
        circle_central.set_zorder(1)
        area_diferencia = 100
    else:
        circle.set_zorder(1)
        circle_central.set_zorder(0)
        area_diferencia = 100 * (1 - (area_interseccion_circulos(0, 0, Radio_star, x, y, z, Radio_planet)) / (np.pi * Radio_star**2))
    time_text.set_text('Brillo: {}'.format(area_diferencia))
    area_dif_values.append(area_diferencia)
    frames = list(range(len(area_dif_values)))
    line.set_data(frames, area_dif_values)
    if len(area_dif_values) > 0:
        moving_circle.center = (frame, area_dif_values[-1])
    else:
        moving_circle.center = (frame, 100)  # Valor de y predeterminado si area_dif_values está vacío
    return circle, circle_central, time_text, line, moving_circle

ani = animation.FuncAnimation(fig, animate, frames=Pasos, interval=1, init_func=init, blit=False, repeat=True)

plt.tight_layout()
plt.show()
