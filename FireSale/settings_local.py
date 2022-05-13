DATABASES = {
  'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'firesale-db',
        'USER': 'adh-firesale-user',
        'PASSWORD': '=qk-V77J?rs(^`),',
        'HOST': '35.246.89.129',
        'PORT': '5432'
    }
}

SECRET_KEY = 'django-insecure-v%s9*p!-dvyp-3kpevf6l15na=a!@r_&f+tyk_(3kfifeevi=h'

WSGI_APPLICATION = 'FireSale.wsgi.application'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'firesale.ehf@gmail.com'
EMAIL_HOST_PASSWORD = 'firesalepassword'