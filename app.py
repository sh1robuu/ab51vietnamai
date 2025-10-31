import streamlit as st
import auth  # Import module auth
import chatbot_config  # Import module chatbot config

# Khởi tạo session state
if 'language' not in st.session_state:
    st.session_state.language = 'vi'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'show_login' not in st.session_state:
    st.session_state.show_login = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False
if 'show_dev_notice' not in st.session_state:
    st.session_state.show_dev_notice = False
if 'selected_grade' not in st.session_state:
    st.session_state.selected_grade = None
if 'selected_subject' not in st.session_state:
    st.session_state.selected_subject = None
if 'highlighted_text' not in st.session_state:
    st.session_state.highlighted_text = None
if 'show_ai_helper' not in st.session_state:
    st.session_state.show_ai_helper = False
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = None  # None, 'practice', 'test'
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'cheating_count' not in st.session_state:
    st.session_state.cheating_count = 0
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

# Dictionary chứa các bản dịch
translations = {
    'vi': {
        'site_name': 'OZA - OpenZone of AI',
        'main_title': 'OZA - OpenZone of AI',
        'subtitle': 'Khu vực mở về Trí tuệ nhân tạo - Made by AB-51 Team',
        'hot_section': 'CÓ GÌ HOT?',
        'nav_home': 'Trang chủ',
        'nav_grades': 'Kiến thức & Bài giảng',
        'nav_detail': 'Chi tiết',
        'nav_tools': 'AI Chatbot',
        'nav_feedback': 'Góp ý',
        'nav_about': 'Giới thiệu',
        'choose_grade': 'KIẾN THỨC VÀ BÀI GIẢNG',
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
        'chatbot': 'AI Chatbot - Trợ lý học tập',
        'chatbot_placeholder': 'Hỏi bất cứ điều gì về học tập...',
        'chatbot_welcome': 'Xin chào! Tôi là trợ lý AI của OZA. Tôi có thể giúp bạn giải đáp các thắc mắc về học tập. Hãy hỏi tôi bất cứ điều gì!',
        'about': 'Giới thiệu',
    },
    'en': {
        'site_name': 'OZA - OpenZone of AI',
        'main_title': 'OZA - OpenZone of AI',
        'subtitle': "Open Zone of Artificial Intelligence - Made by AB-51 Team",
        'hot_section': "WHAT'S HOT?",
        'nav_home': 'Home',
        'nav_grades': 'Knowledge & Lessons',
        'nav_tools': 'AI Chatbot',
        'nav_feedback': 'Feedback',
        'nav_about': 'About',
        'choose_grade': 'KNOWLEDGE AND LESSONS',
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
        'chatbot': 'AI Chatbot - Learning Assistant',
        'chatbot_placeholder': 'Ask me anything about your studies...',
        'chatbot_welcome': 'Hello! I am OZA\'s AI assistant. I can help you with any questions about your studies. Ask me anything!',
        'about': 'About Us',
    }
}

def get_text(key):
    return translations[st.session_state.language][key]

@st.dialog("🤖 AI Learning Assistant", width="large")
def ai_helper_dialog():
    """Dialog AI hỗ trợ học tập khi highlight text"""
    if st.session_state.language == 'vi':
        st.markdown("### 💡 Hỗ trợ học tập với AI")
        st.info(f"**Nội dung được chọn:** {st.session_state.highlighted_text}")
        
        question_type = st.radio(
            "Bạn muốn làm gì với nội dung này?",
            ["Giải thích chi tiết", "Cho ví dụ thêm", "Tóm tắt ngắn gọn", "Tạo câu hỏi ôn tập", "Hỏi tự do"],
            horizontal=True
        )
        
        if question_type == "Hỏi tự do":
            user_question = st.text_area("Nhập câu hỏi của bạn:", placeholder="Ví dụ: Giải thích khái niệm này bằng ngôn ngữ đơn giản hơn...")
        else:
            user_question = None
        
        if st.button("🚀 Hỏi AI", type="primary", use_container_width=True):
            with st.spinner("AI đang suy nghĩ..."):
                # Tạo prompt dựa trên loại câu hỏi
                prompts = {
                    "Giải thích chi tiết": f"Hãy giải thích chi tiết khái niệm sau đây bằng ngôn ngữ dễ hiểu cho học sinh lớp 10:\n\n{st.session_state.highlighted_text}",
                    "Cho ví dụ thêm": f"Hãy cho thêm 2-3 ví dụ cụ thể và dễ hiểu về:\n\n{st.session_state.highlighted_text}",
                    "Tóm tắt ngắn gọn": f"Hãy tóm tắt ngắn gọn (3-5 câu) nội dung sau:\n\n{st.session_state.highlighted_text}",
                    "Tạo câu hỏi ôn tập": f"Hãy tạo 3-5 câu hỏi ôn tập về:\n\n{st.session_state.highlighted_text}",
                    "Hỏi tự do": f"Nội dung tham khảo: {st.session_state.highlighted_text}\n\nCâu hỏi: {user_question}"
                }
                
                prompt = prompts.get(question_type, prompts["Giải thích chi tiết"])
                
                # Tạo messages list theo format của chatbot_config
                messages = [{"role": "user", "content": prompt}]
                
                # Gọi AI
                response = chatbot_config.get_ai_response(messages, language='vi')
                
                st.markdown("### 📝 Câu trả lời:")
                st.markdown(response)
                
    else:  # English version
        st.markdown("### 💡 AI Learning Assistant")
        st.info(f"**Selected content:** {st.session_state.highlighted_text}")
        
        question_type = st.radio(
            "What would you like to do with this content?",
            ["Explain in detail", "Give more examples", "Summarize briefly", "Create practice questions", "Ask freely"],
            horizontal=True
        )
        
        if question_type == "Ask freely":
            user_question = st.text_area("Enter your question:", placeholder="Example: Explain this concept in simpler language...")
        else:
            user_question = None
        
        if st.button("🚀 Ask AI", type="primary", use_container_width=True):
            with st.spinner("AI is thinking..."):
                # Create prompt based on question type
                prompts = {
                    "Explain in detail": f"Please explain the following concept in detail in an easy-to-understand language for 10th grade students:\n\n{st.session_state.highlighted_text}",
                    "Give more examples": f"Please provide 2-3 specific and easy-to-understand examples about:\n\n{st.session_state.highlighted_text}",
                    "Summarize briefly": f"Please summarize briefly (3-5 sentences) the following content:\n\n{st.session_state.highlighted_text}",
                    "Create practice questions": f"Please create 3-5 practice questions about:\n\n{st.session_state.highlighted_text}",
                    "Ask freely": f"Reference content: {st.session_state.highlighted_text}\n\nQuestion: {user_question}"
                }
                
                prompt = prompts.get(question_type, prompts["Explain in detail"])
                
                # Create messages list according to chatbot_config format
                messages = [{"role": "user", "content": prompt}]
                
                # Call AI
                response = chatbot_config.get_ai_response(messages, language='en')
                
                st.markdown("### 📝 Answer:")
                st.markdown(response)

# Dữ liệu câu hỏi cho Toán 10 - Bài 1
QUIZ_DATA_MATH10_LESSON1 = {
    "practice": [
        {
            "id": 1,
            "type": "multiple_choice",
            "question": "Mệnh đề toán học là gì?",
            "options": [
                "Một phát biểu có thể đúng hoặc sai về một sự kiện trong toán học",
                "Một câu hỏi về toán học",
                "Một công thức toán học",
                "Một định lý đã được chứng minh"
            ],
            "correct": 0,
            "explanation": "Mệnh đề toán học là một phát biểu, một khẳng định (có thể đúng hoặc sai) về một sự kiện trong toán học."
        },
        {
            "id": 2,
            "type": "true_false",
            "question": "Mỗi mệnh đề toán học có thể vừa đúng vừa sai.",
            "correct": False,
            "explanation": "Sai! Mỗi mệnh đề toán học phải đúng hoặc sai, không thể vừa đúng vừa sai."
        },
        {
            "id": 3,
            "type": "multiple_choice",
            "question": "Ký hiệu phủ định của mệnh đề P là gì?",
            "options": ["P'", "¬P", "P̄ (P gạch ngang)", "~P"],
            "correct": 2,
            "explanation": "Mệnh đề phủ định của mệnh đề P được ký hiệu là P̄ (đọc là 'P gạch ngang')."
        },
        {
            "id": 4,
            "type": "multiple_choice",
            "question": "Mệnh đề P ⇒ Q sai khi nào?",
            "options": [
                "P đúng, Q đúng",
                "P đúng, Q sai",
                "P sai, Q đúng",
                "P sai, Q sai"
            ],
            "correct": 1,
            "explanation": "Mệnh đề P ⇒ Q chỉ sai khi P đúng và Q sai, các trường hợp còn lại đều đúng."
        },
        {
            "id": 5,
            "type": "true_false",
            "question": "Phủ định của '∀x ∈ X, P(x)' là '∃x ∈ X, P̄(x)'",
            "correct": True,
            "explanation": "Đúng! Phủ định của mệnh đề 'Với mọi' là 'Tồn tại' và ngược lại."
        }
    ],
    "test": [
        {
            "id": 1,
            "type": "multiple_choice",
            "question": "Cho mệnh đề P: '5 > 3'. Mệnh đề này là:",
            "options": ["Đúng", "Sai", "Không xác định", "Cả đúng và sai"],
            "correct": 0,
            "explanation": "Mệnh đề '5 > 3' là mệnh đề đúng vì 5 thực sự lớn hơn 3."
        },
        {
            "id": 2,
            "type": "true_false",
            "question": "Mệnh đề 'n chia hết cho 3' (với n là số tự nhiên) là mệnh đề chứa biến.",
            "correct": True,
            "explanation": "Đúng! Đây là mệnh đề chứa biến vì tính đúng sai phụ thuộc vào giá trị của n."
        },
        {
            "id": 3,
            "type": "multiple_choice",
            "question": "Trong mệnh đề kéo theo P ⇒ Q, P là điều kiện gì của Q?",
            "options": ["Điều kiện cần", "Điều kiện đủ", "Điều kiện cần và đủ", "Không liên quan"],
            "correct": 1,
            "explanation": "P là điều kiện đủ để có Q (có P thì chắc chắn có Q)."
        },
        {
            "id": 4,
            "type": "short_answer",
            "question": "Viết ký hiệu mệnh đề 'P khi và chỉ khi Q'",
            "correct": ["P ⇔ Q", "P<=>Q", "P iff Q"],
            "explanation": "Ký hiệu là P ⇔ Q (hai mũi tên)."
        },
        {
            "id": 5,
            "type": "multiple_choice",
            "question": "Phủ định của mệnh đề '∃x ∈ ℝ, x² < 0' là:",
            "options": [
                "∀x ∈ ℝ, x² < 0",
                "∀x ∈ ℝ, x² ≥ 0",
                "∃x ∈ ℝ, x² ≥ 0",
                "∃x ∈ ℝ, x² > 0"
            ],
            "correct": 1,
            "explanation": "Phủ định của '∃x, P(x)' là '∀x, P̄(x)'. Vậy phủ định của '∃x ∈ ℝ, x² < 0' là '∀x ∈ ℝ, x² ≥ 0'."
        },
        {
            "id": 6,
            "type": "true_false",
            "question": "Nếu P ⇒ Q đúng thì Q ⇒ P cũng đúng.",
            "correct": False,
            "explanation": "Sai! Mệnh đề Q ⇒ P là mệnh đề đảo của P ⇒ Q và không nhất thiết đúng khi P ⇒ Q đúng."
        },
        {
            "id": 7,
            "type": "short_answer",
            "question": "Mệnh đề nào biểu thị 'Với mọi x thuộc X'? (Viết ký hiệu)",
            "correct": ["∀x ∈ X", "forall x in X", "∀x∈X"],
            "explanation": "Ký hiệu là ∀x ∈ X (∀ đọc là 'với mọi' hoặc 'for all')."
        },
        {
            "id": 8,
            "type": "multiple_choice",
            "question": "Mệnh đề P ⇔ Q đúng khi nào?",
            "options": [
                "Chỉ khi P ⇒ Q đúng",
                "Chỉ khi Q ⇒ P đúng",
                "Khi cả P ⇒ Q và Q ⇒ P đều đúng",
                "Khi P và Q đều đúng"
            ],
            "correct": 2,
            "explanation": "P ⇔ Q đúng khi và chỉ khi cả hai chiều P ⇒ Q và Q ⇒ P đều đúng."
        }
    ]
}

