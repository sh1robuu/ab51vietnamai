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
# Universal context - AI sẽ tự động detect và reply bằng ngôn ngữ của user
SYSTEM_CONTEXT_UNIVERSAL = """
You are an intelligent AI educational assistant for OZA (OpenZone of AI) - a trusted online learning platform.

CONTEXT: This is an educational platform. All questions are for learning purposes.

IMPORTANT: Automatically detect the user's language and respond in the SAME language they use.
- If user writes in Vietnamese → Reply in Vietnamese
- If user writes in English → Reply in English  
- If user writes in other languages → Reply in that same language

About OZA:
- Educational platform providing detailed solutions for textbooks and workbooks from Grade 1-12
- Supporting all subjects: Mathematics, Literature, English, Physics, Chemistry, Biology, History, Geography, Social Studies, etc.
- Focused on Vietnam Education System but welcomes international students
- Safe learning environment for students of all ages

Your role as an educational assistant:
- Answer ALL educational questions in detail and easy-to-understand manner
- Explain academic concepts from basic to advanced levels
- Provide step-by-step solutions for homework and exercises
- Guide effective study methods and learning strategies
- Suggest appropriate educational materials and practice exercises
- Encourage critical thinking and independent learning
- Always be friendly, patient, supportive and positive
- Handle sensitive educational topics (history, biology, literature) professionally and age-appropriately

Communication guidelines:
- Use clear, easy-to-understand language (matching user's language)
- Explain step by step with detailed reasoning
- Use appropriate emojis to make learning engaging
- Provide concrete examples and real-world applications
- Encourage students to think independently
- Adapt language complexity to student's level
- Be culturally sensitive and respectful

Educational topics you should answer freely:
- Mathematics, Physics, Chemistry, Biology (including human anatomy for education)
- Literature, History, Social Studies (including sensitive historical events for learning)
- Language learning and grammar
- Science experiments and demonstrations
- Study techniques and exam preparation
- Career guidance and educational planning

Remember: 
- This is an EDUCATIONAL context - answer all learning questions openly
- ALWAYS match the user's language in your response
- Focus on helping students learn and understand concepts
- Maintain academic integrity while being helpful
"""

# Legacy contexts (kept for backward compatibility)
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
    """Khởi tạo Gemini model với safety settings tối ưu cho giáo dục"""
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"  # Không block cho nội dung giáo dục
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"  # Không block cho nội dung giáo dục
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"  # Block content không phù hợp
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"  # Block content nguy hiểm
        }
    ]
    return genai.GenerativeModel(
        'gemini-2.0-flash-exp',  # Sử dụng model mới nhất
        safety_settings=safety_settings
    )

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

def get_system_message(language='auto'):
    """
    Lấy system message theo ngôn ngữ
    
    Args:
        language: 'auto' (default) sử dụng universal context để AI tự detect,
                 'vi' hoặc 'en' để force ngôn ngữ cụ thể (legacy)
    """
    if language == 'auto':
        return SYSTEM_CONTEXT_UNIVERSAL
    return SYSTEM_CONTEXT_VI if language == 'vi' else SYSTEM_CONTEXT_EN

def detect_user_language(messages):
    """
    Detect ngôn ngữ của user từ messages history
    
    Args:
        messages: List các message trong cuộc hội thoại
    
    Returns:
        'vi' nếu phát hiện tiếng Việt, 'en' nếu tiếng Anh, 'en' là default
    """
    if not messages:
        return 'en'
    
    # Lấy tin nhắn cuối cùng từ user
    user_messages = [msg for msg in messages if msg.get('role') == 'user']
    if not user_messages:
        return 'en'
    
    last_message = user_messages[-1].get('content', '')
    
    # Simple detection: check for Vietnamese characters
    vietnamese_chars = ['ă', 'â', 'ê', 'ô', 'ơ', 'ư', 'đ', 'á', 'à', 'ả', 'ã', 'ạ',
                       'é', 'è', 'ẻ', 'ẽ', 'ẹ', 'í', 'ì', 'ỉ', 'ĩ', 'ị',
                       'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ú', 'ù', 'ủ', 'ũ', 'ụ', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ']
    
    for char in vietnamese_chars:
        if char in last_message.lower():
            return 'vi'
    
    return 'en'

def get_ai_response(messages, language='auto'):
    """
    Gọi Google Gemini API để lấy response
    
    Args:
        messages: List các message trong cuộc hội thoại
        language: 'auto' (default) - AI tự động detect và trả lời bằng ngôn ngữ của user
                 'vi' hoặc 'en' - Force ngôn ngữ cụ thể
    
    Returns:
        str: Response từ AI
    """
    try:
        # Detect ngôn ngữ từ messages để trả error message phù hợp
        detected_lang = detect_user_language(messages) if language == 'auto' else language
        
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
        
        # Kiểm tra xem response có hợp lệ không
        if not response or not response.candidates:
            if detected_lang == 'vi':
                return "⚠️ Xin lỗi, không thể tạo phản hồi. Vui lòng thử lại hoặc diễn đạt câu hỏi khác."
            else:
                return "⚠️ Sorry, couldn't generate a response. Please try again or rephrase your question."
        
        # Kiểm tra finish_reason
        candidate = response.candidates[0]
        if candidate.finish_reason not in [1, 0]:  # 1 = STOP (success), 0 = UNSPECIFIED
            if detected_lang == 'vi':
                error_msg = "⚠️ Câu hỏi của bạn có thể vi phạm chính sách an toàn hoặc không được hỗ trợ.\n\n"
                error_msg += "Vui lòng:\n"
                error_msg += "- Diễn đạt lại câu hỏi một cách rõ ràng hơn\n"
                error_msg += "- Tránh nội dung nhạy cảm hoặc không phù hợp\n"
                error_msg += "- Hỏi về các chủ đề học tập và giáo dục"
                return error_msg
            else:
                error_msg = "⚠️ Your question may violate safety policies or is not supported.\n\n"
                error_msg += "Please:\n"
                error_msg += "- Rephrase your question more clearly\n"
                error_msg += "- Avoid sensitive or inappropriate content\n"
                error_msg += "- Ask about educational topics"
                return error_msg
        
        # Kiểm tra xem có text content không
        if hasattr(response, 'text') and response.text:
            return response.text
        else:
            if detected_lang == 'vi':
                return "⚠️ Xin lỗi, không nhận được nội dung phản hồi. Vui lòng thử lại."
            else:
                return "⚠️ Sorry, no response content received. Please try again."
        
    except Exception as e:
        # Detect language for error message
        detected_lang = detect_user_language(messages) if language == 'auto' else language
        if detected_lang == 'vi':
            return f"⚠️ Xin lỗi, đã có lỗi xảy ra: {str(e)}\n\nVui lòng thử lại sau hoặc liên hệ hỗ trợ."
        else:
            return f"⚠️ Sorry, an error occurred: {str(e)}\n\nPlease try again later or contact support."

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
