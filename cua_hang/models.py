from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class DanhMuc(models.Model):
    """Bảng lưu Danh mục sản phẩm (Áo sơ mi, Áo polo, Quần tây, Váy đầm...)"""
    ten_danh_muc = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="Đường dẫn tĩnh (Slug)")
    mo_ta = models.TextField(blank=True, verbose_name="Mô tả danh mục")
    hinh_anh = models.ImageField(upload_to='danh_muc/', blank=True, null=True, verbose_name="Hình ảnh đại diện")

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "1. Quản lý Danh Mục Sản Phẩm"
        ordering = ['ten_danh_muc']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.ten_danh_muc)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ten_danh_muc

    def get_absolute_url(self):
        return reverse('cua_hang:san_pham_theo_danh_muc', args=[self.slug])


class SanPham(models.Model):
    """Bảng lưu thông tin Sản phẩm thời trang"""
    danh_muc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE, related_name='san_phams', verbose_name="Danh mục")
    ten_san_pham = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name="Đường dẫn tĩnh (Slug)")
    hinh_anh = models.ImageField(upload_to='san_pham/', blank=True, null=True, verbose_name="Ảnh sản phẩm")
    gia_ban = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá bán hiện tại (VNĐ)")
    gia_goc = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, verbose_name="Giá niêm yết cũ (VNĐ)")
    mo_ta = models.TextField(verbose_name="Mô tả chi tiết sản phẩm")
    kich_co = models.CharField(max_length=100, default='S, M, L, XL', verbose_name="Các kích cỡ (Size - cách nhau bằng dấu phẩy)")
    mau_sac = models.CharField(max_length=100, default='Trắng, Đen, Xanh', verbose_name="Các màu sắc (cách nhau bằng dấu phẩy)")
    so_luong_kho = models.PositiveIntegerField(default=50, verbose_name="Số lượng tồn kho")
    noi_bat = models.BooleanField(default=False, verbose_name="Sản phẩm nổi bật / Bán chạy")
    dang_kinh_doanh = models.BooleanField(default=True, verbose_name="Đang kinh doanh (Hiển thị lên web)")
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng")
    ngay_cap_nhat = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "2. Quản lý Sản Phẩm Thời Trang"
        ordering = ['-ngay_tao']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.ten_san_pham)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ten_san_pham

    def get_absolute_url(self):
        return reverse('cua_hang:chi_tiet_san_pham', args=[self.slug])

    def danh_sach_kich_co(self):
        """Tách chuỗi kích cỡ thành danh sách để render radio button chọn size"""
        if self.kich_co:
            return [s.strip() for s in self.kich_co.split(',') if s.strip()]
        return ['Freesize']

    def danh_sach_mau_sac(self):
        """Tách chuỗi màu sắc thành danh sách để render radio button chọn màu"""
        if self.mau_sac:
            return [m.strip() for m in self.mau_sac.split(',') if m.strip()]
        return ['Tiêu chuẩn']

    @property
    def phan_tram_giam_gia(self):
        """Tự động tính phần trăm giảm giá nếu có giá gốc cũ"""
        if self.gia_goc and self.gia_goc > self.gia_ban:
            return int(((self.gia_goc - self.gia_ban) / self.gia_goc) * 100)
        return 0
