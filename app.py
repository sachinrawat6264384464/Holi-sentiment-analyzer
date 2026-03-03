from flask import Flask, render_template, request
import pickle
import re

# Create Flask app
app = Flask(__name__)

# Load trained model (pipeline model)
model = pickle.load(open("model.pkl", "rb"))


# Text cleaning function (same as training time)
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    user_input = request.form["message"]

    cleaned_text = clean_text(user_input)

    prediction = model.predict([cleaned_text])[0]

    # Sentiment color mapping
    if prediction == "Positive" or prediction == 2:
        sentiment = "Positive 😊"
        color = "linear-gradient(-45deg, #ff512f, #dd2476, #f9d423, #24c6dc)"
    elif prediction == "Neutral" or prediction == 1:
        sentiment = "Neutral 😐"
        color = "linear-gradient(-45deg, #36d1dc, #5b86e5, #a1c4fd, #c2e9fb)"
    else:
        sentiment = "Negative 😡"
        color = "linear-gradient(-45deg, #485563, #29323c, #bdc3c7)"

    return render_template("index.html",
                           prediction_text=sentiment,
                           bg_color=color)


if __name__ == "__main__":
    app.run(debug=True)