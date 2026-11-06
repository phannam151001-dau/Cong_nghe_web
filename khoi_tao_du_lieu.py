import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from django.contrib.auth.models import User
from cua_hang.models import DanhMuc, SanPham

def khoi_tao():
    # 1. Tạo tài khoản Admin nếu chưa có
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("[+] Tao tai khoan Admin thanh cong: admin / admin123")
    else:
        print("[+] Tai khoan Admin da ton tai.")

    # 2. Khởi tạo các Danh mục thời trang
    danh_muc_mau = [
        {"ten_danh_muc": "Áo Sơ Mi", "slug": "ao-so-mi", "mo_ta": "Áo sơ mi nam nữ công sở, dạo phố chất liệu cotton, oxford cao cấp."},
        {"ten_danh_muc": "Áo Thun & Polo", "slug": "ao-thun-polo", "mo_ta": "Áo phông, áo thun polo basic trẻ trung năng động, co giãn 4 chiều."},
        {"ten_danh_muc": "Quần Tây & Jean", "slug": "quan-tay-jean", "mo_ta": "Quần âu ống đứng, quần jean slimfit tôn dáng thanh lịch."},
        {"ten_danh_muc": "Áo Khoác", "slug": "ao-khoac", "mo_ta": "Áo blazer, bomber, cardigan thời thượng cho mọi thời tiết."},
        {"ten_danh_muc": "Váy & Đầm", "slug": "vay-dam", "mo_ta": "Váy hoa nhí, đầm dự tiệc phong cách nữ tính, cuốn hút."},
    ]

    bang_danh_muc = {}
    for dm in danh_muc_mau:
        obj, _ = DanhMuc.objects.get_or_create(
            slug=dm['slug'],
            defaults={'ten_danh_muc': dm['ten_danh_muc'], 'mo_ta': dm['mo_ta']}
        )
        bang_danh_muc[dm['slug']] = obj

    print("[+] Da khoi tao cac danh muc thoi trang.")

    # 3. Khởi tạo danh sách Sản phẩm thời trang mẫu
    san_pham_mau = [
        {
            "danh_muc": bang_danh_muc["ao-so-mi"],
            "ten_san_pham": "Áo Sơ Mi Nam Oxford Trắng Dài Tay Cao Cấp",
            "slug": "ao-so-mi-oxford-trang",
            "gia_ban": 389000,
            "gia_goc": 490000,
            "mo_ta": "Áo sơ mi vải Oxford dày dặn dệt tổ ong, đứng form, thấm hút mồ hôi tốt. Cổ áo cài nút (button-down) lịch sự phù hợp cả đi làm lẫn đi chơi dạo phố.",
            "kich_co": "S, M, L, XL, XXL",
            "mau_sac": "Trắng, Xanh Nhạt, Hồng Pastel",
            "so_luong_kho": 45,
            "noi_bat": True,
        },
        {
            "danh_muc": bang_danh_muc["ao-so-mi"],
            "ten_san_pham": "Áo Sơ Mi Lụa Cổ V Nữ Thanh Lịch",
            "slug": "ao-so-mi-lua-co-v-nu",
            "gia_ban": 349000,
            "gia_goc": 420000,
            "mo_ta": "Chất lụa ngọc trai mềm mại, rủ tự nhiên không nhăn nhàu. Thiết kế cổ chữ V tôn xương quai xanh quyến rũ, phối cùng chân váy hay quần tây đều chuẩn quý cô công sở.",
            "kich_co": "S, M, L",
            "mau_sac": "Trắng Kem, Hồng Đỗ, Xanh Bạc Hà",
            "so_luong_kho": 30,
            "noi_bat": True,
        },
        {
            "danh_muc": bang_danh_muc["ao-thun-polo"],
            "ten_san_pham": "Áo Polo Nam Phối Cổ Dệt Bo Basic",
            "slug": "ao-polo-nam-phoi-co",
            "gia_ban": 279000,
            "gia_goc": 350000,
            "mo_ta": "Chất vải cá sấu cotton 95% + 5% spandex co giãn 4 chiều cực thoải mái. Cổ áo dệt viền tinh tế, không bai nhão hay xù lông sau khi giặt máy.",
            "kich_co": "M, L, XL, XXL",
            "mau_sac": "Đen, Xanh Navy, Trắng, Xám",
            "so_luong_kho": 80,
            "noi_bat": True,
        },
        {
            "danh_muc": bang_danh_muc["ao-thun-polo"],
            "ten_san_pham": "Áo Thun Unisex Cotton Compact 250gsm Form Rộng",
            "slug": "ao-thun-unisex-oversize",
            "gia_ban": 219000,
            "gia_goc": 260000,
            "mo_ta": "Form áo oversize phong cách streetwear Hàn Quốc. Định lượng vải 250gsm dày dặn, đứng dáng, cổ dệt bo dày 2.5cm chống nhão tuyệt đối.",
            "kich_co": "S, M, L, XL",
            "mau_sac": "Đen, Trắng, Xám Tiêu, Nâu Cafe",
            "so_luong_kho": 100,
            "noi_bat": False,
        },
        {
            "danh_muc": bang_danh_muc["quan-tay-jean"],
            "ten_san_pham": "Quần Tây Nam Ống Đứng Hàn Quốc Cạp Co Giãn",
            "slug": "quan-tay-nam-ong-dung",
            "gia_ban": 420000,
            "gia_goc": 550000,
            "mo_ta": "Quần tây may từ chất vải tuyết mưa cao cấp chống nhăn, có tăng đơ chun co giãn 2 bên sườn hông thông minh tạo cảm giác thoải mái khi đứng ngồi.",
            "kich_co": "29, 30, 31, 32, 33, 34",
            "mau_sac": "Đen, Xanh Đen, Ghi Xám, Be",
            "so_luong_kho": 60,
            "noi_bat": True,
        },
        {
            "danh_muc": bang_danh_muc["quan-tay-jean"],
            "ten_san_pham": "Quần Jean Nữ Ống Loe Cạp Cao Hack Dáng",
            "slug": "quan-jean-nu-ong-loe",
            "gia_ban": 395000,
            "gia_goc": 480000,
            "mo_ta": "Thiết kế cạp cao ôm trọn vòng eo, ống loe nhẹ từ gối giúp kéo dài đôi chân tối đa. Chất denim co giãn mềm mại, giữ màu tốt.",
            "kich_co": "S, M, L",
            "mau_sac": "Xanh Nhạt Vintage, Xanh Đậm, Đen",
            "so_luong_kho": 35,
            "noi_bat": False,
        },
        {
            "danh_muc": bang_danh_muc["ao-khoac"],
            "ten_san_pham": "Áo Blazer Nam Nữ Hàn Quốc 2 Lớp Form Rộng",
            "slug": "ao-blazer-han-quoc-2-lop",
            "gia_ban": 650000,
            "gia_goc": 850000,
            "mo_ta": "Áo khoác blazer lót lụa mềm 2 lớp, đệm vai nhẹ giữ form thanh thoát. Điểm nhấn hoàn hảo cho outfit đi làm, dự tiệc, chụp ảnh thời trang.",
            "kich_co": "M, L, XL",
            "mau_sac": "Đen, Be Sữa, Nâu Tây",
            "so_luong_kho": 25,
            "noi_bat": True,
        },
        {
            "danh_muc": bang_danh_muc["vay-dam"],
            "ten_san_pham": "Đầm Hoa Nhí Dáng Dài Cổ Vuông Tay Bồng",
            "slug": "dam-hoa-nhi-dang-dai",
            "gia_ban": 460000,
            "gia_goc": 580000,
            "mo_ta": "Họa tiết hoa nhí vintage dịu dàng, cổ vuông tôn vòng một khéo léo cùng tay bồng che khuyết điểm bắp tay. Vải voan tơ hàn có lót trong kín đáo.",
            "kich_co": "S, M, L",
            "mau_sac": "Hoa Vàng Nhạt, Hoa Xanh Pastel",
            "so_luong_kho": 40,
            "noi_bat": True,
        },
    ]

    for sp in san_pham_mau:
        SanPham.objects.get_or_create(
            slug=sp['slug'],
            defaults=sp
        )

    print(f"[+] Da them {len(san_pham_mau)} san pham mau thoi trang hoan chinh.")

if __name__ == '__main__':
    khoi_tao()
