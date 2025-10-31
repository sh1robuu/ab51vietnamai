import google.generativeai as genai

# Cấu hình API key
GEMINI_API_KEY = "AIzaSyDDtJB5SL3mdn7IKLV_V_mo-4cN-o2pPAA"
genai.configure(api_key=GEMINI_API_KEY)

# List tất cả models có sẵn
print("Available Gemini models:")
print("=" * 50)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"Model: {model.name}")
        print(f"Display name: {model.display_name}")
        print(f"Description: {model.description}")
        print("-" * 50)
