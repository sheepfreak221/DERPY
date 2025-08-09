import openpyxl
import matplotlib.pyplot as plt
import os
import numpy as np

# Pfad zur Excel-Datei und Speicherpfad für das Diagramm
excel_datei = r'/home/thomas/Desktop/bsc/Auswertung_CBilanz.xlsx'
speicherpfad = r"/home/thomas/Desktop/bsc/Diagramme/C-Bilanz/gesamt"

title = "Total C-Balance from ADH4 Tests"

# Ordner für Diagramme erstellen, falls nicht vorhanden
if not os.path.exists(speicherpfad):
    os.makedirs(speicherpfad)

# Wissenschaftlich bevorzugte Farben
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


def get_color(substanz):
    return farben_fix.get(substanz, "#d9d9d9")


# Arbeitsmappe öffnen
wb = openpyxl.load_workbook(excel_datei, data_only=True)

# Diagrammerstellung
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
handles = []
labels = []

# Nummerierung der gestapelten Balken
balkennummern = [str(i) for i in range(1, 31)]
index = 0

# Durch jedes Blatt iterieren und Werte separat im Diagramm darstellen
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]

    werte = [float(cell.value or 0) for cell in sheet[30][1:]]
    stdabweichungen = [float(cell.value or 0) for cell in sheet[21][1:]]
    spaltennamen = [cell.value for cell in sheet[1][1:]]

    bottom = {"TU2.0": 0, "Δaco1": 0, "TU2.0_Ppta": 0, "Δaco1_Ppta": 0}

    for key in bottom.keys():
        stapel_name = balkennummern[index]
        hat_wert = False

        for wert, std, name in zip(werte, stdabweichungen, spaltennamen):
            if wert > 0 and f"({key})" in name:
                substanz = name.split(" (")[0]
                farbe = get_color(substanz)
                bars = ax.bar(stapel_name, wert, bottom=bottom[key], color=farbe, alpha=0.9)
                hat_wert = True

                if std > 0:
                    ax.errorbar(stapel_name, bottom[key] + wert, yerr=std, fmt='none', ecolor='black',
                                elinewidth=0.8, alpha=0.5, capsize=3)

                bottom[key] += wert

                if substanz not in labels:
                    handles.append(bars[0])
                    labels.append(substanz)

        if hat_wert:
            index += 1

ax.axhline(y=1, color='red', linestyle='--', label='y = 1')  # Horizontale Linie bei y=1

# Diagrammeinstellungen
ax.set_title(title, fontsize=14, family='sans-serif')
ax.set_ylabel("Carbon Equivalents (${Cmol_{product}/Cmol_{consumed}}$)", fontsize=12, family='sans-serif')
ax.legend(handles=handles, labels=labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
plt.xticks(rotation=0, ha='right', fontsize=10, family='sans-serif')
plt.yticks(fontsize=10, family='sans-serif')
plt.tight_layout()

# Speichern
plt.savefig(os.path.join(speicherpfad, "C-Bilanz_Gesamt.png"), bbox_inches='tight')
plt.close()

print("Gesamtdiagramm erfolgreich erstellt und gespeichert.")
