"""
admin.py
Tento soubor slouží k přizpůsobení administrace v Django.
Umožňuje přidání modelů do administrátorské sekce, kde můžeme spravovat obsah databáze přes webové rozhraní.
Můžeme zde také upravovat zobrazení a funkce administrace pro jednotlivé modely.
"""

from django.contrib import admin

from .models import Category, Priority, TodoItemStatus

# Register your models here.

admin.site.register(Category)
admin.site.register(Priority)
admin.site.register(TodoItemStatus)