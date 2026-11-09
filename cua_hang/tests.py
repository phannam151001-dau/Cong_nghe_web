from decimal import Decimal

from django.template import Context, Template
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from .models import DanhMuc, SanPham


class DinhDangTienTests(SimpleTestCase):
    def test_hien_thi_vnd_voi_dau_cham_phan_tach_hang_nghin(self):
        template = Template('{% load tien_te %}{{ amount|vnd }}₫')

        self.assertEqual(
            template.render(Context({'amount': Decimal('12345678')})),
            '12.345.678₫',
        )


class PhanTrangSanPhamTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        danh_muc = DanhMuc.objects.create(
            ten_danh_muc='Áo Thun',
            slug='ao-thun',
        )
        SanPham.objects.bulk_create([
            SanPham(
                danh_muc=danh_muc,
                ten_san_pham=f'Áo thun {so}',
                slug=f'ao-thun-{so}',
                gia_ban=100000 + so,
                mo_ta='Sản phẩm kiểm thử',
            )
            for so in range(10)
        ])

    def test_moi_trang_chi_hien_toi_da_8_san_pham(self):
        response = self.client.get(reverse('cua_hang:trang_chu'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['san_phams']), 8)
        self.assertEqual(response.context['trang_hien_tai'].paginator.count, 10)

    def test_trang_ke_tiep_hien_cac_san_pham_con_lai(self):
        response = self.client.get(
            reverse('cua_hang:trang_chu'),
            {'page': 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['san_phams']), 2)
        self.assertEqual(response.context['trang_hien_tai'].number, 2)

    def test_phan_trang_giu_bo_loc_tim_kiem_va_sap_xep(self):
        response = self.client.get(
            reverse('cua_hang:san_pham_theo_danh_muc', args=['ao-thun']),
            {'q': 'áo', 'sort': 'gia_giam', 'page': 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['san_phams']), 2)
        self.assertEqual(response.context['tu_khoa'], 'áo')
        self.assertEqual(response.context['sap_xep'], 'gia_giam')

    def test_form_sap_xep_quay_lai_khu_vuc_san_pham(self):
        response = self.client.get(reverse('cua_hang:trang_chu'))

        self.assertContains(
            response,
            'action="/#khu-vuc-san-pham"',
        )
