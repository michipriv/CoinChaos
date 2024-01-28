#!/usr/bin/env python3
# -*- coding: utf-8 -*-




import pandas as pd

class Export:
    def __init__(self, data, filename):
        """
        Initialisiert die Export-Klasse.

        Args:
            data (pd.DataFrame): Das DataFrame mit den Daten, das exportiert werden soll.
            filename (str): Der Dateiname für die CSV-Datei.
        """
        self.data = data
        self.filename = filename

    def to_csv(self):
        """
        Exportiert das DataFrame in eine CSV-Datei.
        """
        try:
            self.data.to_csv(self.filename, index=False)
            print(f'Daten wurden erfolgreich in "{self.filename}" exportiert.')
        except Exception as e:
            print(f'Fehler beim Exportieren der Daten: {str(e)}')

