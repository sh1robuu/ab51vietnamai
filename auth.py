import streamlit as st
import json
import hashlib
from pathlib import Path

# CSS để làm cho dialog rộng hơn
DIALOG_CSS = """
<style>
    /* Overlay đồng đều phía sau dialog */
    [data-testid="stDialog"]::before {
        content: "" !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: rgba(0, 0, 0, 0.5) !important;
        z-index: -1 !important;
    }
    
    /* Làm cho dialog rộng hơn và canh giữa */
    [data-testid="stDialog"] {
        width: 600px !important;
        max-width: 90vw !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        z-index: 999 !important;
    }
    
    /* Dialog content */
    [data-testid="stDialog"] > div:first-child {
        position: relative !important;
        transform: none !important;
        margin: 0 auto !important;
        background: white !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        max-height: 90vh !important;
        overflow-y: auto !important;
    }
    
    /* Tăng độ rộng section bên trong dialog */
    [data-testid="stDialog"] section {
        width: 100% !important;
        max-width: 600px !important;
    }
    
    /* Đảm bảo error/success message không bị xuống dòng */
    [data-testid="stDialog"] [data-testid="stAlert"] {
        white-space: nowrap !important;
        overflow: visible !important;
        min-width: max-content !important;
    }
    
    [data-testid="stDialog"] .stAlert p {
        white-space: nowrap !important;
        overflow: visible !important;
    }
    
    /* Tăng padding cho dialog để thoáng hơn */
    [data-testid="stDialog"] > div {
        padding: 2rem !important;
    }
</style>
"""

# File lưu trữ users
USERS_FILE = Path("users.json")

# Khởi tạo file users nếu chưa có
if not USERS_FILE.exists():
    USERS_FILE.write_text(json.dumps({}))

def load_users():
    """Load users từ file"""
    try:
        return json.loads(USERS_FILE.read_text())
    except:
        return {}

def save_users(users):
    """Save users vào file"""
    USERS_FILE.write_text(json.dumps(users, indent=2))

def hash_password(password):
    """Hash password"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, email):
    """Đăng ký user mới"""
    users = load_users()
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        "password": hash_password(password),
        "email": email
    }
    save_users(users)
    return True, "Registration successful"

def login_user(username, password):
    """Đăng nhập user"""
    users = load_users()
    if username not in users:
        return False, "Username not found"
    
    if users[username]["password"] == hash_password(password):
        st.session_state.logged_in = True
        st.session_state.username = username
        return True, "Login successful"
    return False, "Incorrect password"

def logout_user():
    """Đăng xuất user"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.show_login = False
    st.session_state.show_register = False

def show_login_form(language='vi'):
    """Hiển thị form đăng nhập dạng popup dialog"""
    # Thêm CSS để làm dialog rộng hơn
    st.markdown(DIALOG_CSS, unsafe_allow_html=True)
    
    username = st.text_input("Username" if language == 'en' else "Tên đăng nhập")
    password = st.text_input("Password" if language == 'en' else "Mật khẩu", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login" if language == 'en' else "Đăng nhập", 
                    use_container_width=True, type="primary"):
            if username and password:
                success, message = login_user(username, password)
                if success:
                    st.success(message if language == 'en' else "Đăng nhập thành công!")
                    st.session_state.show_login = False
                    st.rerun()
                else:
                    if language == 'vi':
                        if "not found" in message:
                            st.error("Tên đăng nhập không tồn tại!")
                        else:
                            st.error("Sai mật khẩu!")
                    else:
                        st.error(message)
            else:
                st.error("Please fill all fields" if language == 'en' else "Vui lòng điền đầy đủ thông tin")
    
    with col2:
        if st.button("Cancel" if language == 'en' else "Hủy", 
                    use_container_width=True):
            st.session_state.show_login = False
            st.rerun()

def show_register_form(language='vi'):
    """Hiển thị form đăng ký dạng popup dialog"""
    # Thêm CSS để làm dialog rộng hơn
    st.markdown(DIALOG_CSS, unsafe_allow_html=True)
    
    username = st.text_input("Username" if language == 'en' else "Tên đăng nhập")
    email = st.text_input("Email")
    password = st.text_input("Password" if language == 'en' else "Mật khẩu", type="password")
    password_confirm = st.text_input("Confirm Password" if language == 'en' else "Xác nhận mật khẩu", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up" if language == 'en' else "Đăng ký", 
                    use_container_width=True, type="primary"):
            if username and email and password and password_confirm:
                if password != password_confirm:
                    st.error("Passwords do not match" if language == 'en' else "Mật khẩu không khớp!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters" if language == 'en' else "Mật khẩu phải có ít nhất 6 ký tự!")
                else:
                    success, message = register_user(username, password, email)
                    if success:
                        st.success("Registration successful! Please login." if language == 'en' else "Đăng ký thành công! Vui lòng đăng nhập.")
                        st.session_state.show_register = False
                        st.session_state.show_login = True
                        st.rerun()
                    else:
                        st.error("Username already exists" if language == 'en' else "Tên đăng nhập đã tồn tại!")
            else:
                st.error("Please fill all fields" if language == 'en' else "Vui lòng điền đầy đủ thông tin")
    
    with col2:
        if st.button("Cancel" if language == 'en' else "Hủy", 
                    use_container_width=True):
            st.session_state.show_register = False
            st.rerun()

def render_auth_buttons(language='vi'):
    """Render auth buttons trong sidebar"""
    if not st.session_state.logged_in:
        if language == 'vi':
            if st.button("🔐 Đăng nhập", use_container_width=True, type="primary", key="login_btn"):
                st.session_state.show_login = True
                st.session_state.show_register = False
                st.rerun()
            if st.button("📝 Đăng ký", use_container_width=True, key="register_btn"):
                st.session_state.show_register = True
                st.session_state.show_login = False
                st.rerun()
        else:
            if st.button("🔐 Login", use_container_width=True, type="primary", key="login_btn"):
                st.session_state.show_login = True
                st.session_state.show_register = False
                st.rerun()
            if st.button("📝 Sign Up", use_container_width=True, key="register_btn"):
                st.session_state.show_register = True
                st.session_state.show_login = False
                st.rerun()
    else:
        # Hiển thị thông tin user đã đăng nhập
        st.success(f"👤 {st.session_state.username}")
        if language == 'vi':
            if st.button("🚪 Đăng xuất", use_container_width=True, key="logout_btn"):
                logout_user()
                st.rerun()
        else:
            if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                logout_user()
                st.rerun()

def handle_auth_modals(language='vi'):
    """Xử lý hiển thị popup dialog login/register"""
    # Sử dụng @st.dialog để tạo popup modal
    @st.dialog("🔐 Đăng nhập" if language == 'vi' else "🔐 Login")
    def login_dialog():
        show_login_form(language)
    
    @st.dialog("📝 Đăng ký tài khoản" if language == 'vi' else "📝 Sign Up")
    def register_dialog():
        show_register_form(language)
    
    if st.session_state.show_login:
        login_dialog()
    
    if st.session_state.show_register:
        register_dialog()
