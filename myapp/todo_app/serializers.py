from .models import TodoItem, Category, TodoItemStatus, Priority
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name"]

class TodoItemStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItemStatus
        fields = "__all__"

class TodoItemSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False, label="Category"
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True, required=False, label="User"
    )
    category = CategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=TodoItemStatus.objects.all(), source='status', write_only=True, required=True, label="Status"
    )
    status = TodoItemStatusSerializer(read_only=True)
    priority_id = serializers.PrimaryKeyRelatedField(
        queryset=Priority.objects.all(), source='priority', write_only=True, required=False, label="Priority"
    )
    priority = PrioritySerializer(read_only=True)

    class Meta:
        model = TodoItem
        fields = ["id", "name", "description", "category_id", "category", "user_id", "user", "status_id", "status", "priority_id", "priority", "due_date", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

class UserTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = "__all__"
    todos = TodoItemSerializer(many=True, read_only=True, source='UserTodo')

    class Meta:
        model = User
        fields = ["id", "name", "todos"]

