from flask import Flask, render_template, request, jsonify
from sentiment_analysis import analyze_sentiment
from movies import MOVIE_DATA

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_review = data.get("review", "")
    selected_language = data.get("language", "Any")
    selected_genre = data.get("genre", "Any")
    
    # Detect the mood of the user's review
    mood = analyze_sentiment(user_review)
    
    # Get recommendations based on detected mood, language, and genre
    recommendations = [
        movie for movie in MOVIE_DATA 
        if movie['mood'] == mood and
        (selected_language == "Any" or movie['language'] == selected_language) and
        (selected_genre == "Any" or selected_genre in movie['genre'])
    ]
    
    return jsonify({"mood": mood, "movies": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
