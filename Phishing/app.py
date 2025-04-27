from flask import Flask, request, jsonify
import pickle
<<<<<<< HEAD

app = Flask(__name__)

# Load your trained model and TF-IDF vectorizer
with open('spam_classifier.pkl', 'rb') as f:
    model = pickle.load(f)

with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Extract combined text features
    text = data.get('subject', '') + ' ' + data.get('body', '')
    features = vectorizer.transform([text])  # TF-IDF vector

    # Make prediction
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return jsonify({
        'is_phishing': bool(prediction),
        'probability': float(probability),
        'email_subject': data.get('subject', '')
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
=======
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
>>>>>>> 88eb466cec4d50cb0eec0e40a4c5037ca2e7e3ad
