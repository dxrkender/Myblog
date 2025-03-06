# -*- coding: UTF-8 -*-
"""
ASGI config for myblog project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.myblog.settings')

application = get_asgi_application()
