from flask import Flask, request, jsonify
import pickle

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
