#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from classes.TechnicalIndicators import TechnicalIndicators  # Stellen Sie sicher, dass der Importpfad korrekt ist

class CandlestickChart:
    def __init__(self, technical_indicators):
        self.technical_indicators = technical_indicators

    def plot(self, symbol, interval):
        # Stellen Sie sicher, dass die technischen Indikatoren geladen wurden
        self.technical_indicators.load_data()

        # Berechnung der Vektor-Kerzen und EMAs
        df = self.technical_indicators.calc_vector_candles()
        ema_50 = self.technical_indicators.calculate_ema(50)
        ema_100 = self.technical_indicators.calculate_ema(100)

        # Vorbereitung des DataFrames für das Plotting
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['time'], unit='ms')  # Umwandeln von Unix-Zeitstempel in lesbare Datum
        df['Date'] = df['Date'].apply(mdates.date2num)

        # Erstellung des Diagramms
        self.plot_vector_candles(df, ema_50, ema_100, symbol, interval)

    def plot_vector_candles(self, df, ema_50, ema_100, symbol, interval):
        fig, ax = plt.subplots()

        # Zeichnen der Vektor-Kerzen
        for idx, row in df.iterrows():
            color = 'green' if row['close'] > row['open'] else 'red' if row['color'] != 'gray' else 'gray'
            ax.plot([row['Date'], row['Date']], [row['low'], row['high']], color='black')
            ax.plot([row['Date'], row['Date']], [row['open'], row['close']], color=color, linewidth=6)

        # Hinzufügen der EMAs
        ax.plot(df['Date'], ema_50, color='blue', label='EMA 50')
        ax.plot(df['Date'], ema_100, color='green', label='EMA 100')

        # Formatierung und Legenden
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.title(f'{symbol} Vector Candles Chart ({interval})')
        plt.legend()

        plt.figtext(0.1, 0.9, f'Symbol: {symbol}', fontsize=9, ha='left')
        plt.figtext(0.1, 0.88, f'Timeframe: {interval}', fontsize=9, ha='left')
        plt.figtext(0.1, 0.86, f'Data Points: {len(df)}', fontsize=9, ha='left')

        plt.show()
