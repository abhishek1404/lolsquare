"""
Django settings for metastore project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ldap
from django_auth_ldap.config import LDAPSearch

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = BASE_DIR + '/..'
print BASE_DIR
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '18!iyum4lh8@*180@*pts#$35wh1&z0iw)2(v62((vjq*-1y%2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'tastypie',
    'metastore',
    'metastore.apps',
    'tastypie_swagger',
    'django_object_actions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    #'django_zipkin.middleware.ZipkinMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'metastore.urls'

WSGI_APPLICATION = 'metastore.wsgi.application'

'''
CACHES = {
    'old_default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/test_cache',
        'TIMEOUT': 1,
    },
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 2,
    },
}
'''

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lols',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

DEFAULT_TABLESPACE = ''

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/opt/mkhoj/libexec/static/'

app_name = 'metastore'


# Logging
log_file = '/opt/mkhoj/logs/' + app_name + '/access.log'
LOGFILE_PATH = log_file if os.path.exists(log_file) else '%s.access.log' % app_name
LOGFILE_SIZE = 200 * 1024 * 1024  # 200M
LOGFILE_COUNT = 5
METASTORE_LOGFILE_PATH = '/opt/mkhoj/logs/metastore.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },

    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGFILE_PATH,
            'maxBytes': LOGFILE_SIZE,
            'backupCount': LOGFILE_COUNT,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },


    },
    'loggers': {
        # '': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': True
        # },
        'django': {
            'handlers': ['file'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'propagate': False,
        },

    },
}

GRAPPELLI_ADMIN_TITLE = 'metastore'
GRAPPELLI_AUTOCOMPLETE_LIMIT = 5
GRAPPELLI_CLEAN_INPUT_TYPES = True
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'django_auth_ldap.backend.LDAPBackend',
)


