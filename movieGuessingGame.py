import random
import os
from google import genai

# Initiate connection to Gemini
googleGeminiKey = os.getenv("GOOGLE_GEMINI_KEY")
client = genai.Client(api_key=googleGeminiKey)

class GuessingGame:
    def __init__(self):
        self.movieList = ["Holes", "Cars", "Toy Story"] # Films are explicitly stated in this list. This should be changed later
        self.movie = random.choice(self.movieList)

        # Generate movie blurb
        prompt = "Generate a blurb description of the movie " + self.movie+ ". The description should be about 5 sentences long. Give me the text of this description and nothing else."
        blurbResponse = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        self.blurbText = blurbResponse.text

        print(self.blurbText)

game = GuessingGame()