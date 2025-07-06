import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet')
nltk.download('omw-1.4')

def get_word_details(word):
    synsets = wn.synsets(word)
    if not synsets:
        return {"word": word, "error": "No data found."}

    # Take the first synset
    definition = synsets[0].definition()
    examples = synsets[0].examples()

    synonyms = set()
    antonyms = set()

    for syn in synsets:
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
            if lemma.antonyms():
                antonyms.add(lemma.antonyms()[0].name())

    return {
        "word": word,
        "definition": definition,
        "synonyms": list(synonyms),
        "antonyms": list(antonyms),
        "example": examples[0] if examples else "No example available."
    }