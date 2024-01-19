#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
from pytz import timezone
import pytz

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

    def __init__(self, api_key, api_secret, time_zone='UTC'):
         
        """
        Initialisiert die BinanceClient-Klasse mit API-Schlüsseln.

        :param api_key: Der API-Schlüssel für die Binance-API.
        :type api_key: str
        :param api_secret: Das API-Geheimnis für die Binance-API.
        :type api_secret: str
        """
            
        self.client = Client(api_key, api_secret)
        self.data = pd.DataFrame()
        self.time_zone = timezone(time_zone)
        

    def initialize_data(self):
        """
        Initialisiert den DataFrame mit den erforderlichen Spalten.

        
        time (str): Zeitstempel.
        open_price (float): Eröffnungspreis.
        high_price (float): Höchstpreis.
        low_price (float): Tiefstpreis.
        close_price (float): Schlusspreis.
        volume (int): Volumen.
        

        """
        
        
        columns = ['time', 'time1','open_price', 'high_price', 'low_price', 'close_price', 
                      'volume','vector_color', 'lowest_low']
        self.data = pd.DataFrame(columns=columns)

    


    def get_data_binance(self, symbol, interval, limit):
        
        """       
        .. py:method:: BinanceClient.get_data_binance(symbol, interval, days_ago)

        Ruft Handelsdaten für ein bestimmtes Kryptowährungssymbol von der Binance API ab und speichert sie in einem DataFrame. Diese Methode verwendet die aktuelle Serverzeit von Binance, um sicherzustellen, dass die Zeitberechnung genau ist. Die abgerufenen Daten enthalten verschiedene Details zu jedem Handelsintervall, wie Öffnungs-, Höchst-, Tiefst- und Schlusspreise sowie das gehandelte Volumen.

        :param str symbol: Das Handelssymbol für die Abfrage, beispielsweise 'BTCUSDT'.
        :param str interval: Das Zeitintervall für die Daten. Die unterstützten Intervalle sind beispielsweise '1m' (eine Minute), '1h' (eine Stunde), '1d' (ein Tag). Standardmäßig ist das Intervall auf '1d' gesetzt.
        :param int limit: Die Anzahl der Kerzen die abgerufen werden sollen. 

        Die Methode beginnt mit der Abfrage der aktuellen Serverzeit von Binance und berechnet den Start- und Endzeitpunkt für die Datensammlung. Anschließend werden die historischen Kerzendaten ('klines') für das angegebene Symbol und Intervall von der Binance API abgerufen. Jede Kerze wird in ein Datumsformat (im UTC-Standard) umgewandelt und zusammen mit anderen relevanten Handelsdaten in den DataFrame eingefügt.

        :return: Diese Methode gibt nichts zurück, sondern aktualisiert den internen DataFrame der Klasse mit den abgerufenen Handelsdaten.
        :rtype: None

        Beispiel::

        # Erstellen einer Instanz der BinanceClient-Klasse
        client = BinanceClient(api_key, api_secret)

        # Abrufen von Handelsdaten für BTCUSDT für die letzten 10 Balken im 1h Format
        client.get_data_binance('BTCUSDT', '1h', 10)

        """

        # Abrufen der aktuellen Serverzeit von Binance
        server_time = self.client.get_server_time()
        server_dt = datetime.fromtimestamp(server_time['serverTime'] / 1000, pytz.utc)
    
        # Berechnung des Startzeitpunkts basierend auf 'limit' und 'interval'
        if interval.endswith('m'):
            delta = timedelta(minutes=int(interval[:-1]) * limit)
        elif interval.endswith('h'):
            delta = timedelta(hours=int(interval[:-1]) * limit)
        elif interval.endswith('d'):
            delta = timedelta(days=int(interval[:-1]) * limit)
        else:
            raise ValueError("Ungültiges Intervallformat")
    
        start_time = server_dt - delta
    
        # Formatierung der Zeitstempel für die API-Anfrage
        start_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_str = server_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    
        # Abrufen der historischen Kurse mit Limit
        candles = self.client.get_historical_klines(symbol, interval, start_str, end_str, limit=limit)


        for candle in candles:
            
            time = candle[0]
            # Zeitzone konvertieren
            dt = datetime.fromtimestamp(time / 1000, pytz.utc).astimezone(self.time_zone)
            
            # Formatieren des Zeitstempels im ISO 8601-Format
            formatted_time = dt.strftime('%Y-%m-%dT%H:%M:%S')
        
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

    