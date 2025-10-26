
# DER.PY


**Der.py** ist eine Sammlung von Python-Skripten die ich für die Auswertung bioprozesstechnologischer Messwerte, im Rahmen meiner **BSc-Arbeit** geschrieben habe.
Es automatisiert das Erstellen von **wissenschaftlichen Diagrammen** aus:

- OD600/OD660-Messungen
- HPLC-Daten
- C-Bilanzen

Die Diagramme beinhalten automatisch **Fehlerbalken**, standardisierte Formatierungen und ermöglichen den **direkten Vergleich verschiedener Stämme**, sodass Unterschiede zwischen Wildtyp und modifizierten-Stämmen oder anderen Varianten leicht sichtbar werden.

Alle relevanten Parameter (Farben, Marker, Linienarten, Pfade, Diagrammgröße) werden zentral in der `config.py` verwaltet, während `der.py` die einzelnen Auswertungsscripts nacheinander aufruft.


## Features
- Zentralisierte Konfiguration für Farben, Marker, Linienarten und Diagrammgröße

- Automatisches Erstellen von Output-Ordnern

- Erstellung wissenschaftlicher Diagramme inkl. Fehlerbalken

- Vergleich von verschiedenen Stämmen direkt in den Diagrammen

- Modularer Aufbau: einfache Erweiterung auf neue Analysen

## Voraussetzungen
- Python 3.x
- Eine virtuelle Umgebung (empfohlen)

## Installation
```bash
# Erstelle eine virtuelle Umgebung
python3 -m venv derpy

# Aktiviere die virtuelle Umgebung
source derpy/bin/activate

# Installiere die Abhängigkeiten
pip install -r requirements.txt
```

## Abhängigkeiten
- openpyxl
- matplotlib
- pandas
- numpy
- scipy

## Projektstruktur
```arduino
derpy/
│
├── Rohdaten/
│   ├── Auswertung_CBilanz.xlsx
│   ├── Auswertung_HPLC.xlsx
│   └── Auswertung_OD.xlsx
│
├── config.py
├── requirements.txt
├── der.py
├── Diagramme_OD.py
├── Diagramme_HPLC.py
├── Diagramme_CBilanz.py
├── gesamt_cBilanz.py
├── stammvergleich_daco1.py
└── stammvergleich_tu20.py
```

## Verwendung
Platziere die xlsx-Dateien mit den Rohdaten im Verzeichnis **Rohdaten**. Achte darauf, dass die Dateien denselben Aufbau wie die Beispiel-Dateien (*Auswertung_CBilanz.xlsx*, *Auswertung_HPLC.xlsx*, *Auswertung_OD.xlsx*) haben – am einfachsten passt man die eigenen Daten direkt an diese Dateien an. Passe den Pfad und die Parameter in der **config.py** an, um deine spezifischen Anforderungen zu erfüllen.

Führe nun in der virtuellen Umgebung der.py aus - die benötigten Verzeichnisse für die Diagramme werden automatisch erstellt.

## Warum „DER.PY“?

Der Name leitet sich humorvoll von „Derpiness“ (dt. Dummheit / Tollpatschigkeit) ab und ist gleichzeitig eine Hommage an Derpy Hooves aus My Little Pony.

## Lizenz

MIT – nimm, kopiere, teile, verbessere!

Forks & Pull Requests sind absolut willkommen 💜

Anpassungen an das eigene Projekt, z. B. zur Erweiterung um neue Funktionen, sind ausdrücklich erwünscht.