# English version
QUIZ_DATA_MATH10_LESSON1_EN = {
    "practice": [
        {
            "id": 1,
            "type": "multiple_choice",
            "question": "What is a mathematical proposition?",
            "options": [
                "A statement that can be true or false about a mathematical fact",
                "A question about mathematics",
                "A mathematical formula",
                "A proven theorem"
            ],
            "correct": 0,
            "explanation": "A mathematical proposition is a statement or assertion (which can be true or false) about a mathematical fact."
        },
        {
            "id": 2,
            "type": "true_false",
            "question": "Each mathematical proposition can be both true and false.",
            "correct": False,
            "explanation": "False! Each mathematical proposition must be either true or false, not both."
        },
        {
            "id": 3,
            "type": "multiple_choice",
            "question": "What is the symbol for the negation of proposition P?",
            "options": ["P'", "¬P", "P̄ (P bar)", "~P"],
            "correct": 2,
            "explanation": "The negation of proposition P is denoted by P̄ (read as 'P bar')."
        },
        {
            "id": 4,
            "type": "multiple_choice",
            "question": "When is the proposition P ⇒ Q false?",
            "options": [
                "P true, Q true",
                "P true, Q false",
                "P false, Q true",
                "P false, Q false"
            ],
            "correct": 1,
            "explanation": "The proposition P ⇒ Q is false only when P is true and Q is false; all other cases are true."
        },
        {
            "id": 5,
            "type": "true_false",
            "question": "The negation of '∀x ∈ X, P(x)' is '∃x ∈ X, P̄(x)'",
            "correct": True,
            "explanation": "True! The negation of 'For all' is 'There exists' and vice versa."
        }
    ],
    "test": [
        {
            "id": 1,
            "type": "multiple_choice",
            "question": "Given proposition P: '5 > 3'. This proposition is:",
            "options": ["True", "False", "Undefined", "Both true and false"],
            "correct": 0,
            "explanation": "The proposition '5 > 3' is true because 5 is actually greater than 3."
        },
        {
            "id": 2,
            "type": "true_false",
            "question": "The proposition 'n is divisible by 3' (where n is a natural number) is a proposition with a variable.",
            "correct": True,
            "explanation": "True! This is a proposition with a variable because its truth value depends on the value of n."
        },
        {
            "id": 3,
            "type": "multiple_choice",
            "question": "In the implication P ⇒ Q, what condition is P for Q?",
            "options": ["Necessary condition", "Sufficient condition", "Necessary and sufficient condition", "Not related"],
            "correct": 1,
            "explanation": "P is a sufficient condition for Q (having P guarantees Q)."
        },
        {
            "id": 4,
            "type": "short_answer",
            "question": "Write the symbol for 'P if and only if Q'",
            "correct": ["P ⇔ Q", "P<=>Q", "P iff Q"],
            "explanation": "The symbol is P ⇔ Q (double arrow)."
        },
        {
            "id": 5,
            "type": "multiple_choice",
            "question": "The negation of '∃x ∈ ℝ, x² < 0' is:",
            "options": [
                "∀x ∈ ℝ, x² < 0",
                "∀x ∈ ℝ, x² ≥ 0",
                "∃x ∈ ℝ, x² ≥ 0",
                "∃x ∈ ℝ, x² > 0"
            ],
            "correct": 1,
            "explanation": "The negation of '∃x, P(x)' is '∀x, P̄(x)'. So the negation of '∃x ∈ ℝ, x² < 0' is '∀x ∈ ℝ, x² ≥ 0'."
        },
        {
            "id": 6,
            "type": "true_false",
            "question": "If P ⇒ Q is true, then Q ⇒ P is also true.",
            "correct": False,
            "explanation": "False! The proposition Q ⇒ P is the converse of P ⇒ Q and is not necessarily true when P ⇒ Q is true."
        },
        {
            "id": 7,
            "type": "short_answer",
            "question": "Which statement represents 'For all x in X'? (Write the symbol)",
            "correct": ["∀x ∈ X", "forall x in X", "∀x∈X"],
            "explanation": "The symbol is ∀x ∈ X (∀ reads as 'for all')."
        },
        {
            "id": 8,
            "type": "multiple_choice",
            "question": "When is the proposition P ⇔ Q true?",
            "options": [
                "Only when P ⇒ Q is true",
                "Only when Q ⇒ P is true",
                "When both P ⇒ Q and Q ⇒ P are true",
                "When both P and Q are true"
            ],
            "correct": 2,
            "explanation": "P ⇔ Q is true if and only if both directions P ⇒ Q and Q ⇒ P are true."
        }
    ]
}

def render_quiz_question(question, question_num, mode='practice'):
    """Render một câu hỏi quiz"""
    lang = st.session_state.language
    
    if lang == 'vi':
        st.markdown(f"### Câu {question_num}: {question['question']}")
    else:
        st.markdown(f"### Question {question_num}: {question['question']}")
    
    answer_key = f"q_{question['id']}"
    
    if question['type'] == 'multiple_choice':
        answer = st.radio(
            "Chọn đáp án:" if lang == 'vi' else "Choose answer:",
            question['options'],
            key=answer_key,
            index=None
        )
        if answer:
            st.session_state.quiz_answers[question['id']] = question['options'].index(answer)
    
    elif question['type'] == 'true_false':
        answer = st.radio(
            "Chọn đáp án:" if lang == 'vi' else "Choose answer:",
            ["Đúng", "Sai"] if lang == 'vi' else ["True", "False"],
            key=answer_key,
            index=None
        )
        if answer:
            st.session_state.quiz_answers[question['id']] = (answer == ("Đúng" if lang == 'vi' else "True"))
    
    elif question['type'] == 'short_answer':
        answer = st.text_input(
            "Nhập câu trả lời của bạn:" if lang == 'vi' else "Enter your answer:",
            key=answer_key
        )
        if answer:
            st.session_state.quiz_answers[question['id']] = answer.strip()
    
    st.divider()

def check_answer(question, user_answer):
    """Kiểm tra câu trả lời"""
    if question['type'] == 'short_answer':
        # Cho phép nhiều đáp án đúng
        correct_answers = [ans.lower().strip() for ans in question['correct']]
        return user_answer.lower().strip() in correct_answers
    else:
        return user_answer == question['correct']

def calculate_score(questions, answers):
    """Tính điểm"""
    correct = 0
    total = len(questions)
    
    for q in questions:
        if q['id'] in answers:
            if check_answer(q, answers[q['id']]):
                correct += 1
    
    return correct, total

@st.dialog("📊 Kết quả làm bài" if st.session_state.language == 'vi' else "📊 Quiz Results", width="large")
def show_quiz_results(questions, answers, cheating_count, mode='practice'):
    """Hiển thị kết quả quiz"""
    lang = st.session_state.language
    correct, total = calculate_score(questions, answers)
    
    # Trừ điểm gian lận (chỉ áp dụng cho test mode)
    penalty = cheating_count if mode == 'test' else 0
    final_score = max(0, correct - penalty)
    percentage = (final_score / total) * 100
    
    # Hiển thị điểm
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Điểm gốc" if lang == 'vi' else "Original Score", f"{correct}/{total}")
    with col2:
        st.metric("Số lần gian lận" if lang == 'vi' else "Violations", cheating_count, delta=f"-{penalty} {'điểm' if lang == 'vi' else 'pts'}" if penalty > 0 else None)
    with col3:
        st.metric("Điểm cuối cùng" if lang == 'vi' else "Final Score", f"{final_score}/{total}")
    
    st.progress(percentage / 100)
    
    # Đánh giá
    if lang == 'vi':
        if percentage >= 90:
            st.success("🎉 Xuất sắc! Bạn đã nắm vững kiến thức!")
        elif percentage >= 70:
            st.info("👍 Khá tốt! Hãy ôn lại một số phần còn thiếu.")
        elif percentage >= 50:
            st.warning("📚 Cần cố gắng thêm! Hãy xem lại lý thuyết.")
        else:
            st.error("💪 Đừng nản lòng! Hãy học lại lý thuyết và thử lại.")
    else:
        if percentage >= 90:
            st.success("🎉 Excellent! You've mastered the knowledge!")
        elif percentage >= 70:
            st.info("👍 Good job! Review some missing parts.")
        elif percentage >= 50:
            st.warning("📚 Need more effort! Review the theory.")
        else:
            st.error("💪 Don't give up! Study the theory and try again.")
    
    st.divider()
    
    # Chi tiết từng câu
    st.markdown("### 📝 Chi tiết từng câu:" if lang == 'vi' else "### 📝 Detailed Results:")
    
    for i, q in enumerate(questions, 1):
        user_answer = answers.get(q['id'])
        is_correct = check_answer(q, user_answer) if user_answer is not None else False
        
        with st.expander(f"{'Câu' if lang == 'vi' else 'Question'} {i}: {'✅' if is_correct else '❌'}"):
            st.markdown(f"**{q['question']}**")
            
            if q['type'] == 'multiple_choice':
                st.write(f"{'Đáp án của bạn' if lang == 'vi' else 'Your answer'}: {q['options'][user_answer] if user_answer is not None else ('Chưa trả lời' if lang == 'vi' else 'Not answered')}")
                st.write(f"{'Đáp án đúng' if lang == 'vi' else 'Correct answer'}: {q['options'][q['correct']]}")
            elif q['type'] == 'true_false':
                true_false_vi = ['Đúng', 'Sai']
                true_false_en = ['True', 'False']
                tf = true_false_vi if lang == 'vi' else true_false_en
                st.write(f"{'Đáp án của bạn' if lang == 'vi' else 'Your answer'}: {tf[0] if user_answer else tf[1] if user_answer is not None else ('Chưa trả lời' if lang == 'vi' else 'Not answered')}")
                st.write(f"{'Đáp án đúng' if lang == 'vi' else 'Correct answer'}: {tf[0] if q['correct'] else tf[1]}")
            elif q['type'] == 'short_answer':
                st.write(f"{'Đáp án của bạn' if lang == 'vi' else 'Your answer'}: {user_answer if user_answer else ('Chưa trả lời' if lang == 'vi' else 'Not answered')}")
                st.write(f"{'Đáp án đúng' if lang == 'vi' else 'Correct answer'}: {', '.join(q['correct'])}")
            
            st.info(f"💡 **{'Giải thích' if lang == 'vi' else 'Explanation'}:** {q['explanation']}")
    
    if mode == 'test' and cheating_count > 0:
        st.divider()
        if lang == 'vi':
            st.warning(f"⚠️ **Lưu ý:** Bạn đã có {cheating_count} lần hành vi gian lận (thoát fullscreen/chuyển tab). Mỗi lần bị trừ 1 điểm.")
        else:
            st.warning(f"⚠️ **Note:** You had {cheating_count} violations (exiting fullscreen/switching tabs). Each violation deducts 1 point.")

