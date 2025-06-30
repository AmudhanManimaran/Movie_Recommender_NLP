from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from nltk.corpus import wordnet
import nltk

# Download necessary NLTK resources
nltk.download("vader_lexicon")
nltk.download("wordnet")

sia = SentimentIntensityAnalyzer()

# Expand emotion categories dynamically using WordNet
BASE_EMOTION_MAP = {
    "Joy": ["happy", "joyful", "excited", "cheerful", "delight"],
    "Sadness": ["sad", "heartbroken", "miserable", "sorrowful", "depressed"],
    "Fear": ["afraid", "scared", "terrified", "nervous", "anxious"],
    "Anger": ["angry", "furious", "frustrated", "resentful", "annoyed"],
    "Surprise": ["shocked", "amazed", "astonished", "stunned", "startled"],
    "Disgust": ["disgusted", "revolted", "sickened", "appalled", "disturbed"],
    "Anticipation": ["curious", "expectant", "eager", "hopeful", "excited"],
    "Trust": ["trusting", "faithful", "loyal", "reliable", "secure"]
}

# Function to expand emotion words using WordNet synonyms
def expand_emotion_map(emotion_map):
    expanded_map = {}
    for emotion, words in emotion_map.items():
        expanded_words = set(words)  # Use a set to avoid duplicates
        for word in words:
            for syn in wordnet.synsets(word):  # Get synonyms
                for lemma in syn.lemmas():
                    expanded_words.add(lemma.name().replace("_", " "))  # Add synonyms
        expanded_map[emotion] = list(expanded_words)
    return expanded_map

# Generate expanded emotion map
EMOTION_MAP = expand_emotion_map(BASE_EMOTION_MAP)

def detect_emotion(text):
    # Step 1: VADER Sentiment Score
    sentiment_score = sia.polarity_scores(text)["compound"]

    # Step 2: TextBlob for contextual understanding
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Step 3: Keyword Matching with Expanded Emotion Map
    words = text.lower().split()
    detected_emotions = {emotion: sum(word in words for word in keywords) for emotion, keywords in EMOTION_MAP.items()}
    
    # Choose the emotion with the highest match
    detected_mood = max(detected_emotions, key=detected_emotions.get, default="Neutral")

    # Step 4: Combine all analysis with refined conditions
    if polarity > 0.4 and detected_mood in ["Joy", "Trust"]:
        return detected_mood
    elif polarity < -0.4 and detected_mood in ["Sadness", "Fear", "Anger", "Disgust"]:
        return detected_mood
    elif subjectivity > 0.5 and detected_mood in ["Surprise", "Anticipation"]:
        return detected_mood
    else:
        return detected_mood  # Default to most matched emotion

def analyze_sentiment(review):
    return detect_emotion(review)

# Example Usage
text = "I am absolutely delighted and overjoyed with the results!"
emotion = analyze_sentiment(text)
print("Detected Emotion:", emotion)
