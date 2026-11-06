from django.urls import path
from . import views

app_name = 'khach_hang'

urlpatterns = [
    path('dang-ky/', views.dang_ky, name='dang_ky'),
    path('dang-nhap/', views.dang_nhap, name='dang_nhap'),
    path('dang-xuat/', views.dang_xuat, name='dang_xuat'),
    path('lich-su-don-hang/', views.lich_su_don_hang, name='lich_su_don_hang'),
    path('hoa-don/<int:ma_don_hang>/', views.chi_tiet_hoa_don, name='chi_tiet_hoa_don'),
    path('tai-khoan/', views.thong_tin_tai_khoan, name='thong_tin_tai_khoan'),
]
