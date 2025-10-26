# config.py

# -------------------------------
# Pfade
# -------------------------------
base_path = "/home/thomas/Documents/visualHPLC"

# -------------------------------
# Diagrammeinstellungen
# -------------------------------
fig_size = (6, 6)         # quadratisch
#dpi = 150                 # Auflösung
#legend_location = 'lower center'
#legend_ncol = 2           # Anzahl Spalten in der Legende
#line_width = 1.5
#error_alpha = 0.3         # Transparenz der Fehlerbalken

# -------------------------------
# Farben
# -------------------------------
farben_fix = {
    "2,3-Butanediol": "#1f77b4",
    "Acetate": "#ff7f0e",
    "2-Butanone": "#2ca02c",
    "Propionate": "#d62728",
    "1-Propanol": "#9467bd",
    "Ethylene glycol": "#8c564b",
    "Methanol": "#e377c2",
    "Ethanol": "#7f7f7f",
    "1,2-Propanediol": "#ffcc00",
    "Biomass": "#ff99cc",
    "Propanal": "#bcbd22",
    "Formate": "#00aaff",
    "2-Butanol": "#ff1493"
}

# -------------------------------
# Marker pro Substanz
# -------------------------------
marker_fix = {
    "2,3-Butanediol": 'o',
    "Acetate": 's',
    "2-Butanone": 'D',
    "Propionate": '^',
    "1-Propanol": '<',
    "Ethylene glycol": '>',
    "Methanol": 'p',
    "Ethanol": 'v',
    "1,2-Propanediol": '*',
    "Biomass": 'X',
    "Propanal": 'H',
    "Formate": 'P',  # Neuer Marker
    "2-Butanol": 'P'  # Neuer Marker
}
