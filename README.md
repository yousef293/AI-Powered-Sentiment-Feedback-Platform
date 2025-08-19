🧠 Sentiment Analysis Feedback System

A full-stack Sentiment Analysis Feedback System that combines AI, authentication, and API integration.

🚀 Features

AI Sentiment Model (Logistic Regression + TF-IDF)

Classifies text into Positive, Neutral, Negative

Saved as a pre-trained model → no need to re-train on every request

APIs

Node.js (Express + MongoDB + JWT) for authentication & feedback storage

FastAPI microservice for /predict endpoint (AI model inference)

Authentication

JWT-based login & signup

Access & Refresh tokens

📂 Tech Stack

Backend: Node.js (Express), FastAPI

Database: MongoDB (Mongoose)

AI Model: Logistic Regression + TF-IDF

Auth: JWT (Access + Refresh tokens)

🛠 Setup
# Clone repo
git clone https://github.com/your-username/sentiment-feedback-system.git
cd sentiment-feedback-system

# Install dependencies (Node.js)
npm install

# Run Node.js API
npm start

# Run FastAPI microservice
uvicorn app:app --reload

📌 Endpoints

POST /auth/signup → Create user

POST /auth/login → Login & get JWT

POST /feedback → Submit feedback (requires JWT)

GET /feedback → Retrieve feedbacks (requires JWT)

POST /predict (FastAPI) → Predict sentiment
