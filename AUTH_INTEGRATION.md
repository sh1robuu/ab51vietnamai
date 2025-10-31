# Tích hợp Authentication Module

## Tổng quan

Đã tách hệ thống authentication ra thành một module riêng (`auth.py`) để dễ bảo trì và quản lý code.

## Các file đã tạo/sửa đổi

### 1. `auth.py` (File mới)
Module authentication chứa tất cả logic liên quan đến đăng nhập/đăng ký:

**Các hàm quản lý dữ liệu:**
- `load_users()` - Đọc dữ liệu user từ file JSON
- `save_users(users)` - Lưu dữ liệu user vào file JSON
- `hash_password(password)` - Mã hóa mật khẩu bằng SHA-256

**Các hàm xử lý auth:**
- `register_user(username, password, email)` - Đăng ký user mới
- `login_user(username, password)` - Đăng nhập
- `logout_user()` - Đăng xuất

**Các hàm UI:**
- `show_login_form(language)` - Hiển thị form đăng nhập
- `show_register_form(language)` - Hiển thị form đăng ký
- `render_auth_buttons(language)` - Hiển thị các nút Đăng nhập/Đăng ký/Đăng xuất
- `handle_auth_modals(language)` - Xử lý các modal đăng nhập/đăng ký

### 2. `app.py` (Đã cập nhật)
Đã tích hợp module `auth.py`:

**Import:**
```python
import auth  # Import module auth
```

**Sử dụng trong sidebar:**
```python
# Auth buttons - sử dụng function từ auth.py
auth.render_auth_buttons(st.session_state.language)

# Xử lý modal login/register - sử dụng function từ auth.py
auth.handle_auth_modals(st.session_state.language)
```

## Lợi ích của việc tách module

1. **Code dễ đọc hơn**: File `app.py` giờ ngắn gọn hơn (~100 dòng code đã được di chuyển sang `auth.py`)

2. **Dễ bảo trì**: Tất cả logic authentication tập trung ở một nơi

3. **Có thể tái sử dụng**: Module `auth.py` có thể được import và sử dụng ở các file khác nếu cần

4. **Dễ test**: Có thể test riêng các hàm authentication mà không cần chạy toàn bộ app

## Cách hoạt động

1. User nhấn nút "Đăng nhập" hoặc "Đăng ký" → `render_auth_buttons()` xử lý
2. Modal hiển thị → `handle_auth_modals()` xử lý form
3. User submit form:
   - Đăng ký → `register_user()` lưu vào `users.json`
   - Đăng nhập → `login_user()` kiểm tra credentials
   - Đăng xuất → `logout_user()` clear session

## File dữ liệu

- `users.json` - Lưu trữ thông tin user (được tạo tự động khi có user đầu tiên đăng ký)
  ```json
  {
    "username1": {
      "password": "hashed_password",
      "email": "user@example.com"
    }
  }
  ```

## Session State Variables

Module auth sử dụng các session state variables:
- `st.session_state.logged_in` - Trạng thái đăng nhập (True/False)
- `st.session_state.username` - Tên user đang đăng nhập
- `st.session_state.show_login` - Hiển thị modal đăng nhập
- `st.session_state.show_register` - Hiển thị modal đăng ký

## Bảo mật

- Mật khẩu được hash bằng SHA-256 trước khi lưu vào file
- Không lưu trữ mật khẩu dạng plain text
- Mật khẩu tối thiểu 6 ký tự

## Hướng dẫn sử dụng

### Chạy ứng dụng:
```bash
streamlit run app.py
```

### Test đăng ký/đăng nhập:
1. Click nút "Đăng ký" (hoặc "Sign Up")
2. Nhập username, email, password
3. Sau khi đăng ký thành công, click "Đăng nhập"
4. Nhập username và password để đăng nhập
5. Khi đã đăng nhập, nút "Đăng xuất" sẽ xuất hiện

## Mở rộng trong tương lai

Có thể dễ dàng thêm các tính năng:
- Reset password
- Email verification
- User profile management
- Social login (Google, Facebook)
- Database integration (thay thế JSON file)
- JWT tokens
- Session timeout
