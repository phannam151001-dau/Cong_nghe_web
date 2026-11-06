from django.db import models
from django.contrib.auth.models import User
from cua_hang.models import SanPham


class DonHang(models.Model):
    """Bảng lưu thông tin đơn đặt hàng của khách"""
    TRANG_THAI_CHOICES = [
        ('cho_xac_nhan', 'Chờ xác nhận'),
        ('da_xac_nhan', 'Đã xác nhận'),
        ('dang_giao', 'Đang giao hàng'),
        ('hoan_thanh', 'Đã hoàn thành'),
        ('da_huy', 'Đã hủy đơn'),
    ]

    khach_hang = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cac_don_hang', verbose_name="Tài khoản khách hàng")
    ten_khach_hang = models.CharField(max_length=100, verbose_name="Họ và tên khách hàng")
    so_dien_thoai = models.CharField(max_length=20, verbose_name="Số điện thoại liên hệ")
    email = models.EmailField(blank=True, null=True, verbose_name="Địa chỉ Email")
    dia_chi_giao_hang = models.TextField(verbose_name="Địa chỉ giao hàng chi tiết")
    ghi_chu = models.TextField(blank=True, null=True, verbose_name="Ghi chú đơn hàng")
    tong_tien = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Tổng tiền thanh toán (VNĐ)")
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='cho_xac_nhan', verbose_name="Trạng thái đơn hàng")
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian đặt hàng")

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "1. Quản lý Đơn Đặt Hàng"
        ordering = ['-ngay_tao']

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.ten_khach_hang}"


class ChiTietDonHang(models.Model):
    """Bảng lưu từng món sản phẩm trong đơn hàng"""
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE, related_name='danh_sach_san_pham_dat', verbose_name="Đơn hàng")
    san_pham = models.ForeignKey(SanPham, on_delete=models.SET_NULL, null=True, verbose_name="Sản phẩm")
    ten_san_pham = models.CharField(max_length=200, verbose_name="Tên sản phẩm lúc mua")
    don_gia = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Đơn giá")
    so_luong = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    kich_co = models.CharField(max_length=20, default='M', verbose_name="Kích thước (Size)")
    mau_sac = models.CharField(max_length=50, blank=True, default='', verbose_name="Màu sắc")

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "2. Chi tiết từng món trong đơn"

    def __str__(self):
        return f"{self.ten_san_pham} (Size: {self.kich_co}) x {self.so_luong}"

    def tinh_thanh_tien(self):
        return self.don_gia * self.so_luong
