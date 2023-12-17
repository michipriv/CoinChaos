#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


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

        Returns:
            pandas.DataFrame: Der aktualisierte DataFrame mit einer neuen Spalte 'color', die die Farben der Kerzen enthält.
        """
        average_volume = self.data['volume'].rolling(window=10).mean()
        volume_spread = self.data['volume'] * (self.data['high_price'] - self.data['low_price'])
        highest_volume_spread = volume_spread.rolling(window=10).max()

        climax_condition = (self.data['volume'] >= 2 * average_volume.shift(1)) | (volume_spread >= highest_volume_spread.shift(1))
        rising_volume_condition = self.data['volume'] >= 1.5 * average_volume.shift(1)

        self.data['color'] = 'gray'
        self.data.loc[climax_condition & (self.data['close_price'] > self.data['open_price']), 'color'] = 'green'
        self.data.loc[climax_condition & (self.data['close_price'] <= self.data['open_price']), 'color'] = 'red'
        self.data.loc[rising_volume_condition & ~climax_condition & (self.data['close_price'] > self.data['open_price']), 'color'] = 'blue'
        self.data.loc[rising_volume_condition & ~climax_condition & (self.data['close_price'] <= self.data['open_price']), 'color'] = 'violet'

        return self.data

    
