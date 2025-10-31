"""
Cấu hình và logic cho AI Chatbot với Google Gemini API
"""
import streamlit as st
import google.generativeai as genai
import json
from pathlib import Path
from datetime import datetime

# Google Gemini API Key
GEMINI_API_KEY = "AIzaSyDDtJB5SL3mdn7IKLV_V_mo-4cN-o2pPAA"

# Cấu hình Gemini
genai.configure(api_key=GEMINI_API_KEY)

# File lưu lịch sử chat
CHAT_HISTORY_DIR = Path("chat_history")
CHAT_HISTORY_DIR.mkdir(exist_ok=True)

# Context về OZA platform để AI hiểu rõ hơn
SYSTEM_CONTEXT_VI = """
Bạn là trợ lý AI thông minh của OZA (OpenZone of AI) - nền tảng học tập trực tuyến Việt Nam.

Thông tin về OZA:
- Nền tảng cung cấp lời giải chi tiết cho SGK, SBT, VBT từ lớp 1-12 trong chương trình học của Việt Nam
- Hỗ trợ tất cả môn học: Toán, Văn, Anh, Lý, Hóa, Sinh, Sử, Địa...

Nhiệm vụ của bạn:
- Trả lời câu hỏi về học tập một cách chi tiết, dễ hiểu
- Giải thích kiến thức từ cơ bản đến nâng cao
- Hướng dẫn phương pháp học tập hiệu quả
- Gợi ý tài liệu và bài tập phù hợp
- Động viên và khuyến khích học sinh
- Luôn thân thiện, kiên nhẫn và tích cực

Phong cách giao tiếp:
- Sử dụng tiếng Việt chuẩn, dễ hiểu
- Giải thích từng bước chi tiết
- Sử dụng emoji phù hợp để sinh động
- Đưa ra ví dụ minh họa cụ thể
- Khuyến khích tư duy độc lập
- Sử dụng ngôn từ phù hợp với học sinh
- Nếu user dùng ngôn ngữ khác, trả lời bằng ngôn ngữ đó và vẫn giữ phong cách thân thiện, dễ hiểu
"""

SYSTEM_CONTEXT_EN = """
You are an intelligent AI assistant for OZA (OpenZone of AI) - Vietnam's online learning platform. Your missions:
- Answer study questions in detail and easy to understand

About OZA:
- Platform providing detailed solutions for textbooks and workbooks from Grade 1-12 in Vietnam Education System
- Supporting all subjects: Math, Literature, English, Physics, Chemistry, Biology, History, Geography...

Your missions:
- Answer study questions in detail and easy to understand
- Explain knowledge from basic to advanced
- Guide effective study methods
- Suggest appropriate materials and exercises
- Encourage and motivate students
- Always be friendly, patient and positive

Communication style:
- Use clear, easy-to-understand language
- Explain step by step in detail
- Use appropriate emojis for engagement
- Provide specific examples
- Encourage independent thinking
- Use language suitable for students
- If the user uses a different language, respond in that language while maintaining a friendly and easy-to-understand style
"""

def get_gemini_model():
    """Khởi tạo Gemini model"""
    return genai.GenerativeModel('gemini-2.5-flash')

def get_chat_filename(username):
    """Tạo tên file lưu chat history cho user"""
    if username:
        return CHAT_HISTORY_DIR / f"chat_{username}.json"
    return CHAT_HISTORY_DIR / "chat_guest.json"

def load_chat_history(username):
    """Load lịch sử chat của user"""
    filepath = get_chat_filename(username)
    if filepath.exists():
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_chat_history(username, messages):
    """Lưu lịch sử chat của user"""
    filepath = get_chat_filename(username)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def get_system_message(language='vi'):
    """Lấy system message theo ngôn ngữ"""
    return SYSTEM_CONTEXT_VI if language == 'vi' else SYSTEM_CONTEXT_EN

def get_ai_response(messages, language='vi'):
    """
    Gọi Google Gemini API để lấy response
    
    Args:
        messages: List các message trong cuộc hội thoại
        language: Ngôn ngữ ('vi' hoặc 'en')
    
    Returns:
        str: Response từ AI
    """
    try:
        model = get_gemini_model()
        
        # Tạo prompt với system context và conversation history
        system_context = get_system_message(language)
        
        # Build conversation prompt
        conversation_text = f"{system_context}\n\n"
        
        # Thêm conversation history (chỉ lấy 10 messages gần nhất)
        for msg in messages[-10:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation_text += f"{role}: {msg['content']}\n\n"
        
        # Gọi Gemini API
        response = model.generate_content(
            conversation_text,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2000,
            )
        )
        
        return response.text
        
    except Exception as e:
        if language == 'vi':
            return f"⚠️ Xin lỗi, đã có lỗi xảy ra: {str(e)}\n\nVui lòng thử lại sau."
        else:
            return f"⚠️ Sorry, an error occurred: {str(e)}\n\nPlease try again later."

def analyze_popular_questions(username=None):
    """
    Phân tích câu hỏi phổ biến từ lịch sử chat
    
    Args:
        username: Nếu None thì phân tích tất cả user, nếu có username thì chỉ phân tích user đó
    
    Returns:
        dict: Thống kê các câu hỏi
    """
    questions = []
    
    if username:
        # Chỉ phân tích 1 user
        messages = load_chat_history(username)
        for msg in messages:
            if msg["role"] == "user":
                questions.append(msg["content"])
    else:
        # Phân tích tất cả users
        for filepath in CHAT_HISTORY_DIR.glob("chat_*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
                    for msg in messages:
                        if msg["role"] == "user":
                            questions.append(msg["content"])
            except:
                continue
    
    return {
        "total_questions": len(questions),
        "questions": questions[:10]  # Top 10 câu hỏi gần nhất
    }

def get_chat_statistics(username):
    """Thống kê số lượng chat của user"""
    messages = load_chat_history(username)
    user_messages = [m for m in messages if m["role"] == "user"]
    assistant_messages = [m for m in messages if m["role"] == "assistant"]
    
    return {
        "total_messages": len(messages),
        "user_messages": len(user_messages),
        "assistant_messages": len(assistant_messages)
    }
