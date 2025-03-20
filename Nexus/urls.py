from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView


from core.views import (
    CustomLoginView,
    register,
    home,
    organograma_data,
    organograma_page,
    simulacao_page,
    CustomSocialLoginView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Login e logout
    path(
        "login/",
        RedirectView.as_view(url="/login_direct/", permanent=True),
        name="login",
    ),
    path("login_direct/", CustomLoginView.as_view(), name="login_direct"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/login_direct/"),
        name="logout",
    ),
    path("accounts/", include("allauth.urls")),  # Rotas do Allauth
    path(
        "accounts/social/signup/",
        CustomSocialLoginView.as_view(),
        name="socialaccount_signup",
    ),
    # Rota adicional para resolver o problema de redirecionamento
    path(
        "accounts/social/signup",
        RedirectView.as_view(url="/home/", permanent=True),
    ),
    path("register/", register, name="register"),
    path("home/", home, name="home"),
    path("organograma/data/", organograma_data, name="organograma_data"),
    path("organograma/", organograma_page, name="organograma"),
    path("simulacao/", simulacao_page, name="simulacao"),
    # Rota raíz -> envia para 'home' (opcional)
    path("", home, name="root_home"),
]
