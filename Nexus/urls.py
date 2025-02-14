from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


from core.views import CustomLoginView, register, home, organograma_data, organograma_page

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login e logout
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('accounts/', include('allauth.urls')),  # Rotas do Allauth
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('organograma/data/', organograma_data, name='organograma_data'),

    # Rota raíz -> envia para 'home' (opcional)
    path('', home, name='root_home'),
]
