#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:59:33 2023

@author: administrator
"""

import pandas as pd

class TechnicalIndicators:
    def __init__(self, df):
        self.df = df

    def calculate_ema(self, period):
        ema = self.df['close'].ewm(span=period, adjust=False).mean()
        return ema
    
   

    def calc_vector_candles(self):
        # Berechnung des durchschnittlichen Volumens und des Volumen-Spreads
        average_volume = self.df['volume'].rolling(window=10).mean()
        volume_spread = self.df['volume'] * (self.df['high'] - self.df['low'])
        highest_volume_spread = volume_spread.rolling(window=10).max()
    
        # Vektorisierte Bedingungen für die Farbzuweisung
        climax_condition = (self.df['volume'] >= 2 * average_volume.shift(1)) | (volume_spread >= highest_volume_spread.shift(1))
        rising_volume_condition = self.df['volume'] >= 1.5 * average_volume.shift(1)
    
        # Zuweisung der Farben
        self.df['color'] = 'gray'  # Standardfarbe
        self.df.loc[climax_condition & (self.df['close'] > self.df['open']), 'color'] = 'green'
        self.df.loc[climax_condition & (self.df['close'] <= self.df['open']), 'color'] = 'red'
        self.df.loc[rising_volume_condition & ~climax_condition & (self.df['close'] > self.df['open']), 'color'] = 'blue'
        self.df.loc[rising_volume_condition & ~climax_condition & (self.df['close'] <= self.df['open']), 'color'] = 'violet'
    
        return self.df


    #test vector candle, zählt die roten,grüne,pink nd blauen candle
    def calc_vector_candles_test(self):
        average_volume = self.df['volume'].rolling(window=10).mean()
        volume_spread = self.df['volume'] * (self.df['high'] - self.df['low'])
        highest_volume_spread = volume_spread.rolling(window=10).max()
    
        for index, row in self.df.iterrows():
            if row['volume'] >= 2 * average_volume[index] or volume_spread[index] >= highest_volume_spread[index]:
                self.df.at[index, 'color'] = 'green' if row['close'] > row['open'] else 'red'
            elif row['volume'] >= 1.5 * average_volume[index]:
                self.df.at[index, 'color'] = 'blue' if row['close'] > row['open'] else 'pink'
            else:
                self.df.at[index, 'color'] = 'gray'
    
        # Debugging: Ausgabe der Anzahl der Kerzen jeder Farbe
        print(self.df['color'].value_counts())
    
        return self.df

