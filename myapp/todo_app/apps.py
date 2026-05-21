"""
apps.py
Tento soubor definuje konfiguraci aplikace v rámci projektu Django.
Obsahuje třídu, která specifikuje jméno aplikace a další vlastnosti.
Slouží k registraci aplikace v projektu a může být použit i pro specifické nastavení dané aplikace.
"""

from django.apps import AppConfig

class TodoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_app'
