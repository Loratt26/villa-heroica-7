import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-villa-heroica-local-dev-key-2024')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'control',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'asistencia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'asistencia.wsgi.application'

# ── Base de datos ─────────────────────────────────────────────────────────────
# PostgreSQL si DATABASE_URL está definido (Railway/producción)
# SQLite con WAL en desarrollo/Vercel
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-ve'
TIME_ZONE = 'America/Caracas'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# ── Kiosco ────────────────────────────────────────────────────────────────────
KIOSCO_TOLERANCIA_TARDANZA_MIN  = int(os.environ.get('TOLERANCIA_TARDANZA_MIN', 20))
KIOSCO_TOLERANCIA_SALIDA_ANT_MIN = int(os.environ.get('TOLERANCIA_SALIDA_ANT_MIN', 40))
KIOSCO_BIENVENIDA_SEGUNDOS      = int(os.environ.get('BIENVENIDA_SEGUNDOS', 4))
KIOSCO_IDLE_SEGUNDOS            = int(os.environ.get('IDLE_SEGUNDOS', 30))

# ── Cache (para idempotencia de marcaje) ─────────────────────────────────────
# En producción reemplazar con Redis: django-redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'villa-heroica-cache',
    }
}

# ── Logging ───────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestamp': {
            'format': '{asctime} {levelname} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'timestamp',
        },
        'archivo': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(BASE_DIR / 'logs' / 'asistencia.log'),
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 3,
            'formatter': 'timestamp',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'control.asistencia': {
            'handlers': ['console', 'archivo'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Crear directorio de logs si no existe
import os as _os
_logs_dir = BASE_DIR / 'logs'
if not _logs_dir.exists():
    _logs_dir.mkdir(exist_ok=True)

# ── CSRF ──────────────────────────────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.railway.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
