# -*- coding: utf-8 -*-
import sys
import os

sys.path.append('/home/p/pavelsq2/gamestore')  # указываем директорию с проектом
sys.path.append('/home/p/pavelsq2/.local/lib/python3.6/site-packages')  # указываем директорию с библиотеками, куда поставили Flask
from main import main  # когда Flask стартует, он ищет application. Если не указать 'as application', сайт не заработает

application = main()

from werkzeug.debug import DebuggedApplication  # Опционально: подключение модуля отладки
application.wsgi_app = DebuggedApplication(application.wsgi_app, True)  # Опционально: включение модуля отадки
application.debug = True  # Опционально: True/False устанавливается по необходимости в отладке
