"""
Django settings for fashion_store project.
Hệ thống cấu hình dự án Web Bán Quần Áo (Fashion Store)
"""

from pathlib import Path
import os
import dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-local-development-key'
)

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1'
).split(',')

# 1. Các ứng dụng đã cài đặt (INSTALLED_APPS)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',      # Định dạng số tiền (100,000đ)
    'cua_hang',                     # App quản lý Cửa hàng & Sản phẩm
    'gio_hang',                     # App quản lý Giỏ hàng & Đơn đặt hàng
    'khach_hang',                   # App quản lý Khách hàng & Lịch sử đơn hàng
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'fashion_store.urls'

# 2. Cấu hình giao diện HTML Templates
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
                # Context Processors chia sẻ dữ liệu toàn cục cho Navbar:
                'cua_hang.context_processors.truyen_danh_muc_toan_cuc',
                'gio_hang.context_processors.truyen_gio_hang_toan_cuc',
            ],
        },
    },
]

WSGI_APPLICATION = 'fashion_store.wsgi.application'

# 3. Cấu hình Cơ sở dữ liệu (Database)
# Mặc định sử dụng SQLite. Khi bạn bật MySQL trên XAMPP và tạo database `web_ban_ao_quan`,
# bạn chỉ cần mở đoạn cấu hình MySQL bên dưới và comment lại SQLite:

# 3. Cấu hình Cơ sở dữ liệu MySQL XAMPP
if os.environ.get('DATABASE_URL'):
    # Khi chạy trên Render: sử dụng PostgreSQL
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Khi chạy trên máy tính: sử dụng MySQL XAMPP
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'web_ban_ao_quan',
            'USER': 'root',
            'PASSWORD': '0828937914n',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
        }
    }
#     }
# }

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

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True

# 4. Cấu hình Static Files (CSS, JS, Hình ảnh tĩnh)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# 5. Cấu hình Media Files (Ảnh sản phẩm tải lên)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
