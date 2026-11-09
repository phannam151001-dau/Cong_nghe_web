from django.contrib import admin
from django.utils.html import format_html
from .formatters import format_vnd
from .models import DanhMuc, SanPham


@admin.register(DanhMuc)
class DanhMucAdmin(admin.ModelAdmin):
    list_display = ['anh_dai_dien', 'ten_danh_muc', 'slug', 'so_san_pham']
    prepopulated_fields = {'slug': ('ten_danh_muc',)}
    search_fields = ['ten_danh_muc']

    def anh_dai_dien(self, obj):
        if obj.hinh_anh:
            return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 6px;" />', obj.hinh_anh.url)
        return format_html('<span style="color: #999;">Chưa có ảnh</span>')
    anh_dai_dien.short_description = "Ảnh"

    def so_san_pham(self, obj):
        return f"{obj.san_phams.count()} sản phẩm"
    so_san_pham.short_description = "Số lượng SP"


@admin.register(SanPham)
class SanPhamAdmin(admin.ModelAdmin):
    list_display = [
        'anh_san_pham',
        'ten_san_pham',
        'danh_muc',
        'gia_ban_vnd',
        'gia_goc_vnd',
        'so_luong_kho',
        'noi_bat',
        'dang_kinh_doanh',
        'ngay_tao'
    ]
    list_filter = ['danh_muc', 'dang_kinh_doanh', 'noi_bat', 'ngay_tao']
    list_editable = ['so_luong_kho', 'noi_bat', 'dang_kinh_doanh']
    prepopulated_fields = {'slug': ('ten_san_pham',)}
    search_fields = ['ten_san_pham', 'mo_ta', 'danh_muc__ten_danh_muc']
    list_per_page = 20

    def anh_san_pham(self, obj):
        if obj.hinh_anh:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px;" />', obj.hinh_anh.url)
        return format_html('<span style="color: #999;">Chưa có ảnh</span>')
    anh_san_pham.short_description = "Ảnh"

    def gia_ban_vnd(self, obj):
        gia_str = f"{format_vnd(obj.gia_ban)}₫"
        return format_html('<strong style="color: #dc3545;">{}</strong>', gia_str)
    gia_ban_vnd.short_description = "Giá bán"

    def gia_goc_vnd(self, obj):
        if obj.gia_goc:
            return f"{format_vnd(obj.gia_goc)}₫"
        return "-"
    gia_goc_vnd.short_description = "Giá gốc"