def render_practice_quiz(lesson_id):
    """Render bài tập thực hành"""
    lang = st.session_state.language
    questions = QUIZ_DATA_MATH10_LESSON1['practice'] if lang == 'vi' else QUIZ_DATA_MATH10_LESSON1_EN['practice']
    
    st.markdown("## 📝 Bài tập thực hành - Mệnh đề toán học" if lang == 'vi' else "## 📝 Practice Exercises - Mathematical Propositions")
    st.info("💡 Làm bài tập để củng cố kiến thức. Bạn có thể xem giải thích sau khi nộp bài." if lang == 'vi' else "💡 Do exercises to reinforce knowledge. You can view explanations after submission.")
    
    st.divider()
    
    # Render câu hỏi
    for i, q in enumerate(questions, 1):
        render_quiz_question(q, i, mode='practice')
    
    # Nút nộp bài
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("✅ Nộp bài" if lang == 'vi' else "✅ Submit", type="primary", use_container_width=True):
            if len(st.session_state.quiz_answers) < len(questions):
                st.warning("⚠️ Vui lòng trả lời tất cả các câu hỏi!" if lang == 'vi' else "⚠️ Please answer all questions!")
            else:
                st.session_state.quiz_submitted = True
                show_quiz_results(questions, st.session_state.quiz_answers, 0, mode='practice')
    
    if st.button("🔙 Quay lại bài học" if lang == 'vi' else "🔙 Back to Lesson"):
        st.session_state.quiz_mode = None
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.rerun()

def render_test_quiz(lesson_id):
    """Render bài kiểm tra"""
    lang = st.session_state.language
    questions = QUIZ_DATA_MATH10_LESSON1['test'] if lang == 'vi' else QUIZ_DATA_MATH10_LESSON1_EN['test']
    
    if not st.session_state.quiz_started:
        # Màn hình bắt đầu
        st.markdown("## 📋 Bài kiểm tra - Mệnh đề toán học" if lang == 'vi' else "## 📋 Test - Mathematical Propositions")
        
        if lang == 'vi':
            st.warning("""
        ### ⚠️ Lưu ý quan trọng:
        - Bài kiểm tra sẽ được làm ở **chế độ toàn màn hình**
        - Hệ thống sẽ **cảnh báo** nếu bạn:
          - Thoát chế độ toàn màn hình
          - Chuyển sang tab/cửa sổ khác (Alt+Tab, Windows+D, v.v.)
        - **Nếu vô tình vi phạm**, hãy click nút "Báo cáo vi phạm" để ghi nhận
        - **Mỗi lần vi phạm sẽ bị trừ 1 điểm**
        - Bài kiểm tra có {} câu hỏi
        - Thời gian không giới hạn (nhưng nên hoàn thành trong 15 phút)
        - Làm bài trung thực để đánh giá đúng năng lực của bản thân!
        """.format(len(questions)))
            st.info("💡 Hãy chuẩn bị tinh thần, tập trung làm bài và không gian lận!")
        else:
            st.warning("""
        ### ⚠️ Important Notes:
        - The test will be taken in **fullscreen mode**
        - The system will **warn** if you:
          - Exit fullscreen mode
          - Switch to another tab/window (Alt+Tab, Windows+D, etc.)
        - **If you accidentally violate**, click "Report Violation" button to record it
        - **Each violation will deduct 1 point**
        - The test has {} questions
        - No time limit (but should complete within 15 minutes)
        - Be honest to assess your true abilities!
        """.format(len(questions)))
            st.info("💡 Prepare yourself, focus on the test, and don't cheat!")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Bắt đầu làm bài" if lang == 'vi' else "🚀 Start Test", type="primary", use_container_width=True):
                st.session_state.quiz_started = True
                st.session_state.cheating_count = 0
                st.rerun()
        
        if st.button("🔙 Quay lại bài học" if lang == 'vi' else "🔙 Back to Lesson"):
            st.session_state.quiz_mode = None
            st.rerun()
    
    else:
        # Đang làm bài
        lang = st.session_state.language
        st.markdown("## 📋 Bài kiểm tra - Mệnh đề toán học" if lang == 'vi' else "## 📋 Test - Mathematical Propositions")
        
        if lang == 'vi':
            st.warning("""
        ⚠️ **Lưu ý:** Nếu bạn vô tình thoát fullscreen hoặc chuyển tab, hãy click nút "➕ Báo cáo vi phạm" 
        để ghi nhận (mỗi lần sẽ trừ 1 điểm). Làm bài trung thực để đánh giá đúng năng lực!
        """)
        else:
            st.warning("""
        ⚠️ **Note:** If you accidentally exit fullscreen or switch tabs, click "➕ Report Violation" 
        to record it (each time deducts 1 point). Be honest to assess your true abilities!
        """)
        
        # Thêm JavaScript để detect gian lận và fullscreen
        alert_fullscreen = '⚠️ Cảnh báo: Bạn đã thoát chế độ toàn màn hình! -1 điểm' if lang == 'vi' else '⚠️ Warning: You exited fullscreen mode! -1 point'
        alert_tab = '⚠️ Cảnh báo: Bạn đã chuyển sang tab khác! -1 điểm' if lang == 'vi' else '⚠️ Warning: You switched to another tab! -1 point'
        alert_window = '⚠️ Cảnh báo: Bạn đã chuyển sang cửa sổ khác! -1 điểm' if lang == 'vi' else '⚠️ Warning: You switched to another window! -1 point'
        
        st.markdown(f"""
        <script>
        // Request fullscreen
        function enterFullscreen() {{
            var elem = document.documentElement;
            if (elem.requestFullscreen) {{
                elem.requestFullscreen();
            }} else if (elem.webkitRequestFullscreen) {{
                elem.webkitRequestFullscreen();
            }} else if (elem.msRequestFullscreen) {{
                elem.msRequestFullscreen();
            }}
        }}
        
        // Detect fullscreen change
        document.addEventListener('fullscreenchange', function() {{
            if (!document.fullscreenElement) {{
                // Thoát fullscreen - gian lận
                alert('{alert_fullscreen}');
                // Trigger increment cheating count
                window.parent.postMessage({{type: 'cheating'}}, '*');
            }}
        }});
        
        // Detect tab visibility change
        document.addEventListener('visibilitychange', function() {{
            if (document.hidden) {{
                alert('{alert_tab}');
                window.parent.postMessage({{type: 'cheating'}}, '*');
            }}
        }});
        
        // Detect window blur (Alt+Tab)
        window.addEventListener('blur', function() {{
            alert('{alert_window}');
            window.parent.postMessage({{type: 'cheating'}}, '*');
        }});
        
        // Auto enter fullscreen when page loads
        setTimeout(enterFullscreen, 500);
        </script>
        
        <style>
        /* Hide Streamlit menu and footer during test */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        </style>
        """, unsafe_allow_html=True)
        
        # Thông tin trạng thái
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.info(f"🔒 {'Chế độ bài kiểm tra' if lang == 'vi' else 'Test Mode'} - {'Câu hỏi' if lang == 'vi' else 'Questions'}: {len(questions)}")
        with col2:
            st.error(f"⚠️ {'Vi phạm' if lang == 'vi' else 'Violations'}: {st.session_state.cheating_count}")
        with col3:
            # Nút để tăng số lần vi phạm (học sinh tự báo cáo)
            if st.button("➕ " + ("Báo cáo vi phạm" if lang == 'vi' else "Report Violation"), help="Nếu bạn vô tình thoát fullscreen/đổi tab, click vào đây" if lang == 'vi' else "If you accidentally exit fullscreen/switch tab, click here"):
                st.session_state.cheating_count += 1
                st.rerun()
        
        st.divider()
        
        # Render câu hỏi
        for i, q in enumerate(questions, 1):
            render_quiz_question(q, i, mode='test')
        
        # Nút nộp bài
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("✅ " + ("Nộp bài" if lang == 'vi' else "Submit"), type="primary", use_container_width=True):
                if len(st.session_state.quiz_answers) < len(questions):
                    st.warning("⚠️ Vui lòng trả lời tất cả các câu hỏi!" if lang == 'vi' else "⚠️ Please answer all questions!")
                else:
                    st.session_state.quiz_submitted = True
                    show_quiz_results(questions, st.session_state.quiz_answers, st.session_state.cheating_count, mode='test')
                    # Reset quiz state
                    st.session_state.quiz_started = False
                    st.session_state.quiz_mode = None
                    st.session_state.quiz_answers = {}

