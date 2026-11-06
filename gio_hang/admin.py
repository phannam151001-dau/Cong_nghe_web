from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import DonHang, ChiTietDonHang


class ChiTietDonHangInline(admin.TabularInline):
    model = ChiTietDonHang
    extra = 0
    can_delete = False
    fields = ['hinh_anh_sp', 'ten_san_pham', 'kich_co', 'mau_sac', 'don_gia_vnd', 'so_luong', 'thanh_tien_vnd']
    readonly_fields = ['hinh_anh_sp', 'ten_san_pham', 'kich_co', 'mau_sac', 'don_gia_vnd', 'so_luong', 'thanh_tien_vnd']

    def has_add_permission(self, request, obj=None):
        """Tắt nút 'Thêm vào đơn hàng' để tránh phát sinh dòng trống lỗi khi quản lý đơn đã đặt"""
        return False

    def hinh_anh_sp(self, obj):
        if obj and obj.san_pham and obj.san_pham.hinh_anh:
            return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 6px;" />', obj.san_pham.hinh_anh.url)
        return format_html('<span style="color: #999;">Không có ảnh</span>')
    hinh_anh_sp.short_description = "Ảnh"

    def don_gia_vnd(self, obj):
        if obj and obj.don_gia is not None:
            return f"{obj.don_gia:,.0f}₫"
        return "0₫"
    don_gia_vnd.short_description = "Đơn giá"

    def thanh_tien_vnd(self, obj):
        if obj and obj.id:
            tien_str = f"{obj.tinh_thanh_tien():,.0f}₫"
            return format_html('<strong style="color: #dc3545;">{}</strong>', tien_str)
        return "0₫"
    thanh_tien_vnd.short_description = "Thành tiền"


@admin.register(DonHang)
class DonHangAdmin(admin.ModelAdmin):
    list_display = [
        'ma_don_hang',
        'thong_tin_khach',
        'danh_sach_san_pham_dat_mua',
        'tong_so_luong',
        'tong_tien_vnd',
        'trang_thai',             # Trường gốc để chỉnh sửa dropdown trực tiếp trên bảng
        'ngay_tao_dinh_dang',
        'xem_hoa_don'             # Biểu tượng con mắt 👁️ xem phiếu hóa đơn chuẩn đẹp
    ]
    list_editable = ['trang_thai'] # Cho phép Admin đổi trực tiếp trạng thái ngay trên danh sách
    list_filter = ['trang_thai', 'ngay_tao']
    search_fields = [
        'id',
        'ten_khach_hang',
        'so_dien_thoai',
        'email',
        'dia_chi_giao_hang',
        'danh_sach_san_pham_dat__ten_san_pham'
    ]
    readonly_fields = ['ngay_tao', 'tong_tien_vnd', 'xem_hoa_don']
    list_per_page = 20

    fieldsets = [
        ('1. Thông tin Khách Hàng & Tài Khoản', {
            'fields': ['khach_hang', 'ten_khach_hang', 'so_dien_thoai', 'email']
        }),
        ('2. Địa Chỉ Giao Hàng & Ghi Chú', {
            'fields': ['dia_chi_giao_hang', 'ghi_chu', 'ngay_tao']
        }),
        ('3. Thanh Toán & Trạng Thái Đơn Hàng', {
            'fields': ['trang_thai', 'tong_tien', 'tong_tien_vnd', 'xem_hoa_don']
        }),
    ]
    inlines = [ChiTietDonHangInline]

    def ma_don_hang(self, obj):
        return format_html('<strong>#HD{}</strong>', obj.id)
    ma_don_hang.short_description = "Mã đơn"

    def thong_tin_khach(self, obj):
        tai_khoan = f" (TK: {obj.khach_hang.username})" if obj.khach_hang else " (Khách vãng lai)"
        return format_html(
            '<div><strong>{}</strong>{}</div><div style="font-size: 12px; color: #666;"><i class="fa fa-phone"></i> {}</div>',
            obj.ten_khach_hang,
            tai_khoan,
            obj.so_dien_thoai
        )
    thong_tin_khach.short_description = "Khách hàng"

    def danh_sach_san_pham_dat_mua(self, obj):
        """Hiển thị danh sách tất cả các sản phẩm có trong đơn hàng ra bảng danh sách"""
        items = obj.danh_sach_san_pham_dat.all()
        if not items:
            return format_html('<span style="color: #999;">Trống</span>')
        
        dong_html = []
        for item in items:
            dong_html.append(
                f'<div style="margin-bottom: 4px; padding: 2px 0; border-bottom: 1px dashed #eee;">'
                f'• <strong>{item.ten_san_pham}</strong> '
                f'<span style="background: #f1f5f9; padding: 1px 6px; border-radius: 4px; font-size: 11px;">Size: {item.kich_co}</span> '
                f'<span style="color: #0284c7; font-weight: bold;">x{item.so_luong}</span>'
                f'</div>'
            )
        return format_html("".join(dong_html))
    danh_sach_san_pham_dat_mua.short_description = "Sản phẩm đặt mua (Chi tiết)"

    def tong_so_luong(self, obj):
        tong_sl = sum(item.so_luong for item in obj.danh_sach_san_pham_dat.all())
        return format_html('<span style="font-weight: bold; font-size: 13px;">{} món</span>', tong_sl)
    tong_so_luong.short_description = "Tổng món"

    def tong_tien_vnd(self, obj):
        if obj and obj.tong_tien is not None:
            tien_str = f"{obj.tong_tien:,.0f}₫"
            return format_html('<strong style="color: #dc3545; font-size: 14px;">{}</strong>', tien_str)
        return "0₫"
    tong_tien_vnd.short_description = "Tổng tiền"

    def ngay_tao_dinh_dang(self, obj):
        return obj.ngay_tao.strftime("%d/%m/%Y %H:%M")
    ngay_tao_dinh_dang.short_description = "Thời gian đặt"

    def xem_hoa_don(self, obj):
        """Biểu tượng con mắt xem và in phiếu hóa đơn bán lẻ chuyên nghiệp"""
        url = reverse('gio_hang:in_hoa_don', args=[obj.id])
        return format_html(
            '<a href="{}" target="_blank" title="Xem & in phiếu hóa đơn" style="text-decoration: none; font-size: 20px; display: inline-block; cursor: pointer;">'
            '👁️'
            '</a>',
            url
        )
    xem_hoa_don.short_description = "Hóa đơn"


