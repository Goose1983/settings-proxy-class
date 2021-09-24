import json
import logging
import threading
import time
from typing import Set, Any, Dict
import requests


class SettingsProxy:
    _settings_keys: Set[str]
    _settings: Dict[Any, Any]
    _seconds_until_renew_settings: int
    _settings_service_endpoint: str
    _settings_json: str

    # TODO
    # def __new__(cls, *args):
    #     # pattern singleton realisation
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(SettingsProxy, cls).__new__(cls, *args)
    #     return cls.instance

    def __init__(self, settings_service_endpoint, settings_keys, seconds_until_renew_settings=600):
        self._settings_keys = settings_keys
        self._seconds_until_renew_settings = seconds_until_renew_settings
        self._settings_service_endpoint = settings_service_endpoint
        self._renew_settings()
        x = threading.Thread(target=self._start_regular_renew)
        x.start()

    def _renew_settings(self):
        try:
            response = requests.get(self._settings_service_endpoint, json={
                "parameters": self._settings_keys
            })
        except Exception as e:
            logging.error("Ошибка получения настроек из сервиса настроек %s", str(e))
        if response.status_code != 200:
            logging.error("Ошибка получения настроек из сервиса настроек. Статус %s %s", response.status_code,
                          response.reason)
            return
        self._settings = response.json()["settings"]
        self._settings_json = json.dumps(self._settings)

    def _start_regular_renew(self):
        while True:
            time.sleep(self._seconds_until_renew_settings)
            self._renew_settings()

    def get(self, setting_key):
        if setting_key not in self._settings:
            self._settings_keys.append(setting_key)
            self._renew_settings()
        return self._settings[setting_key]