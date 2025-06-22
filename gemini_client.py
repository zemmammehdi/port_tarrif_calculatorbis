import google.generativeai as genai

API_KEY = "api key"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")