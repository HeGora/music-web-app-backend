from django.urls import path, include
from user.api.views import LoginView, RegisterView

urlpatterns = [
    path('api/auth/', include('knox.urls')),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('register/', RegisterView.as_view(), name='knox_register'),
]