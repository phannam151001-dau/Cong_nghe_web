from django.contrib import admin
from .models import HoSoKhachHang


@admin.register(HoSoKhachHang)
class HoSoKhachHangAdmin(admin.ModelAdmin):
    list_display = ['user', 'so_dien_thoai', 'dia_chi', 'ngay_tao']
    search_fields = ['user__username', 'user__first_name', 'so_dien_thoai', 'dia_chi']
