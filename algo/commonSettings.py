"""
Importable settings file
"""
import os
import sys

SETTINGS_FILE = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)) + r"/settings.ini"
