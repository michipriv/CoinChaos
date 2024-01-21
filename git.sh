#!/bin/bash

# Überprüfen des übergebenen Arguments
case "$1" in
    u)  # Code aktualisieren
        git add .
        git commit -m "Update"
        git push
        ;;
    t)  # Tag setzen
        if [ -z "$2" ]; then
            echo "Kein Tag-Name angegeben. Benutzung: ./git.sh t [tagname]"
        else
            git tag -a "$2" -m "Tag gesetzt: $2"
            git push origin "$2"
        fi
        ;;
    *)  # Ungültige Option
        echo "Ungültige Option: $1"
        echo "Benutzung: ./git.sh u (für Update) oder ./git.sh t [tagname] (für Tag setzen)"
        ;;
esac

