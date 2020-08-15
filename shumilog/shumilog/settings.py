from .settings_common import *
import os


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'shumilog': {
            'handlers': ['file'],
            'level': 'INFO',
        }
    },
    'handlers': {
      'file': {
          'level': 'INFO',
          'class': 'logging.handlers.TimedRotatingFileHandler',
          'filename': os.path.join(BASE_DIR, 'logs/django.log'),
          'formatter': 'prod',
          'when': 'D',
          'interval': 1,
          'backupCount': 7,
      },
    },
    'formatters': {
        'prod': {
            'format': '\t'.join({
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            })
        },
    }
}

#security
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_PRELOAD = True
