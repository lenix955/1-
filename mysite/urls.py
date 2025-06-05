# mysite/urls.py

from django.contrib import admin
from django.urls import path, include  # Добавляем include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myblog/', include('myblog.urls')),  # Подключаем урлы из приложения myblog
]
