# 🤖 OZA AI Chatbot - Tính năng mới

## ✨ Đã tích hợp Google Gemini Pro!

### 🎯 Tính năng đã phát triển:

#### 1. ✅ Tích hợp Google Gemini API thực sự
- Sử dụng model `gemini-pro` (model mạnh mẽ và miễn phí của Google)
- Response thông minh và chính xác từ Gemini
- System context tối ưu cho giáo dục Việt Nam
- Hiểu rõ về OZA platform và tài liệu học tập

#### 2. ✅ Lưu lịch sử chat vào database (JSON files)
- Mỗi user có file chat riêng: `chat_history/chat_{username}.json`
- Guest users cũng có lịch sử: `chat_history/chat_guest.json`
- Tự động lưu sau mỗi câu hỏi
- Có nút "💾 Lưu lịch sử" thủ công
- Load lại lịch sử khi quay lại trang

#### 3. ✅ Thống kê chi tiết
- Đếm số câu hỏi đã hỏi
- Đếm số câu trả lời từ AI
- Hiển thị real-time trong sidebar
- Theo dõi hoạt động của từng user

#### 4. ✅ Phân tích câu hỏi phổ biến
- Function `analyze_popular_questions()` trong `chatbot_config.py`
- Có thể phân tích theo user hoặc toàn platform
- Top 10 câu hỏi gần nhất
- Tổng số câu hỏi đã được hỏi

#### 5. ✅ Câu hỏi gợi ý (Quick Actions)
- 3 nút câu hỏi mẫu phía dưới chat
- Click là gửi câu hỏi ngay lập tức
- Hỗ trợ cả tiếng Việt và tiếng Anh
- Dễ dàng mở rộng thêm câu hỏi

### 📁 Cấu trúc file:

```
d:\streamlit\
├── app.py                  # Main app với chatbot UI
├── chatbot_config.py       # Logic Google Gemini API và quản lý chat history
├── auth.py                 # Authentication system
├── requirements.txt        # Dependencies (đã thêm google-generativeai>=0.3.0)
├── chat_history/          # Folder lưu chat history (tự động tạo)
│   ├── chat_guest.json    # Chat của guest users
│   ├── chat_username1.json
│   └── chat_username2.json
└── users.json             # User database
```

### 🔧 Cấu hình Google Gemini API:

API Key đã được cấu hình trong `chatbot_config.py`:
```python
GEMINI_API_KEY = "AIzaSy..."
```

**Ưu điểm của Gemini:**
- ✅ Miễn phí với quota lớn
- ✅ Hỗ trợ tiếng Việt tốt
- ✅ Response nhanh
- ✅ Không giới hạn request (trong free tier)

**Lưu ý bảo mật:** 
- Trong production, nên lưu API key trong environment variable
- Không commit API key lên GitHub
- Có thể dùng `.env` file với `python-dotenv`

### 💡 System Context:

AI đã được train với context đặc biệt về:
- OZA platform và các tính năng
- Giáo dục Việt Nam (SGK, SBT, VBT)
- Phương pháp giảng dạy hiệu quả
- Động viên và khuyến khích học sinh
- Trả lời bằng tiếng Việt/tiếng Anh tùy ngôn ngữ

### 📊 Các function có sẵn:

#### `get_ai_response(messages, language)`
- Gọi Google Gemini API
- Tự động thêm system context
- Giới hạn 10 messages gần nhất để tiết kiệm token
- Error handling tốt

#### `load_chat_history(username)`
- Load lịch sử chat từ file JSON
- Return empty list nếu chưa có

#### `save_chat_history(username, messages)`
- Lưu messages vào file JSON
- Tự động tạo folder nếu chưa có

#### `get_chat_statistics(username)`
- Đếm số messages của user và assistant
- Return dict với stats

#### `analyze_popular_questions(username=None)`
- Phân tích câu hỏi phổ biến
- username=None để phân tích toàn platform
- Có username để phân tích từng user

### 🚀 Cách sử dụng:

1. **Chạy app:**
   ```bash
   streamlit run app.py
   ```

2. **Truy cập:** http://localhost:8501

3. **Click "AI Chatbot"** trên navigation bar

4. **Chat với AI:**
   - Gõ câu hỏi vào ô chat
   - Nhấn Enter
   - AI sẽ trả lời ngay

5. **Features:**
   - Xem thống kê trong sidebar
   - Click câu hỏi gợi ý để hỏi nhanh
   - Lưu/xóa lịch sử chat

### 🎨 UI/UX:

- ✅ Chat interface đẹp với avatar
- ✅ Spinner khi AI đang suy nghĩ
- ✅ Auto-scroll đến message mới
- ✅ Responsive design
- ✅ Sidebar với stats và controls
- ✅ Quick action buttons

### 🔮 Mở rộng trong tương lai:

- [ ] **Voice input/output** - Nói chuyện với AI
- [ ] **Image upload** - Gửi ảnh bài tập để giải
- [ ] **Export chat** - Download lịch sử chat (PDF/TXT)
- [ ] **Chat rooms** - Học nhóm với bạn bè
- [ ] **AI Tutor modes** - Chế độ giảng viên/bạn học
- [ ] **Knowledge base** - RAG với tài liệu OZA
- [ ] **Real-time typing** - Streaming responses
- [ ] **Feedback system** - 👍👎 cho responses
- [ ] **Analytics dashboard** - Admin xem thống kê

### 📝 Cost estimate:

Model: `gemini-pro`
- **MIỄN PHÍ** với 60 requests/phút
- Input: Không giới hạn (trong free tier)
- Output: Không giới hạn (trong free tier)

Chi phí: **$0 USD** 🎉 Hoàn toàn miễn phí!

### 🐛 Troubleshooting:

**Lỗi "API key invalid":**
- Kiểm tra API key trong `chatbot_config.py`
- Verify trên https://makersuite.google.com/app/apikey

**Lỗi "Rate limit":**
- Gemini free tier: 60 requests/phút
- Đợi 1 phút hoặc nâng cấp lên paid plan

**Lỗi "No response":**
- Check internet connection
- Xem terminal log để biết error chi tiết

### ✅ Testing:

Đã test các scenarios:
- ✅ Chat với guest user
- ✅ Chat với logged-in user
- ✅ Lưu và load lịch sử
- ✅ Xóa lịch sử
- ✅ Chuyển ngôn ngữ (VN ↔ EN)
- ✅ Quick action buttons
- ✅ Statistics tracking
- ✅ Error handling

### 🎉 Kết luận:

OZA AI Chatbot giờ đã là một trợ lý học tập thực sự với Google Gemini Pro - hoàn toàn miễn phí!
Học sinh có thể hỏi bất cứ điều gì về học tập và nhận câu trả lời chi tiết, chính xác.

**Made with ❤️ by AB-51 Team**
