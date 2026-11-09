from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from cua_hang.models import DanhMuc, SanPham
from .models import ChiTietDonHang, DonHang


class ThemVaoGioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        danh_muc = DanhMuc.objects.create(
            ten_danh_muc='Áo Thun',
            slug='ao-thun',
        )
        cls.san_pham = SanPham.objects.create(
            danh_muc=danh_muc,
            ten_san_pham='Áo thun kiểm thử',
            slug='ao-thun-kiem-thu',
            gia_ban=100000,
            mo_ta='Sản phẩm kiểm thử',
        )

    def test_them_gio_quay_lai_danh_sach_va_giu_trang_hien_tai(self):
        response = self.client.post(
            reverse('gio_hang:them_vao_gio', args=[self.san_pham.id]),
            {
                'next': '/?page=2#khu-vuc-san-pham',
                'so_luong': '1',
                'kich_co': 'M',
                'mau_sac': 'Đen',
            },
        )

        self.assertRedirects(
            response,
            '/?page=2#khu-vuc-san-pham',
            fetch_redirect_response=False,
        )

    def test_form_trong_danh_sach_gui_duong_dan_quay_lai_khu_vuc_san_pham(self):
        response = self.client.get(reverse('cua_hang:trang_chu'))

        self.assertContains(
            response,
            'name="next" value="/#khu-vuc-san-pham"',
        )

    def test_them_gio_tu_danh_sach_khong_can_tai_lai_trang(self):
        response = self.client.post(
            reverse('gio_hang:them_vao_gio', args=[self.san_pham.id]),
            {
                'so_luong': '1',
                'kich_co': 'M',
                'mau_sac': 'Đen',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['cart_count'], 1)
        self.assertIn(self.san_pham.ten_san_pham, response.json()['message'])
        self.assertEqual(len(self.client.session['gio_hang']), 1)
        self.assertEqual(list(get_messages(response.wsgi_request)), [])

    def test_tu_choi_url_quay_lai_ben_ngoai(self):
        response = self.client.post(
            reverse('gio_hang:them_vao_gio', args=[self.san_pham.id]),
            {
                'next': 'https://example.com/',
                'so_luong': '1',
                'kich_co': 'M',
                'mau_sac': 'Đen',
            },
        )

        self.assertRedirects(
            response,
            self.san_pham.get_absolute_url(),
            fetch_redirect_response=False,
        )

    def test_khong_co_url_quay_lai_khong_chuyen_ve_trang_chu(self):
        response = self.client.post(
            reverse('gio_hang:them_vao_gio', args=[self.san_pham.id]),
            {
                'so_luong': '1',
                'kich_co': 'M',
                'mau_sac': 'Đen',
            },
        )

        self.assertRedirects(
            response,
            self.san_pham.get_absolute_url(),
            fetch_redirect_response=False,
        )

    def test_khach_chua_dang_nhap_duoc_chuyen_den_dang_nhap_de_checkout(self):
        self.client.post(
            reverse('gio_hang:them_vao_gio', args=[self.san_pham.id]),
            {'so_luong': '1', 'kich_co': 'M', 'mau_sac': 'Đen'},
        )

        response = self.client.get(reverse('gio_hang:thanh_toan'))

        self.assertRedirects(
            response,
            f"{reverse('khach_hang:dang_nhap')}?next={reverse('gio_hang:thanh_toan')}",
            fetch_redirect_response=False,
        )
        self.assertEqual(len(self.client.session['gio_hang']), 1)

    def test_khach_chua_dang_nhap_khong_the_tao_don_hang(self):
        self.client.post(
            reverse('gio_hang:them_vao_gio', args=[self.san_pham.id]),
            {'so_luong': '1', 'kich_co': 'M', 'mau_sac': 'Đen'},
        )

        response = self.client.post(
            reverse('gio_hang:thanh_toan'),
            {
                'ten_khach_hang': 'Khách chưa đăng nhập',
                'so_dien_thoai': '0900000000',
                'dia_chi_giao_hang': 'Địa chỉ kiểm thử',
            },
        )

        self.assertEqual(DonHang.objects.count(), 0)
        self.assertEqual(response.status_code, 302)

    def test_dang_nhap_quay_lai_checkout(self):
        user = User.objects.create_user(username='khach', password='matkhau123')

        response = self.client.post(
            f"{reverse('khach_hang:dang_nhap')}?next={reverse('gio_hang:thanh_toan')}",
            {
                'ten_dang_nhap': user.username,
                'mat_khau': 'matkhau123',
                'next': reverse('gio_hang:thanh_toan'),
            },
        )

        self.assertRedirects(
            response,
            reverse('gio_hang:thanh_toan'),
            fetch_redirect_response=False,
        )

    def test_dang_nhap_tu_choi_next_ben_ngoai(self):
        user = User.objects.create_user(username='khach', password='matkhau123')

        response = self.client.post(
            reverse('khach_hang:dang_nhap'),
            {
                'ten_dang_nhap': user.username,
                'mat_khau': 'matkhau123',
                'next': 'https://example.com/',
            },
        )

        self.assertRedirects(
            response,
            reverse('cua_hang:trang_chu'),
            fetch_redirect_response=False,
        )

    def test_dat_hang_tru_ton_kho_va_giu_nguyen_gia_giam(self):
        user = User.objects.create_user(username='khach', password='matkhau123')
        self.client.force_login(user)
        self.san_pham.so_luong_kho = 5
        self.san_pham.gia_goc = 150000
        self.san_pham.save()
        self.client.post(
            reverse('gio_hang:them_vao_gio', args=[self.san_pham.id]),
            {'so_luong': '2', 'kich_co': 'M', 'mau_sac': 'Đen'},
        )

        response = self.client.post(
            reverse('gio_hang:thanh_toan'),
            {
                'ten_khach_hang': 'Khách kiểm thử',
                'so_dien_thoai': '0900000000',
                'dia_chi_giao_hang': 'Địa chỉ kiểm thử',
            },
        )

        self.assertRedirects(
            response,
            reverse('gio_hang:dat_hang_thanh_cong', args=[1]),
            fetch_redirect_response=False,
        )
        self.san_pham.refresh_from_db()
        self.assertEqual(self.san_pham.so_luong_kho, 3)
        self.assertEqual(self.san_pham.gia_ban, 100000)
        self.assertEqual(self.san_pham.gia_goc, 150000)
        self.assertEqual(ChiTietDonHang.objects.get().don_gia, 100000)
        self.assertContains(
            self.client.get(self.san_pham.get_absolute_url()),
            '-33%',
        )
        self.assertContains(
            self.client.get(reverse('cua_hang:trang_chu')),
            '-33%',
        )

    def test_khong_tao_don_hoac_tru_kho_khi_ton_kho_khong_du(self):
        user = User.objects.create_user(username='khach', password='matkhau123')
        self.client.force_login(user)
        self.san_pham.so_luong_kho = 1
        self.san_pham.save()
        self.client.post(
            reverse('gio_hang:them_vao_gio', args=[self.san_pham.id]),
            {'so_luong': '2', 'kich_co': 'M', 'mau_sac': 'Đen'},
        )

        response = self.client.post(
            reverse('gio_hang:thanh_toan'),
            {
                'ten_khach_hang': 'Khách kiểm thử',
                'so_dien_thoai': '0900000000',
                'dia_chi_giao_hang': 'Địa chỉ kiểm thử',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'không đủ tồn kho')
        self.assertEqual(DonHang.objects.count(), 0)
        self.san_pham.refresh_from_db()
        self.assertEqual(self.san_pham.so_luong_kho, 1)
        self.assertEqual(len(self.client.session['gio_hang']), 1)


class ThongKeDoanhThuAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='matkhau123',
        )

    def test_trang_thong_ke_phan_biet_don_huy_va_don_hoan_thanh(self):
        DonHang.objects.create(
            ten_khach_hang='Đơn hoàn thành',
            so_dien_thoai='0900000001',
            dia_chi_giao_hang='Địa chỉ 1',
            tong_tien=200000,
            trang_thai='hoan_thanh',
        )
        DonHang.objects.create(
            ten_khach_hang='Đơn chờ xác nhận',
            so_dien_thoai='0900000002',
            dia_chi_giao_hang='Địa chỉ 2',
            tong_tien=100000,
            trang_thai='cho_xac_nhan',
        )
        DonHang.objects.create(
            ten_khach_hang='Đơn đã hủy',
            so_dien_thoai='0900000003',
            dia_chi_giao_hang='Địa chỉ 3',
            tong_tien=50000,
            trang_thai='da_huy',
        )
        self.client.force_login(self.admin)

        response = self.client.get(reverse('admin:gio_hang_donhang_revenue'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tong_doanh_thu'], 300000)
        self.assertEqual(response.context['doanh_thu_hoan_thanh'], 200000)
        self.assertEqual(response.context['so_don_hop_le'], 2)
        self.assertEqual(response.context['so_don_da_huy'], 1)
        self.assertEqual(
            response.context['cac_thang'][-1]['doanh_thu'],
            300000,
            response.context['cac_thang'],
        )
        self.assertEqual(response.context['cac_thang'][-1]['so_don'], 2)

    def test_danh_sach_don_hang_co_lien_ket_den_thong_ke(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse('admin:gio_hang_donhang_changelist'))

        self.assertContains(response, reverse('admin:gio_hang_donhang_revenue'))

    def test_trang_chu_admin_khong_hien_muc_doanh_thu_rieng(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse('admin:index'))

        self.assertNotContains(response, '3. Doanh thu')

    def test_trang_thong_ke_chi_danh_cho_quan_tri(self):
        response = self.client.get(reverse('admin:gio_hang_donhang_revenue'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('admin:login'), response.url)
