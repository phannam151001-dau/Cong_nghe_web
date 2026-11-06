from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from gio_hang.models import DonHang
from .models import HoSoKhachHang


def dang_ky(request):
    """Trang đăng ký tài khoản khách hàng mới"""
    if request.user.is_authenticated:
        return redirect('khach_hang:lich_su_don_hang')

    if request.method == 'POST':
        ten_dang_nhap = request.POST.get('ten_dang_nhap', '').strip()
        ho_ten = request.POST.get('ho_ten', '').strip()
        email = request.POST.get('email', '').strip()
        so_dien_thoai = request.POST.get('so_dien_thoai', '').strip()
        dia_chi = request.POST.get('dia_chi', '').strip()
        mat_khau = request.POST.get('mat_khau', '')
        xac_nhan_mat_khau = request.POST.get('xac_nhan_mat_khau', '')

        # Kiểm tra tính hợp lệ
        if not ten_dang_nhap or not mat_khau:
            messages.error(request, 'Vui lòng nhập tên đăng nhập và mật khẩu!')
            return render(request, 'khach_hang/dang_ky.html', {'du_lieu': request.POST})

        if mat_khau != xac_nhan_mat_khau:
            messages.error(request, 'Xác nhận mật khẩu không trùng khớp!')
            return render(request, 'khach_hang/dang_ky.html', {'du_lieu': request.POST})

        if len(mat_khau) < 6:
            messages.error(request, 'Mật khẩu phải có độ dài tối thiểu 6 ký tự!')
            return render(request, 'khach_hang/dang_ky.html', {'du_lieu': request.POST})

        if User.objects.filter(username=ten_dang_nhap).exists():
            messages.error(request, f'Tên đăng nhập "{ten_dang_nhap}" đã có người sử dụng. Vui lòng chọn tên khác!')
            return render(request, 'khach_hang/dang_ky.html', {'du_lieu': request.POST})

        if email and User.objects.filter(email=email).exists():
            messages.warning(request, f'Email "{email}" đã được đăng ký. Bạn có thể dùng email khác hoặc đăng nhập.')

        # Tạo tài khoản User
        user = User.objects.create_user(
            username=ten_dang_nhap,
            email=email,
            password=mat_khau
        )
        if ho_ten:
            user.first_name = ho_ten
            user.save()

        # Cập nhật thông tin hồ sơ (SĐT, Địa chỉ)
        if hasattr(user, 'ho_so'):
            user.ho_so.so_dien_thoai = so_dien_thoai
            user.ho_so.dia_chi = dia_chi
            user.ho_so.save()

        # Đăng nhập tự động ngay sau khi đăng ký thành công
        login(request, user)
        messages.success(request, f'Chúc mừng {ho_ten or ten_dang_nhap}, bạn đã đăng ký tài khoản thành công!')
        return redirect('cua_hang:trang_chu')

    return render(request, 'khach_hang/dang_ky.html')


def dang_nhap(request):
    """Trang đăng nhập tài khoản khách hàng"""
    if request.user.is_authenticated:
        return redirect('khach_hang:lich_su_don_hang')

    tiep_tuc = request.GET.get('next', '')

    if request.method == 'POST':
        ten_dang_nhap = request.POST.get('ten_dang_nhap', '').strip()
        mat_khau = request.POST.get('mat_khau', '')

        user = authenticate(request, username=ten_dang_nhap, password=mat_khau)

        if user is not None:
            login(request, user)
            messages.success(request, f'Chào mừng trở lại, {user.first_name or user.username}!')
            next_url = request.POST.get('next') or 'cua_hang:trang_chu'
            return redirect(next_url)
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác!')
            return render(request, 'khach_hang/dang_nhap.html', {'ten_dang_nhap': ten_dang_nhap, 'next': tiep_tuc})

    return render(request, 'khach_hang/dang_nhap.html', {'next': tiep_tuc})


def dang_xuat(request):
    """Đăng xuất tài khoản khách hàng"""
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất thành công khỏi hệ thống.')
    return redirect('cua_hang:trang_chu')


@login_required(login_url='khach_hang:dang_nhap')
def lich_su_don_hang(request):
    """Trang xem lịch sử các đơn hàng và hóa đơn của khách hàng đang đăng nhập"""
    cac_don_hang = DonHang.objects.filter(khach_hang=request.user).order_by('-ngay_tao')
    tong_tien_da_mua = sum(dh.tong_tien for dh in cac_don_hang)

    context = {
        'cac_don_hang': cac_don_hang,
        'tong_so_don': cac_don_hang.count(),
        'tong_tien_da_mua': tong_tien_da_mua,
    }
    return render(request, 'khach_hang/lich_su_don_hang.html', context)


@login_required(login_url='khach_hang:dang_nhap')
def chi_tiet_hoa_don(request, ma_don_hang):
    """Xem chi tiết một hóa đơn cụ thể của khách hàng"""
    don_hang = get_object_or_404(DonHang, id=ma_don_hang, khach_hang=request.user)
    return render(request, 'khach_hang/chi_tiet_hoa_don.html', {'don_hang': don_hang})


@login_required(login_url='khach_hang:dang_nhap')
def thong_tin_tai_khoan(request):
    """Trang xem và cập nhật thông tin cá nhân của khách hàng"""
    user = request.user
    ho_so, _ = HoSoKhachHang.objects.get_or_create(user=user)

    if request.method == 'POST':
        ho_ten = request.POST.get('ho_ten', '').strip()
        email = request.POST.get('email', '').strip()
        so_dien_thoai = request.POST.get('so_dien_thoai', '').strip()
        dia_chi = request.POST.get('dia_chi', '').strip()

        user.first_name = ho_ten
        user.email = email
        user.save()

        ho_so.so_dien_thoai = so_dien_thoai
        ho_so.dia_chi = dia_chi
        ho_so.save()

        messages.success(request, 'Cập nhật thông tin tài khoản thành công!')
        return redirect('khach_hang:thong_tin_tai_khoan')

    return render(request, 'khach_hang/thong_tin_tai_khoan.html', {'user': user, 'ho_so': ho_so})