@admin.register(ChiTietDonHang)
class ChiTietDonHangAdmin(admin.ModelAdmin):
    """Mục quản lý chi tiết từng món đồ đã bán theo sản phẩm"""
    list_display = [
        'id',
        'hinh_anh_sp',
        'ten_san_pham',
        'lien_ket_don_hang',
        'kich_co',
        'mau_sac',
        'don_gia_vnd',
        'so_luong',
        'thanh_tien_vnd',
        'ngay_dat_hang'
    ]
    list_filter = ['kich_co', 'don_hang__trang_thai', 'don_hang__ngay_tao']
    search_fields = [
        'ten_san_pham',
        'don_hang__id',
        'don_hang__ten_khach_hang',
        'don_hang__so_dien_thoai'
    ]
    readonly_fields = ['don_hang', 'san_pham', 'ten_san_pham', 'don_gia', 'so_luong', 'kich_co', 'mau_sac']

    def has_add_permission(self, request):
        return False

    def hinh_anh_sp(self, obj):
        if obj and obj.san_pham and obj.san_pham.hinh_anh:
            return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 6px;" />', obj.san_pham.hinh_anh.url)
        return format_html('<span style="color: #999;">Không có ảnh</span>')
    hinh_anh_sp.short_description = "Ảnh"

    def lien_ket_don_hang(self, obj):
        url = reverse('admin:gio_hang_donhang_change', args=[obj.don_hang.id])
        return format_html('<a href="{}" style="font-weight: bold;">Đơn #HD{} ({})</a>', url, obj.don_hang.id, obj.don_hang.ten_khach_hang)
    lien_ket_don_hang.short_description = "Đơn hàng"

    def don_gia_vnd(self, obj):
        if obj and obj.don_gia is not None:
            return f"{obj.don_gia:,.0f}₫"
        return "0₫"
    don_gia_vnd.short_description = "Đơn giá"

    def thanh_tien_vnd(self, obj):
        if obj and obj.id:
            tien_str = f"{obj.tinh_thanh_tien():,.0f}₫"
            return format_html('<strong style="color: #dc3545;">{}</strong>', tien_str)
        return "0₫"
    thanh_tien_vnd.short_description = "Thành tiền"

    def ngay_dat_hang(self, obj):
        return obj.don_hang.ngay_tao.strftime("%d/%m/%Y %H:%M")
    ngay_dat_hang.short_description = "Ngày đặt"
