from pathlib import Path
import environ
import os

env = environ.Env(
	DEBUG=(bool, False)
)


BASE_DIR = Path(__file__).resolve().parent.parent

env_file = os.path.join(BASE_DIR, '.env')

environ.Env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY', default='Optional_Default_Value_If_Not_Found')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = []

if DEBUG:
	ALLOWED_HOSTS = ['*']
else:
	ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'base',
	'corsheaders',
	'rest_framework',
	'rest_framework.authtoken',
]

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.IsAuthenticated',
	),
	'DATE_INPUT_FORMATS': ['%d/%m/%Y'],
	'DATE_FORMAT': '%d/%m/%Y',
	'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
}



CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])

ROOT_URLCONF = 'back_port.urls'

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

WSGI_APPLICATION = 'back_port.wsgi.application'


DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': env('DB_NAME'),
		'USER': env('DB_USER'),
		'PASSWORD': env('DB_PASSWORD'),
		'HOST': env('DB_HOST'),
		'PORT': env('DB_PORT'),
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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATE_INPUT_FORMATS = ['%d/%m/%Y']

DATE_FORMAT = 'd/m/Y'

DATETIME_FORMAT = 'd/m/Y H:i'