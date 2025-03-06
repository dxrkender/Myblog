# -*- coding: UTF-8 -*-
"""This module creates celery application."""
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.myblog.settings")

app = Celery("myblog")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
