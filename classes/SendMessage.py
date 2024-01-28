#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

class SendMessage:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.pushbullet.com/v2/pushes"

    def send_notification(self, title, body):
        headers = {
            "Access-Token": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "type": "note",
            "title": title,
            "body": body
        }
        print(headers)

        response = requests.post(self.url, headers=headers, json=data)

        if response.status_code == 200:
            return "Benachrichtigung erfolgreich gesendet!"
        else:
            return "Fehler beim Senden der Benachrichtigung."

    def send_notification_with_image(self, title, body, image_url):
          headers = {
              "Access-Token": self.api_key,
              "Content-Type": "application/json"
          }
          data = {
              "type": "file",
              "title": title,
              "body": body,
              "file_url": image_url
          }
    
          response = requests.post(self.url, headers=headers, json=data)
    
          if response.status_code == 200:
              return "Benachrichtigung mit Bild erfolgreich gesendet!"
          else:
              return "Fehler beim Senden der Benachrichtigung mit Bild."
