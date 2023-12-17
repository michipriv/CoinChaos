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

    client = BinanceClient(api_keys.get('api_key'), api_keys.get('secret_key'))
    symbol = 'BTCUSDT'
    interval = '1h'
    days = 5
    data = client.get_crypto_data(symbol, days, interval)
    chart = CandlestickChart()
    chart.plot(data, symbol, interval)
    
if __name__ == "__main__":
    main()
