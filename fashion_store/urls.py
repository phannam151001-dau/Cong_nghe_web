from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Thay đổi tiêu đề trang quản trị Django Admin sang tiếng Việt
admin.site.site_header = "HỆ THỐNG QUẢN TRỊ FASHION STORE"
admin.site.site_title = "Quản trị Fashion Store"
admin.site.index_title = "Bảng điều khiển quản lý bán hàng"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('khach-hang/', include('khach_hang.urls', namespace='khach_hang')),
    path('gio-hang/', include('gio_hang.urls', namespace='gio_hang')),
    path('', include('cua_hang.urls', namespace='cua_hang')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
