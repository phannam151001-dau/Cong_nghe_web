from django.urls import path
from . import views

app_name = 'cua_hang'

urlpatterns = [
    path('', views.danh_sach_san_pham, name='trang_chu'),
    path('danh-muc/<slug:slug_danh_muc>/', views.danh_sach_san_pham, name='san_pham_theo_danh_muc'),
    path('san-pham/<slug:slug>/', views.chi_tiet_san_pham, name='chi_tiet_san_pham'),
    path('gioi-thieu/', views.gioi_thieu, name='gioi_thieu'),
    path('lien-he/', views.lien_he, name='lien_he'),
]
