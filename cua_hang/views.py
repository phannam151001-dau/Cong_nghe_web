from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import DanhMuc, SanPham


def danh_sach_san_pham(request, slug_danh_muc=None):
    """View hiển thị danh sách sản phẩm, lọc theo danh mục, tìm kiếm và sắp xếp"""
    danh_muc_hien_tai = None
    san_phams = SanPham.objects.filter(dang_kinh_doanh=True)
    tu_khoa = request.GET.get('q', '').strip()
    sap_xep = request.GET.get('sort', '')

    if slug_danh_muc:
        danh_muc_hien_tai = get_object_or_404(DanhMuc, slug=slug_danh_muc)
        san_phams = san_phams.filter(danh_muc=danh_muc_hien_tai)

    if tu_khoa:
        san_phams = san_phams.filter(
            Q(ten_san_pham__icontains=tu_khoa) |
            Q(mo_ta__icontains=tu_khoa) |
            Q(danh_muc__ten_danh_muc__icontains=tu_khoa)
        )

    if sap_xep == 'gia_tang':
        san_phams = san_phams.order_by('gia_ban')
    elif sap_xep == 'gia_giam':
        san_phams = san_phams.order_by('-gia_ban')
    elif sap_xep == 'moi_nhat':
        san_phams = san_phams.order_by('-ngay_tao')

    san_pham_noi_bat = SanPham.objects.filter(dang_kinh_doanh=True, noi_bat=True)[:4]

    du_lieu = {
        'danh_muc_hien_tai': danh_muc_hien_tai,
        'san_phams': san_phams,
        'tu_khoa': tu_khoa,
        'sap_xep': sap_xep,
        'san_pham_noi_bat': san_pham_noi_bat,
    }
    return render(request, 'cua_hang/danh_sach_san_pham.html', du_lieu)


def chi_tiet_san_pham(request, slug):
    """View hiển thị trang chi tiết một sản phẩm thời trang"""
    san_pham = get_object_or_404(SanPham, slug=slug, dang_kinh_doanh=True)
    san_pham_lien_quan = SanPham.objects.filter(
        danh_muc=san_pham.danh_muc,
        dang_kinh_doanh=True
    ).exclude(id=san_pham.id)[:4]

    du_lieu = {
        'san_pham': san_pham,
        'san_pham_lien_quan': san_pham_lien_quan,
    }
    return render(request, 'cua_hang/chi_tiet_san_pham.html', du_lieu)


def gioi_thieu(request):
    """Trang Giới thiệu thương hiệu thời trang"""
    return render(request, 'cua_hang/gioi_thieu.html')


def lien_he(request):
    """Trang Liên hệ cửa hàng"""
    return render(request, 'cua_hang/lien_he.html')
