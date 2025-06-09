from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='account_login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='account_logout'),
    path('accounts/signup/', TemplateView.as_view(template_name='registration/signup.html'), name='account_signup'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)