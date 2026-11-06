from .models import DanhMuc


def truyen_danh_muc_toan_cuc(request):
    """Chia sẻ danh sách danh mục cho tất cả các file HTML (ví dụ Navbar)"""
    cac_danh_muc = DanhMuc.objects.all()
    return {'cac_danh_muc': cac_danh_muc}
