from todos import views
from django.urls import path


urlpatterns = [
    # path('create', views.CreateTodoAPIView.as_view(), name = 'create-todo'),
    # path('list', views.TodoListAPIView.as_view(), name = 'list-todo'),
    path('', views.TodosAPIView.as_view(), name = 'todos'),
    path('<int:id>', views.TodoDetailAPIView.as_view(), name = 'todo')
]
