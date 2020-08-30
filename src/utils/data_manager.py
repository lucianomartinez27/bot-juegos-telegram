#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import json


class DataManager:
    def __init__(self, path):
        self.path = path+'/data.json'

    def load_info(self):
        with open(self.path, 'r') as datafile:
            return json.load(datafile)

    def save_info(self, data):
        with open(self.path, 'w') as datafile:
            json.dump(data, datafile)

    def generate_info(self, default_info):
        try:
            return self.load_info()
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.save_info(default_info)
            return default_info
