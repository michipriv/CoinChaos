#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:51:11 2023

@author: administrator
"""





import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from classes.TechnicalIndicators import TechnicalIndicators

class CandlestickChart:
    def plot(self, data, symbol, interval):
        # Umwandlung der Daten in ein pandas DataFrame
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('Date', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

        # Berechnung der Vector Candles und EMAs
        technical_indicators = TechnicalIndicators(df)
        df = technical_indicators.calc_vector_candles()
        ema_50 = technical_indicators.calculate_ema(50)
        ema_100 = technical_indicators.calculate_ema(100)

        # Zeichnen des Diagramms
        self.plot_vector_candles(df, ema_50, ema_100, symbol, interval)

    def plot_vector_candles(self, df, ema_50, ema_100, symbol, interval):
        # Konvertieren der Zeit in matplotlib-Format
        df.reset_index(inplace=True)
        df['Date'] = df['Date'].apply(mdates.date2num)
    
        fig, ax = plt.subplots()
    
        # Zeichnen der Vector Candles
        for idx, row in df.iterrows():
            color = 'green' if row['close'] > row['open'] else 'red' if row['color'] != 'gray' else 'gray'
            ax.plot([row['Date'], row['Date']], [row['low'], row['high']], color='black')
            ax.plot([row['Date'], row['Date']], [row['open'], row['close']], color=color, linewidth=6)
    
        # Hinzufügen der EMAs - Farben geändert
        ax.plot(df['Date'], ema_50, color='blue', label='EMA 50')
        ax.plot(df['Date'], ema_100, color='green', label='EMA 100')  # Farbe zu Grün geändert
    
        # Formatierung und Hinzufügen von Legenden
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.title(f'{symbol} Vector Candles Chart ({interval})')
        plt.legend()
        
        # Hinzufügen von zusätzlichen Informationen
        plt.figtext(0.1, 0.9, f'Symbol: {symbol}', fontsize=9, ha='left')
        plt.figtext(0.1, 0.88, f'Timeframe: {interval}', fontsize=9, ha='left')
        plt.figtext(0.1, 0.86, f'Data Points: {len(df)}', fontsize=9, ha='left')
    
        plt.show()

