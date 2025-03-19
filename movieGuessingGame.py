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
        prompt = "Generate a blurb description of the movie " + self.movie+ ". The description should be about 5 sentences long and should not explicitly say the names of any people or places. Give me the text of this description and nothing else."
        blurbResponse = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        self.blurbText = blurbResponse.text

        # Decide which characters should be redacted and which should not
        # All should be at first
        self.redactedList = [True for i in range(len(self.blurbText))]
    
    def printRedacted(self):
        # Print the blurb with the chosen characters redacted
        redactedString = "".join("-" if redacted else char for char, redacted in zip(self.blurbText, self.redactedList))
        print(redactedString)

    def updateRedactedList(self):
        # Make about 20% of the currently redacted characters unredacted
        for i in range(len(self.redactedList)):
            if self.redactedList[i]:
                if random.random() < 0.2:
                    self.redactedList[i] = False
    
    def makeGuess(self):
        userGuess = input("What movie do you think this is?")
        if userGuess.lower() == self.movie.lower():
            print("Well done! The movie was", self.movie)
            self.redactedList = [False for i in range(len(self.blurbText))]
            self.printRedacted()
        else:
            # Generate feedback for user
            prompt = "Generate a message expressing whether or not a user's guess of the movie'" + userGuess + "' is close to the answer of the movie '" + self.movie + "'. Start your response with something like 'So close!' or 'Not at all!', and give a very slight clue. Do not explicitly reference any names or places. Give me the text of this message and nothing else."
            feedbackResponse = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            responseText = feedbackResponse.text
            print(responseText)

game = GuessingGame()
for i in range(10):
    game.printRedacted()
    game.makeGuess()
    game.updateRedactedList()