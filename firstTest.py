from google import genai
import os

googleGeminiKey = os.getenv("GOOGLE_GEMINI_KEY")

client = genai.Client(api_key=googleGeminiKey)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Congratulate me on setting up my API key properly"
)

print(response.text)