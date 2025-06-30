function getRecommendations() {
    let review = document.getElementById("review").value;
    let language = document.getElementById("language").value;
    let genre = document.getElementById("genre").value;

    fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ review, language, genre })
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById("result");
        resultDiv.innerHTML = `<h2>Mood Detected: ${data.mood}</h2>`;

        if (data.movies.length > 0) {
            let movieList = "<h3>Recommended Movies:</h3><ul>";
            data.movies.forEach(movie => {
                movieList += `<li><strong>${movie.title}</strong> - ${movie.genre.join(", ")}</li>`;
            });
            movieList += "</ul>";
            resultDiv.innerHTML += movieList;
        } else {
            resultDiv.innerHTML += "<p>No movies found for your mood and preferences.</p>";
        }
    });
}
