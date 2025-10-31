# Ứng dụng Streamlit

Đây là một ứng dụng Streamlit cơ bản để bắt đầu dự án của bạn.

## Cài đặt

1. Tạo môi trường ảo (khuyến nghị):
```bash
python -m venv venv
```

2. Kích hoạt môi trường ảo:
- Windows:
```bash
venv\Scripts\activate
```
- Mac/Linux:
```bash
source venv/bin/activate
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ tự động mở trong trình duyệt tại địa chỉ `http://localhost:8501`

## Cấu trúc dự án

```
streamlit/
│
├── app.py              # File chính của ứng dụng
├── requirements.txt    # Các thư viện Python cần thiết
├── README.md          # Hướng dẫn sử dụng
├── .gitignore         # File ignore cho Git
└── .streamlit/        # Thư mục cấu hình (tùy chọn)
    └── config.toml    # File cấu hình Streamlit
```

## Tính năng

- 🎨 Giao diện đẹp mắt và dễ sử dụng
- 📊 Trực quan hóa dữ liệu
- 🚀 Dễ dàng triển khai
- 🔧 Dễ dàng tùy chỉnh

## Tùy chỉnh

Bạn có thể tùy chỉnh ứng dụng bằng cách chỉnh sửa file `app.py` và thêm các tính năng mới theo nhu cầu của bạn.

## Triển khai

Bạn có thể triển khai ứng dụng lên Streamlit Cloud miễn phí:
1. Push code lên GitHub
2. Truy cập https://streamlit.io/cloud
3. Kết nối repository và triển khai

## Hỗ trợ

Để biết thêm thông tin về Streamlit, truy cập: https://docs.streamlit.io
