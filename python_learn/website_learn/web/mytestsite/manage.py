#!/usr/bin/env python
"""
Author: zhangyifan1
Date: 2023-07-26 17:04:11
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2023-07-26 18:51:33
FilePath: //website_learn//web//mytestsite//manage.py
Description: 

"""
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mytestsite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
