"""
views.py
Tento soubor obsahuje view funkce nebo třídy, které obsluhují požadavky uživatelů.
Zpracovávají data, která jsou získána z modelů nebo jiných zdrojů, a vrací odpověď
uživateli (např. HTML stránku nebo JSON).
"""

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from todo_app.forms import TodoItemForm
from todo_app.models import TodoItem, Category, TodoItemStatus, Priority, UserTodo
from rest_framework import viewsets
from .serializers import TodoItemSerializer, CategorySerializer, UserSerializer, TodoItemStatusSerializer, PrioritySerializer, UserTodoSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request):
    context = {"message": "Todo App"}
    return render(request, "index.html", context)


class TodoListView(ListView):
    model = TodoItem
    template_name = 'todo_app/todo_list.html'
    context_object_name = 'todos'
    paginate_by = 10


class TodoDetailView(DetailView):
    model = TodoItem
    template_name = 'todo_app/todo_detail.html'
    context_object_name = 'todo'


class TodoCreateView(CreateView):
    model = TodoItem
    form_class = TodoItemForm
    template_name = 'todo_app/todo_form.html'
    success_url = reverse_lazy('todo_list')


class TodoUpdateView(UpdateView):
    model = TodoItem
    form_class = TodoItemForm
    template_name = 'todo_app/todo_form.html'
    success_url = reverse_lazy('todo_list')


class TodoDeleteView(DeleteView):
    model = TodoItem
    template_name = 'todo_app/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')


# REST API ViewSets
class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TodoItemStatusViewSet(viewsets.ModelViewSet):
    queryset = TodoItemStatus.objects.all()
    serializer_class = TodoItemStatusSerializer


class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


class UserTodoViewSet(viewsets.ModelViewSet):
    queryset = UserTodo.objects.all()
    serializer_class = UserTodoSerializer
    serializer_class = TodoItemSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TodoItemStatusViewSet(viewsets.ModelViewSet):
    queryset = TodoItemStatus.objects.all()
    serializer_class = TodoItemStatusSerializer

class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer

class UserTodoViewSet(viewsets.ModelViewSet):
    queryset = UserTodo.objects.all()
    serializer_class = UserTodoSerializer