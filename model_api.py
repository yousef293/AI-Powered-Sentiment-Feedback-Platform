from fastapi import FastAPI
from Model import SentimentModel
from pymongo import MongoClient
# running on port 8000/ host 127.0.0.1(local host)
model=SentimentModel()
model.load_model()
app=FastAPI()
Url='mongodb+srv://admin:nHLfecsVHTG3Hkgu@cluster0.4pvvsk6.mongodb.net/Recommender_system?retryWrites=true&w=majority'
client=MongoClient(Url)

# text prediction ------------------------------------
@app.get('/predict/{text}')
def predict(text:str):
    return model.predict(text)
# -------------------------------------------------
