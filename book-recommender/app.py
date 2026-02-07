from flask import Flask, request, jsonify, send_file
import json

app = Flask(__name__)

# Load books from JSON file
with open("books.json", "r", encoding="utf-8") as f:
    books = json.load(f)


@app.route("/")
def home():
    return send_file("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    interest = data.get("interest")
    time = data.get("time")

    # Block empty interest
    if not interest or not interest.strip():
        return jsonify({"error": "Please enter an interest."})

    interest = interest.lower()

    # Handle invalid time
    try:
        time = int(time) if time else 100000
    except:
        time = 100000

    results = []

    for book in books:
        if any(interest in subject.lower() for subject in book["subjects"]):
            if book["reading_time_minutes"] <= time:
                results.append({
                    "title": book["title"],
                    "reading_time_minutes": book["reading_time_minutes"]
                })

    # Sort by shortest reading time
    results.sort(key=lambda x: x["reading_time_minutes"])

    if not results:
        return jsonify({"message": "No books found within that time range."})

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
