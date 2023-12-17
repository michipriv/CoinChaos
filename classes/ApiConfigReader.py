#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:33:01 2023

@author: administrator
"""

class ApiConfigReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_config(self):
        keys = {}
        with open(self.filepath, 'r') as file:
            for line in file:
                if "=" in line:
                    key, value = line.strip().split('=', 1)
                    keys[key] = value
        return keys
