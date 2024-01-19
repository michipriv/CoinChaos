import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.ticker import FuncFormatter



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
        df['Date'] = pd.to_datetime(df['time'])  
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
        ax.plot(df['Date'], df['ema_5'], label='EMA-5', color='yellow', linewidth=2)
        ax.plot(df['Date'], df['ema_13'], label='EMA-13', color='orange', linewidth=2)
        ax.plot(df['Date'], df['ema_50'], label='EMA-50', color='blue', linewidth=2)

        ax.plot(df['Date'], df['ema_100'], label='EMA-100', color='green', linewidth=2)
        ax.plot(df['Date'], df['ema_200'], label='EMA-200', color='white', linewidth=2)
        ax.plot(df['Date'], df['ema_800'], label='EMA-800', color='violet', linewidth=2)
        
        
    def format_chart(self, ax, symbol, interval):
            def custom_formatter(x, pos):
                dt = mdates.num2date(x)
                return dt.strftime('%H:%M')  # Format für Stunden und Minuten
        
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(FuncFormatter(custom_formatter))
        
            plt.xticks(rotation=0)
            plt.title(f'{symbol} Candlestick Chart ({interval})')
            plt.ylabel('Price')
            plt.legend()


    ################################################



    def plot_candlestick(self, df, symbol, interval):
        # main plot function
        # aufruf der subfunktionen
        
        df = self.prepare_dataframe(df)
        fig, ax = plt.subplots()

        ax.set_facecolor('black')  # Setzt den Hintergrund auf Schwarz
        self.draw_candles(ax, df)       #Kerzen zeichnen
        self.draw_ema_lines(ax, df)     # emas zeichnen
        self.format_chart(ax, symbol, interval)  # Chart formatieren
        #self.draw_lowest_low(ax,df)
        #self.draw_highest_high(ax,df)
        self.draw_w_pattern(ax,df)
        
        plt.show()      # Finale aufruf des Chrts zur ANzeige
        
    ################################################

    def draw_lowest_low(self, ax, df):
        length_candle = 5   #länge der Lnie in Kerzen
        
        for idx, row in df.iterrows():
            end_idx = min(idx + length_candle, len(df))
    
            # Berechne xmin und xmax für die Linien
            xmin = idx / len(df)
            xmax = end_idx / len(df)
    
            # Zeichne eine Linie für 'LL'
            if row['lower_low'] == 'LL':
                ax.axhline(y=row['low_price'], color='blue', linestyle='--', xmin=xmin, xmax=xmax)
    
                
    def draw_w_pattern(self, ax, df):
        length_candle = 1  # Länge der Linie in Anzahl der Kerzen
    
        for idx, row in df.iterrows():
            # Berechne xmin und xmax für die Linien
            # Die x-Position jeder Kerze entspricht ihrem Index im DataFrame
            xmin = (idx - 0.5) / len(df)  # Verschiebe xmin ein wenig nach links von der Kerze
            xmax = (idx + length_candle - 0.5) / len(df)  # xmax auf die Länge der Linie einstellen
    
            # Zeichne eine Linie für Start des Musters = lower_low
            if row['w_start'] == 'AA':
                ax.axhline(y=row['low_price'], color='orange', linestyle='--', xmin=xmin, xmax=xmax)
    
            # Zeichne eine Linie für Mitte des Musters 
            if row['w_middle'] == 'MM':
                ax.axhline(y=row['low_price'], color='yellow', linestyle='--', xmin=xmin, xmax=xmax)
    
            # Zeichne eine Linie für 50%-Punkt des Musters 
            # if row['w_50_percent'] == '50%':
            #    ax.axhline(y=row['low_price'], color='red', linestyle='--', xmin=xmin, xmax=xmax)

