#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Modulbeschreibungen:

ApiConfigReader: 
Diese Klasse ist für das Lesen von API-Konfigurationsdaten aus einer externen Datei zuständig.
Sie wird verwendet, um API-Schlüssel und andere Konfigurationseinstellungen sicher und effizient zu verwalten.

BinanceClient: 
Diese Klasse dient als Schnittstelle zur Binance API.
Sie ermöglicht es, Handelsdaten abzurufen, wie z.B. Candlestick-Daten für verschiedene Kryptowährungen.

CandlestickChart: 
Diese Klasse ist für die Visualisierung von Handelsdaten in Form von Candlestick-Diagrammen zuständig.
Sie verwendet die von BinanceClient abgerufenen Daten, um Diagramme zu erstellen, die für die Analyse von Preisbewegungen hilfreich sind.
"""

from classes.ApiConfigReader import ApiConfigReader
from classes.BinanceClient import BinanceClient
from classes.CandlestickChart import CandlestickChart
from classes.TechnicalIndicators import TechnicalIndicators


def main():
    """
    Hauptfunktion des Crypto-Projekts.

    Erstellt ein ApiConfigReader-Objekt, um die API-Schlüssel aus der Konfigurationsdatei zu lesen.
    Abrufen der API-Schlüssel aus der Konfigurationsdatei.
    Erstellen eines BinanceClient-Objekts mit den gelesenen API-Schlüsseln.
    Definieren der Handelssymbol-, Intervall- und Tagesparameter für den Datenabruf.
    Abrufen der Handelsdaten vom Binance-Client.
    Erstellen eines CandlestickChart-Objekts zur Darstellung der abgerufenen Daten.
    Zeichnen des Candlestick-Diagramms mit den abgerufenen Daten.
    """
    
    config_path = 'etc/config.txt'
    config_reader = ApiConfigReader(config_path)
    api_keys = config_reader.read_config()

    symbol = 'BTCUSDT'
    interval = '4h'  # String für INterval 1m,3m,5m,1d, 1w, 1M
    days_ago = 14 # Integer für abzurufende Tage

    
    binance_client = BinanceClient(api_keys.get('api_key'), api_keys.get('secret_key'))
    
    # Daten abrufen und aufbereiten
    binance_client.initialize_data()
    binance_client.get_data_binance(symbol, interval,  days_ago, )  # korrigierte Reihenfolge der Parameter
  
    #technische INdikatoren berechnen für die abgerufenen Daten und im Panda Framework abspeichern    
    
    technical_indicators = TechnicalIndicators(binance_client)
    technical_indicators.calculate_ema(50)
    technical_indicators.calculate_ema(100)
    technical_indicators.calc_vector_candles()
    technical_indicators.calculate_candle_color()
    
    binance_client.print_data()
   
    
   #Anzeige des Chart
    chart = CandlestickChart(binance_client)
    chart.plot( symbol, interval, days_ago)
    
    
if __name__ == "__main__":
    main()
