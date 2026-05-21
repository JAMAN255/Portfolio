"""
models.py
Tento soubor definuje datové modely (třídy), které představují tabulky v databázi.
Každá třída v tomto souboru reprezentuje jednu tabulku a jednotlivé vlastnosti jsou
sloupce této tabulky.
"""

from django.db import models
from django.conf import settings

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class TodoItemStatus(models.Model):
    name = models.CharField(max_length=200, blank=False)
    
    class Meta:
        verbose_name_plural = "Todo Item Statuses"
    
    def __str__(self):
        return self.name

class Priority(models.Model):
    level = models.IntegerField(blank=False, unique=True)
    
    class Meta:
        verbose_name_plural = "Priorities"
    
    def __str__(self):
        return f"Priority {self.level}"


class TodoItem(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="todo_items", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="todo_items", null=True, blank=True)
    status = models.ForeignKey(TodoItemStatus, on_delete=models.CASCADE, related_name="todo_items", null=True, blank=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, related_name="todo_items", null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Todo Items"
    
    def __str__(self):
        return self.name

class UserTodo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_todos", null=True, blank=True)
    todo_item = models.ForeignKey(TodoItem, on_delete=models.CASCADE, related_name="user_todos", null=True, blank=True)

    class Meta:
        verbose_name_plural = "User Todos"

    def __str__(self):
        return f"{self.user} - {self.todo_item}"