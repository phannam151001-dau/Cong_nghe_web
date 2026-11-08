from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from cua_hang.models import SanPham
from .xu_ly_gio_hang import GioHang
from .models import DonHang, ChiTietDonHang


def xem_gio_hang(request):
    """Trang xem chi tiết giỏ hàng và danh sách món đã chọn"""
    gio = GioHang(request)
    return render(request, 'gio_hang/chi_tiet_gio_hang.html', {'gio_hang': gio})


def them_vao_gio(request, ma_san_pham):
    """Thêm sản phẩm với Size và Màu sắc vào giỏ hàng"""
    gio = GioHang(request)
    san_pham = get_object_or_404(SanPham, id=ma_san_pham)

    if request.method == 'POST':
        so_luong = int(request.POST.get('so_luong', 1))
        kich_co = request.POST.get('kich_co', 'M')
        mau_sac = request.POST.get('mau_sac', '')
        gio.them_san_pham(san_pham=san_pham, so_luong=so_luong, kich_co=kich_co, mau_sac=mau_sac)

        hanh_dong = request.POST.get('hanh_dong')
        if hanh_dong == 'mua_ngay':
            messages.success(request, f'Đã thêm "{san_pham.ten_san_pham}" (Size: {kich_co}) vào giỏ hàng!')
            return redirect('gio_hang:xem_gio_hang')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'message': f'Đã thêm "{san_pham.ten_san_pham}" vào giỏ hàng!',
                'cart_count': len(gio),
            })
        messages.success(request, f'Đã thêm "{san_pham.ten_san_pham}" (Size: {kich_co}) vào giỏ hàng!')

    url_quay_lai = request.POST.get('next') or request.META.get('HTTP_REFERER', '')
    if url_has_allowed_host_and_scheme(
        url=url_quay_lai,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(url_quay_lai)
    return redirect(san_pham.get_absolute_url())


def cap_nhat_so_luong(request):
    """Cập nhật số lượng của một món trong giỏ hàng"""
    gio = GioHang(request)
    if request.method == 'POST':
        khoa = request.POST.get('khoa')
        so_luong = request.POST.get('so_luong')
        if khoa and so_luong:
            gio.cap_nhat_so_luong(khoa=khoa, so_luong=int(so_luong))
            messages.info(request, 'Đã cập nhật số lượng món đồ trong giỏ.')
    return redirect('gio_hang:xem_gio_hang')


def xoa_khoi_gio(request, khoa):
    """Xóa một món đồ khỏi giỏ hàng"""
    gio = GioHang(request)
    gio.xoa_san_pham(khoa)
    messages.warning(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    return redirect('gio_hang:xem_gio_hang')


@login_required(login_url='khach_hang:dang_nhap')
def thanh_toan(request):
    """Trang nhập thông tin giao hàng và xác nhận đặt hàng"""
    gio = GioHang(request)
    if len(gio) == 0:
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('cua_hang:trang_chu')

    # Lấy thông tin mặc định nếu khách hàng đã đăng nhập
    thong_tin = {
        'ten_khach_hang': '',
        'so_dien_thoai': '',
        'email': '',
        'dia_chi_giao_hang': ''
    }
    if request.user.is_authenticated:
        thong_tin['ten_khach_hang'] = request.user.get_full_name() or request.user.username
        thong_tin['email'] = request.user.email
        if hasattr(request.user, 'ho_so'):
            thong_tin['so_dien_thoai'] = request.user.ho_so.so_dien_thoai
            thong_tin['dia_chi_giao_hang'] = request.user.ho_so.dia_chi

    if request.method == 'POST':
        ten_khach_hang = request.POST.get('ten_khach_hang', '').strip()
        so_dien_thoai = request.POST.get('so_dien_thoai', '').strip()
        email = request.POST.get('email', '').strip()
        dia_chi_giao_hang = request.POST.get('dia_chi_giao_hang', '').strip()
        ghi_chu = request.POST.get('ghi_chu', '').strip()

        if not ten_khach_hang or not so_dien_thoai or not dia_chi_giao_hang:
            messages.error(request, 'Vui lòng nhập đầy đủ họ tên, số điện thoại và địa chỉ nhận hàng!')
            return render(request, 'gio_hang/thanh_toan.html', {'gio_hang': gio, 'thong_tin': request.POST})

        khach_hang_user = request.user if request.user.is_authenticated else None

        don_hang = DonHang.objects.create(
            khach_hang=khach_hang_user,
            ten_khach_hang=ten_khach_hang,
            so_dien_thoai=so_dien_thoai,
            email=email,
            dia_chi_giao_hang=dia_chi_giao_hang,
            ghi_chu=ghi_chu,
            tong_tien=gio.tong_tien()
        )

        for item in gio:
            ChiTietDonHang.objects.create(
                don_hang=don_hang,
                san_pham=item['san_pham'],
                ten_san_pham=item['san_pham'].ten_san_pham,
                don_gia=item['don_gia'],
                so_luong=item['so_luong'],
                kich_co=item['kich_co'],
                mau_sac=item['mau_sac']
            )

        # Cập nhật địa chỉ mặc định cho khách nếu chưa có
        if request.user.is_authenticated and hasattr(request.user, 'ho_so'):
            if not request.user.ho_so.so_dien_thoai and so_dien_thoai:
                request.user.ho_so.so_dien_thoai = so_dien_thoai
            if not request.user.ho_so.dia_chi and dia_chi_giao_hang:
                request.user.ho_so.dia_chi = dia_chi_giao_hang
            request.user.ho_so.save()

        gio.lam_trong_gio()
        return redirect('gio_hang:dat_hang_thanh_cong', ma_don_hang=don_hang.id)

    return render(request, 'gio_hang/thanh_toan.html', {'gio_hang': gio, 'thong_tin': thong_tin})


def dat_hang_thanh_cong(request, ma_don_hang):
    """Trang hiển thị thông báo đặt hàng thành công của khách"""
    don_hang = get_object_or_404(DonHang, id=ma_don_hang)
    return render(request, 'gio_hang/dat_hang_thanh_cong.html', {'don_hang': don_hang})


def in_hoa_don(request, ma_don_hang):
    """Trang xem và in phiếu hóa đơn chuẩn đẹp cho Admin và Khách hàng"""
    don_hang = get_object_or_404(DonHang, id=ma_don_hang)
    # Quyền xem: Admin/Staff hoặc chính khách hàng sở hữu đơn
    if not request.user.is_staff and don_hang.khach_hang != request.user:
        messages.error(request, 'Bạn không có quyền xem hóa đơn này!')
        return redirect('cua_hang:trang_chu')

    return render(request, 'gio_hang/in_hoa_don.html', {'don_hang': don_hang})
