#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:42:14 2023

@author: administrator
"""

from binance.client import Client
from datetime import datetime, timedelta

class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_crypto_data(self, symbol, days_ago, interval='1d'):
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days_ago)
        start_str = start_time.strftime('%d %b, %Y')
        end_str = end_time.strftime('%d %b, %Y')

        candles = self.client.get_historical_klines(symbol, interval, start_str, end_str)
        formatted_data = []
        for candle in candles:
            data = {
                "time": candle[0],    # Öffnungszeit
                "open": candle[1],    # Eröffnungspreis
                "high": candle[2],    # Höchstpreis
                "low": candle[3],     # Tiefstpreis
                "close": candle[4],   # Schlusspreis
                "volume": candle[5]   # Handelsvolumen
            }
            formatted_data.append(data)
        return formatted_data

    def testAbruf(self, symbol, days_ago, interval='1d'):
        data = self.get_crypto_data(symbol, days_ago, interval)
        print(f"Data for {symbol}: {data}")
