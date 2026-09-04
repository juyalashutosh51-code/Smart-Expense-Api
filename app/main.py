from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return{"message":"Smart Expense App is Running"}