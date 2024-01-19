#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta

class BinanceClient:
    """
    Eine Klasse zur Interaktion mit der Binance-API.

    Diese Klasse ermöglicht das Abrufen historischer Handelsdaten von der Binance-Plattform
    und ihre Speicherung in einem Pandas DataFrame.

    :param api_key: Der API-Schlüssel für die Binance-API.
    :type api_key: str
    :param api_secret: Das API-Geheimnis für die Binance-API.
    :type api_secret: str

    :ivar client: Eine Instanz des Binance API-Clients.
    :vartype client: binance.client.Client
    :ivar data: Ein DataFrame zur Speicherung der abgerufenen Handelsdaten.
    :vartype data: pandas.DataFrame
    """
    
    
    def __init__(self, api_key, api_secret):
        """
        Initialisiert die BinanceClient-Klasse mit API-Schlüsseln.

        :param api_key: Der API-Schlüssel für die Binance-API.
        :type api_key: str
        :param api_secret: Das API-Geheimnis für die Binance-API.
        :type api_secret: str
        """
            
        self.client = Client(api_key, api_secret)
        self.data = pd.DataFrame()
        

    def initialize_data(self):
        """
        Initialisiert den DataFrame mit den erforderlichen Spalten.

        Die Spalten sind: 'time', 'open_price', 'high_price', 'low_price', 'close_price', 
        'volume', 'ema_50', 'ema_100' und 'vector_color'.
        """
        
        
        columns = ['time', 'open_price', 'high_price', 'low_price', 'close_price', 
                      'volume','ema_50','ema_100','vector_color']
        self.data = pd.DataFrame(columns=columns)

    


    def get_data_binance(self, symbol, interval, days_ago):
        
        """
        Ruft Handelsdaten für ein bestimmtes Symbol ab und speichert sie im DataFrame.

        :param symbol: Das Handelssymbol, z.B. 'BTCUSDT'.
        :type symbol: str
        :param interval: Das Zeitintervall für die Daten. Standardmäßig '1d' (1 Tag).
        :type interval: str
        :param days_ago: Anzahl der Tage in der Vergangenheit für den Beginn der Datenabfrage.
        :type days_ago: int
        """
        
        # Umwandlung des Interval-Strings in timedelta
        end_time = datetime.now()
       
        start_time = end_time - timedelta(days=days_ago)
        start_str = start_time.strftime('%d %b, %Y')
        end_str = end_time.strftime('%d %b, %Y')
   
        candles = self.client.get_historical_klines(symbol, interval, start_str, end_str)
   
    
        for candle in candles:
            time = candle[0]
            open_price = float(candle[1])
            high_price = float(candle[2])
            low_price = float(candle[3])
            close_price = float(candle[4])
            volume = float(candle[5])
    
            # Verwende die append_data-Methode, um die Daten zum DataFrame hinzuzufügen
            self.append_data(         
               time=time,
               symbol=symbol,
               interval=interval,
               open_price=open_price,
               high_price=high_price,
               low_price=low_price,
               close_price=close_price,
               volume=volume
           )

   

    def append_data(self, **kwargs):
        """
        Hängt Daten an ein vorhandenes Pandas DataFrame an.

        :param kwargs: Keyword-Argumente für die Daten, die hinzugefügt werden sollen.
                       Beinhaltet: 'time', 'open_price', 'high_price', 'low_price', 
                       'close_price' und 'volume'.
        """
        
        new_row = kwargs
        new_row_df = pd.DataFrame([new_row])
        self.data = pd.concat([self.data, new_row_df], ignore_index=True)
        
 
    def print_data(self):
        """
        Zeigt alle Daten des internen DataFrame an.

        Gibt den aktuellen Inhalt des DataFrame `self.data` aus.
        """
        
        
        pd.set_option('display.max_rows', None)  # Zeige alle Zeilen
        pd.set_option('display.max_columns', None)  # Zeige alle Spalten
  
        
        if self.data.empty:
            print("Der DataFrame ist leer.")
        else:
            print("init data")
            print(self.data)
            
            #achtung es werdennciht immer alle werte in einer reihe angezeigt-> selektive ausgabe verwenden
            #selektierte daten ausgeben
            #elected_columns = self.data.loc[:, ['open_price', 'high_price', 'ema_50']]
            #print(selected_columns)
   
    def add_column(self, column_name, values):
        """
        Fügt eine neue Spalte zum DataFrame hinzu.

        :param column_name: Name der neuen Spalte.
        :type column_name: str
        :param values: Werte für die neue Spalte.
        :type values: list, pandas.Series
        """


        self.data[column_name] = values
        


    def get_data(self):
        """
        Gibt den aktuellen DataFrame mit Handelsdaten zurück.

        :return: Der DataFrame mit Handelsdaten.
        :rtype: pandas.DataFrame
        """
        
        return self.data

    