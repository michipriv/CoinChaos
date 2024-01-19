import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.ticker import FuncFormatters

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

   





    def prepare_dataframe(self, df):
        df['Date'] = pd.to_datetime(df['time'], unit='ms')
        df['Date'] = df['Date'].apply(mdates.date2num)
        return df

  
    def draw_candles(self, ax, df):
        for idx, row in df.iterrows():
            candle_color = row['vector_color']

            # Bestimmen der Docht-Farbe basierend auf der 'Kerze'-Spalte
            if row['Kerze'] == 'Grün':
                wick_color = 'green'
            elif row['Kerze'] == 'Rot':
                wick_color = 'red'
            else:
                wick_color = 'black'  # Standardfarbe, falls 'Kerze' weder 'Grün' noch 'Rot' ist

            # Docht zeichnen
            ax.plot([row['Date'], row['Date']], [row['low_price'], row['high_price']], color=wick_color)

            # Kerzenkörper zeichnen
            ax.plot([row['Date'], row['Date']], [row['open_price'], row['close_price']], color=candle_color, linewidth=8)



    def draw_ema_lines(self, ax, df):
        ax.plot(df['Date'], df['ema_50'], label='EMA-50', color='blue', linewidth=2)
        ax.plot(df['Date'], df['ema_100'], label='EMA-100', color='purple', linewidth=2)
        
    
    def format_chart(self, ax, symbol, interval):
        """Formatiert das Chart mit Titeln, Achsenbeschriftungen und Legenden."""

        def custom_time_formatter(x, pos):
            """Benutzerdefinierte Formatierung für Zeitstempel auf der X-Achse."""
            dt = mdates.num2date(x)
            if interval.endswith('m'):
                return dt.strftime('%M')
            elif interval.endswith('h'):
                return dt.strftime('%H')
            else:
                return dt.strftime('%Y-%m-%d')

        ax.xaxis.set_major_formatter(FuncFormatter(custom_time_formatter))
         
        plt.xticks(rotation=45)
        plt.title(f'{symbol} Candlestick Chart ({interval})')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        

    def plot_candlestick(self, df, symbol, interval):
        if 'ema_50' not in df.columns or 'ema_100' not in df.columns or 'vector_color' not in df.columns:
            raise ValueError("Eine oder mehrere erforderliche Spalten fehlen im DataFrame.")

        df = self.prepare_dataframe(df)
        fig, ax = plt.subplots()
        self.draw_candles(ax, df)
        self.draw_ema_lines(ax, df)
        self.format_chart(ax, symbol, interval)
        plt.show()
