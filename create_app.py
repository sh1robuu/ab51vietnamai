# Script để tạo app.py
code = '''import streamlit as st

# Khởi tạo session state cho ngôn ngữ
if 'language' not in st.session_state:
    st.session_state.language = 'vi'

# Dictionary chứa các bản dịch
translations = {
    'vi': {
        'site_name': 'LOIGIAIHAY.COM',
        'main_title': 'LỜI GIẢI HAY',
        'subtitle': 'Hệ thống học tập trực tuyến hàng đầu Việt Nam',
        'hot_section': 'CÓ GÌ HOT?',
        'nav_home': 'Trang chủ',
        'nav_grades': 'Chọn lớp',
        'nav_detail': 'Chi tiết',
        'nav_tools': 'Công cụ',
        'nav_about': 'Giới thiệu',
        'choose_grade': 'LỰA CHỌN LỚP',
        'grade': 'LỚP',
        'high_school': 'Cấp THPT',
        'middle_school': 'Cấp THCS',
        'elementary': 'Cấp Tiểu học',
        'solutions': 'Lời giải - Bài soạn Lớp',
        'back': 'Quay lại',
        'literature': 'Ngữ Văn',
        'math': 'Toán',
        'english': 'Tiếng Anh',
        'vietnamese': 'Tiếng Việt',
        'tools': 'Công cụ học tập',
        'about': 'Giới thiệu',
    },
    'en': {
        'site_name': 'LOIGIAIHAY.COM',
        'main_title': 'STUDY SOLUTIONS',
        'subtitle': "Vietnam's Leading Online Learning System",
        'hot_section': "WHAT'S HOT?",
        'nav_home': 'Home',
        'nav_grades': 'Choose Grade',
        'nav_detail': 'Details',
        'nav_tools': 'Tools',
        'nav_about': 'About',
        'choose_grade': 'CHOOSE GRADE',
        'grade': 'GRADE',
        'high_school': 'High School',
        'middle_school': 'Middle School',
        'elementary': 'Elementary',
        'solutions': 'Solutions - Grade',
        'back': 'Back',
        'literature': 'Literature',
        'math': 'Math',
        'english': 'English',
        'vietnamese': 'Vietnamese',
        'tools': 'Learning Tools',
        'about': 'About Us',
    }
}

def get_text(key):
    return translations[st.session_state.language][key]

# Cấu hình trang
st.set_page_config(
    page_title="Lời Giải Hay",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    html, body, [class*="css"] { font-size: 18px; }
    h1 { font-size: 2.5rem !important; font-weight: 700 !important; }
    h2 { font-size: 2rem !important; font-weight: 600 !important; }
    h3 { font-size: 1.5rem !important; font-weight: 600 !important; }
    p, div, span, li { font-size: 1.1rem !important; line-height: 1.8 !important; }
    .stButton button { font-size: 1.2rem !important; padding: 0.75rem 1.5rem !important; }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Các hàm trang
def home():
    st.markdown(f"<h1 style='text-align: center; color: #667eea;'>📚 {get_text('main_title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #666;'>{get_text('subtitle')}</h3>", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"## 🌟 {get_text('hot_section')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📚 Đầy đủ lời giải SGK - SBT - VBT")
        st.success("🧠 Lý thuyết dạng sơ đồ tư duy")
    with col2:
        st.warning("📝 Hệ thống đề thi phong phú")
        st.error("✅ Kho bài tập trắc nghiệm")

def choose_grade():
    st.markdown(f"## 🎓 {get_text('choose_grade')}")
    st.write("")
    
    st.markdown(f"### 🏫 {get_text('high_school')}")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f"📕 {get_text('grade')} 12", use_container_width=True, type="primary"):
            st.session_state.selected_grade = 12
            st.rerun()
    with col2:
        if st.button(f"📗 {get_text('grade')} 11", use_container_width=True, type="primary"):
            st.session_state.selected_grade = 11
            st.rerun()
    with col3:
        if st.button(f"📘 {get_text('grade')} 10", use_container_width=True, type="primary"):
            st.session_state.selected_grade = 10
            st.rerun()
    
    st.write("")
    st.markdown(f"### 🏫 {get_text('middle_school')}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(f"📙 {get_text('grade')} 9", use_container_width=True):
            st.session_state.selected_grade = 9
            st.rerun()
    with col2:
        if st.button(f"📙 {get_text('grade')} 8", use_container_width=True):
            st.session_state.selected_grade = 8
            st.rerun()
    with col3:
        if st.button(f"📙 {get_text('grade')} 7", use_container_width=True):
            st.session_state.selected_grade = 7
            st.rerun()
    with col4:
        if st.button(f"📙 {get_text('grade')} 6", use_container_width=True):
            st.session_state.selected_grade = 6
            st.rerun()
    
    st.write("")
    st.markdown(f"### 🏫 {get_text('elementary')}")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button(f"📔 {get_text('grade')} 5", use_container_width=True):
            st.session_state.selected_grade = 5
            st.rerun()
    with col2:
        if st.button(f"📔 {get_text('grade')} 4", use_container_width=True):
            st.session_state.selected_grade = 4
            st.rerun()
    with col3:
        if st.button(f"📔 {get_text('grade')} 3", use_container_width=True):
            st.session_state.selected_grade = 3
            st.rerun()
    with col4:
        if st.button(f"📔 {get_text('grade')} 2", use_container_width=True):
            st.session_state.selected_grade = 2
            st.rerun()
    with col5:
        if st.button(f"📔 {get_text('grade')} 1", use_container_width=True):
            st.session_state.selected_grade = 1
            st.rerun()

def grade_detail():
    if 'selected_grade' not in st.session_state:
        st.session_state.selected_grade = 12
    
    grade = st.session_state.selected_grade
    st.markdown(f"## 📚 {get_text('solutions')} {grade}")
    
    if st.button(f"⬅️ {get_text('back')}"):
        st.rerun()
    
    st.divider()
    
    tabs = st.tabs([
        f"📖 {get_text('literature')}", 
        f"🔢 {get_text('math')}", 
        f"🌏 {get_text('english')}"
    ])
    
    for tab in tabs:
        with tab:
            st.write("Nội dung bài học...")
            st.info("📖 Sách Giáo Khoa (SGK)")
            st.success("📝 Sách Bài Tập (SBT)")

def tools():
    st.markdown(f"## 🛠️ {get_text('tools')}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="feature-card"><h3>📖 Từ điển</h3><p>Tra cứu nhanh</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card"><h3>🔢 Máy tính</h3><p>Tính toán nhanh</p></div>', unsafe_allow_html=True)

def about():
    st.markdown(f"## 📱 {get_text('about')}")
    if st.session_state.language == 'vi':
        st.write("**Lời Giải Hay** là hệ thống học tập trực tuyến hàng đầu Việt Nam")
    else:
        st.write("**Study Solutions** is Vietnam's leading online learning system")

# Sidebar
with st.sidebar:
    st.markdown(f"### 📚 {get_text('site_name')}")
    st.divider()
    st.markdown("#### 🌐 Language / Ngôn ngữ")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇻🇳 Việt", use_container_width=True, 
                    type="primary" if st.session_state.language == 'vi' else "secondary"):
            st.session_state.language = 'vi'
            st.rerun()
    with col2:
        if st.button("🇬🇧 Eng", use_container_width=True,
                    type="primary" if st.session_state.language == 'en' else "secondary"):
            st.session_state.language = 'en'
            st.rerun()

# Navigation
pg = st.navigation([
    st.Page(home, title=get_text('nav_home'), icon="🏠"),
    st.Page(choose_grade, title=get_text('nav_grades'), icon="🎓"),
    st.Page(grade_detail, title=get_text('nav_detail'), icon="📚"),
    st.Page(tools, title=get_text('nav_tools'), icon="🔧"),
    st.Page(about, title=get_text('nav_about'), icon="ℹ️"),
])

pg.run()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>© 2025 - Lời Giải Hay / Study Solutions</p>
    <p>📧 support@loigiaihay.com | 📱 1900 xxxx</p>
</div>
""", unsafe_allow_html=True)
'''

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("File app.py đã được tạo thành công!")
