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

    def __init__(self, binance_client):
        """
        Initialisiert die TechnicalIndicators-Klasse mit einem BinanceClient-Objekt.

        Args:
            binance_client: Eine Instanz des BinanceClient.
        """
  
        self.binance_client = binance_client
        self.data = None  # Initialisieren als None
        self.load_data()

    def load_data(self):
        """
        Lädt die Handelsdaten vom BinanceClient.
        """
        self.data = self.binance_client.get_data()       
        

    def calculate_ema(self, period):
        
        self.binance_client.data[f'ema_{period}'] = self.binance_client.data['close_price'].ewm(span=period, adjust=False).mean()



    def calc_vector_candles(self):
        """
        Berechnet die Farben der Vektor-Kerzen basierend auf Handelsvolumen und Preisbewegungen.

        Fügt dem DataFrame eine neue Spalte 'vector_color' hinzu, die die Farben der Kerzen enthält.
        """
        # Berechnungen für das Volumen und den Spread
        average_volume = self.data['volume'].rolling(window=10).mean()
        volume_spread = self.data['volume'] * (self.data['high_price'] - self.data['low_price'])
        highest_volume_spread = volume_spread.rolling(window=10).max()

        # Bedingungen für Vektor-Kerzen
        climax_condition = (self.data['volume'] >= 2 * average_volume.shift(1)) | (volume_spread >= highest_volume_spread.shift(1))
        rising_volume_condition = (self.data['volume'] >= 1.5 * average_volume.shift(1)) & ~climax_condition

        # Farben für verschiedene Bedingungen festlegen
        # Farben können hier als Farbcodes oder Farbnamen definiert werden
        red_vector_color = 'red'
        green_vector_color = 'green'
        violet_vector_color = 'violet'
        blue_vector_color = 'blue'
        dark_grey_candle_color = 'darkgrey'
        light_gray_candle_color = 'lightgrey'

        # Zuweisung der Farben basierend auf den Bedingungen
        self.data['vector_color'] = self.data.apply(
            lambda row: green_vector_color if climax_condition[row.name] and row['close_price'] > row['open_price']
                        else red_vector_color if climax_condition[row.name] and row['close_price'] <= row['open_price']
                        else blue_vector_color if rising_volume_condition[row.name] and row['close_price'] > row['open_price']
                        else violet_vector_color if rising_volume_condition[row.name] and row['close_price'] <= row['open_price']
                        else light_gray_candle_color if row['close_price'] > row['open_price']
                        else dark_grey_candle_color, axis=1)

    
    def calculate_candle_color(self):
        """
        Fügt eine neue Spalte 'Kerze' zum DataFrame hinzu, die angibt, ob die Kerze grün oder rot ist.
        'Grün' bedeutet, dass der Schlusskurs höher als der Eröffnungskurs ist, und 'Rot', dass er niedriger ist.
        """
        self.data['Kerze'] = self.data.apply(
            lambda row: 'Grün' if row['close_price'] > row['open_price'] else 'Rot', axis=1)
        
     
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
