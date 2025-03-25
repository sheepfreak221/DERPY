import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Pfad zur Excel-Datei mit mehreren Arbeitsmappen
excel_path = r'Pfad/Auswertung_HPLC.xlsx'
output_path = r'Pfad/Diagramme/HPLC/'

# Farben für farbenblindenfreundliche Darstellung (gleich wie C-Bilanz)
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
    "Biomass": "#17becf",  # Türkis
    "Propanal": "#bcbd22",  # Olivgrün
    "Formate": "#00bfff",  # Cyan
    "2-Butanol": "#ff1493"  # Helles Pink
}

# Marker für Substanzen
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

# Lade die Excel-Datei
excel_file = pd.ExcelFile(excel_path)

# Für jede Arbeitsmappe ein Diagramm erstellen
for sheet_name in excel_file.sheet_names:
    df = excel_file.parse(sheet_name)

    # Diagrammtitel aus Zelle A50 lesen (wenn vorhanden)
    if len(df) > 49 and not pd.isna(df.iloc[49, 0]):
        diagramm_titel = df.iloc[49, 0]
    else:
        diagramm_titel = sheet_name

    # Zeitspalte nach unten auffüllen (falls sie Lücken aufweist)
    df['time [h]'] = df['time [h]'].ffill()

    # Konvertiere alle Werte in numerische Werte, nicht-numerische Werte werden zu NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    # Mittelwerte und Standardabweichungen pro Zeitpunkt und Chemikalie berechnen
    mean_values = df.groupby('time [h]').mean()
    std_dev = df.groupby('time [h]').std()

    # Quadratisches Diagramm erstellen
    fig, ax1 = plt.subplots(figsize=(9, 6))

    # Handles und Labels für die Legenden vorbereiten
    substance_handles = {}
    strain_handles = []

    # Zweite Achse für 2-Butanol vorbereiten
    ax2 = ax1.twinx()
    #y1_lower_limit = ax1.get_ylim()[0]
   # y1_zero_position = y1_lower_limit
    y1_lower_limit = ax1.get_ylim()[0]  # Untere Grenze der y-Achse von ax1
    ax2.set_ylim(0, 0.3)  # Setze die y-Achse von 0 bis 0.3
    #y2_lower_limit = y1_lower_limit + (0.3 - (0 - y1_lower_limit))
    #ax2.spines['left'].set_position(('outward', y1_zero_position))  # Verschiebe die linke Achse nach außen
    #ax2.spines['right'].set_position(('outward', y1_zero_position))  # Verschiebe die rechte Achse nach außen
    #ax2.set_ylim(y1_zero_position, y1_zero_position + 0.3)
    #ax2.set_ylim(y2_lower_limit, y2_lower_limit + 0.3)  # Setze die y-Achse von ax2
    # Erkennung der enthaltenen Stämme
    # Setze die Position des Nullpunkts der zweiten Achse auf die Höhe des Nullpunkts von ax1
    ax2.spines['left'].set_position(
        ('outward', y1_lower_limit))  # Verschiebe die linke Achse auf die Höhe des Nullpunkts von ax1
    ax2.spines['right'].set_position(
        ('outward', y1_lower_limit))  # Verschiebe die rechte Achse auf die Höhe des Nullpunkts von ax1

    # Optional: Wenn du eine horizontale Linie für den Nullpunkt der 2-Butanol-Achse zeichnen möchtest
    ax2.axhline(y=y1_lower_limit, color='pink', linestyle='--', linewidth=1)  # Horizontale Linie für 2-Butanol
    strains_in_sheet = set()
    for column in mean_values.columns:
        if '(TU2.0)' in column:
            strains_in_sheet.add('TU2.0')
        elif '(Δaco1)' in column:
            strains_in_sheet.add('Δaco1')
        elif '(TU2.0_Ppta)' in column:
            strains_in_sheet.add('TU2.0_Ppta')
        elif '(Δaco1_Ppta)' in column:
            strains_in_sheet.add('Δaco1_Ppta')

    # Substanzen mit festen Farben und Markern darstellen
    for column in mean_values.columns:
        base_name = column.replace('(TU2.0)', '').replace('(Δaco1)', '').replace('(TU2.0_Ppta)', '').replace('(Δaco1_Ppta)', '').strip()
        if '(TU2.0)' in column or '(TU2.0_Ppta)' in column:
            linestyle = '-'
        elif '(Δaco1)' in column or '(Δaco1_Ppta)' in column:
            linestyle = '--'
        else:
            linestyle = '-'

        marker = marker_fix.get(base_name, 'o')
        color = farben_fix.get(base_name, "#d9d9d9")

        x = mean_values.index
        y = mean_values[column]
        yerr = std_dev[column]

        # 2-Butanol auf zweiter y-Achse darstellen
        if base_name == "2-Butanol":
            ax2.errorbar(
                x, y, yerr=yerr, fmt=marker,
                color=color, linestyle=linestyle,
                capsize=3, alpha=0.6, markersize=4, linewidth=1,
            )
            ax2.set_ylabel("2-Butanol (mM)", fontsize=12, color=color)
            ax2.tick_params(axis='y', labelcolor=color)
        else:
            ax1.errorbar(
                x, y, yerr=yerr, fmt=marker,
                color=color, linestyle=linestyle,
                capsize=3, alpha=0.6, markersize=4, linewidth=1,
            )

        if base_name not in substance_handles:
            substance_handles[base_name] = mlines.Line2D(
                [], [], color=color, marker=marker, linestyle='-', label=base_name
            )

    # Legende für Substanzen
    legend_substances = ax1.legend(
        handles=list(substance_handles.values()),
        loc='upper center',
        bbox_to_anchor=(0.5, -0.13),
        frameon=False,
        ncol=4
    )
    ax1.add_artist(legend_substances)

    # Separate Legende für die Stämme
    strain_styles = {
        'TU2.0': ('black', '-'),
        'Δaco1': ('black', '--'),
        'TU2.0_Ppta': ('black', '-'),
        'Δaco1_Ppta': ('black', '--')
    }
    for strain, (color, linestyle) in strain_styles.items():
        if strain in strains_in_sheet:
            strain_handles.append(mlines.Line2D([], [], color=color, linestyle=linestyle, label=strain))

    legend_strains = ax1.legend(
        handles=strain_handles,
        loc='upper center',
        bbox_to_anchor=(0.5, -0.25),
        frameon=False,
        fontsize=10,
        ncol=2
    )

    # Achsentitel und Diagrammtitel
    ax1.set_xlabel("time (h)", fontsize=12)
    ax1.set_ylabel("concentration (mM)", fontsize=12)
    ax1.set_title(diagramm_titel, fontsize=14)

    # Dezentes Raster einfügen und Rahmen reduzieren
    ax1.grid(True, linestyle='--', linewidth=0.3)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    # Layout anpassen
    fig.tight_layout()

    # Diagramm als PNG speichern
    output_filename = f"{output_path}/HPLC_{sheet_name}.png"
    plt.savefig(output_filename, dpi=300, format='png')
    plt.close()

print("Diagramme für alle Arbeitsmappen wurden erfolgreich erstellt und gespeichert.")
