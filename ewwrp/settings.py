import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'm^$n!$^l#lzwk1)m%)j^xf&&l%dee@_!-au7qa&8bu*c)x$hjw'

# Don't run with debug turned on in production
DEBUG = True

# Not sure if this is necessary
DATABASES = {'default': {'ENGINE': '', 'NAME': ''}}

# The collections
DEFAULT_ORDERING = 'author' # Default way to order results
DEFAULT_COLLECTION = 'ewwrp'
COLLECTIONS = {
    'ewwrp': {
        'name': 'Emory Women Writers Resource Project',
        'shortname': 'ewwrp',
        'longname': ('Emory Women Writers', 'Resource Project'),
        'color': '336633'
    },
    'genrefiction': {
        'name': 'Genre Fiction',
        'shortname': 'genrefiction',
        'longname': ('Women\'s Genre Fiction', 'Project'),
        'color': '990000'
    },
    'earlymodern': {
        'name': 'Early Modern through the 18th Century',
        'shortname': 'earlymodern',
        'longname': ('Early Modern through the', '18th Century'),
        'color': '990066'
    },
    'twentiethcentury': {
        'name': 'Early 20th Century Literature',
        'shortname': 'twentiethcentury',
        'longname': ('Early 20th Century', 'Literature'),
        'color': '660099'
    },
    'worldwari': {
        'name': 'World War I',
        'shortname': 'worldwari',
        'longname': ('World War I Poetry', 'Collection'),
        'color': '330099'
    },
    'nativeamerican': {
        'name': 'Native American',
        'shortname': 'nativeamerican',
        'longname': ('Native American', 'Collection'),
        'color': '003399'
    },
    'abolition': {
        'name': 'Abolition, Freedom, and Rights',
        'shortname': 'abolition',
        'longname': ('Abolition, Freedom, and', 'Rights Collection'),
        'color': '009966'
    },
    'advocacy': {
        'name': 'Women\'s Advocacy',
        'shortname': 'advocacy',
        'longname': ('Women\'s Advocacy', 'Collection'),
        'color': '339900'
    },
}


try:
    from secret import *
except ImportError:
    #ExistDB settings
    EXISTDB_SERVER_PROTOCOL = "http://"
    EXISTDB_SERVER_HOST     = "kamina.library.emory.edu:8080/exist/"
    EXISTDB_SERVER_USER     = ""
    EXISTDB_SERVER_PASSWORD = ""
    EXISTDB_SERVER_URL      = EXISTDB_SERVER_PROTOCOL + EXISTDB_SERVER_HOST
    EXISTDB_ROOT_COLLECTION = "/ewwrp"

EXISTDB_INDEX_CONFIGFILE = os.path.join(BASE_DIR, "collections.xconf")

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # EULXML-related
    'eulexistdb',
    'eulxml',
    'eulcommon',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ewwrp.urls'
WSGI_APPLICATION = 'ewwrp.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Customize
MEDIA_ROOT = os.path.join(BASE_DIR, 'ewwrp', 'static')
MEDIA_URL = ''
STATIC_URL = '/static/'

# May not be necessary
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'ewwrp', 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'ewwrp', 'templates'),
)