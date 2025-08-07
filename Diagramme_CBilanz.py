import openpyxl
import matplotlib.pyplot as plt
import os

# Pfad zur Excel-Datei und Speicherpfad für die Diagramme
excel_datei = r'/home/thomas/Desktop/bsc/Auswertung_CBilanz.xlsx'
speicherpfad = r"/home/thomas/Desktop/bsc/Diagramme/C-Bilanz/"

# Ordner für Diagramme erstellen, falls nicht vorhanden
if not os.path.exists(speicherpfad):
    os.makedirs(speicherpfad)

# Wissenschaftlich bevorzugte Farben
farben_fix = {
    "2,3-Butanediol": "#1f77b4",  # Blau
    "Acetate": "#ff7f0e",  # Orange
    "2-Butanone": "#2ca02c",  # Grün
    "Propionate": "#d62728",  # Rot
    "1-Propanol": "#9467bd",  # Violett
    "Ethylene glycol": "#8c564b",  # Braun
    "Methanol": "#e377c2",  # Pink
    "Ethanol": "#7f7f7f",  # Grau
    "1,2-Propanediol": "#ffcc00",  # Dunkelgelb
    "Biomass": "#ff99cc",  # Helles Rosa
    "Propanal": "#bcbd22",  # Olivgrün
    "Formate": "#00aaff",  # Helles Blau
    "2-Butanol": "#ff1493"  # Helles Pink
}

# Funktion zum Abrufen einer Farbe für eine Substanz
def get_color(substanz):
    return farben_fix.get(substanz, "#d9d9d9")

# Arbeitsmappe öffnen
wb = openpyxl.load_workbook(excel_datei, data_only=True)

# Durch jedes Blatt iterieren
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]

    # Diagrammtitel aus Zelle B18 lesen
    diagramm_titel = sheet["B18"].value or sheet_name

    # Daten aus Zeile 30 (Werte) und Zeile 21 (Standardabweichungen) abrufen und filtern
    werte = [float(cell.value or 0) for cell in sheet[30][1:]]  # Zeile 30, Spalten ab 2
    stdabweichungen = [float(cell.value or 0) for cell in sheet[21][1:]]  # Zeile 21, Spalten ab 2
    spaltennamen = [cell.value for cell in sheet[1][1:]]  # Spaltennamen in Zeile 1

    # Werte und Spaltennamen filtern: Nur Werte > 0 behalten
    gefilterte_werte = [
        (wert, std, spaltenname)
        for wert, std, spaltenname in zip(werte, stdabweichungen, spaltennamen)
        if wert > 0
    ]

    # Aufteilen in TU2.0, Δaco1, TU2.0_Ppta und Δaco1_Ppta basierend auf gefilterten Werten
    tu2_werte = [(wert, std, name) for wert, std, name in gefilterte_werte if '(TU2.0)' in name]
    delta_werte = [(wert, std, name) for wert, std, name in gefilterte_werte if '(Δaco1)' in name]
    tu2_ppta_werte = [(wert, std, name) for wert, std, name in gefilterte_werte if '(TU2.0_Ppta)' in name]
    delta_ppta_werte = [(wert, std, name) for wert, std, name in gefilterte_werte if '(Δaco1_Ppta)' in name]

    # Diagrammerstellung basierend auf TU2.0, Δaco1, TU2.0_Ppta und Δaco1_Ppta Werten
    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)

    # Gestapelte Balken erstellen
    bottom_tu2 = 0
    bottom_delta = 0
    bottom_tu2_ppta = 0
    bottom_delta_ppta = 0
    handles = []
    labels = []

    for wert, std, name in tu2_werte:
        farbe = get_color(name.replace(' (TU2.0)', ''))
        bar_tu2 = ax.bar("TU2.0", wert, bottom=bottom_tu2, color=farbe, alpha=0.9)
        if std > 0:  # Fehlerbalken oben an den Balken
            ax.errorbar(
                x="TU2.0",
                y=bottom_tu2 + wert,
                yerr=std,
                fmt='none',
                ecolor='black',
                elinewidth=0.8,
                alpha=0.5,
                capsize=3
            )
        bottom_tu2 += wert
        if name.replace(' (TU2.0)', '') not in labels:
            handles.append(bar_tu2[0])
            labels.append(name.replace(' (TU2.0)', ''))

    for wert, std, name in delta_werte:
        farbe = get_color(name.replace(' (Δaco1)', ''))
        bar_delta = ax.bar("Δaco1", wert, bottom=bottom_delta, color=farbe, alpha=0.9)
        if std > 0:  # Fehlerbalken oben an den Balken
            ax.errorbar(
                x="Δaco1",
                y=bottom_delta + wert,
                yerr=std,
                fmt='none',
                ecolor='black',
                elinewidth=0.8,
                alpha=0.5,
                capsize=3
            )
        bottom_delta += wert

    for wert, std, name in tu2_ppta_werte:
        farbe = get_color(name.replace(' (TU2.0_Ppta)', ''))
        bar_tu2_ppta = ax.bar("TU2.0_Ppta", wert, bottom=bottom_tu2_ppta, color=farbe, alpha=0.9)
        if std > 0:  # Fehlerbalken oben an den Balken
            ax.errorbar(
                x="TU2.0_Ppta",
                y=bottom_tu2_ppta + wert,
                yerr=std,
                fmt='none',
                ecolor='black',
                elinewidth=0.8,
                alpha=0.5,
                capsize=3
            )
        bottom_tu2_ppta += wert
        if name.replace(' (TU2.0_Ppta)', '') not in labels:
            handles.append(bar_tu2_ppta[0])
            labels.append(name.replace(' (TU2.0_Ppta)', ''))

    for wert, std, name in delta_ppta_werte:
        farbe = get_color(name.replace(' (Δaco1_Ppta)', ''))
        bar_delta_ppta = ax.bar("Δaco1_Ppta", wert, bottom=bottom_delta_ppta, color=farbe, alpha=0.9)
        if std > 0:  # Fehlerbalken oben an den Balken
            ax.errorbar(
                x="Δaco1_Ppta",
                y=bottom_delta_ppta + wert,
                yerr=std,
                fmt='none',
                ecolor='black',
                elinewidth=0.8,
                alpha=0.5,
                capsize=3
            )
        bottom_delta_ppta += wert
        if name.replace(' (Δaco1_Ppta)', '') not in labels:
            handles.append(bar_delta_ppta[0])
            labels.append(name.replace(' (Δaco1_Ppta)', ''))

        # Diagrammeinstellungen und Speichern
    ax.set_title(diagramm_titel, fontsize=14, family='sans-serif')
    ax.set_ylabel("Carbon Equivalents (Cmol$_{produced}$/Cmol$_{consumed}$)", fontsize=12, family='sans-serif')
    ax.legend(handles=handles, labels=labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    plt.xticks(rotation=45, ha='right', fontsize=10, family='sans-serif')
    plt.yticks(fontsize=10, family='sans-serif')
    plt.tight_layout()
    plt.savefig(os.path.join(speicherpfad, f"C-Bilanz_{sheet_name}.png"), bbox_inches='tight')
    plt.close()

print("Diagramme erfolgreich erstellt und gespeichert.")
