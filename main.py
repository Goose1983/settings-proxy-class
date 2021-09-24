import time

from settings_proxy.settings_proxy import SettingsProxy

if __name__ == '__main__':
    settings_proxy = SettingsProxy("http://127.0.0.1:8000/api/v1/matrix_settings",
                                   [
                                       "ATTR_MOD",
                                       "REQUEST_PARAMETERS",
                                       "TIMEOUT",
                                       "REPEAT_INTERVAL",
                                       "TEST"
                                   ],
                                   10)
