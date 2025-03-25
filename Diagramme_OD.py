import pandas as pd
import matplotlib.pyplot as plt

# Pfad zur Excel-Datei mit mehreren Arbeitsmappen
excel_path = r'Pfad'
excel_file = pd.ExcelFile(excel_path)

# Definierte Farben für OD660 und OD600
farben = {
    "OD660": "#4C72B0",  # Bläulichste Farbe
    "OD600": "#DD8452"   # Oranglichste Farbe
}

# Marker für die Darstellung
markers = {
    "OD660": "o",
    "OD600": "s"
}

# Für jede Arbeitsmappe ein Diagramm erstellen
for sheet_name in excel_file.sheet_names:
    # Arbeitsmappe laden
    df = excel_file.parse(sheet_name)

    # Diagrammtitel aus Zelle A50 lesen (wenn vorhanden)
    if len(df) > 49 and not pd.isna(df.iloc[49, 0]):
        diagramm_titel = df.iloc[49, 0]
    else:
        diagramm_titel = sheet_name

    # Zeitspalte nach unten auffüllen (falls sie Lücken aufweist)
    df['time [h]'] = df['time [h]'].ffill()

    # Spalten mit OD660 und (auskommentiert) OD600 auswählen
    columns_to_plot = [col for col in df.columns if "OD660" in str(col)]

    # Auskommentierte Option: OD600 hinzufügen
    #columns_to_plot += [col for col in df.columns if "OD600" in str(col)]

    # Erstelle einen DataFrame mit den ausgewählten Spalten
    df_to_plot = df[['time [h]'] + columns_to_plot]

    # Konvertiere alle Werte in numerische Werte, nicht-numerische Werte werden zu NaN
    df_to_plot = df_to_plot.apply(pd.to_numeric, errors='coerce')

    # Mittelwerte und Standardabweichungen pro Zeitpunkt und Chemikalie berechnen
    mean_values = df_to_plot.groupby('time [h]').mean()
    std_dev = df_to_plot.groupby('time [h]').std()

    # Quadratisches Diagramm erstellen
    plt.figure(figsize=(9, 6))

    # Substanzen darstellen
    for column in mean_values.columns:
        if "OD660" in column:
            color = farben["OD660"]
            marker = markers["OD660"]
        elif "OD600" in column:
            color = farben["OD600"]
            marker = markers["OD600"]
        else:
            continue

        # Linie und Stil festlegen
        if "Δaco1" in column:
            linestyle = "--"  # Gestrichelte Linie für Δaco1
        else:
            linestyle = "-"   # Durchgezogene Linie für andere

        label = column

        # X- und Y-Werte
        x = mean_values.index
        y = mean_values[column]
        yerr = std_dev[column]

        # Fehlerbalken und Linien plotten mit kleineren Markern und dünneren Linien
        plt.errorbar(
            x, y, yerr=yerr, fmt=marker,
            color=color, linestyle=linestyle, capsize=3, label=label,
            alpha=0.6, markersize=4, linewidth=1
        )

    # Achsentitel und Diagrammtitel
    plt.xlabel("time (h)", fontsize=12)
    plt.ylabel("OD$_{660}$", fontsize=12)
    plt.title(diagramm_titel, fontsize=14)

    # Legende unterhalb des Diagramms
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), frameon=False, ncol=2)

    # Dezentes Raster einfügen und Rahmen reduzieren
    plt.grid(True, linestyle='--', linewidth=0.3)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    # Layout anpassen
    plt.tight_layout()

    # Diagramm als PNG speichern
    output_filename = fr"Pfad/OD660_{sheet_name}.png"
    plt.savefig(output_filename, dpi=300, format='png')

    # Diagramm schließen
    plt.close()

print("Diagramme für alle Arbeitsmappen wurden erfolgreich erstellt und gespeichert.")
