import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Pfad zur Excel-Datei mit mehreren Arbeitsmappen
excel_path = r'/home/thomas/Desktop/bsc/Auswertung_HPLC.xlsx'
output_path = r'/home/thomas/Desktop/bsc/Diagramme/HPLC'

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

remove_OD660 = False

# Für jede Arbeitsmappe ein Diagramm erstellen
for sheet_name in excel_file.sheet_names:
    df = excel_file.parse(sheet_name)

    # Diagrammtitel aus Zelle A50 lesen (wenn vorhanden)
    if len(df) > 49 and not pd.isna(df.iloc[49, 0]):
        diagramm_titel = df.iloc[49, 0]
    else:
        diagramm_titel = sheet_name

    # Zeitspalte nach unten auffüllen
    df['time [h]'] = df['time [h]'].ffill()

    # Konvertieren zu numerischen Werten
    df = df.apply(pd.to_numeric, errors='coerce')

    # Mittelwerte & Standardabweichungen
    mean_values = df.groupby('time [h]').mean()
    std_dev = df.groupby('time [h]').std()

    # Plot vorbereiten
    fig, ax = plt.subplots(figsize=(6, 6))
    ax2 = ax.twinx()  # zweite Y-Achse

    # Farbe der zweiten Achse für 2-Butanol
    ax2.tick_params(axis='y', colors='#ff1493')
    ax2.spines['right'].set_color('#ff1493')
    ax2.yaxis.label.set_color('#ff1493')

    # Handles für Legenden
    substance_handles = {}
    strain_handles = []

    # Erkennung der enthaltenen Stämme
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

    # Stile für Stämme
    strain_styles = {
        'TU2.0': ('black', '-'),
        'Δaco1': ('black', '--'),
        'TU2.0_Ppta': ('black', '-'),
        'Δaco1_Ppta': ('black', '--')
    }

    # Plotten
    for column in mean_values.columns:
        base_name = column.replace('(TU2.0)', '').replace('(Δaco1)', '').replace('(TU2.0_Ppta)', '').replace('(Δaco1_Ppta)', '').strip()

        # Falls OD660 raus soll, überspringen
        if remove_OD660 and "OD660" in base_name:
            continue

        # Stammansatz bestimmen
        if '(TU2.0)' in column:
            strain = 'TU2.0'
        elif '(Δaco1)' in column:
            strain = 'Δaco1'
        elif '(TU2.0_Ppta)' in column:
            strain = 'TU2.0_Ppta'
        elif '(Δaco1_Ppta)' in column:
            strain = 'Δaco1_Ppta'
        else:
            strain = None

        linestyle = strain_styles.get(strain, ('black', '-'))[1]
        marker = marker_fix.get(base_name, 'o')
        color = farben_fix.get(base_name, "#d9d9d9")

        x = mean_values.index
        y = mean_values[column]
        yerr = std_dev[column]

        # Für 2-Butanol zweite Achse verwenden
        target_ax = ax2 if base_name == "2-Butanol" else ax

        target_ax.errorbar(
            x, y, yerr=yerr, fmt=marker,
            color=color, linestyle=linestyle,
            capsize=3, alpha=0.6, markersize=4, linewidth=1,
        )

        # Substanzen-Legende nur einmalig hinzufügen
        if base_name not in substance_handles:
            substance_handles[base_name] = mlines.Line2D(
                [], [], color=color, marker=marker, linestyle='-', label=base_name
            )

    # Legende für Substanzen
    legend_substances = ax.legend(
        handles=list(substance_handles.values()),
        loc='upper center',
        bbox_to_anchor=(0.5, -0.13),
        frameon=False,
        ncol=4
    )
    ax.add_artist(legend_substances)

    # Legende für Stämme
    for strain, (color, linestyle) in strain_styles.items():
        if strain in strains_in_sheet:
            strain_handles.append(mlines.Line2D([], [], color=color, linestyle=linestyle, label=strain))

    ax.legend(
        handles=strain_handles,
        loc='upper center',
        bbox_to_anchor=(0.5, -0.25),
        frameon=False,
        fontsize=10,
        ncol=2
    )

    # Achsen-Beschriftung & Titel
    ax.set_xlabel("time [h]")
    ax.set_ylabel("concentration (mM)")
    ax2.set_ylabel("2-Butanol (mM)", color='#ff1493')
    ax.set_title(diagramm_titel)

    # Layout & Anzeige
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    plt.tight_layout()
    # Diagramm als PNG speichern
    output_filename = f"{output_path}/HPLC_{sheet_name}.png"
    plt.savefig(output_filename, dpi=300, format='png')
    plt.close()

print("Diagramme für alle Arbeitsmappen wurden erfolgreich erstellt und gespeichert.")
