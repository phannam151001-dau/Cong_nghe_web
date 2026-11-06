# Website Bán Quần Áo Thời Trang (Fashion Store) - Django & Python

Dự án được xây dựng bám sát theo các kiến thức và lộ trình chuẩn của khóa học **"Lập trình web với Python bằng Django"** từ [HowKteam](https://howkteam.vn/course/lap-trinh-web-voi-python-bang-django-36).

Hệ thống đã được cấu trúc theo **tên Tiếng Việt trực quan, dễ hiểu** cho người học lập trình, đồng thời đã liên kết trực tiếp với cơ sở dữ liệu **MySQL trên XAMPP** (`web_ban_ao_quan`).

---

## 🌟 Cấu Trúc Mã Nguồn Tiếng Việt (Project Structure)

```text
Python_Dijango/
├── venv/                           # Môi trường ảo Python
├── fashion_store/                  # Thư mục cấu hình Project chính
│   ├── settings.py                 # File cài đặt trung tâm (Database MySQL, Apps, Templates...)
│   ├── urls.py                     # Điều hướng các đường dẫn chính (/khach-hang/, /gio-hang/, /admin/...)
│   ├── wsgi.py
│   └── __init__.py                 # Nạp sẵn driver kết nối MySQL XAMPP (pymysql)
│
├── cua_hang/                       # [App 1] Quản lý Cửa Hàng & Sản Phẩm Thời Trang
│   ├── models.py                   # Các bảng dữ liệu: DanhMuc, SanPham
│   ├── views.py                    # Các hàm xử lý: danh_sach_san_pham, chi_tiet_san_pham, gioi_thieu, lien_he
│   ├── urls.py                     # Định tuyến: /danh-muc/, /san-pham/<slug>/...
│   ├── admin.py                    # Đăng ký hiển thị DanhMuc, SanPham vào trang Admin
│   └── context_processors.py       # Chia sẻ danh mục cho thanh menu Navbar
│
├── gio_hang/                       # [App 2] Quản lý Giỏ Hàng & Đơn Đặt Hàng
│   ├── models.py                   # Các bảng dữ liệu: DonHang, ChiTietDonHang
│   ├── xu_ly_gio_hang.py           # Lớp GioHang lưu trữ giỏ hàng trong Session
│   ├── views.py                    # Các hàm: xem_gio_hang, them_vao_gio, cap_nhat_so_luong, thanh_toan...
│   ├── urls.py                     # Định tuyến: /gio-hang/, /thanh-toan/...
│   ├── admin.py                    # Quản lý đơn hàng và chi tiết sản phẩm khách đặt trong Admin
│   └── context_processors.py       # Chia sẻ số lượng món trong giỏ lên icon Navbar
│
├── khach_hang/                     # [App 3] Quản lý Khách Hàng, Đăng Ký & Lịch Sử Hóa Đơn
│   ├── models.py                   # Bảng HoSoKhachHang (liên kết User)
│   ├── views.py                    # Các hàm: dang_ky, dang_nhap, dang_xuat, lich_su_don_hang, chi_tiet_hoa_don, thong_tin_tai_khoan
│   ├── urls.py                     # Định tuyến: /khach-hang/dang-ky/, /lich-su-don-hang/, /hoa-don/<id>/...
│   └── admin.py                    # Quản lý hồ sơ khách hàng trong Admin
│
├── templates/                      # Thư mục chứa giao diện HTML (Bootstrap 5)
│   ├── bo_cuc_chung.html           # Khung layout chuẩn (Navbar, Menu người dùng, Footer, Flash Message)
│   ├── cua_hang/                   # Giao diện của App Cửa Hàng
│   │   ├── danh_sach_san_pham.html # Trang chủ: Banner, danh sách áo/quần, tìm kiếm, lọc
│   │   ├── chi_tiet_san_pham.html  # Xem chi tiết: Chọn Size, Màu sắc, Số lượng, Mua ngay
│   │   ├── gioi_thieu.html         # Trang giới thiệu thương hiệu
│   │   └── lien_he.html            # Trang liên hệ và gửi góp ý
│   ├── gio_hang/                   # Giao diện của App Giỏ Hàng
│   │   ├── chi_tiet_gio_hang.html  # Bảng giỏ hàng, sửa số lượng, xóa món
│   │   ├── thanh_toan.html         # Form điền thông tin (Tự động điền nếu đã đăng nhập)
│   │   └── dat_hang_thanh_cong.html# Hóa đơn xác nhận đặt hàng thành công
│   └── khach_hang/                 # Giao diện của App Khách Hàng
│       ├── dang_ky.html            # Form đăng ký tài khoản khách hàng mới
│       ├── dang_nhap.html          # Form đăng nhập tài khoản
│       ├── lich_su_don_hang.html   # Trang quản lý danh sách các hóa đơn đã mua
│       ├── chi_tiet_hoa_don.html   # Hóa đơn chi tiết có nút In hóa đơn (Print)
│       └── thong_tin_tai_khoan.html# Trang xem và cập nhật thông tin cá nhân
│
├── static/                         # Thư mục chứa CSS, JavaScript, Hình ảnh tĩnh
├── media/                          # Thư mục chứa Hình ảnh sản phẩm do Admin tải lên
├── khoi_tao_du_lieu.py             # Script nạp sẵn danh mục, sản phẩm mẫu và tài khoản Admin
└── manage.py                       # File thực thi các lệnh Django
```

---

## 🚀 Hướng Dẫn Khởi Chạy Website

Mở PowerShell tại thư mục `d:\Python_Dijango` và chạy lệnh:

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Truy cập trên trình duyệt:
- 🌐 **Trang chủ bán hàng:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 📝 **Đăng ký tài khoản khách hàng:** [http://127.0.0.1:8000/khach-hang/dang-ky/](http://127.0.0.1:8000/khach-hang/dang-ky/)
- 🔑 **Đăng nhập khách hàng:** [http://127.0.0.1:8000/khach-hang/dang-nhap/](http://127.0.0.1:8000/khach-hang/dang-nhap/)
- 🧾 **Lịch sử hóa đơn khách hàng:** [http://127.0.0.1:8000/khach-hang/lich-su-don-hang/](http://127.0.0.1:8000/khach-hang/lich-su-don-hang/)
- ⚙️ **Trang quản trị Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### 👤 Các tài khoản mẫu có sẵn:
1. **Tài khoản Khách Hàng (Đã có sẵn 1 hóa đơn mẫu để xem ngay):**
   - **Tên đăng nhập:** `khachhang1`
   - **Mật khẩu:** `123456`
2. **Tài khoản Quản Trị Hệ Thống:**
   - **Tên đăng nhập:** `admin`
   - **Mật khẩu:** `admin123`
