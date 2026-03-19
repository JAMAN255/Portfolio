from django.urls import path
from . import views

urlpatterns = [
    # Todo Web Views
    path('todos/', views.TodoListView.as_view(), name='todo_list'),
    path('todos/<int:pk>/', views.TodoDetailView.as_view(), name='todo_detail'),
    path('todos/create/', views.TodoCreateView.as_view(), name='todo_create'),
    path('todos/<int:pk>/update/', views.TodoUpdateView.as_view(), name='todo_update'),
    path('todos/<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo_delete'),
]
