
# Projekt Dokumentation

## Installation der erforderlichen Module

Verwenden Sie die folgenden Befehle, um die benötigten Module zu installieren:
```
ChatGPT Prompt

Verhalte ich wie ein Crypto Trader und Python Entwickler.
Verwende Klassen zum aufteilen der funktionen und zur übersichtlichkeit
Verwende Sphinx zur dokumentation in den Klassen und funktionen
Antworte mit BINGO wenn es klar für dich ist.

Programme
Spyder          https://www.spyder-ide.org/
Anaconda        https://www.anaconda.com/download
sqlitebrowser   https://sqlitebrowser.org/dl/

für Linux:
pip install python-binance
pip install matplotlib mplfinance
pip install sphinx


Für Windows
Anaconda installieren und darüber Spyder starten
ansonstne sind die libs hier nicht inkludiert

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

Mainfile und klassen hinzufügen für die verarbeitung
sphinx-apidoc -o sdocs/source/ /home/administrator/crypto
sphinx-apidoc -o docs/source/ classes/

Aktualisieren Sie Ihre Dokumentation, indem Sie den folgenden Befehl ausführen

im Hauptverz. ~/crypto
sphinx-build -b html docs/source/ docs/build/


Das erstellt die HTML-Dokumentation in "docs/build/html". Sie können nun Ihre Dokumentation anzeigen, 
indem Sie die HTML-Dateien in einem Webbrowser öffnen.
=======
Das erstellt die HTML-Dokumentation in "docs/build/html". Sie können nun Ihre Dokumentation anzeigen, indem Sie die HTML-Dateien in einem Webbrowser öffnen.
```

##Github
```

für spyder in der Console:
Code commit zu github

import subprocess; subprocess.run(["./git.sh", "u"])

Neues Tag setzen

import subprocess; subprocess.run(["./git.sh", "t", "v1.0.0"])



# Neues Repo auschecken

Repository am PC initalisieren
git clone https://TOKEN@github.com/michipriv/CoinChaos
git checkout branch-name





Code in Repository speichern
git add .
git commit -m "Update"
git push

Code von Repository holen
git pull

Branch erstellen
ein Branch wird für zwischenduch (intern) beim Entwickeln verwendet ununterstützend kanna auch parallel entwicklungen 
git checkout -b 03-further
git add .
git commit -m "new branch"
git push origin 03-further
git push --set-upstream origin 03-further


Tag erstellen (das hier verwenden zum üben)
EIn Tag wird für finanle oder bestimmte Revisionen (extern) die weitergeeben werden verwendet
git tag -a v1.0. -m "Mein Release 1.0.0"
git push origin v1.0



Git Repository
https://github.com/michipriv/CoinChaos



debian subsystem auf win10

in Powersehll als Admin
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
wsl --set-default-version 2

im Microsoft store debian installieren
aufruf über die windows zeile: debian

```
