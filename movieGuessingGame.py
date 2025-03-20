import random
import os
from google import genai

# Initiate connection to Gemini
googleGeminiKey = os.getenv("GOOGLE_GEMINI_KEY")
client = genai.Client(api_key=googleGeminiKey)

# Movie List
movies = [
    "The Shawshank Redemption", "The Godfather", "The Dark Knight", "Pulp Fiction", "The Lord of the Rings: The Return of the King",
    "Forrest Gump", "Inception", "Fight Club", "The Matrix", "Goodfellas",
    "The Empire Strikes Back", "Interstellar", "The Lord of the Rings: The Fellowship of the Ring", "One Flew Over the Cuckoo's Nest", "The Lord of the Rings: The Two Towers",
    "Se7en", "The Silence of the Lambs", "Saving Private Ryan", "The Green Mile", "Star Wars: A New Hope",
    "Parasite", "The Lion King", "Gladiator", "Terminator 2: Judgment Day", "Back to the Future",
    "The Prestige", "The Departed", "Whiplash", "The Usual Suspects", "The Pianist",
    "The Intouchables", "The Good, the Bad and the Ugly", "Schindler's List", "Spirited Away", "Joker",
    "Avengers: Infinity War", "Avengers: Endgame", "Django Unchained", "The Dark Knight Rises", "Inglourious Basterds",
    "1917", "The Wolf of Wall Street", "Shutter Island", "The Grand Budapest Hotel", "Blade Runner 2049",
    "No Country for Old Men", "There Will Be Blood", "Logan", "Mad Max: Fury Road", "The Social Network",
    "The Revenant", "A Beautiful Mind", "Braveheart", "Casino", "The Big Lebowski",
    "The Truman Show", "A Clockwork Orange", "Requiem for a Dream", "Inside Out", "Coco",
    "Up", "Ratatouille", "Toy Story", "WALL-E", "Finding Nemo",
    "The Incredibles", "Howl's Moving Castle", "Princess Mononoke", "Your Name", "Akira",
    "Oldboy", "Train to Busan", "The Thing", "The Shining", "Psycho",
    "Alien", "Aliens", "Jaws", "The Exorcist", "It",
    "The Sixth Sense", "Hereditary", "Get Out", "A Quiet Place", "The Conjuring",
    "John Wick", "John Wick: Chapter 2", "John Wick: Chapter 3 - Parabellum", "The Batman", "Spider-Man: No Way Home",
    "Spider-Man: Into the Spider-Verse", "Guardians of the Galaxy", "Guardians of the Galaxy Vol. 2", "Doctor Strange", "Thor: Ragnarok",
    "Iron Man", "Captain America: The Winter Soldier", "Black Panther", "X-Men: Days of Future Past", "Deadpool",
    "Deadpool 2", "The Suicide Squad", "Zombieland", "The Lego Movie", "The Hunger Games"
]


class GuessingGame:
    def __init__(self, movies):
        self.movieList = movies # Films are explicitly stated in this list. This should be changed later
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
        self.redactedList = [False if self.blurbText[i] == " " else True for i in range(len(self.blurbText))]

        self.done = False
    
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
            self.done = True
        else:
            if random.random() < 0.4: # Only give the user a hint sometimes
                # Generate feedback for user
                prompt = "Generate a message expressing whether or not a user's guess of the movie'" + userGuess + "' is close to the answer of the movie '" + self.movie + "'. Start your response with something like 'So close!' or 'Not at all!', and give a very slight clue. Do not explicitly reference any names or places. Give me the text of this message and nothing else."
                feedbackResponse = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                responseText = feedbackResponse.text
                print(responseText)
            else: # The rest of the time choose one of these stock phrases
                responseText = random.choice(["Not quite...", "That is not correct.", "Nope!"])
                print(responseText)

game = GuessingGame(movies)
while not game.done:
    game.printRedacted()
    game.makeGuess()
    game.updateRedactedList()