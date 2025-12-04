from pathlib import Path
import os
from dotenv import load_dotenv

# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root (guaranteed)
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# Debug prints — safe to keep while testing, remove later
print("ENV LOADED:", env_path.exists())
print("GEMINI_KEY?", bool(os.getenv("GEMINI_API_KEY")))


SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-secret')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'reviews',
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


ROOT_URLCONF = 'code_review_assistant.urls'


TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [BASE_DIR / 'templates'],
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


WSGI_APPLICATION = 'code_review_assistant.wsgi.application'


DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}


AUTH_PASSWORD_VALIDATORS = []


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static',]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'