import re
import heapq
from flask import Flask, request, render_template

app = Flask(__name__)


def summarize_text(text, ratio=0.3):
    text = text.strip()
    if not text:
        return ""

    sentences = re.split(r'(?<=[.!?]) +', text)

    words = re.findall(r'\w+', text.lower())

    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    max_freq = max(freq.values())
    for w in freq:
        freq[w] /= max_freq

    sentence_scores = {}

    for sent in sentences:
        sent_words = re.findall(r'\w+', sent.lower())
        score = sum(freq.get(w, 0) for w in sent_words)
        sentence_scores[sent] = score

    n = max(1, int(len(sentences) * ratio))

    best_sentences = heapq.nlargest(
        n, sentence_scores, key=sentence_scores.get)
    best_sentences = sorted(best_sentences, key=lambda s: sentences.index(s))

    summary = " ".join(best_sentences)

    return summary


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "")
        summary = summarize_text(text)
        return render_template("result.html", original=text, summary=summary)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
