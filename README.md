
# Projekt Dokumentation

## Installation der erforderlichen Module

Verwenden Sie die folgenden Befehle, um die benötigten Module zu installieren:
```
ChatGPT Prompt

Verhalte ich wie ein Crypto Trader und Python Entwickler.
Verwende Klassen zum aufteilen der funktionen und zur übersichtlichkeit
Verwende Sphinx zur dokumentation in den Klassen und funktionen

Antworte mit BINGO wenn es klar für dich ist.

pip install python-binance
pip install matplotlib mplfinance
pip install sphinx

```
## Sphinx-Dokumentation
```

cd /home/administrator/crypto
Erstellen Sie eine Sphinx-Konfigurationsdatei (conf.py) im Verzeichnis "docs/source/":
python
Copy code
import os
import sys

sys.path.insert(0, os.path.abspath('/home/administrator/crypto'))
extensions = ['sphinx.ext.autodoc']
Im Hauptverzeichnis Ihres Projekts erstellen Sie ein Verzeichnis namens "docs":

mkdir docs
cd docs
Initialisieren Sie das Dokumentationsprojekt mit Sphinx:

sphinx-quickstart
Erstellen Sie RST-Dateien für Ihre Module mit dem folgenden Befehl (stellen Sie sicher, dass sich Ihr aktuelles Verzeichnis in "docs" befindet):

sphinx-apidoc -o source/ /home/administrator/crypto
Aktualisieren Sie Ihre Dokumentation, indem Sie den folgenden Befehl ausführen (immer noch im "docs"-Verzeichnis):

sphinx-build -b html docs/source/ docs/build/
Das erstellt die HTML-Dokumentation in "docs/build/html". Sie können nun Ihre Dokumentation anzeigen, indem Sie die HTML-Dateien in einem Webbrowser öffnen.
```

##Github

```
Repository am PC initalisieren
git clone https://TOKEN@github.com/michipriv/CoinChaos

Code in Repository speichern
git add .
git commit -m "Update"
git push

Code von Repository holen
git pull


Git Repository
https://github.com/michipriv/CoinChaos
```
