# Django settings for django-selenium-testapp project.
import os
import sys


DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# The postgres database is configured to work with travis-ci. Do not change the username!
if 'test' in sys.argv:
    # Use an in memory test database as default because this is faster. A second 
    # test database is created using the django_ttdb database as a template.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        },
        'development': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'django_ttdb',
            'USER': 'postgres',
            'HOST': '127.0.0.1',
            'TEST_TEMPLATE': True,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'django_ttdb',
            'USER': 'postgres',
            'HOST': '127.0.0.1',
        }
    }

# Use the ttdb test runner
TEST_RUNNER = 'ttdb.runner.TemplateDatabaseRunner'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Pacific/Auckland'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''#os.path.join(PROJECT_DIR, 'staticfiles')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'),)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'o5d==72stu@)03$quxuw#4=tdyji$$h88h6+8^^a)r@(22j_(h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'tests',
)
