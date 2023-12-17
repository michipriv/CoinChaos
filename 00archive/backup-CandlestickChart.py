#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:51:11 2023

@author: administrator
"""
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from classes.TechnicalIndicators import TechnicalIndicators

class CandlestickChart:
    def plot(self, data, symbol, interval):
       # Umwandlung der Daten in ein pandas DataFrame
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('Date', inplace=True)
        df = df[['open', 'high', 'low', 'close']].astype(float)
        
        
        # Erweiterter Teil: Plot der Vector Candles
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('Date', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)  # Stellen Sie sicher, dass Volumen enthalten ist

        # Berechnung der Vector Candles (zusätzlich zu den EMAs)
        technical_indicators = TechnicalIndicators(df)
        df = technical_indicators.calc_vector_candles()  # Berechnet Vector Candle Farben

        
       # Hinzufügen der EMAs zum Diagramm
        ema_50 = technical_indicators.calculate_ema(50)
        ema_100 = technical_indicators.calculate_ema(100)
        apds = [mpf.make_addplot(ema_50, color='blue'), 
                mpf.make_addplot(ema_100, color='red')]

        # Anpassen der Kerzenfarben für Vector Candles
        color_dict = {'up': df['color'], 'down': df['color']}

        # Erstellen des Candlestick-Diagramms
        title = f'{symbol} Candlestick Chart ({interval})'
        mpf.plot(df, type='candle', title=title, style='charles', addplot=apds, candle_color_dict=color_dict)

        # Hinzufügen von Texten und Legenden
        plt.figtext(0.1, 0.9, f'Symbol: {symbol}', fontsize=9, ha='left')
        plt.figtext(0.1, 0.88, f'Timeframe: {interval}', fontsize=9, ha='left')
        plt.figtext(0.1, 0.86, f'Data Points: {len(df)}', fontsize=9, ha='left')
        plt.figtext(0.1, 0.84, 'EMA 50 (blue)', color='blue', fontsize=9, ha='left')
        plt.figtext(0.1, 0.82, 'EMA 100 (red)', color='red', fontsize=9, ha='left')

        plt.show()
        
        
        
        
        
    def plot_vector_candles(self, technical_indicators):
        df = technical_indicators.calc_vector_candles()

        # Anpassen der Kerzenfarben für Vector Candles
        color_dict = {'up': df['color'], 'down': df['color']}

        # Erstellen des Candlestick-Diagramms mit Vector Candles
        mpf.plot(df, type='candle', style='charles', title="Vector Candles Chart",
                 show_nontrading=True, candle_color_dict=color_dict)

