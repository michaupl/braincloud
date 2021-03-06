import os

from datetime import timedelta

from mongoengine import connect

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

#from mongoengine import register_connection

# Django settings for braincloud project.

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

PROJECT_NAME = 'braincloud'
DBNAME = 'braincloud'

# register default connection with mongo
connect(DBNAME)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dev.db'),
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
MEDIA_ROOT = 'media/'
MEDIA_URL = 'media/'
STATIC_ROOT = '/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'braincloud.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'djcelery',
    'kombu.transport.django',
    'tastypie',
    'tastypie_mongoengine',
    'pagination',
    'django_extensions',
)

BRAIN_APPS = (
    'braincloud',
    'core',
    'brainblog',
    'brainindex',
    'cloudtag',
    'common',
)

INSTALLED_APPS += BRAIN_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s][%(asctime)s %(module)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# loggers for my apps
BRAIN_LOGGERS = {}
for app in BRAIN_APPS:
    BRAIN_LOGGERS[app] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    }
LOGGING['loggers'].update(BRAIN_LOGGERS)

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cloud_cache',
    }
}

# Elasticsearch
DEFAULT_INDEX = 'braincloud'
ELASTICSEARCH_URL = '127.0.0.1:9200'

DEFAULT_RESULT_SIZE = 50
SEARCH_BAR_RESULT_SIZE = 5

# INDEX_SETTINGS = {
#     'settings': {
#         'index': {
#             'analysis': {
#                 'analyzer': {
#                     'tags_analyzer': {
#                         'tokenizer': 'tags_pattern_tokenizer'
#                     }
#                 },
#                 'tokenizer': {
#                     'tags_pattern_tokenizer': {
#                         'type': 'pattern',
#                         # tokenize every tag separately
#                         'pattern': '\\"([^\"]+)\\"',
#                     }
#                 }
#             }
#         }
#     }
# }

#TODO: (maybe) exclude _all and _source from index
INDEX_MAPPINGS = {
    'mappings': {
        'text_thought': {
            'properties': {
                'title': {'type': 'string'},
                'content': {'type': 'string'},
                'pub_date': {'type': 'date'},
                'tags': {
                    # 'search_analyzer': 'tags_analyzer',
                    # 'index_analyzer': 'tags_analyzer',
                    'type': 'string'
                },
            }
        }
    }
}

import djcelery
djcelery.setup_loader()
BROKER_URL = 'django://'

CELERYBEAT_SCHEDULE = {
    "runs-every-24-hours": {
        "task": "tasks.clear_expired_sessions",
        "schedule": timedelta(hours=24),
    },
}

# shell plus
SHELL_PLUS_PRE_IMPORTS = (
    ('brainblog.models', '*'),
    ('cloudtag.models', '*'),
)

# import local settings
import platform
local_settings = '%s/%s.py' % (BASE_DIR, 'braincloud/conf/settings-%s' % platform.node().replace('.', '_'))
execfile(local_settings)

