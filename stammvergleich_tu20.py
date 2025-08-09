import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Pfad zur Excel-Datei mit mehreren Arbeitsmappen
excel_path = r'/home/thomas/Desktop/bsc/Auswertung_HPLC.xlsx'
output_path = r'/home/thomas/Desktop/bsc/Diagramme/HPLC/Stammvergleich'

# Farben und Marker für die Darstellung
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

# Durchlaufe alle Arbeitsblätter und suche nach Paaren
sheet_names = excel_file.sheet_names
for sheet_name in sheet_names:
    # Überprüfen, ob das Arbeitsblatt mit dem Präfix "Ppta_" beginnt
    if sheet_name.startswith("Ppta_"):
        base_name = sheet_name[5:]  # Entferne das Präfix "Ppta_"

        # Debugging-Ausgabe: Zeige den Basisnamen an
        print(f"Basisname gefunden: '{base_name}' für Arbeitsblatt '{sheet_name}'")

        #Entferne Kommas aus dem Basisnamen, um sicherzustellen, dass der Vergleich funktioniert
        base_name_cleaned = base_name.replace(',', '')  # Entferne Kommas
       # base_name_cleaned = base_name  # Keine Entfernung von Kommas mehr

        # Überprüfen, ob das Basis-Arbeitsblatt existiert
        if base_name_cleaned in [name.replace(',', '') for name in sheet_names]:
            sheet_name_1 = base_name_cleaned  # Basis-Arbeitsblatt ohne Präfix
            sheet_name_2 = sheet_name          # Arbeitsblatt mit Präfix

            # Debugging-Ausgabe
            print(f"Gefundenes Paar: '{sheet_name_1}' und '{sheet_name_2}'")

            # Daten aus den beiden Arbeitsblättern laden
            try:
                df1 = excel_file.parse(sheet_name_1)
                df2 = excel_file.parse(sheet_name_2)
                print(f"Arbeitsblätter '{sheet_name_1}' und '{sheet_name_2}' erfolgreich geladen.")  # Debugging-Ausgabe
            except Exception as e:
                print(f"Fehler beim Laden der Arbeitsblätter '{sheet_name_1}' und '{sheet_name_2}': {e}")
                continue  # Überspringe diese Iteration und gehe zum nächsten Paar


            # Überprüfen, ob die benötigten Spalten vorhanden sind
            if 'time [h]' not in df1.columns or 'time [h]' not in df2.columns:
                print(f"Die Spalte 'time [h]' fehlt in einem der Arbeitsblätter: '{sheet_name_1}' oder '{sheet_name_2}'.")
                continue  # Überspringe diese Iteration und gehe zum nächsten Paar

            # Überprüfen, ob die DataFrames Daten enthalten
            if df1.empty or df2.empty:
                print(f"Die Arbeitsblätter '{sheet_name_1}' oder '{sheet_name_2}' sind leer.")
                continue  # Überspringe diese Iteration und gehe zum nächsten Paar

            # Diagrammtitel aus Zelle A50 lesen (wenn vorhanden)
            diagramm_titel_1 = df1.iloc[49, 0] if len(df1) > 49 and not pd.isna(df1.iloc[49, 0]) else sheet_name_1
            diagramm_titel_2 = df2.iloc[49, 0] if len(df2) > 49 and not pd.isna(df2.iloc[49, 0]) else sheet_name_2

            # Zeitspalte nach unten auffüllen (falls sie Lücken aufweist)
            df1['time [h]'] = df1['time [h]'].ffill()
            df2['time [h]'] = df2['time [h]'].ffill()

            # Konvertiere alle Werte in numerische Werte, nicht-numerische Werte werden zu NaN
            df1 = df1.apply(pd.to_numeric, errors='coerce')
            df2 = df2.apply(pd.to_numeric, errors='coerce')

            # Mittelwerte und Standardabweichungen pro Zeitpunkt und Chemikalie berechnen
            mean_values_1 = df1.groupby('time [h]').mean()
            std_dev_1 = df1.groupby('time [h]').std()
            mean_values_2 = df2.groupby('time [h]').mean()
            std_dev_2 = df2.groupby('time [h]').std()

            # Überprüfen, ob Mittelwerte und Standardabweichungen berechnet wurden
            if mean_values_1.empty or mean_values_2.empty:
                print(f"Keine Mittelwerte für '{sheet_name_1}' oder '{sheet_name_2}' berechnet.")
                continue  # Überspringe diese Iteration und gehe zum nächsten Paar

            # Abschnitt 1: Substanzen aus dem ersten DataFrame darstellen
            fig, ax1 = plt.subplots(figsize=(6, 6))
            ax2 = ax1.twinx()  # Zweite Achse für 2-Butanol vorbereiten

            # Handles und Labels für die Legenden vorbereiten
            substance_handles = {}
            strain_handles = []  # Stelle sicher, dass die Liste leer ist, bevor wir sie füllen

            # Abschnitt 2: Substanzen aus dem ersten DataFrame darstellen
            for column in mean_values_1.columns:
                base_name = column.replace('(TU2.0)', '').replace('(Δaco1)', '').replace('(TU2.0_Ppta)', '').replace(
                    '(Δaco1_Ppta)', '').strip()

                # Nur die Stämme Δaco1 und Δaco1_Ppta nicht plottieren
                if 'Δaco1' in column or 'Δaco1_Ppta' in column:
                #if 'TU2.0' in column or 'TU2.0_Ppta' in column:
                    continue  # Überspringe diese Iteration, wenn der Stamm nicht passt

                linestyle = '-'  # Standardlinienstil
                if '(TU2.0_Ppta)' in column:
                #if '(Δaco1_Ppta)' in column:
                    linestyle = '--'  # Gestrichelte Linie für TU2.0_Ppta
                marker = marker_fix.get(base_name, 'o')
                color = farben_fix.get(base_name, "#d9d9d9")

                x = mean_values_1.index
                y = mean_values_1[column]
                yerr = std_dev_1[column]

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

                # Abschnitt 3: Substanzen aus dem zweiten DataFrame darstellen
                for column in mean_values_2.columns:
                    base_name = column.replace('(TU2.0)', '').replace('(Δaco1)', '').replace('(TU2.0_Ppta)', '').replace('(Δaco1_Ppta)','').strip()

                    # Nur die Stämme Δaco1 und Δaco1_Ppta nicht plottieren
                    if 'Δaco1' in column or 'Δaco1_Ppta' in column:
                    #if 'TU2.0' in column or 'TU2.0_Ppta' in column:
                        continue  # Überspringe diese Iteration, wenn der Stamm nicht passt

                    linestyle = '-'  # Standardlinienstil
                    if '(TU2.0_Ppta)' in column:
                    #if '(Δaco1_Ppta)' in column:
                        linestyle = '--'  # Gestrichelte Linie für TU2.0_Ppta
                    marker = marker_fix.get(base_name, 'o')
                    color = farben_fix.get(base_name, "#d9d9d9")

                    x = mean_values_2.index
                    y = mean_values_2[column]
                    yerr = std_dev_2[column]

                    # 2-Butanol auf zweiter y-Achse darstellen
                    if base_name == "2-Butanol":
                        ax2.errorbar(
                            x, y, yerr=yerr, fmt=marker,
                            color=color, linestyle=linestyle,
                            capsize=3, alpha=0.6, markersize=4, linewidth=1,
                        )
                    else:
                        ax1.errorbar(
                            x, y, yerr=yerr, fmt=marker,
                            color=color, linestyle=linestyle,
                            capsize=3, alpha=0.6, markersize=4, linewidth=1,
                        )

                    # Handle für die Legende erstellen
                    if base_name not in substance_handles:
                        substance_handles[base_name] = mlines.Line2D(
                            [], [], color=color, marker=marker, linestyle=linestyle, label=base_name
                        )

                # Handle für die Legende erstellen
                if base_name not in substance_handles:
                    substance_handles[base_name] = mlines.Line2D(
                        [], [], color=color, marker=marker, linestyle=linestyle, label=base_name
                    )

            # Abschnitt 4: Achsentitel und Diagrammtitel
            ax1.set_xlabel("time (h)", fontsize=12)
            ax1.set_ylabel("concentration (mM)", fontsize=12)
            ax1.set_title(f"comparison of TU2.0 & TU2.0_Ppta ({diagramm_titel_1})", fontsize=12)
            #ax1.set_title(f"comparison of Δaco1 & Δaco1_Ppta ({diagramm_titel_1})", fontsize=14)

            # Abschnitt 5: Legende hinzufügen
            handles = list(substance_handles.values())
            strain_handles = [
            mlines.Line2D([], [], color='black', linestyle='-', label='TU2.0'),
            mlines.Line2D([], [], color='black', linestyle='--', label='TU2.0_Ppta')
            #mlines.Line2D([], [], color='black', linestyle='-', label='Δaco1'),
            #mlines.Line2D([], [], color='black', linestyle='--', label='Δaco1_Ppta')
            ]

            # Kombiniere Handles für die Legende
            all_handles = handles + strain_handles

            # Platz für die Legende schaffen
            fig.subplots_adjust(bottom=0.2)  # Erhöhe den unteren Rand

            # Legende unter dem Diagramm hinzufügen
            ax1.legend(handles=all_handles, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=10, frameon=False)

            # Abschnitt 6: Dezentes Raster einfügen und Rahmen reduzieren
            ax1.grid(True, linestyle='--', linewidth=0.3)
            ax1.spines['right'].set_visible(True)
            ax1.spines['top'].set_visible(True)
            ax2.spines['top'].set_visible(True)
            #ax1.spines['top'].set_visible(False)
            #ax2.spines['top'].set_visible(False)

            # Abschnitt 7: Layout anpassen
            fig.tight_layout()

            # Abschnitt 8: Diagramm als PNG speichern
            output_filename = f"{output_path}/Vergleich_{sheet_name_1}_TU2.0.png"
            #output_filename = f"{output_path}/Vergleich_{sheet_name_1}_aco1.png"
            plt.savefig(output_filename, dpi=300, format='png')
            plt.close()

print(f"Diagramm für die Arbeitsblätter '{sheet_name_1}' und '{sheet_name_2}' wurde erfolgreich erstellt und gespeichert.")