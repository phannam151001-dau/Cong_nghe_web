from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import HoSoKhachHang


class ThongTinTaiKhoanTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='matkhau123',
            is_staff=True,
        )
        self.user.ho_so.delete()
        self.client.force_login(self.user)

    def test_admin_khong_co_ho_so_van_mo_duoc_trang_cai_dat(self):
        response = self.client.get(reverse('khach_hang:thong_tin_tai_khoan'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(HoSoKhachHang.objects.filter(user=self.user).exists())

    def test_admin_khong_co_ho_so_van_luu_duoc_thong_tin(self):
        response = self.client.post(
            reverse('khach_hang:thong_tin_tai_khoan'),
            {
                'ho_ten': 'Quản trị viên',
                'email': 'admin@example.com',
                'so_dien_thoai': '0900000000',
                'dia_chi': 'Thành phố Hồ Chí Minh',
            },
        )

        self.assertRedirects(
            response,
            reverse('khach_hang:thong_tin_tai_khoan'),
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Quản trị viên')
        self.assertEqual(self.user.email, 'admin@example.com')
        self.user.ho_so.refresh_from_db()
        self.assertEqual(self.user.ho_so.so_dien_thoai, '0900000000')
        self.assertEqual(self.user.ho_so.dia_chi, 'Thành phố Hồ Chí Minh')
