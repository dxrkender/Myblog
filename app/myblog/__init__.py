# -*- coding: UTF-8 -*-
"""Initialize package namespace."""
from .celery import app as celery_app

__all__ = (celery_app,)
