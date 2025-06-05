from django.urls import path
from . import views

app_name = 'myblog'  # обязательно при использовании namespace в include()

urlpatterns = [
    path('', views.post_list, name='post_list'),  # это главная страница блога
    path('<int:id>/', views.post_detail, name='post_detail'),  # детальная страница поста
]
