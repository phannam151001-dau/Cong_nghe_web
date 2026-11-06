from django.urls import path
from . import views

app_name = 'gio_hang'

urlpatterns = [
    path('', views.xem_gio_hang, name='xem_gio_hang'),
    path('them/<int:ma_san_pham>/', views.them_vao_gio, name='them_vao_gio'),
    path('cap-nhat/', views.cap_nhat_so_luong, name='cap_nhat_so_luong'),
    path('xoa/<str:khoa>/', views.xoa_khoi_gio, name='xoa_khoi_gio'),
    path('thanh-toan/', views.thanh_toan, name='thanh_toan'),
    path('dat-hang-thanh-cong/<int:ma_don_hang>/', views.dat_hang_thanh_cong, name='dat_hang_thanh_cong'),
    path('in-hoa-don/<int:ma_don_hang>/', views.in_hoa_don, name='in_hoa_don'),
]
