from flask import Flask, request, jsonify
import pickle
import re
import string

# Load saved model and vectorizer
with open("spam_classifier.pkl", "rb") as model_file:
    nb_model = pickle.load(model_file)

with open("tfidf_vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Initialize Flask app
app = Flask(__name__)

# Function to clean text (same as before)
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"\d+", "", text)  # Remove numbers
    text = re.sub(r"https?://\S+|www\.\S+", "", text)  # Remove URLs
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

# API endpoint for classification
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json  # Get JSON input
    if "email_text" not in data:
        return jsonify({"error": "Missing 'email_text' field"}), 400

    email_text = data["email_text"]
    email_cleaned = clean_text(email_text)  # Clean text
    email_vectorized = vectorizer.transform([email_cleaned])  # Convert to numerical features
    prediction = nb_model.predict(email_vectorized)[0]  # Predict

    result = "Spam" if prediction == 1 else "Not Spam"
    return jsonify({"prediction": result})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
