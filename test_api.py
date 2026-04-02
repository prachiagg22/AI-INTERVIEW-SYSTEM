from config import GEMINI_API_KEY
import google.generativeai as genai

print("Key starts with:", GEMINI_API_KEY[:10])

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

try:
    response = model.generate_content("Say hello in one word.")
    print("SUCCESS:", response.text)
except Exception as e:
    print("ERROR:", str(e))