import os

DEBUG = True
ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print 'asdasdadsadad', BASE_DIR
TITLE = 'ZUP'
SECRET_KEY = '55y#@=es!l$u!2+a70ur1j1ao-2%u2&45*c_ax!^j-mouli+m('

DB_ENGINE = 'django.db.backends.sqlite3'
DB_NAME = os.path.join(BASE_DIR, 'sqlite/zup.sqlite3')

LANGUAGE_CODE = 'en-us'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

PYTHON_INTERPRETER = '/Users/daniele.guido/Envs/zup/bin/python'

ENABLE_CDN_SERVICES = False#True