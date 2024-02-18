# -*- coding: utf-8 -*-

import os
import sqlite3

class CoinChaosDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)

    def install(self):
        """
        Erstellt die Datenbank im angegebenen Pfad, falls sie noch nicht existiert.
        Die Methode überprüft zunächst, ob der Pfad existiert, und erstellt den Pfad, falls nicht.
        Anschließend wird eine SQLite-Datenbankdatei erstellt, falls sie noch nicht existiert
        und erstellt die Tabelle 'coin_data', falls sie nicht existiert.
        """
        # Überprüfen, ob das Verzeichnis existiert, und bei Bedarf erstellen
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))
        
        # Verbindung zur Datenbank herstellen
       
        print(f'Datenbank {self.db_path} wurde erfolgreich erstellt/verbunden.')
        
        # Cursor erstellen
        c = self.conn.cursor()
        
        
        ### Kerzen Kurs daten
        # Tabelle 'coin_data' löschen, falls sie existiert
        c.execute("DROP TABLE IF EXISTS coin_data")
        
        # Tabelle 'coin_data' erstellen
        c.execute("""
            CREATE TABLE IF NOT EXISTS coin_data (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                coin TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                timeunix INTEGER NOT NULL,
                timestd DATETIME NOT NULL,
                open_price REAL NOT NULL,
                high_price REAL NOT NULL,
                low_price REAL NOT NULL,
                close_price REAL NOT NULL,
                volume REAL NOT NULL
            );
        """)
        
        ### Kerzen Farbe grün oder rot
        
        c.execute("DROP TABLE IF EXISTS kerzenfarbe")
    
        # Tabelle 'kerzenfarbe' erstellen
        c.execute("""
            CREATE TABLE IF NOT EXISTS kerzenfarbe (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                pk_coin_data INTEGER NOT NULL,
                kerze TEXT NOT NULL CHECK(kerze IN ('green', 'red')),
                FOREIGN KEY(pk_coin_data) REFERENCES coin_data(pk)
            );
        """)
        
        # Lösche die Tabelle 'vector_candles', falls sie existiert
        c.execute("DROP TABLE IF EXISTS vector_candles")

        # Erstelle die Tabelle 'vector_candles'
        c.execute("""
            CREATE TABLE vector_candles (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                pk_coin_data INTEGER NOT NULL,
                vector_color TEXT NOT NULL,
                FOREIGN KEY(pk_coin_data) REFERENCES coin_data(pk)
            );
        """)
        
    
        #Ema Tabelle
        # Lösche die Tabelle 'ema', falls sie existiert
        c.execute("DROP TABLE IF EXISTS ema")
    
        # Erstelle die Tabelle 'ema'
        c.execute("""
            CREATE TABLE ema (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                pk_coin_data INTEGER NOT NULL,
                ema_value REAL NOT NULL,
                ema_periode INTEGER NOT NULL,
                FOREIGN KEY(pk_coin_data) REFERENCES coin_data(pk)
            );
        """)

        # Änderungen in der Datenbank speichern
        self.conn.commit()
        
    def delete_database(self):
        """
        Löscht die Datenbankdatei vom Dateisystem.
        """
        # Schließe die Verbindung zur Datenbank, falls offen
        if self.conn:
            self.conn.close()
            self.conn = None
            
        # Lösche die Datenbankdatei, falls sie existiert
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f'Datenbank {self.db_path} wurde erfolgreich gelöscht.')
        else:
            print("Die Datenbankdatei existiert nicht und kann nicht gelöscht werden.")

        

    def connect(self):
        """Stellt eine Verbindung zur Datenbank her, falls noch nicht verbunden."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def close(self):
        """Schließt die Verbindung zur Datenbank, falls sie offen ist."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print('Datenbankverbindung wurde geschlossen.')