# Cấu hình trang
st.set_page_config(
    page_title="OZA - OpenZone of AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh để tăng font chữ
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
    
    /* Logo ở đầu sidebar */
    [data-testid="stSidebarNav"]::before {
        content: "🤖 OZA";
        display: block;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        color: #667eea;
        padding: 0.5rem 0 0.8rem 0;
        margin: 0;
        border-bottom: 1px solid #444;
    }
    
    /* Xóa khoảng trắng thừa trong sidebar */
    [data-testid="stSidebarNav"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    [data-testid="stSidebarNav"] ul {
        padding-top: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Các hàm trang
def home():
    # Reset grade/subject selection khi vào home
    if 'selected_grade' in st.session_state:
        st.session_state.selected_grade = None
    if 'selected_subject' in st.session_state:
        st.session_state.selected_subject = None
    
    st.markdown(f"<h1 style='text-align: center; color: #667eea;'>🤖 {get_text('main_title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #666;'>{get_text('subtitle')}</h3>", unsafe_allow_html=True)
    st.divider()
    
    # Banner chào mừng
    if st.session_state.language == 'vi':
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;'>
            <h2>🎓 Chào mừng đến với OZA!</h2>
            <p style='font-size: 1.1rem; margin-top: 1rem;'>
                Dự án học tập kết hợp AI của nhóm <strong>AB-51 Team</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;'>
            <h2>🎓 Welcome to OZA!</h2>
            <p style='font-size: 1.1rem; margin-top: 1rem;'>
                Student learning project with AI by <strong>AB-51 Team</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"## 🌟 {get_text('hot_section')}")
    st.write("")
    
    # Phần tính năng nổi bật với icons và mô tả chi tiết
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.language == 'vi':
            st.markdown("""
            <div style='background-color: #e3f2fd; padding: 1.5rem; border-radius: 10px; 
                        border-left: 5px solid #2196F3; margin-bottom: 1rem;'>
                <h3 style='color: #1976D2; margin-top: 0;'>📚 Tài liệu tham khảo</h3>
                <p style='color: #333; margin-bottom: 0.5rem;'>Hệ thống tài liệu <strong>từ lớp 1 đến 12</strong></p>
                <ul style='color: #555; margin-left: 1.2rem;'>
                    <li>Kiến thức được lấy từ sách giáo khoa và các nguồn uy tín</li>
                    <li>Giao diện thân thiện, dễ sử dụng</li>
                    <li>Phân loại theo lớp học</li>
                    <li>Dự án học tập của học sinh</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #e3f2fd; padding: 1.5rem; border-radius: 10px; 
                        border-left: 5px solid #2196F3; margin-bottom: 1rem;'>
                <h3 style='color: #1976D2; margin-top: 0;'>📚 Study Materials</h3>
                <p style='color: #333; margin-bottom: 0.5rem;'>Resources for <strong>Grade 1-12</strong></p>
                <ul style='color: #555; margin-left: 1.2rem;'>
                    <li>Knowledge extracted from textbooks and reliable sources</li>
                    <li>User-friendly interface</li>
                    <li>Organized by grade level</li>
                    <li>Student learning project</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        if st.session_state.language == 'vi':
            st.markdown("""
            <div style='background-color: #f3e5f5; padding: 1.5rem; border-radius: 10px; 
                        border-left: 5px solid #9C27B0; margin-bottom: 1rem;'>
                <h3 style='color: #7B1FA2; margin-top: 0;'>� AI Chatbot</h3>
                <p style='color: #333; margin-bottom: 0.5rem;'>Trợ lý học tập thông minh</p>
                <ul style='color: #555; margin-left: 1.2rem;'>
                    <li>Tích hợp Google Gemini AI</li>
                    <li>Trả lời câu hỏi học tập</li>
                    <li>Hỗ trợ tiếng Việt và tiếng Anh</li>
                    <li>Miễn phí sử dụng</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #f3e5f5; padding: 1.5rem; border-radius: 10px; 
                        border-left: 5px solid #9C27B0; margin-bottom: 1rem;'>
                <h3 style='color: #7B1FA2; margin-top: 0;'>� AI Chatbot</h3>
                <p style='color: #333; margin-bottom: 0.5rem;'>Smart learning assistant</p>
                <ul style='color: #555; margin-left: 1.2rem;'>
                    <li>Powered by Google Gemini AI</li>
                    <li>Answer study questions</li>
                    <li>Vietnamese & English support</li>
                    <li>Free to use</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.session_state.language == 'vi':
            st.markdown("""
            <div style='background-color: #fff3e0; padding: 1.5rem; border-radius: 10px; 
                        border-left: 5px solid #FF9800; margin-bottom: 1rem;'>
                <h3 style='color: #F57C00; margin-top: 0;'>🌐 Đa ngôn ngữ</h3>
                <p style='color: #333; margin-bottom: 0.5rem;'>Hỗ trợ <strong>2 ngôn ngữ</strong></p>
                <ul style='color: #555; margin-left: 1.2rem;'>
                    <li>Tiếng Việt đầy đủ</li>
                    <li>Tiếng Anh hoàn chỉnh</li>
                    <li>Chuyển đổi dễ dàng</li>
                    <li>Giao diện thân thiện</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #fff3e0; padding: 1.5rem; border-radius: 10px; 
                        border-left: 5px solid #FF9800; margin-bottom: 1rem;'>
                <h3 style='color: #F57C00; margin-top: 0;'>🌐 Multi-language</h3>
                <p style='color: #333; margin-bottom: 0.5rem;'>Support <strong>2 languages</strong></p>
                <ul style='color: #555; margin-left: 1.2rem;'>
                    <li>Full Vietnamese support</li>
                    <li>Complete English version</li>
                    <li>Easy language switching</li>
                    <li>User-friendly interface</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        if st.session_state.language == 'vi':
            st.markdown("""
            <div style='background-color: #ffebee; padding: 1.5rem; border-radius: 10px; 
                        border-left: 5px solid #F44336; margin-bottom: 1rem;'>
                <h3 style='color: #C62828; margin-top: 0;'>🔐 Hệ thống tài khoản</h3>
                <p style='color: #333; margin-bottom: 0.5rem;'>Quản lý cá nhân hóa</p>
                <ul style='color: #555; margin-left: 1.2rem;'>
                    <li>Đăng ký & đăng nhập</li>
                    <li>Lưu lịch sử chat AI</li>
                    <li>Bảo mật mật khẩu</li>
                    <li>Dữ liệu cá nhân hóa</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #ffebee; padding: 1.5rem; border-radius: 10px; 
                        border-left: 5px solid #F44336; margin-bottom: 1rem;'>
                <h3 style='color: #C62828; margin-top: 0;'>🔐 Account System</h3>
                <p style='color: #333; margin-bottom: 0.5rem;'>Personalized management</p>
                <ul style='color: #555; margin-left: 1.2rem;'>
                    <li>Register & Login</li>
                    <li>Save AI chat history</li>
                    <li>Password security</li>
                    <li>Personalized data</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Call to action
    if st.session_state.language == 'vi':
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 2rem; border-radius: 10px; color: white; text-align: center;'>
            <h3 style='margin-top: 0;'>🚀 Khám phá ngay!</h3>
            <p style='font-size: 1.1rem; margin-bottom: 1rem;'>
                Dự án học sinh được phát triển với ❤️ bởi AB-51 Team
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 2rem; border-radius: 10px; color: white; text-align: center;'>
            <h3 style='margin-top: 0;'>🚀 Explore Now!</h3>
            <p style='font-size: 1.1rem; margin-bottom: 1rem;'>
                Student project developed with ❤️ by AB-51 Team
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; padding: 1rem; color: #666; font-size: 0.9rem;'>
        Made by <strong style='color: #667eea;'>AB-51 Team</strong> 💜
    </div>
    """, unsafe_allow_html=True)

def choose_grade():
    # Initialize session state variables if not exists
    if 'selected_grade' not in st.session_state:
        st.session_state.selected_grade = None
    if 'selected_subject' not in st.session_state:
        st.session_state.selected_subject = None
    
    # Nếu đã chọn subject, hiển thị nội dung subject
    if st.session_state.selected_subject is not None:
        show_subject_content()
        return
    
    # Nếu đã chọn grade, hiển thị danh sách môn học
    if st.session_state.selected_grade is not None:
        grade = st.session_state.selected_grade
        
        # Header
        st.markdown(f"## 📚 {get_text('solutions')} {grade}")
        
        if st.button(f"← {get_text('back')}"):
            st.session_state.selected_grade = None
            st.rerun()
        
        st.divider()
        
        # Banner mô tả
        if st.session_state.language == 'vi':
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
                <p style='font-size: 1.1rem; margin: 0; text-align: center;'>
                    Chọn môn học để xem tài liệu và bài giảng 📖
                </p>
                <p style='font-size: 0.95rem; margin-top: 1rem; text-align: center; opacity: 0.9;'>
                    <strong>Lưu ý:</strong> Website đang trong quá trình phát triển, hiện tại chỉ có nội dung Toán 10 - Bài 1 của bộ sách Cánh diều là có sẵn. Cảm ơn các bạn đã ủng hộ OZA!
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
                <p style='font-size: 1.1rem; margin: 0; text-align: center;'>
                    Choose a subject to view materials and lessons 📖
                </p>
                <p style='font-size: 0.95rem; margin-top: 1rem; text-align: center; opacity: 0.9;'>
                    <strong>Note:</strong> The website is under development, currently only the content for Math 10 - Lesson 1 of the Canh Dieu textbook is available. Thank you for supporting OZA!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Danh sách môn học theo nhóm
        if st.session_state.language == 'vi':
            # Nhóm Khoa học Tự nhiên
            st.markdown("""
            <div style='background-color: #e3f2fd; padding: 1rem; border-radius: 10px; 
                        border-left: 5px solid #2196F3; margin-bottom: 1rem;'>
                <h3 style='color: #1976D2; margin: 0;'>🔬 Khoa học Tự nhiên</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📐 Toán học", key="math"):
                    st.session_state.selected_subject = "math"
                    st.rerun()
                if st.button("⚗️ Hóa học", key="chemistry"):
                    st.info("Nội dung môn Hóa đang được phát triển...")
            with col2:
                if st.button("⚛️ Vật lý", key="physics"):
                    st.info("Nội dung môn Lý đang được phát triển...")
                if st.button("🧬 Sinh học", key="biology"):
                    st.info("Nội dung môn Sinh đang được phát triển...")
        
        else:
            # English version - Natural Sciences
            st.markdown("""
            <div style='background-color: #e3f2fd; padding: 1rem; border-radius: 10px; 
                        border-left: 5px solid #2196F3; margin-bottom: 1rem;'>
                <h3 style='color: #1976D2; margin: 0;'>🔬 Natural Sciences</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📐 Mathematics", key="math"):
                    st.session_state.selected_subject = "math"
                    st.rerun()
                if st.button("⚗️ Chemistry", key="chemistry"):
                    st.info("Chemistry content is under development...")
            with col2:
                if st.button("⚛️ Physics", key="physics"):
                    st.info("Physics content is under development...")
                if st.button("🧬 Biology", key="biology"):
                    st.info("Biology content is under development...")
        
        # Footer
        st.divider()
        st.markdown("""
        <div style='text-align: center; padding: 1rem; color: #666; font-size: 0.9rem;'>
            Made by <strong style='color: #667eea;'>AB-51 Team</strong> 💜
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Dialog thông báo đang phát triển
    @st.dialog("🚧 Đang phát triển" if st.session_state.language == 'vi' else "🚧 Under Development")
    def show_dev_notice():
        if st.session_state.language == 'vi':
            st.warning("⚠️ Website đang trong thời gian phát triển và phần kiến thức này sẽ được thêm vào trong thời gian sắp tới. Cảm ơn bạn đã ủng hộ OZA!.")
            st.info("💡 Hiện tại chỉ có nội dung **Lớp 10** là có sẵn.")
        else:
            st.warning("⚠️ The website is under development and this knowledge section will be added to this page soon. Thank you for supporting OZA!.")
            st.info("💡 Currently only **Grade 10** content is available.") 
        
        if st.button("OK", type="primary", use_container_width=True):
            st.session_state.show_dev_notice = False
            st.rerun()
    
    # Hiển thị dialog nếu cần
    if st.session_state.show_dev_notice:
        show_dev_notice()
    
    # Banner header
    st.markdown(f"## 📚 {get_text('choose_grade')}")
    
    if st.session_state.language == 'vi':
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
            <p style='font-size: 1.1rem; margin: 0; text-align: center;'>
                Chọn lớp học để khám phá kiến thức và bài giảng phong phú 🎓
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
            <p style='font-size: 1.1rem; margin: 0; text-align: center;'>
                Choose your grade to explore rich knowledge and lessons 🎓
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Cấp THPT với container đẹp
    st.markdown("""
    <div style='background-color: #fff3e0; padding: 1rem; border-radius: 10px; 
                border-left: 5px solid #FF9800; margin-bottom: 1rem;'>
        <h3 style='color: #F57C00; margin: 0;'>📚 """ + get_text('high_school') + """</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"🎯 {get_text('grade')} 12 - Ôn thi THPT Quốc Gia" if st.session_state.language == 'vi' else f"🎯 {get_text('grade')} 12 - National Exam Prep", 
                type="primary", key="grade_12"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    if st.button(f"🎯 {get_text('grade')} 11 - Nền tảng quan trọng" if st.session_state.language == 'vi' else f"🎯 {get_text('grade')} 11 - Important Foundation", 
                type="primary", key="grade_11"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    if st.button(f"🎯 {get_text('grade')} 10 - Khởi đầu THPT" if st.session_state.language == 'vi' else f"🎯 {get_text('grade')} 10 - High School Start", 
                type="primary", key="grade_10"):
        st.session_state.selected_grade = 10
        st.rerun()
    
    st.write("")
    
    # Cấp THCS với container đẹp
    st.markdown("""
    <div style='background-color: #e3f2fd; padding: 1rem; border-radius: 10px; 
                border-left: 5px solid #2196F3; margin-bottom: 1rem;'>
        <h3 style='color: #1976D2; margin: 0;'>📖 """ + get_text('middle_school') + """</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"📘 {get_text('grade')} 9 - Chuẩn bị vào 10" if st.session_state.language == 'vi' else f"📘 {get_text('grade')} 9 - Grade 10 Prep", 
                key="grade_9"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    if st.button(f"📘 {get_text('grade')} 8 - Kiến thức nâng cao" if st.session_state.language == 'vi' else f"📘 {get_text('grade')} 8 - Advanced Knowledge", 
                key="grade_8"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    if st.button(f"📘 {get_text('grade')} 7 - Phát triển tư duy" if st.session_state.language == 'vi' else f"📘 {get_text('grade')} 7 - Critical Thinking", 
                key="grade_7"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    if st.button(f"📘 {get_text('grade')} 6 - Khởi đầu THCS" if st.session_state.language == 'vi' else f"📘 {get_text('grade')} 6 - Middle School Start", 
                key="grade_6"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    st.write("")
    
    # Cấp Tiểu học với container đẹp
    st.markdown("""
    <div style='background-color: #f3e5f5; padding: 1rem; border-radius: 10px; 
                border-left: 5px solid #9C27B0; margin-bottom: 1rem;'>
        <h3 style='color: #7B1FA2; margin: 0;'>📝 """ + get_text('elementary') + """</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"✏️ {get_text('grade')} 5 - Chuẩn bị lên cấp 2" if st.session_state.language == 'vi' else f"✏️ {get_text('grade')} 5 - Next Level Prep", 
                key="grade_5"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    if st.button(f"✏️ {get_text('grade')} 4 - Rèn luyện kỹ năng" if st.session_state.language == 'vi' else f"✏️ {get_text('grade')} 4 - Skill Building", 
                key="grade_4"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    if st.button(f"✏️ {get_text('grade')} 3 - Học vui chơi" if st.session_state.language == 'vi' else f"✏️ {get_text('grade')} 3 - Fun Learning", 
                key="grade_3"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    if st.button(f"✏️ {get_text('grade')} 2 - Nền tảng vững chắc" if st.session_state.language == 'vi' else f"✏️ {get_text('grade')} 2 - Strong Foundation", 
                key="grade_2"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    if st.button(f"✏️ {get_text('grade')} 1 - Khởi đầu hành trình" if st.session_state.language == 'vi' else f"✏️ {get_text('grade')} 1 - Journey Begins", 
                key="grade_1"):
        st.session_state.show_dev_notice = True
        st.rerun()
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 1rem; color: #666; font-size: 0.9rem;'>
        Made by <strong style='color: #667eea;'>AB-51 Team</strong> 💜
    </div>
    """, unsafe_allow_html=True)

def show_subject_content():
    """Hiển thị nội dung chi tiết của môn học"""
    subject = st.session_state.selected_subject
    grade = st.session_state.selected_grade
    
    # Kiểm tra nếu đang ở quiz mode
    if st.session_state.quiz_mode == 'practice':
        render_practice_quiz('math10_lesson1')
        return
    elif st.session_state.quiz_mode == 'test':
        render_test_quiz('math10_lesson1')
        return
    
    # Header
    subject_names = {
        'math': {'vi': '📐 Toán học', 'en': '📐 Mathematics'}
    }
    
    subject_name = subject_names.get(subject, {'vi': 'Môn học', 'en': 'Subject'})[st.session_state.language]
    st.markdown(f"## {subject_name} - Lớp {grade}")
    
    if st.button(f"← {get_text('back')}"):
        st.session_state.selected_subject = None
        st.rerun()
    
    st.divider()
    
    # Thêm AI Helper với text selection
    st.markdown("""
    <style>
    .ai-helper-container {
        position: sticky;
        top: 80px;
        z-index: 999;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .ai-helper-title {
        color: white;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="ai-helper-container">', unsafe_allow_html=True)
        if st.session_state.language == 'vi':
            st.markdown('<div class="ai-helper-title">💡 Trợ lý AI học tập</div>', unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            with col1:
                highlighted_input = st.text_area(
                    "Bôi đen và copy text muốn hỏi, sau đó paste vào đây:",
                    placeholder="Ví dụ: Mệnh đề toán học là gì?",
                    height=80,
                    key="highlight_input"
                )
            with col2:
                st.write("")  # Spacing
                if st.button("🚀 Hỏi AI", type="primary", use_container_width=True):
                    if highlighted_input:
                        st.session_state.highlighted_text = highlighted_input
                        ai_helper_dialog()
                    else:
                        st.error("Vui lòng nhập nội dung!")
        else:
            st.markdown('<div class="ai-helper-title">💡 AI Learning Assistant</div>', unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            with col1:
                highlighted_input = st.text_area(
                    "Highlight and copy text to ask, then paste here:",
                    placeholder="Example: What is a mathematical proposition?",
                    height=80,
                    key="highlight_input"
                )
            with col2:
                st.write("")  # Spacing
                if st.button("🚀 Ask AI", type="primary", use_container_width=True):
                    if highlighted_input:
                        st.session_state.highlighted_text = highlighted_input
                        ai_helper_dialog()
                    else:
                        st.error("Please enter content!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Nội dung môn Toán lớp 10
    if subject == 'math' and grade == 10:
        if st.session_state.language == 'vi':
            st.markdown("### 📖 Chương 1: Mệnh đề toán học. Tập hợp")
            
            with st.expander("📚 **Bài 1: Mệnh đề toán học**", expanded=False):
                st.markdown("""
                #### I. MỆNH ĐỀ TOÁN HỌC
                
                **Định nghĩa:** Mệnh đề toán học là một phát biểu, một khẳng định (có thể đúng hoặc sai) về một sự kiện trong toán học.
                
                **Lưu ý:** Mỗi mệnh đề toán học phải **đúng** hoặc **sai**, không thể vừa đúng vừa sai.
                
                **Ví dụ:**
                - "$5 > 3$" là mệnh đề **đúng**
                - "Số 6 chia hết cho 4" là mệnh đề **sai**
                
                ---
                
                #### II. MỆNH ĐỀ CHỨA BIẾN
                
                **Định nghĩa:** Mệnh đề chứa biến là phát biểu chưa khẳng định được tính đúng sai của câu. Nhưng với mỗi giá trị cụ thể của biến, câu này cho ta một mệnh đề toán học mà ta có thể khẳng định được tính đúng sai của mệnh đề đó.
                
                **Ví dụ:**
                - "$n$ chia hết cho 3" với $n$ là số tự nhiên
                - $P(n)$: "$2n$ lớn hơn 10", là một mệnh đề chứa biến
                
                ---
                
                #### III. PHỦ ĐỊNH CỦA MỘT MỆNH ĐỀ
                
                **Định nghĩa:** Mệnh đề phủ định của mệnh đề $P$, là mệnh đề "Không phải $P$" và kí hiệu là $\\overline{P}$.
                
                **Cách lập:** Ta thêm (hoặc bớt) "không phải" vào vị trí hợp lí để lập mệnh đề phủ định.
                
                **Tính chất:**
                - Mệnh đề $\\overline{P}$ **đúng** khi $P$ **sai**
                - Mệnh đề $\\overline{P}$ **sai** khi $P$ **đúng**
                
                ---
                
                #### IV. MỆNH ĐỀ KÉO THEO
                
                **Định nghĩa:** Cho hai mệnh đề $P$ và $Q$. Mệnh đề "Nếu $P$ thì $Q$" được gọi là mệnh đề kéo theo và kí hiệu là $P \\Rightarrow Q$.
                
                **Tính đúng sai:**
                - Mệnh đề $P \\Rightarrow Q$ **sai** khi $P$ đúng, $Q$ sai
                - Mệnh đề $P \\Rightarrow Q$ **đúng** trong các trường hợp còn lại
                
                **Các cách phát biểu khác:**
                - "$P$ kéo theo $Q$"
                - "$P$ suy ra $Q$"
                - "Vì $P$ nên $Q$"
                
                **Nhận xét:** Với các định lí toán học dạng $P \\Rightarrow Q$:
                - $P$ là giả thiết, $Q$ là kết luận của định lí
                - $P$ là điều kiện **đủ** để có $Q$
                - $Q$ là điều kiện **cần** để có $P$
                
                ---
                
                #### V. MỆNH ĐỀ ĐẢO. HAI MỆNH ĐỀ TƯƠNG ĐƯƠNG
                
                **Mệnh đề đảo:** Mệnh đề $Q \\Rightarrow P$ được gọi là mệnh đề đảo của mệnh đề $P \\Rightarrow Q$.
                
                **Mệnh đề tương đương:** Nếu cả hai mệnh đề $P \\Rightarrow Q$ và $Q \\Rightarrow P$ đều đúng thì $P \\Leftrightarrow Q$ (hai mệnh đề tương đương).
                
                ---
                
                #### VI. KÍ HIỆU $\\forall$ VÀ $\\exists$
                
                Cho mệnh đề "$P(x)$, $x \\in X$":
                
                **Phủ định của mệnh đề với kí hiệu $\\forall$ (với mọi):**
                - Phủ định của mệnh đề "$\\forall x \\in X, P(x)$" là mệnh đề "$\\exists x \\in X, \\overline{P(x)}$"
                - Đọc: "Với mọi $x$ thuộc $X$, $P(x)$ đúng" có phủ định là "Tồn tại $x$ thuộc $X$, $P(x)$ sai"
                
                **Phủ định của mệnh đề với kí hiệu $\\exists$ (tồn tại):**
                - Phủ định của mệnh đề "$\\exists x \\in X, P(x)$" là mệnh đề "$\\forall x \\in X, \\overline{P(x)}$"
                - Đọc: "Tồn tại $x$ thuộc $X$, $P(x)$ đúng" có phủ định là "Với mọi $x$ thuộc $X$, $P(x)$ sai"
                
                ---
                
                ### 💡 Tóm tắt
                
                | Khái niệm | Kí hiệu | Ý nghĩa |
                |-----------|---------|---------|
                | Phủ định | $\\overline{P}$ | Không phải $P$ |
                | Kéo theo | $P \\Rightarrow Q$ | Nếu $P$ thì $Q$ |
                | Tương đương | $P \\Leftrightarrow Q$ | $P$ khi và chỉ khi $Q$ |
                | Với mọi | $\\forall x \\in X$ | For all $x$ in $X$ |
                | Tồn tại | $\\exists x \\in X$ | There exists $x$ in $X$ |
                
                ---
                
                ### 📝 Ghi chú
                
                Nội dung được tham khảo từ SGK Toán 10 Cánh diều và [Loigiaihay.com](https://loigiaihay.com/ly-thuyet-menh-de-toan-hoc-sgk-toan-10-canh-dieu-a110419.html)
                """)
                
                # Nút bài tập và kiểm tra cho Bài 1
                st.markdown("---")
                st.markdown("### 🎯 " + ("Củng cố kiến thức" if st.session_state.language == 'vi' else "Reinforce Knowledge"))
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📝 " + ("Bài tập thực hành" if st.session_state.language == 'vi' else "Practice Exercises"), key="practice_lesson1", use_container_width=True, type="secondary"):
                        st.session_state.quiz_mode = 'practice'
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                with col2:
                    if st.button("📋 " + ("Bài kiểm tra" if st.session_state.language == 'vi' else "Test"), key="test_lesson1", use_container_width=True, type="primary"):
                        st.session_state.quiz_mode = 'test'
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_started = False
                        st.rerun()
            
            st.divider()
            
            with st.expander("📚 **Bài 2: Tập hợp. Các phép toán trên tập hợp**", expanded=False):
                st.markdown("""
                #### I. TẬP HỢP
                
                **Định nghĩa:** Tập hợp là một khái niệm cơ bản trong toán học, biểu thị một sự tập trung các đối tượng xác định và phân biệt với nhau.
                
                **Lưu ý:**
                - Tập hợp không chứa phần tử nào được gọi là **tập hợp rỗng** (viết là $\\emptyset$)
                - Một tập hợp có thể không có phần tử nào, có một phần tử, có nhiều phần tử, hoặc có vô số phần tử
                
                ---
                
                #### II. TẬP CON VÀ TẬP HỢP BẰNG NHAU
                
                **1. Tập con**
                
                $A \\subset B \\Leftrightarrow (\\forall x, x \\in A \\Rightarrow x \\in B)$
                
                **Ký hiệu:**
                - Khi $A \\subset B$, ta cũng viết $B \\supset A$
                - Nếu $A$ không phải là tập con của $B$, ta viết $A \\not\\subset B$
                
                **Nhận xét:**
                - $A \\subset A$ với mọi tập hợp $A$
                - Nếu $A \\subset B$ và $B \\subset C$ thì $A \\subset C$
                
                **2. Tập hợp bằng nhau**
                
                $A = B \\Leftrightarrow \\begin{cases} A \\subset B \\\\ B \\subset A \\end{cases}$
                
                ---
                
                #### III. GIAO CỦA HAI TẬP HỢP
                
                **Định nghĩa:** $A \\cap B = \\{x | x \\in A$ và $x \\in B\\}$
                
                Giao của hai tập hợp $A$ và $B$ là tập hợp gồm các phần tử vừa thuộc $A$ vừa thuộc $B$.
                
                ---
                
                #### IV. HỢP CỦA HAI TẬP HỢP
                
                **Định nghĩa:** $A \\cup B = \\{x | x \\in A$ hoặc $x \\in B\\}$
                
                Hợp của hai tập hợp $A$ và $B$ là tập hợp gồm các phần tử thuộc $A$ hoặc thuộc $B$.
                
                ---
                
                #### V. PHẦN BÙ. HIỆU CỦA HAI TẬP HỢP
                
                **Hiệu của hai tập hợp:** $A \\setminus B = \\{x | x \\in A$ và $x \\notin B\\}$
                
                Hiệu của $A$ và $B$ là tập hợp gồm các phần tử thuộc $A$ nhưng không thuộc $B$.
                
                **Phần bù:** Nếu $A \\subset B$, kí hiệu: $C_B^A = B \\setminus A$ (Phần bù của $A$ trong $B$)
                
                ---
                
                #### VI. CÁC TẬP HỢP SỐ
                
                **Quan hệ bao hàm:** $\\mathbb{N} \\subset \\mathbb{Z} \\subset \\mathbb{Q} \\subset \\mathbb{R}$
                
                Trong đó:
                - $\\mathbb{N}$: Tập hợp các số tự nhiên
                - $\\mathbb{Z}$: Tập hợp các số nguyên
                - $\\mathbb{Q}$: Tập hợp các số hữu tỷ
                - $\\mathbb{R}$: Tập hợp các số thực
                
                **Các tập con thường dùng:**
                - $\\mathbb{N}^*$: Tập hợp các số tự nhiên khác 0
                - $\\mathbb{Z}^+$: Tập hợp các số nguyên dương
                - $\\mathbb{Z}^-$: Tập hợp các số nguyên âm
                - $\\mathbb{Q}^+$, $\\mathbb{Q}^-$, $\\mathbb{R}^+$, $\\mathbb{R}^-$: Tương tự cho số hữu tỷ và số thực
                
                ---
                
                ### 💡 Tóm tắt
                
                | Khái niệm | Ký hiệu | Ý nghĩa |
                |-----------|---------|---------|
                | Thuộc | $x \\in A$ | $x$ là phần tử của $A$ |
                | Không thuộc | $x \\notin A$ | $x$ không là phần tử của $A$ |
                | Tập con | $A \\subset B$ | Mọi phần tử của $A$ đều thuộc $B$ |
                | Giao | $A \\cap B$ | Phần tử thuộc cả $A$ và $B$ |
                | Hợp | $A \\cup B$ | Phần tử thuộc $A$ hoặc $B$ |
                | Hiệu | $A \\setminus B$ | Phần tử thuộc $A$ nhưng không thuộc $B$ |
                | Tập rỗng | $\\emptyset$ | Tập không có phần tử nào |
                
                ---
                
                ### 📝 Ghi chú
                
                Nội dung được tham khảo từ SGK Toán 10 Cánh diều và [Loigiaihay.com](https://loigiaihay.com/ly-thuyet-tap-hop-cac-phep-toan-tren-tap-hop-sgk-toan-10-canh-dieu-a110530.html)
                """)
            
            st.divider()
            st.info("💡 Các bài tiếp theo đang được cập nhật...")
        
        else:  # English version
            st.markdown("### 📖 Chapter 1: Mathematical Propositions. Sets")
            
            with st.expander("📚 **Lesson 1: Mathematical Propositions**", expanded=False):
                st.markdown("""
                #### I. MATHEMATICAL PROPOSITIONS
                
                **Definition:** A mathematical proposition is a statement or assertion (which can be true or false) about a mathematical fact.
                
                **Note:** Each mathematical proposition must be **true** or **false**, it cannot be both true and false.
                
                **Examples:**
                - "$5 > 3$" is a **true** proposition
                - "The number 6 is divisible by 4" is a **false** proposition
                
                ---
                
                #### II. PROPOSITIONS WITH VARIABLES
                
                **Definition:** A proposition with a variable is a statement whose truth value cannot be determined yet. However, for each specific value of the variable, this statement gives us a mathematical proposition whose truth value can be determined.
                
                **Examples:**
                - "$n$ is divisible by 3" where $n$ is a natural number
                - $P(n)$: "$2n$ is greater than 10", is a proposition with a variable
                
                ---
                
                #### III. NEGATION OF A PROPOSITION
                
                **Definition:** The negation of proposition $P$, is the proposition "Not $P$" and is denoted by $\\overline{P}$.
                
                **How to form:** We add (or remove) "not" at an appropriate position to form the negation.
                
                **Properties:**
                - Proposition $\\overline{P}$ is **true** when $P$ is **false**
                - Proposition $\\overline{P}$ is **false** when $P$ is **true**
                
                ---
                
                #### IV. IMPLICATION
                
                **Definition:** Given two propositions $P$ and $Q$. The proposition "If $P$ then $Q$" is called an implication and is denoted by $P \\Rightarrow Q$.
                
                **Truth value:**
                - Proposition $P \\Rightarrow Q$ is **false** when $P$ is true and $Q$ is false
                - Proposition $P \\Rightarrow Q$ is **true** in all other cases
                
                **Other ways to state:**
                - "$P$ implies $Q$"
                - "$P$ entails $Q$"
                - "Because $P$, therefore $Q$"
                
                **Remark:** For mathematical theorems in the form $P \\Rightarrow Q$:
                - $P$ is the hypothesis, $Q$ is the conclusion of the theorem
                - $P$ is a **sufficient** condition for $Q$
                - $Q$ is a **necessary** condition for $P$
                
                ---
                
                #### V. CONVERSE PROPOSITION. EQUIVALENT PROPOSITIONS
                
                **Converse proposition:** The proposition $Q \\Rightarrow P$ is called the converse of proposition $P \\Rightarrow Q$.
                
                **Equivalent propositions:** If both propositions $P \\Rightarrow Q$ and $Q \\Rightarrow P$ are true, then $P \\Leftrightarrow Q$ (the two propositions are equivalent).
                
                ---
                
                #### VI. SYMBOLS $\\forall$ AND $\\exists$
                
                Given the proposition "$P(x)$, $x \\in X$":
                
                **Negation of a proposition with symbol $\\forall$ (for all):**
                - The negation of proposition "$\\forall x \\in X, P(x)$" is the proposition "$\\exists x \\in X, \\overline{P(x)}$"
                - Reading: "For all $x$ in $X$, $P(x)$ is true" has negation "There exists $x$ in $X$, $P(x)$ is false"
                
                **Negation of a proposition with symbol $\\exists$ (there exists):**
                - The negation of proposition "$\\exists x \\in X, P(x)$" is the proposition "$\\forall x \\in X, \\overline{P(x)}$"
                - Reading: "There exists $x$ in $X$, $P(x)$ is true" has negation "For all $x$ in $X$, $P(x)$ is false"
                
                ---
                
                ### 💡 Summary
                
                | Concept | Symbol | Meaning |
                |---------|--------|---------|
                | Negation | $\\overline{P}$ | Not $P$ |
                | Implication | $P \\Rightarrow Q$ | If $P$ then $Q$ |
                | Equivalence | $P \\Leftrightarrow Q$ | $P$ if and only if $Q$ |
                | For all | $\\forall x \\in X$ | For all $x$ in $X$ |
                | There exists | $\\exists x \\in X$ | There exists $x$ in $X$ |
                
                ---
                
                ### 📝 Note
                
                Content is referenced from Math 10 Textbook (Canh Dieu) and [Loigiaihay.com](https://loigiaihay.com/ly-thuyet-menh-de-toan-hoc-sgk-toan-10-canh-dieu-a110419.html)
                """)
                
                # Quiz buttons for Lesson 1 (English)
                st.markdown("---")
                st.markdown("### 🎯 Consolidate Knowledge")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📝 Practice Exercises", key="practice_en_lesson1", use_container_width=True):
                        st.session_state.quiz_mode = 'practice'
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_answers = {}
                        st.rerun()
                with col2:
                    if st.button("📋 Test", key="test_en_lesson1", use_container_width=True):
                        st.session_state.quiz_mode = 'test'
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_started = False
                        st.session_state.cheating_count = 0
                        st.rerun()
            
            st.divider()
            
            with st.expander("📚 **Lesson 2: Sets. Operations on Sets**", expanded=False):
                st.markdown("""
                #### I. SETS
                
                **Definition:** A set is a fundamental concept in mathematics, representing a collection of distinct and well-defined objects.
                
                **Notes:**
                - A set containing no elements is called an **empty set** (denoted as $\\emptyset$)
                - A set can have no elements, one element, many elements, or infinitely many elements
                
                ---
                
                #### II. SUBSETS AND SET EQUALITY
                
                **1. Subset**
                
                $A \\subset B \\Leftrightarrow (\\forall x, x \\in A \\Rightarrow x \\in B)$
                
                **Notation:**
                - When $A \\subset B$, we also write $B \\supset A$
                - If $A$ is not a subset of $B$, we write $A \\not\\subset B$
                
                **Remarks:**
                - $A \\subset A$ for all sets $A$
                - If $A \\subset B$ and $B \\subset C$ then $A \\subset C$
                
                **2. Set equality**
                
                $A = B \\Leftrightarrow \\begin{cases} A \\subset B \\\\ B \\subset A \\end{cases}$
                
                ---
                
                #### III. INTERSECTION OF TWO SETS
                
                **Definition:** $A \\cap B = \\{x | x \\in A$ and $x \\in B\\}$
                
                The intersection of two sets $A$ and $B$ is the set of elements that belong to both $A$ and $B$.
                
                ---
                
                #### IV. UNION OF TWO SETS
                
                **Definition:** $A \\cup B = \\{x | x \\in A$ or $x \\in B\\}$
                
                The union of two sets $A$ and $B$ is the set of elements that belong to $A$ or $B$.
                
                ---
                
                #### V. COMPLEMENT. DIFFERENCE OF TWO SETS
                
                **Difference of two sets:** $A \\setminus B = \\{x | x \\in A$ and $x \\notin B\\}$
                
                The difference of $A$ and $B$ is the set of elements that belong to $A$ but not to $B$.
                
                **Complement:** If $A \\subset B$, notation: $C_B^A = B \\setminus A$ (Complement of $A$ in $B$)
                
                ---
                
                #### VI. NUMBER SETS
                
                **Inclusion relation:** $\\mathbb{N} \\subset \\mathbb{Z} \\subset \\mathbb{Q} \\subset \\mathbb{R}$
                
                Where:
                - $\\mathbb{N}$: Set of natural numbers
                - $\\mathbb{Z}$: Set of integers
                - $\\mathbb{Q}$: Set of rational numbers
                - $\\mathbb{R}$: Set of real numbers
                
                **Commonly used subsets:**
                - $\\mathbb{N}^*$: Set of positive natural numbers (non-zero)
                - $\\mathbb{Z}^+$: Set of positive integers
                - $\\mathbb{Z}^-$: Set of negative integers
                - $\\mathbb{Q}^+$, $\\mathbb{Q}^-$, $\\mathbb{R}^+$, $\\mathbb{R}^-$: Similarly for rational and real numbers
                
                ---
                
                ### 💡 Summary
                
                | Concept | Symbol | Meaning |
                |---------|--------|---------|
                | Element of | $x \\in A$ | $x$ is an element of $A$ |
                | Not element of | $x \\notin A$ | $x$ is not an element of $A$ |
                | Subset | $A \\subset B$ | Every element of $A$ belongs to $B$ |
                | Intersection | $A \\cap B$ | Elements in both $A$ and $B$ |
                | Union | $A \\cup B$ | Elements in $A$ or $B$ |
                | Difference | $A \\setminus B$ | Elements in $A$ but not in $B$ |
                | Empty set | $\\emptyset$ | Set with no elements |
                
                ---
                
                ### 📝 Note
                
                Content is referenced from Math 10 Textbook (Canh Dieu) and [Loigiaihay.com](https://loigiaihay.com/ly-thuyet-tap-hop-cac-phep-toan-tren-tap-hop-sgk-toan-10-canh-dieu-a110530.html)
                """)
                
                # Quiz buttons for Lesson 2 (English) - Coming soon
                st.markdown("---")
                st.markdown("### 🎯 Consolidate Knowledge")
                st.info("📝 Practice Exercises and 📋 Test for this lesson are coming soon...")
            
            st.divider()
            st.info("💡 More lessons are being updated...")
    
    else:
        if st.session_state.language == 'vi':
            st.warning("Nội dung đang được phát triển...")
        else:
            st.warning("Content is under development...")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; padding: 1rem; color: #666; font-size: 0.9rem;'>
        Made by <strong style='color: #667eea;'>AB-51 Team</strong> 💜
    </div>
    """, unsafe_allow_html=True)

def chatbot():
    """Trang AI Chatbot - Trợ lý học tập với OpenAI API thật"""
    # Reset grade/subject selection khi vào chatbot
    if 'selected_grade' in st.session_state:
        st.session_state.selected_grade = None
    if 'selected_subject' in st.session_state:
        st.session_state.selected_subject = None
    
    st.markdown(f"## 🤖 {get_text('chatbot')}")
    
    # Lấy username hiện tại
    current_user = st.session_state.username if st.session_state.logged_in else "guest"
    
    # Khởi tạo chat history từ file nếu chưa có trong session state
    if "messages" not in st.session_state:
        # Load từ file nếu có
        saved_messages = chatbot_config.load_chat_history(current_user)
        if saved_messages:
            st.session_state.messages = saved_messages
        else:
            st.session_state.messages = [
                {"role": "assistant", "content": get_text('chatbot_welcome')}
            ]
    
    # Sidebar với thống kê và tính năng
    with st.sidebar:
        st.divider()
        st.markdown("### 📊 Thống kê Chat" if st.session_state.language == 'vi' else "### 📊 Chat Statistics")
        
        stats = chatbot_config.get_chat_statistics(current_user)
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Câu hỏi 💬" if st.session_state.language == 'vi' else "Questions 💬",
                value=stats['user_messages']
            )
        with col2:
            st.metric(
                label="Trả lời 🤖" if st.session_state.language == 'vi' else "Answers 🤖",
                value=stats['assistant_messages']
            )
        
        st.divider()
        
        # Nút lưu lịch sử
        if st.button("💾 Lưu lịch sử" if st.session_state.language == 'vi' else "💾 Save History", 
                    use_container_width=True, type="secondary"):
            if chatbot_config.save_chat_history(current_user, st.session_state.messages):
                st.success("✅ Đã lưu!" if st.session_state.language == 'vi' else "✅ Saved!")
            else:
                st.error("❌ Lỗi lưu" if st.session_state.language == 'vi' else "❌ Save failed")
        
        # Nút xóa lịch sử
        if st.button("🗑️ Xóa lịch sử" if st.session_state.language == 'vi' else "🗑️ Clear History", 
                    use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": get_text('chatbot_welcome')}
            ]
            chatbot_config.save_chat_history(current_user, st.session_state.messages)
            st.rerun()
    
    # Hiển thị chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input(get_text('chatbot_placeholder')):
        # Thêm user message vào chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Gọi OpenAI API để lấy response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Đang suy nghĩ..." if st.session_state.language == 'vi' else "🤔 Thinking..."):
                response = chatbot_config.get_ai_response(
                    st.session_state.messages,
                    st.session_state.language
                )
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Auto-save sau mỗi câu hỏi
        chatbot_config.save_chat_history(current_user, st.session_state.messages)
    
    # Phần câu hỏi gợi ý ở cuối trang - chỉ hiện khi chưa có tin nhắn từ user
    # Kiểm tra xem có tin nhắn nào từ user không (loại trừ tin nhắn welcome đầu tiên)
    has_user_messages = any(msg['role'] == 'user' for msg in st.session_state.messages)
    
    if not has_user_messages:
        st.divider()
        
        if st.session_state.language == 'vi':
            st.markdown("### 💡 Câu hỏi gợi ý")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📐 Giải phương trình bậc 2", use_container_width=True):
                    st.session_state.suggested_question = "Hướng dẫn cách giải phương trình bậc 2 chi tiết"
                    st.rerun()
            
            with col2:
                if st.button("📝 Cách viết bài văn nghị luận", use_container_width=True):
                    st.session_state.suggested_question = "Hướng dẫn cách viết bài văn nghị luận văn học"
                    st.rerun()
            
            with col3:
                if st.button("🧪 Bảng tuần hoàn hóa học", use_container_width=True):
                    st.session_state.suggested_question = "Giải thích bảng tuần hoàn các nguyên tố hóa học"
                    st.rerun()
        else:
            st.markdown("### 💡 Suggested Questions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📐 Solve quadratic equations", use_container_width=True):
                    st.session_state.suggested_question = "Guide me how to solve quadratic equations"
                    st.rerun()
            
            with col2:
                if st.button("📝 How to write essays", use_container_width=True):
                    st.session_state.suggested_question = "Guide me how to write argumentative essays"
                    st.rerun()
            
            with col3:
                if st.button("🧪 Periodic table", use_container_width=True):
                    st.session_state.suggested_question = "Explain the periodic table of elements"
                    st.rerun()
    
    # Xử lý suggested question
    if hasattr(st.session_state, 'suggested_question'):
        question = st.session_state.suggested_question
        del st.session_state.suggested_question
        
        # Thêm vào messages
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Get AI response
        response = chatbot_config.get_ai_response(
            st.session_state.messages,
            st.session_state.language
        )
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Save and rerun
        chatbot_config.save_chat_history(current_user, st.session_state.messages)
        st.rerun()

def feedback():
    """Trang Feedback - Thu thập ý kiến đóng góp từ người dùng"""
    # Reset grade/subject selection khi vào feedback
    if 'selected_grade' in st.session_state:
        st.session_state.selected_grade = None
    if 'selected_subject' in st.session_state:
        st.session_state.selected_subject = None
    
    st.markdown(f"## 💭 {get_text('nav_feedback')}")
    
    if st.session_state.language == 'vi':
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
            <h3 style='margin: 0; text-align: center;'>📝 Ý kiến của bạn rất quan trọng!</h3>
            <p style='font-size: 0.95rem; margin-top: 1rem; text-align: center; opacity: 0.9;'>
                Hãy chia sẻ trải nghiệm, góp ý hoặc báo lỗi để giúp OZA ngày càng tốt hơn
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Form feedback
        with st.form("feedback_form", clear_on_submit=True):
            st.markdown("### 📋 Biểu mẫu góp ý")
            
            # Thông tin người dùng
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("👤 Tên của bạn", placeholder="Nguyễn Văn A")
            with col2:
                email = st.text_input("📧 Email (tùy chọn)", placeholder="example@email.com")
            
            # Loại feedback
            feedback_type = st.selectbox(
                "📌 Loại góp ý",
                ["💡 Đề xuất tính năng mới", "🐛 Báo lỗi", "⭐ Đánh giá chung", "❓ Câu hỏi", "💬 Khác"]
            )
            
            # Đánh giá
            st.markdown("#### ⭐ Đánh giá trải nghiệm của bạn")
            rating = st.slider("", 1, 5, 5, help="1 = Rất tệ, 5 = Rất tốt")
            
            # Nội dung feedback
            feedback_content = st.text_area(
                "✍️ Nội dung chi tiết",
                placeholder="Chia sẻ ý kiến, đề xuất hoặc báo lỗi của bạn...",
                height=200
            )
            
            # Submit button
            submitted = st.form_submit_button("🚀 Gửi góp ý", use_container_width=True, type="primary")
            
            if submitted:
                if not name or not feedback_content:
                    st.error("⚠️ Vui lòng điền tên và nội dung góp ý!")
                else:
                    # Lưu feedback vào file
                    import datetime
                    import os
                    
                    feedback_data = {
                        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'name': name,
                        'email': email if email else "N/A",
                        'type': feedback_type,
                        'rating': rating,
                        'content': feedback_content,
                        'language': 'vi'
                    }
                    
                    # Tạo thư mục feedbacks nếu chưa có
                    os.makedirs('feedbacks', exist_ok=True)
                    
                    # Lưu vào file
                    filename = f"feedbacks/feedback_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"=== FEEDBACK FROM OZA ===\n")
                        f.write(f"Thời gian: {feedback_data['timestamp']}\n")
                        f.write(f"Tên: {feedback_data['name']}\n")
                        f.write(f"Email: {feedback_data['email']}\n")
                        f.write(f"Loại: {feedback_data['type']}\n")
                        f.write(f"Đánh giá: {feedback_data['rating']}/5 ⭐\n")
                        f.write(f"Ngôn ngữ: {feedback_data['language']}\n")
                        f.write(f"\n--- Nội dung ---\n")
                        f.write(feedback_data['content'])
                        f.write(f"\n==================\n")
                    
                    st.success("✅ Cảm ơn bạn đã góp ý! Chúng tôi sẽ xem xét và cải thiện OZA.")
                    st.balloons()
    
    else:  # English version
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
            <h3 style='margin: 0; text-align: center;'>📝 Your opinion matters!</h3>
            <p style='font-size: 0.95rem; margin-top: 1rem; text-align: center; opacity: 0.9;'>
                Share your experience, suggestions, or report bugs to help OZA improve
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Form feedback
        with st.form("feedback_form", clear_on_submit=True):
            st.markdown("### 📋 Feedback Form")
            
            # User info
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("👤 Your Name", placeholder="John Doe")
            with col2:
                email = st.text_input("📧 Email (optional)", placeholder="example@email.com")
            
            # Feedback type
            feedback_type = st.selectbox(
                "📌 Feedback Type",
                ["💡 Feature Request", "🐛 Bug Report", "⭐ General Review", "❓ Question", "💬 Other"]
            )
            
            # Rating
            st.markdown("#### ⭐ Rate your experience")
            rating = st.slider("", 1, 5, 5, help="1 = Very Bad, 5 = Excellent")
            
            # Feedback content
            feedback_content = st.text_area(
                "✍️ Detailed Content",
                placeholder="Share your thoughts, suggestions, or bug reports...",
                height=200
            )
            
            # Submit button
            submitted = st.form_submit_button("🚀 Submit Feedback", use_container_width=True, type="primary")
            
            if submitted:
                if not name or not feedback_content:
                    st.error("⚠️ Please fill in your name and feedback content!")
                else:
                    # Save feedback to file
                    import datetime
                    import os
                    
                    feedback_data = {
                        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'name': name,
                        'email': email if email else "N/A",
                        'type': feedback_type,
                        'rating': rating,
                        'content': feedback_content,
                        'language': 'en'
                    }
                    
                    # Create feedbacks directory if not exists
                    os.makedirs('feedbacks', exist_ok=True)
                    
                    # Save to file
                    filename = f"feedbacks/feedback_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"=== FEEDBACK FROM OZA ===\n")
                        f.write(f"Timestamp: {feedback_data['timestamp']}\n")
                        f.write(f"Name: {feedback_data['name']}\n")
                        f.write(f"Email: {feedback_data['email']}\n")
                        f.write(f"Type: {feedback_data['type']}\n")
                        f.write(f"Rating: {feedback_data['rating']}/5 ⭐\n")
                        f.write(f"Language: {feedback_data['language']}\n")
                        f.write(f"\n--- Content ---\n")
                        f.write(feedback_data['content'])
                        f.write(f"\n==================\n")
                    
                    st.success("✅ Thank you for your feedback! We will review and improve OZA.")
                    st.balloons()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; padding: 1rem; color: #666; font-size: 0.9rem;'>
        Made by <strong style='color: #667eea;'>AB-51 Team</strong> 💜
    </div>
    """, unsafe_allow_html=True)

def about():
    # Reset grade/subject selection khi vào about
    if 'selected_grade' in st.session_state:
        st.session_state.selected_grade = None
    if 'selected_subject' in st.session_state:
        st.session_state.selected_subject = None
    
    st.markdown(f"## {get_text('about')}")
    if st.session_state.language == 'vi':
        st.markdown("""
        ### Về OZA - OpenZone of AI
        
        **OZA (OpenZone of AI)** là nền tảng mở về Trí tuệ nhân tạo, được phát triển bởi **AB-51 Team**.
        
        ### Sứ mệnh
        
        Chúng tôi cam kết:
        - Mang AI đến gần hơn với mọi người
        - Cung cấp kiến thức và công cụ AI chất lượng
        - Xây dựng cộng đồng AI mở và thân thiện
        - Thúc đẩy đổi mới sáng tạo trong lĩnh vực AI
        
        ### AB-51 Team
        
        Đội ngũ phát triển đam mê công nghệ và AI, luôn nỗ lực tạo ra những sản phẩm hữu ích cho cộng đồng.
        
        ---
        
        **"Mở cửa tri thức AI cho mọi người"**
        """)
    else:
        st.markdown("""
        ### About OZA - OpenZone of AI
        
        **OZA (OpenZone of AI)** is an open platform for Artificial Intelligence, developed by **AB-51 Team**.
        
        ### Mission
        
        We are committed to:
        - Bringing AI closer to everyone
        - Providing quality AI knowledge and tools
        - Building an open and friendly AI community
        - Promoting innovation in the AI field
        
        ### AB-51 Team
        
        A team of tech and AI enthusiasts, always striving to create useful products for the community.
        
        ---
        
        **"Opening AI knowledge for everyone"**
        """)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; padding: 1rem; color: #666; font-size: 0.9rem;'>
        Made by <strong style='color: #667eea;'>AB-51 Team</strong> 💜
    </div>
    """, unsafe_allow_html=True)

# Navigation
pg = st.navigation([
    st.Page(home, title=get_text('nav_home'), icon=":material/home:"),
    st.Page(choose_grade, title=get_text('nav_grades'), icon=":material/school:"),
    st.Page(chatbot, title=get_text('nav_tools'), icon=":material/chat:"),
    st.Page(feedback, title=get_text('nav_feedback'), icon=":material/feedback:"),
    st.Page(about, title=get_text('nav_about'), icon=":material/info:"),
])

pg.run()

# Sidebar - Phần dưới cùng (Language và Auth buttons)
with st.sidebar:
    st.divider()
    
    # Language selector
    st.markdown("**Language**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("VN", use_container_width=True, 
                    type="primary" if st.session_state.language == 'vi' else "secondary"):
            st.session_state.language = 'vi'
            st.rerun()
    with col2:
        if st.button("EN", use_container_width=True,
                    type="primary" if st.session_state.language == 'en' else "secondary"):
            st.session_state.language = 'en'
            st.rerun()
    
    st.divider()
    
    # Auth buttons - sử dụng function từ auth.py
    auth.render_auth_buttons(st.session_state.language)

# Xử lý modal login/register - sử dụng function từ auth.py
auth.handle_auth_modals(st.session_state.language)
