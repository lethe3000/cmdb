import os
import ipaddress
import environ
from pathlib import Path

import ldap
from django_auth_ldap.config import LDAPSearch

env = environ.Env()

# Path helper
location = lambda x: os.path.join(os.path.dirname(__file__), x)

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

EMAIL_SUBJECT_PREFIX = '[Django Template] '
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Use a Sqlite database by default
DATABASES = {
    'default': {
        'ENGINE': env.str('DATABASE_ENGINE', 'django.db.backends.mysql'),  # django.db.backends.mysql
        'NAME': env.str('DATABASE_NAME', 'cmdb'),
        'USER': env.str('DATABASE_USER', 'root'),
        'PASSWORD': env.str('DATABASE_PASSWORD', 'root'),
        'HOST': env.str('DATABASE_HOST', '127.0.0.1'),
        'PORT': env.int('DATABASE_PORT', 3306),
        'ATOMIC_REQUESTS': True,
    }
}

CACHES = {
    'default': env.cache(default='locmemcache://'),
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
USE_TZ = True
TIME_ZONE = 'Asia/Shanghai'

## unittest-xml-reporting
TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_FILE_NAME = 'unittest.xml'

## nosetest
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

## default
# TEST_RUNNER = 'django.test.runner.DiscoverRunner'

SITE_ID = 1
SITE_NAME = env.str('SITE_NAME', 'app')
SITE_DOMAIN = env.str('SITE_DOMAIN', 'app.example.com')

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = location("public/media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# Default relative url: "/media/"
MEDIA_URL = env.str('MEDIA_URL', '/media/')

STATIC_URL = '/static/'
STATIC_ROOT = location('public/static')

STATIC_DIR = location('static/')
if not os.path.exists(STATIC_DIR):
    Path(STATIC_DIR).mkdir(parents=True, exist_ok=True)
    Path(STATIC_DIR).chmod(0o777)

STATICFILES_DIRS = (
    STATIC_DIR,
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = env.str('SECRET_KEY', default='UajFCuyjDKmWHe29neauXzHi9eZoRXr6RMbT5JyAdPiACBP6Cra2')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            location('templates'),
        ],
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
            'builtins': ['apps.main.templatetags.swagger'],
        }
    }
]

MIDDLEWARE = [
    'apps.api.middleware.DisableCSRFCheck',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # Allow languages to be selected
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'urls'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'django.log')
REQUEST_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'django_request.log')
SERVICE_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'service.log')
DEFAULT_LOG_DIR = os.path.dirname(DEFAULT_LOG_FILE)
Path(DEFAULT_LOG_DIR).mkdir(parents=True, exist_ok=True)
Path(DEFAULT_LOG_DIR).chmod(0o777)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(process)d %(thread)d [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s [%(name)s:%(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'default_log_file': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'filename': DEFAULT_LOG_FILE,
            'maxBytes': 16777216,  # 16megabytes
            'backupCount': 5,
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'filename': REQUEST_LOG_FILE,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'service_handler': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'filename': SERVICE_LOG_FILE,
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default_log_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_handler', 'console'],
            'level': 'DEBUG',
            # let parent logger also record the log if propagate is true
            'propagate': True,
        },
        'commands': {
            'handlers': ['console'],
            'level': 'DEBUG',
            # let parent logger also record the log if propagate is true
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['default_log_file', 'console'],
            'propagate': False,
        },
        'service': {
            'handlers': ['service_handler', 'console'],
            'level': 'DEBUG',
            # let parent logger also record the log if propagate is true
            'propagate': True,
        },
    }
}

SYS_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
]

DEP_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
]

PROJECT_APPS = [
    'apps.api',
    'apps.main',
]

INSTALLED_APPS = SYS_APPS + DEP_APPS + PROJECT_APPS

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    "django_auth_ldap.backend.LDAPBackend",
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = '/'
APPEND_SLASH = True

# ====================
# Messages contrib wework
# ====================

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# =============
# Debug Toolbar
# =============

INTERNAL_IPS = ['127.0.0.1', '::1']

# CORS
# ====

SESSION_COOKIE_SAMESITE = None
# Django 1.6 has switched to JSON serializing for security reasons, but it does not
# serialize Models. We should resolve this by extending the
# django/core/serializers/json.Serializer to have the `dumps` function. Also
# in tests/config.py
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Security
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# REST framework
# ====
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'apps.api.authentication.AuthOrAnonymousAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
}


# LDAP
# ====
AUTH_LDAP_SERVER_URI = "ldap://10.193.10.102:389"
AUTH_LDAP_BIND_DN = "CN=sa_ops,OU=SA,DC=ad,DC=yunlizhi,DC=cn"
AUTH_LDAP_BIND_PASSWORD = "D2lteBJVoV4K0Nhh"
AUTH_LDAP_START_TLS = False
AUTH_LDAP_DENY_GROUP = None
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "OU=User,DC=ad,DC=yunlizhi,DC=cn", ldap.SCOPE_SUBTREE, "(mail=%(user)s)"
)


AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn", "email": "mail"}
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0,
    ldap.OPT_NETWORK_TIMEOUT: 30
}
