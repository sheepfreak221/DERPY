#!/usr/bin/env python3
import subprocess
import os

# Liste der Scripts, die ausgeführt werden sollen
scripts = [
    "Diagramme_OD.py",
    "Diagramme_HPLC.py",
    "Diagramme_CBilanz.py",
    "gesamt_cBilanz.py",
    "stammvergleich_tu20.py",
    "stammvergleich_daco1.py"
]

print("=== Starte Auswertung der Rohdaten===\n")

for script in scripts:
    path = os.path.join(os.path.dirname(__file__), script)
    print(f"Führe {script} aus...")
    try:
        # Ruft das Script mit Python auf
        subprocess.run(["python3", path], check=True)
        print(f"✅  {script} erfolgreich abgeschlossen.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌  Fehler in {script}: {e}\n")

print("=== Alle Auswertungen abgeschlossen!  ===")