from .xu_ly_gio_hang import GioHang


def truyen_gio_hang_toan_cuc(request):
    """Chia sẻ đối tượng giỏ hàng và tổng số lượng món đồ cho Navbar"""
    gio = GioHang(request)
    return {
        'gio_hang': gio,
        'so_luong_gio_hang': len(gio)
    }
