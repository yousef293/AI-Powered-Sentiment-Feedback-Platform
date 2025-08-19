#running on port 8080/ host 127.0.0.1 (local host)
from fastapi import FastAPI,HTTPException,Depends,Header
from pymongo import MongoClient
import requests
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from datetime import datetime,timedelta
from database_model import Client_data,Feedback_schema
import bcrypt
import jwt
from jose import JWTError,jwt

app=FastAPI()
Url='mongodb+srv://admin:nHLfecsVHTG3Hkgu@cluster0.4pvvsk6.mongodb.net/Recommender_system?retryWrites=true&w=majority'
client=MongoClient(Url)
f_database=client['Sentiment']['feedbacks']
u_database=client['Sentiment']['Clients_data']
Secret_key='bchjdsbhjsjhhsdj0vv-o0jjivjdfjdnjnjjskff-'

@app.post('/auth/signup')
def signup(data:Client_data):
    data_dict=data.dict()
    in_db=u_database.find_one({"user_name":data_dict["user_name"]})
    if (in_db):
        raise HTTPException(status_code=409,detail="The User is already in database")
    data_dict['password']=bcrypt.hashpw(data_dict['password'].encode('utf-8'),bcrypt.gensalt(rounds=12)).decode('utf-8')
    u_database.insert_one(data_dict)
    token=jwt.encode({"name":data_dict['user_name']},Secret_key)
    return{"message":"user created successfully",
           "token":token}


@app.post('/auth/login')
def login(data:Client_data):
    data_dict=data.dict()
    user=u_database.find_one({"user_name":data_dict["user_name"]})
    if (not user):
        raise HTTPException(status_code=400, detail='Invalid User name or Password')
    check=bcrypt.checkpw(data_dict["password"].encode('utf-8'),user["password"].encode('utf-8'))
    if (not check):
        raise HTTPException(status_code=400, detail='Invalid User name or Password')

    token=jwt.encode({"id":data_dict["user_id"],"name":data_dict["user_name"]},Secret_key)
    return {
        "message":"Loged in successfully",
        "token":token
    }

def get_user(authorization: str=Header(...)):
    try:
        scheme,token=authorization.split()
        if scheme.lower() !="bearer":
            raise HTTPException(status_code=401,detail="invalid scheme")
    except ValueError:
        raise HTTPException(status_code=401,detail="invalid authorization")
    try: 
        payload=jwt.decode(token,Secret_key)
        return payload
    except JWTError:
        raise HTTPException(status_code=409,detail="Invalid or expired token")


        
@app.post('/feedback')
def create_feedback(feedback:Feedback_schema,current_user:dict=Depends(get_user)):
    feedback_dict=feedback.dict()
    feedback_dict['user_id']=current_user["id"]
    text=feedback_dict["text"]
   
    url=(f"http://127.0.0.1:8000/predict/{text}")
    response=(requests.get(url)).json()
    feedback_dict['sentiment']=response["sentiment"]
    feedback_dict['confidence']=response["confidence"]
    time=datetime.utcnow()
    one_minute_ago=time-timedelta(minutes=1)
    count = f_database.count_documents({
    "user_id": feedback_dict['user_id'],
    "createdAt": {"$gte": one_minute_ago}})
    if (count>5):
        raise HTTPException(status_code=429,detail="Rate limit exceeded: Max 5 feedbacks per minute.")
    
    f_database.insert_one(feedback_dict)
    feedback_dict.pop("_id", None) 
    return feedback_dict
@app.get('/feedback')
def get_feedbacks(current_user: dict=Depends(get_user)):
    id=current_user["id"]
    data=f_database.find({"user_id":id})
    feedbacks=[]
    for doc in data: 
        doc["_id"]=str(doc["_id"])
        feedbacks.append(doc)

    return feedbacks

# Error handler 
@app.middleware("http")
async def catch_all(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:  # Catch actual error instance
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred", "details": str(e)}
        )


