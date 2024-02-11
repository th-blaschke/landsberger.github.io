"""Das untenstehende Skript basiert auf 
https://matplotlib.org/stable/gallery/lines_bars_and_markers/timeline.html#sphx-glr-gallery-lines-bars-and-markers-timeline-py (letzter Zugriff 06.02.2024) 
und wurde in ähnlicher Form bereits in einem Seminar zu "Kunstgeschichtliche Visualisierungsprojekte", 
Dozentin Katharina Hefele, WiSe 2022/2023 im Rahmen eines studentischen Projekt von mir verwendet.
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Einstellen der Schriftgröße der Graphik
matplotlib.rcParams.update({"font.size": 18})
matplotlib.rcParams.update({"axes.titlesize" : 26})

# Einlesen der in einer CSV-Datei gespeicherten Lebensdaten in zwei Listen
df_bio = pd.read_csv("Lebenslauf-Landsberger.csv", encoding="utf-8")
names = df_bio["Ereignis"].to_list()
dates = df_bio["Jahr"].to_list()

# Festlegen von verschiedenen Höhenstufen, in denen die Lebensdaten abhängig von der Achse angezeigt werden
levels = np.tile([-3, 3, -1, 1, -2, 2],
                 int(np.ceil(len(dates)/6)))[:len(dates)]

# Erstellen des plot basierend auf den Jahresangaben
fig, ax = plt.subplots(figsize=(26, 12), constrained_layout=True)
ax.set(title="Lebenslauf Landsberger")

ax.vlines(dates, 0, levels, color="tab:green")  # Einfügen der vertikalen Linien
ax.plot(dates, np.zeros_like(dates), "-o",
        color="k", markerfacecolor="w")  # Einfügen der Baseline und der Marker

# Annotierung
for d, l, r in zip(dates, levels, names):
    ax.annotate(r, xy=(d, l),
                xytext=(-3, np.sign(l)*3), textcoords="offset points",
                horizontalalignment="center",
                verticalalignment="bottom" if l > 0 else "top")

plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# Entfernen der y-Achse und der Spines
ax.yaxis.set_visible(False)
ax.spines[["left", "top", "right"]].set_visible(False)

ax.margins(y=0.3)

# Speichern der Graphik als PNG-Datei
plt.savefig("lebenslauf.png")