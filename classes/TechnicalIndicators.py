#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


class TechnicalIndicators:
    """
    Diese Klasse berechnet technische Indikatoren und Vektor-Kerzen für Handelsdaten.

    Attributes:
        binance_client: Eine Instanz des BinanceClient, von der die Handelsdaten abgerufen werden.
        data: DataFrame, der die Handelsdaten enthält.
    """

    def __init__(self, binance_client, db):
        """
        Initialisiert die TechnicalIndicators-Klasse mit einem BinanceClient-Objekt.

        Args:
            binance_client: Eine Instanz des BinanceClient.
        """
  
        self.binance_client = binance_client
        self.db = db        

     

    def calculate_ema(self, ema_periode, symbol, timeframe):
        
        """
        Berechnet den exponentiell gleitenden Durchschnitt (EMA) für einen gegebenen Zeitraum und speichert die Ergebnisse in der 'ema' Tabelle.
        
        Diese Funktion prüft zunächst, welche Einträge in der 'coin_data' Tabelle basierend auf dem Symbol und Intervall noch keinen berechneten EMA-Wert haben. Anschließend wird der EMA für diese ungefüllten Einträge berechnet und in der 'ema' Tabelle gespeichert.
        
        :param ema_value: Die Spanne (Anzahl der Perioden) für die EMA-Berechnung. Muss eine positive Ganzzahl sein.
        :param symbol: Das Kryptowährungssymbol, für das der EMA berechnet werden soll (z.B. 'BTCUSDT').
        :param interval: Das Zeitintervall der Daten (z.B. '1m', '5m', '1h').
        :type ema_value: int
        :type symbol: str
        :type interval: str
        :raises Exception: Gibt einen Fehler aus, wenn das Speichern der EMA-Werte in der Datenbank fehlschlägt.
        
        :return: Gibt nichts zurück. Die berechneten EMA-Werte werden direkt in die Datenbank eingefügt.
        """
        
        # Lade die Daten aus 'coin_data' in einen DataFrame, berücksichtige Symbol und timeframe
        # zeige immer alle datn aus der "rechten" Tabelle 1:1 relation an und zeige nur die Daten an wo ema_value ist NUll - also keine Daten eingetragen sind
            
        query = """
            SELECT 
                cd.pk, 
                cd.close_price, 
                COALESCE(em.ema_value, 'NULL') AS ema_value, 
                COALESCE(em.ema_periode, 'NULL') AS ema_periode
            FROM 
                coin_data cd
                LEFT JOIN ema em ON cd.pk = em.pk_coin_data AND em.ema_periode = ?
            WHERE 
                cd.coin = ? 
                AND cd.timeframe = ?
                AND em.ema_value IS NULL;
            """
        #print(query)
            
        
        # Stelle sicher, dass die Parameter in der korrekten Reihenfolge übergeben werden
        
        
        df = pd.read_sql_query(query, self.db.conn, params=(ema_periode, symbol, timeframe))
        
        if df.empty:
            print("Keine Daten für EMA: ", symbol, " ", timeframe )
            return
    
       
        # Berechnung des EMA im DataFrame
        df['ema'] = df['close_price'].ewm(span=ema_periode, adjust=False).mean()

    
        # Vorbereitung der Daten für das Einfügen
        data_to_insert = [(row['pk'], ema_periode, row['ema']) for index, row in df.iterrows()]
    
        # Einfügen der EMA-Werte in die 'ema' Tabelle
        insert_query = "INSERT INTO ema (pk_coin_data, ema_periode, ema_value) VALUES (?, ?, ?)"
        
        try:
            self.db.conn.executemany(insert_query, data_to_insert)
            self.db.conn.commit()
            print(f"{len(data_to_insert)} EMA-Werte {timeframe} gespeichert.")
        except Exception as e:
            print("Fehler beim Speichern der EMA-Werte:", e)
            self.db.conn.rollback()
        
        
        
    

    def calc_vector_candles(self, symbol, timeframe):
        # Lade notwendige Daten aus der Datenbank
        
        query = """
            SELECT 
                cd.pk, 
                cd.open_price, 
                cd.close_price, 
                cd.high_price, 
                cd.low_price, 
                cd.volume,
                -- Verwende COALESCE, um sicherzustellen, dass für fehlende Werte in 'vector_candles' ein Platzhalter angezeigt wird
                COALESCE(vc.vector_color, 'NULL') AS vector_color
            FROM 
                coin_data cd
                LEFT JOIN vector_candles vc ON cd.pk = vc.pk_coin_data
            WHERE 
                cd.coin = ? 
                AND cd.timeframe = ?
                AND vc.pk_coin_data IS NULL;
            """
        
        #print(query)
        
        df = pd.read_sql_query(query, self.db.conn, params=(symbol, timeframe))
    
        if df.empty:
            print("Keine neuen Daten für Vektor-Kerzen.")
            return
    
        
        # Konvertiere das timeframe in eine numerische Spanne für die EMA-Berechnung
        interval_to_span = {"1m": 1, "5m": 5, "15m": 15, "30m": 30}  # Beispielzuordnung
        span = interval_to_span.get(timeframe, 0)  # 0 setzen falls nicht gefunden


    
        # Berechnungen für Vektor-Kerzen durchführen

        # Berechnungen für das Volumen und den Spread
        average_volume = df['volume'].rolling(window=10).mean()
        volume_spread = df['volume'] * (df['high_price'] - df['low_price'])
        highest_volume_spread = volume_spread.rolling(window=10).max()

        # Bedingungen für Vektor-Kerzen
        climax_condition = (df['volume'] >= 2 * average_volume.shift(1)) | (volume_spread >= highest_volume_spread.shift(1))
        rising_volume_condition = (df['volume'] >= 1.5 * average_volume.shift(1)) & ~climax_condition

        # Zuweisung der Farben basierend auf den Bedingungen
        df['vector_color'] = np.where(
            climax_condition & (df['close_price'] > df['open_price']), 'green',
            np.where(
                climax_condition & (df['close_price'] <= df['open_price']), 'red',
                np.where(
                    rising_volume_condition & (df['close_price'] > df['open_price']), 'blue',
                    np.where(
                        rising_volume_condition & (df['close_price'] <= df['open_price']), 'violet',
                        np.where(df['close_price'] > df['open_price'], 'lightgrey', 'darkgrey')
                    )
                )
            )
        )
    
        # Bereite Daten für das Einfügen vor
        data_to_insert = [(row['pk'], row['vector_color']) for index, row in df.iterrows()]
    
        # Füge die berechneten Vektor-Kerzenfarben in die Datenbank ein
        insert_query = "INSERT INTO vector_candles (pk_coin_data, vector_color) VALUES (?, ?)"
        try:
            c = self.db.conn.cursor()
            c.executemany(insert_query, data_to_insert)
            self.db.conn.commit()
            print(f"{len(data_to_insert)} Vektor-Kerzenfarben wurden aktualisiert.")
        except Exception as e:
            print("Fehler beim Einfügen der Vektor-Kerzenfarben:", e)



    
    def calculate_candle_color(self,symbol, timeframe):
        """
        Berechnet die Kerzenfarbe für jeden Eintrag in der 'coin_data' Tabelle und speichert das Ergebnis in der 'kerzenfarbe' Tabelle.
        Es wird nur für Einträge berechnet, für die noch keine Kerzenfarbe abgespeichert wurde.
        """
        # Stelle sicher, dass die Datenbankverbindung ordnungsgemäß gehandhabt wird
        try:
            # Hole alle Einträge aus 'coin_data', für die noch keine Kerzenfarbe in 'kerzenfarbe' gespeichert wurde,
            # und die dem spezifizierten Symbol und Zeitrahmen entsprechen
            
            
            query = """
            SELECT 
                cd.pk, 
                cd.open_price, 
                cd.close_price, 
                -- Verwende COALESCE, um sicherzustellen, dass für fehlende Werte in 'kerzenfarbe' ein Platzhalter angezeigt wird
                COALESCE(kf.kerze, 'NULL') AS kerzenfarbe
            FROM 
                coin_data cd
                LEFT JOIN kerzenfarbe kf ON cd.pk = kf.pk_coin_data
            WHERE 
                cd.coin = ? 
                AND cd.timeframe = ?
                AND kf.pk_coin_data IS NULL;
            """
            #print(query)
            
            # Führe die SQL-Abfrage aus und lade die Ergebnisse in einen DataFrame
            df = pd.read_sql_query(query, self.db.conn, params=(symbol, timeframe))


    
            if df.empty:
                print(f"Keine Daten für Kerzenfarbe: {symbol}  {timeframe} ")
                return


            # Berechne die Kerzenfarbe für jede Zeile
            df['kerze'] = df.apply(lambda row: 'green' if row['close_price'] > row['open_price'] else 'red', axis=1)
        
            # Bereite die Daten für das Einfügen in die 'kerzenfarbe' Tabelle vor
            data_to_insert = [(row['pk'], row['kerze']) for index, row in df.iterrows()]
        
            # Füge die berechneten Kerzenfarben in die 'kerzenfarbe' Tabelle ein
            insert_query = "INSERT INTO kerzenfarbe (pk_coin_data, kerze) VALUES (?, ?)"
            
            # Verwende eine Transaktion, um die Einfügeoperationen zu gruppieren
            with self.db.conn:
                self.db.conn.executemany(insert_query, data_to_insert)
            
            print(f"{len(data_to_insert)} Kerzenfarben wurden aktualisiert.")
            
        except Exception as e:
            print(f"Kerzenfarbe ein Fehler ist aufgetreten: {e}")
    
            
        
    
    
    
    
    
    #gehört noch auf db umgestellt
    
    def lower_low(self):
        """
        Identifiziert das tiefste Tief innerhalb eines Musters von zwei roten und zwei grünen Kerzen.
        
        Diese Methode fügt dem DataFrame drei neue Spalten hinzu: 'lower_low', 'muster_start' und 'muster_ende'.
        Diese Spalten markieren 'LL' für die Kerze mit dem tiefsten Tief, 'AA' für den Anfang und 'EE' für das Ende des Musters.
        
        Returns:
            DataFrame: Der bearbeitete DataFrame mit den neuen Spalten.
        """
        df = self.data
        df['lower_low'] = ''  # Initialisiere alle Werte mit 'NA'
        df['lower_low_start'] = ''  # Für den Anfang des Musters
        df['lower_low_ende'] = ''  # Für das Ende des Musters
        df['lower_low_last'] = ''  # Das letzte Lower_low
        
        last_lowest_low_index = -1  # Index des letzten gefundenen lowest_low
        
        for i in range(2, len(df) - 2):
            if df['Kerze'][i - 2] == 'Rot' and df['Kerze'][i - 1] == 'Rot':
                # Markiere den Anfang des Musters
                df.at[i - 2, 'lower_low_start'] = 'AA'
        
                # Suche nach zwei aufeinanderfolgenden grünen Kerzen nach den roten Kerzen
                for j in range(i, len(df) - 1):
                    if df['Kerze'][j] == 'Grün' and df['Kerze'][j + 1] == 'Grün':
                        # Markiere das Ende des Musters
                        df.at[j + 1, 'lower_low_ende'] = 'EE'
        
                        # Finde das tiefste Tief im Muster
                        start = i - 2
                        ende = j + 1
                        lowest_low_index = df['low_price'][start:ende + 1].idxmin()
                        df.at[lowest_low_index, 'lower_low'] = 'LL'
        
                        # Setze das letzte Lower_low mit 'LA'
                        if last_lowest_low_index != -1:
                            df.at[last_lowest_low_index, 'lower_low_last'] = ''
                        df.at[lowest_low_index, 'lower_low_last'] = 'LA'
                        last_lowest_low_index = lowest_low_index
                        break
        
        return df
    

    #gehört noch auf db umgestellt
    def w_pattern(self):
        """
        Identifiziert das W-Muster in den Handelsdaten.
        Fügt dem DataFrame Spalten 'w_pattern', 'w_start', 'w_middle', 'w_50_percent' und 'w1_last' hinzu,
        die das Vorhandensein des Musters und dessen verschiedene Phasen markieren.
        """
        df = self.data
        
        
        df['w1'] = ''
        df['w_middle'] = ''
       
        df['w1_last'] = ''  # Variable zur Speicherung des letzten 'w1'
    
        last_w1_index = -1  # Speichert den Index des letzten 'w1'
    
        # Iteriere durch die Daten, um das W-Muster und die lower_low zu identifizieren
        for idx, row in df.iterrows():
            # Stelle sicher, dass das Muster nur unterhalb des EMA-50 gesucht wird
            if row['ema_50'] is not None and row['close_price'] < row['ema_50']:
                # Hier kannst du die Bedingungen für das Erkennen von W-Mustern und lower_low definieren
                # Zum Beispiel: Wenn ein lower_low auftritt, setze 'LL' in die 'w1'-Spalte
                if row['lower_low'] == 'LL':
                    df.at[idx, 'w1'] = 'w1'
                    last_w1_index = idx  # Aktualisiere den Index des letzten 'w1'
    
        # Setze das letzte 'w1' mit 'LA'
        if last_w1_index != -1:
            df.at[last_w1_index, 'w1_last'] = 'LA'
    
        return df
