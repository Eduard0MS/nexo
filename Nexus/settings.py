from pathlib import Path
import allauth

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-..."
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "core",
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.microsoft",
    "allauth.socialaccount.providers.google",
]
CRISPY_TEMPLATE_PACK = "bootstrap4"
SITE_ID = 1
STATIC_URL = "/static/"

LOGIN_URL = "/login/"  # nome da rota 'login'
LOGIN_REDIRECT_URL = "/home/"  # nome da rota 'home'
LOGOUT_REDIRECT_URL = "/login/"  # nome da rota 'logout'


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "Nexus.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Ajuste conforme sua estrutura
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Nexus.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Social Account Configuration
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "861236763311-nahlsmosovr7ulan1v7vfd1jpisqbatn.apps.googleusercontent.com",
            "secret": "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",
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "microsoft": {
        "APP": {
            "client_id": "YOUR_MICROSOFT_CLIENT_ID",  # Replace with your Microsoft Client ID
            "secret": "YOUR_MICROSOFT_CLIENT_SECRET",  # Replace with your Microsoft Client Secret
            "key": "",
            "tenant": "common",
        },
        "SCOPE": [
            "profile",
            "email",
            "openid",
        ],
    },
}

# Additional allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"

# Configurações para resolver o loop de redirecionamento
LOGIN_REDIRECT_URL = "/home/"
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
SOCIALACCOUNT_ADAPTER = (
    "core.adapters.CustomSocialAccountAdapter"  # Usando nosso adaptador personalizado
)

# Permitir criar contas sem e-mail verificado
SOCIALACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"

# Desativar formulários de signup sociais
SOCIALACCOUNT_FORMS = {}

# Desativar o processo de signup social para evitar o redirecionamento
SOCIALACCOUNT_AUTO_SIGNUP = True
