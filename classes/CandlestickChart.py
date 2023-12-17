import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

class CandlestickChart:
    def __init__(self, binance_client):
        """
        Initialisiert die CandlestickChart-Klasse.

        Args:
            binance_client (BinanceClient): Eine Instanz der BinanceClient-Klasse.
            technical_indicators (TechnicalIndicators, optional): Eine Instanz der TechnicalIndicators-Klasse.
        """
        self.binance_client = binance_client

    def plot(self, symbol, interval, days_ago):
        # Daten von Binance abrufen
        df = self.binance_client.get_data()

        # Diagramm zeichnen
        self.plot_candlestick(df, symbol, interval)

    def plot_candlestick(self, df, symbol, interval):
        # Überprüfen, ob EMA-Spalten vorhanden sind
        if 'ema_50' not in df.columns or 'ema_100' not in df.columns:
            raise ValueError("Die Spalten 'ema_50' oder 'ema_100' fehlen im DataFrame.")

        # DataFrame vorbereiten
        df['Date'] = pd.to_datetime(df['time'], unit='ms')
        df['Date'] = df['Date'].apply(mdates.date2num)

        # Figure und Axes erstellen
        fig, ax = plt.subplots()

        # Jede Kerze zeichnen
        for idx, row in df.iterrows():
            color = 'green' if row['close_price'] > row['open_price'] else 'red'
            # Kerzenkörper
            ax.plot([row['Date'], row['Date']], [row['low_price'], row['high_price']], color='black')  # Docht
            ax.plot([row['Date'], row['Date']], [row['open_price'], row['close_price']], color=color, linewidth=8)  # Kerzenkörper

        # EMA-50 und EMA-100 Linien zeichnen
        ax.plot(df['Date'], df['ema_50'], label='EMA-50', color='blue', linewidth=2)
        ax.plot(df['Date'], df['ema_100'], label='EMA-100', color='green', linewidth=2)

        # X-Achse als Datum formatieren
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        # Titel, Legende und Achsenbeschriftungen
        plt.title(f'{symbol} Candlestick Chart ({interval})')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()

        plt.show()
