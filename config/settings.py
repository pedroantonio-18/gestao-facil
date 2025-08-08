from pathlib import Path
from decouple import config
import re

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

# Adicione hosts locais
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'config',
    'core',
    'contratos',
    'pessoal',
    'insumos',
    'penalidades',
    'pagamentos',
    'pages.apps.PagesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Configuração do Banco de Dados
db_url = config('DATABASE_URL')

pattern = r'postgres(?:ql)?://(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:/]+)(?::(?P<port>\d+))?/(?P<name>[^\?]+)(?:\?sslmode=(?P<sslmode>\w+))?'
match = re.match(pattern, db_url)

if not match:
    raise ValueError("DATABASE_URL inválida")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': match.group('name'),
        'USER': match.group('user'),
        'PASSWORD': match.group('password'),
        'HOST': match.group('host'),
        'PORT': match.group('port') or '5432',
        'OPTIONS': {
            'sslmode': match.group('sslmode') or 'require',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# =================================================================================
# Configuração de Arquivos Estáticos (Static Files) - CORRIGIDA
# =================================================================================

STATIC_URL = '/static/'

# A pasta 'staticfiles' na raiz do seu projeto será a ORIGEM de arquivos estáticos.
STATICFILES_DIRS = [
   BASE_DIR / "pages" / "static",
]

# A pasta 'static_collected' será o DESTINO final onde os arquivos serão coletados.
# É crucial que esta pasta seja diferente de 'STATICFILES_DIRS'.
STATIC_ROOT = BASE_DIR / 'static_collected'


# =================================================================================


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Informações para envio de emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Informações para envio de mensagens no Teams
TEAMS_WEBHOOK = config('TEAMS_WEBHOOK')

# Adicione também para media files se necessário
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'