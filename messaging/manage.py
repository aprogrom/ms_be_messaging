#!/usr/bin/env python3
import sys
import os
from config.utils import EnviromentVariable

if __name__ == "__main__":
    SETTINGS = "config.settings." + EnviromentVariable().SETTINGS
    # print(SETTINGS)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS)
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)