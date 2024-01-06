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
        Fügt dem DataFrame Spalten 'lower_low', 'muster_start' und 'muster_ende' hinzu, 
        die 'LL' für die Kerze mit dem tiefsten Tief, 'AA' für den Anfang und 'EE' für das Ende des Musters markieren.
        """
        df = self.data
        df['lower_low'] = 'NA'  # Initialisiere alle Werte mit 'NA'
        df['muster_start'] = 'NA'  # Für den Anfang des Musters
        df['muster_ende'] = 'NA'  # Für das Ende des Musters
    
        for i in range(2, len(df) - 2):
            if df['Kerze'][i - 2] == 'Rot' and df['Kerze'][i - 1] == 'Rot':
                # Markiere den Anfang des Musters
                df.at[i - 2, 'muster_start'] = 'AA'
    
                # Suche nach zwei aufeinanderfolgenden grünen Kerzen nach den roten Kerzen
                for j in range(i, len(df) - 1):
                    if df['Kerze'][j] == 'Grün' and df['Kerze'][j + 1] == 'Grün':
                        # Markiere das Ende des Musters
                        df.at[j + 1, 'muster_ende'] = 'EE'
    
                        # Finde das tiefste Tief im Muster
                        start = i - 2
                        ende = j + 1
                        lowest_low_index = df['low_price'][start:ende + 1].idxmin()
                        df.at[lowest_low_index, 'lower_low'] = 'LL'
                        break
    
        return df
    
    def higher_high(self):
        """
        Identifiziert das höchste Hoch innerhalb eines Musters von zwei grünen und zwei roten Kerzen.
        Fügt dem DataFrame eine Spalte 'higher_high' hinzu,
        die 'HH' für die Kerze mit dem höchsten Hoch, 'AA' für den Anfang und 'EE' für das Ende des Musters markiert.
        """
        df = self.data
        df['higher_high'] = 'NA'  # Initialisiere alle Werte mit 'NA'
    
        for i in range(2, len(df) - 2):
            if df['Kerze'][i - 2] == 'Grün' and df['Kerze'][i - 1] == 'Grün':
                # Markiere den Anfang des Musters
                df.at[i - 2, 'higher_high'] = 'AA'
    
                # Suche nach zwei aufeinanderfolgenden roten Kerzen nach den grünen Kerzen
                for j in range(i, len(df) - 1):
                    if df['Kerze'][j] == 'Rot' and df['Kerze'][j + 1] == 'Rot':
                        # Markiere das Ende des Musters
                        df.at[j + 1, 'higher_high'] = 'EE'
    
                        # Finde das höchste Hoch im Muster
                        start = i - 2
                        ende = j + 1
                        highest_high_index = df['high_price'][start:ende + 1].idxmax()
                        df.at[highest_high_index, 'higher_high'] = 'HH'
                        break
    
        return df
