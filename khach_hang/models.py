from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class HoSoKhachHang(models.Model):
    """Thông tin mở rộng của khách hàng (SĐT, Địa chỉ mặc định)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ho_so', verbose_name="Tài khoản")
    so_dien_thoai = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    dia_chi = models.TextField(blank=True, verbose_name="Địa chỉ mặc định")
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng ký")

    class Meta:
        verbose_name = "Hồ sơ khách hàng"
        verbose_name_plural = "Hồ sơ khách hàng"

    def __str__(self):
        return f"Hồ sơ của {self.user.username}"



@receiver(post_save, sender=User)
def tao_ho_so_khach_hang(sender, instance, created, raw=False, **kwargs):
    """Tự động tạo hồ sơ khi tài khoản mới được tạo"""
    if created and not raw:
        HoSoKhachHang.objects.get_or_create(user=instance)
