import os
from decouple import config
from pathlib import Path
from datetime import timedelta


import os


# Load environment variables from .env file
# load_dotenv()

DB_ENGINE_DEV = os.getenv('DB_ENGINE_DEV')
DB_NAME_DEV = os.getenv('DB_NAME_DEV')
DB_USER_DEV = os.getenv('DB_USER_DEV')
DB_PASSWORD_DEV = os.getenv('DB_PASSWORD_DEV')
DB_HOST_DEV = os.getenv('DB_HOST_DEV')
DB_PORT_DEV = os.getenv('DB_PORT_DEV')

DB_ENGINE_PROD = os.getenv('DB_ENGINE_PROD')
DB_NAME_PROD = os.getenv('DB_NAME_PROD')
DB_USER_PROD = os.getenv('DB_USER_PROD')
DB_PASSWORD_PROD = os.getenv('DB_PASSWORD_PROD')
DB_HOST_PROD = os.getenv('DB_HOST_PROD')
DB_PORT_PROD = os.getenv('DB_PORT_PROD')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL =os.getenv('DEFAULT_FROM_EMAIL')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1yd$y6)cjv&o8p&-fl&alj=n+s6!tu7)z(160ld%ml%m36qax!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    # apps
    "events",
    "chamber",
    "message",
    "newsletters.apps.NewslettersConfig",
    "block.apps.BlockConfig",
    "core.apps.CoreConfig",
    "notifications",
    "search",
    "portfolio",
    # install app
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "taggit",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "guardian",
    'drf_yasg' ,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "pyramid.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": False,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
ASGI_APPLICATION = "pyramid.routing.application"
WSGI_APPLICATION = "pyramid.wsgi.application"
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if os.environ.get('ENVIRONMENT') == 'DEV':
    DB_ENGINE = DB_ENGINE_DEV
    DB_NAME = DB_NAME_DEV
    DB_USER = DB_USER_DEV
    DB_PASSWORD = DB_PASSWORD_DEV
    DB_HOST = DB_HOST_DEV
    DB_PORT = DB_PORT_DEV
else:
    DB_ENGINE = DB_ENGINE_PROD
    DB_NAME = DB_NAME_PROD
    DB_USER = DB_USER_PROD
    DB_PASSWORD = DB_PASSWORD_PROD
    DB_HOST = DB_HOST_PROD
    DB_PORT = DB_PORT_PROD
DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    }
}

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# media
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# logging
from .logger import LOGGING

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "core.User"





# api
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "TEST_REQUEST_RENDERER_CLASSES": [
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"login": "7/day"},
    "DEFAULT_PERMISSION_CLASSES": [
        #  'rest_framework.permissions.IsSuperUserOrReadOnly',
        "rest_framework.permissions.AllowAny",
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


CORS_ORIGIN_ALLOW_ALL = True

# CORS

CORS_ALLOW_HEADERS = [
    "x-requested-with",
    "content-type",
    "accept",
    "origin",
    "authorization",
    "accept-encoding",
    "x-csrftoken",
    "access-control-allow-origin",
    "content-disposition",
]
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    # 'UPDATE_LAST_LOGIN': False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    # 'AUDIENCE': None,
    # 'ISSUER': None,
    # 'JWK_URL': None,
    # 'LEEWAY': 0,
    #'AUTH_HEADER_TYPES': ('Bearer','JWT',),
    # 'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    # 'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    # 'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    # 'JTI_CLAIM': 'jti',
    # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # default
    "guardian.backends.ObjectPermissionBackend",
)

DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE')

STATIC_LOCATION = "static"
MEDIA_LOCATION = "media"

AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
